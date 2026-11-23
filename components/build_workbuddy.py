#!/usr/bin/env python3
"""Build local WorkBuddy submission ZIPs; never connect, install or publish."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import struct
import zipfile


COMPONENTS = Path(__file__).resolve().parent
REPOSITORY = COMPONENTS.parent
DEFAULT_OUTPUT = COMPONENTS / "targets"
MCP_SOURCE = "contract/query.md"
REPORTING_SOURCE = "contract/report.md"
LINKS = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def frontmatter(values):
    # JSON values are also valid YAML scalars/collections; no YAML dependency.
    # WorkBuddy's quick_validate.py checks the literal name on this line.
    if not IDENTIFIER.fullmatch(values["name"]):
        raise ValueError("Invalid WorkBuddy frontmatter name")
    lines = [f"{key}: {value if key == 'name' else json.dumps(value, ensure_ascii=False)}"
             for key, value in values.items()]
    return "---\n" + "\n".join(lines) + "\n---\n\n"


def source_file(relative):
    path = (COMPONENTS / relative).resolve()
    if not path.is_relative_to(COMPONENTS) or not path.is_file():
        raise ValueError(f"Missing or external component resource: {relative}")
    return path


def require_text(mapping, keys):
    for key in keys:
        if not isinstance(mapping.get(key), str) or not mapping[key].strip():
            raise ValueError(f"Missing text field: {key}")


def catalog_checks(component):
    """Read check names from the Skill-owned catalog, without another definition."""
    checks = set()
    for line in source_file(component["entry"]).read_text(encoding="utf-8").splitlines():
        columns = [column.strip() for column in line.strip().strip("|").split("|")]
        if line.startswith("| ") and len(columns) == 4 and re.fullmatch(
                r"\[Method\]\(methods\.md#[^)]+\)", columns[-1]):
            checks.add(columns[0])
    if not checks:
        raise ValueError(f"Missing Skill check catalog: {component['entry']}")
    return checks


def validate_sources(manifest, platform):
    if manifest["schema_version"] != 1 or platform["schema_version"] != 1:
        raise ValueError("Unsupported component or WorkBuddy metadata version")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest["source_version"]):
        raise ValueError("WorkBuddy release version must be semantic x.y.z")
    require_text(platform["author"], ("name", "email"))
    for kind in ("professionals", "experts", "workflows", "endpoint_skills"):
        if set(manifest[kind]) != set(platform[kind]):
            raise ValueError(f"WorkBuddy {kind} metadata does not match sources")
    for component in manifest["professionals"].values():
        name = component["export_name"]
        if not IDENTIFIER.fullmatch(name) or len(name) > 64:
            raise ValueError(f"Invalid Skill name: {name}")
        resources = {source_file(path) for path in component["resources"]}
        if source_file(component["entry"]) not in resources:
            raise ValueError(f"Skill entry is not bundled: {name}")
        for path in resources:
            if not (path.is_relative_to(COMPONENTS / "skill/datas")
                    or path.is_relative_to(COMPONENTS / "contract")):
                raise ValueError(f"Non-professional resource in Skill: {path}")
            for _, target in LINKS.findall(path.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                if (path.parent / target.split("#", 1)[0]).resolve() not in resources:
                    raise ValueError(f"Unbundled Skill reference: {path}: {target}")
    for component_id, item in platform["professionals"].items():
        require_text(item, ("display_name", "display_name_en", "description_zh", "description_en"))
        if not manifest["professionals"][component_id]["description"].strip():
            raise ValueError(f"Missing trigger description: {component_id}")
        for key in ("examples_zh", "examples_en"):
            if not item.get(key) or any(not text.strip() for text in item[key]):
                raise ValueError(f"Missing Skill examples: {component_id}/{key}")
    report = manifest["report_skill"]
    require_text(report, ("export_name", "entry", "description"))
    if (not IDENTIFIER.fullmatch(report["export_name"])
            or len(report["export_name"]) > 64
            or report["export_name"] in {c["export_name"] for c in manifest["professionals"].values()}):
        raise ValueError("Invalid or duplicate report Skill name")
    require_text(platform["report_skill"], ("display_name", "display_name_en", "description_zh", "description_en"))
    report_paths = {source_file(path): destination for path, destination in report["resources"].items()}
    destinations = list(report_paths.values())
    if (len({name.casefold() for name in destinations}) != len(destinations)
            or "SKILL.md" in destinations):
        raise ValueError("Colliding report Skill resource paths")
    validate_skill_layout({"SKILL.md": b"", **dict.fromkeys(destinations, b"")})
    for path in [source_file(report["entry"]), *report_paths]:
        if not (path.is_relative_to(COMPONENTS / "tools/report")
                or path == COMPONENTS / REPORTING_SOURCE):
            raise ValueError(f"Non-report resource in report Skill: {path}")
        if path.suffix != ".md":
            continue
        for _, target in LINKS.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            if (path.parent / target.split("#", 1)[0]).resolve() not in report_paths:
                raise ValueError(f"Unbundled report Skill reference: {path}: {target}")
    names = {item["export_name"] for item in manifest["professionals"].values()}
    names.add(report["export_name"])
    if report.get("kind") != "tool" or any(item.get("kind") != "data"
                                           for item in manifest["professionals"].values()):
        raise ValueError("Invalid WorkBuddy Skill kind")
    for key, data in manifest["endpoint_skills"].items():
        name = data["export_name"]
        if (data["kind"] != "data" or not IDENTIFIER.fullmatch(name) or len(name) > 64
                or name in names or key in manifest["professionals"] or key in manifest["workflows"]):
            raise ValueError(f"Invalid endpoint Skill: {key}")
        if "fallback_skill" in data:
            raise ValueError(f"Data Skills cannot depend on other data Skills: {key}")
        names.add(name)
        require_text(data, ("entry", "endpoint", "description"))
        require_text(platform["endpoint_skills"][key], ("display_name", "display_name_en",
                                                       "description_zh", "description_en"))
    for key, workflow in manifest["workflows"].items():
        name = workflow["export_name"]
        if (key in manifest["professionals"] or workflow.get("kind") != "workflow" or not IDENTIFIER.fullmatch(name)
                or len(name) > 64 or name in names):
            raise ValueError(f"Invalid workflow Skill: {name}")
        names.add(name)
        source_file(workflow["entry"])
        require_text(workflow, ("description",))
        require_text(platform["workflows"][key], ("display_name", "display_name_en",
                                                  "description_zh", "description_en"))
        for language in ("zh", "en"):
            examples = platform["workflows"][key][f"examples_{language}"]
            if len(examples) != 3 or not all(example.strip() for example in examples):
                raise ValueError(f"Invalid workflow examples: {key}")
        if not re.fullmatch(r"\d+\.\d+\.\d+", workflow.get("version", manifest["source_version"])):
            raise ValueError(f"Invalid workflow version: {key}")
        dependencies = workflow.get("data_skills", [])
        if len(dependencies) != len(set(dependencies)) or not set(dependencies) <= set(manifest["endpoint_skills"]):
            raise ValueError(f"Invalid workflow data Skills: {key}")
        if not dependencies or "allowed_checks" in workflow:
            raise ValueError(f"Workflow must select data Skills directly: {key}")
    expert_names = set()
    avatar_digests = set()
    for expert_id, item in platform["experts"].items():
        require_text(item, ("name", "description", "categoryId"))
        if not IDENTIFIER.fullmatch(item["name"]) or item["name"] in expert_names:
            raise ValueError(f"Invalid or duplicate expert name: {expert_id}")
        expert_names.add(item["name"])
        avatar = source_file(item["avatar"]).read_bytes()
        if (len(avatar) < 24 or avatar[:8] != b"\x89PNG\r\n\x1a\n"
                or len(avatar) > 500 * 1024 or struct.unpack(">II", avatar[16:24]) != (512, 512)):
            raise ValueError(f"Expected a 512×512 PNG under 500KB for {expert_id}")
        digest = hashlib.sha256(avatar).digest()
        if digest in avatar_digests:
            raise ValueError(f"Another expert uses the same avatar as {expert_id}")
        avatar_digests.add(digest)
        if not 40 <= len(item["displayDescription"]["zh"]) <= 50:
            raise ValueError(f"Expert Chinese description must be 40–50 characters: {expert_id}")
        for key in ("tags", "quickPrompts"):
            if len(item[key]) != 3:
                raise ValueError(f"Expert {key} requires exactly three entries: {expert_id}")
        localized = [item[key] for key in ("displayName", "profession", "displayDescription")]
        for entry in localized + item["tags"] + item["quickPrompts"]:
            require_text(entry, ("zh", "en"))
        expert = manifest["experts"][expert_id]
        if "workflow" in expert:
            if (expert["workflow"] not in manifest["workflows"]
                    or {"primary_professionals", "optional_professionals", "allowed_checks"} & expert.keys()):
                raise ValueError(f"Invalid workflow binding: {expert_id}")
            continue
        bindings = expert["primary_professionals"] + expert["optional_professionals"]
        if (len(expert["primary_professionals"]) != 1
                or len(bindings) != len(set(bindings))
                or not set(bindings) <= set(manifest["professionals"])):
            raise ValueError(f"Invalid professional bindings: {expert_id}")
        scope = expert.get("allowed_checks")
        if not isinstance(scope, dict) or set(scope) != set(bindings):
            raise ValueError(f"Invalid expert check scope: {expert_id}")
        for domain, checks in scope.items():
            if (not isinstance(checks, list) or not checks
                    or any(not isinstance(check, str) for check in checks)
                    or len(checks) != len(set(checks))
                    or not set(checks) <= catalog_checks(manifest["professionals"][domain])):
                raise ValueError(f"Invalid expert check scope: {expert_id}/{domain}")
    connector = platform["connector"]
    require_text(connector, ("source", "name", "name_en", "description",
                             "description_zh", "description_en", "token_key"))
    if not IDENTIFIER.fullmatch(connector["source"]):
        raise ValueError("Invalid connector source")
    package_name = connector.get("package_name", connector["source"])
    if not isinstance(package_name, str) or not IDENTIFIER.fullmatch(package_name):
        raise ValueError("Invalid connector package name")
    if not connector["mcp_url"].startswith("https://"):
        raise ValueError("Remote MCP must use HTTPS")
    source_file(connector["icon"])


def skill_resource_paths(component):
    """Map component sources to a flat, collision-checked references directory."""
    paths = {}
    used_names = set()
    for relative in component["resources"]:
        parts = PurePosixPath(relative).parts
        # Keep the published reference names independent of repository organization.
        if parts[:2] == ("skill", "datas"):
            parts = ("skills", *parts[2:])
        elif parts[0] == "contract":
            parts = ("contracts", *parts[1:])
        elif parts[0] == "skill":
            parts = ("skills", *parts[1:])
        destination = "references/" + "-".join(parts)
        if relative == MCP_SOURCE:
            destination = "references/contracts-mcp.md"
        if relative == REPORTING_SOURCE:
            # Preserve the installed resource name across the source directory move.
            destination = "references/contracts-reporting.md"
        if destination.casefold() in used_names:
            raise ValueError(f"Colliding flattened Skill resource: {relative}")
        used_names.add(destination.casefold())
        paths[source_file(relative)] = destination
    return paths


def rewrite_resource_links(path, content, resource_paths, prefix="", destination=None):
    """Retarget local Markdown links while preserving labels, fragments and URLs."""
    def replace(match):
        label, target = match.groups()
        if target.startswith(("https://", "http://", "#", "mailto:")):
            return match.group()
        relative, separator, fragment = target.partition("#")
        resolved = (path.parent / relative).resolve()
        if resolved not in resource_paths:
            raise ValueError(f"Unbundled Skill reference: {path}: {target}")
        filename = (posixpath.relpath(resource_paths[resolved], str(PurePosixPath(destination).parent))
                    if destination else PurePosixPath(resource_paths[resolved]).name)
        return f"[{label}]({prefix}{filename}{separator}{fragment})"

    return LINKS.sub(replace, content)


def validate_skill_layout(files):
    """A Skill root may contain files and one directory level, e.g. references/."""
    if "SKILL.md" not in files:
        raise ValueError("Skill package has no SKILL.md")
    for relative in files:
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or len(path.parts) > 2:
            raise ValueError(f"Skill directory depth exceeds WorkBuddy's two-level limit: {relative}")


def render_skill(component_id, manifest, platform):
    component = manifest["professionals"][component_id]
    resource_paths = skill_resource_paths(component)

    def reference(relative):
        return resource_paths[source_file(relative)]

    fields = {
        "name": component["export_name"],
        **platform["professionals"][component_id],
        "description": component["description"],
        "version": manifest["source_version"],
        "author": platform["author"]["name"],
    }
    body = f"""# {fields['display_name_en']}

## Required instructions

1. @{reference(component['entry'])} owns the analysis object, task catalog, inputs and baseline report content. Select only tasks needed by the question.
2. @{reference('contract/evidence.md')} defines data scope, missing-value handling and the evidence required for findings.
3. @{reference(REPORTING_SOURCE)} defines report presentation and the checks to apply before replying.

## Task-dependent resources

1. Before analysis, read the selected [method]({reference(f'skill/datas/{component_id}/methods.md')}) and relevant [semantics]({reference(f'skill/datas/{component_id}/semantics.md')}).
2. Before a new query, read [MCP rules]({reference(MCP_SOURCE)}) and inspect the connected tool's description and schemas.
3. When interpreting supplied private reports or operating inputs, load [seller evidence]({reference('contract/seller-evidence.md')}).
4. Load another domain's semantics only when the selected task definition requires them.

5. Use only the intended reads in [capability scope](references/capabilities.json); resolve callable names from the connected tools.
6. Resolve resource paths relative to the containing document.

## Deliver the analysis result

1. Produce the selected task's data analysis report from acquired or supplied evidence.
2. Keep the Skill report focused on data findings; business interpretation belongs to the expert.
"""
    files = {"SKILL.md": (frontmatter(fields) + body).encode("utf-8")}
    for path, destination in resource_paths.items():
        content = path.read_bytes().decode("utf-8")
        files[destination] = rewrite_resource_links(path, content, resource_paths).encode("utf-8")
    files["references/capabilities.json"] = json_bytes({
        "logical_read_endpoints": component["capabilities"],
        "endpoint_ids_are_callable_names": False,
    })
    validate_skill_layout(files)
    return files


def bind_mcp_operations(markdown, server):
    """Qualify documented operation IDs without deriving them from endpoint paths."""
    return re.sub(r"`(openapi_v[0-9]+_[a-z0-9_]+)`", rf"`mcp__{server}__\1`",
                  markdown.replace("{{mcp_server}}", server))


def endpoint_instructions(entry):
    return (entry.read_text().rstrip() + "\n\nApply the [evidence rules](../../../contract/evidence.md) "
            "and [presentation rules](../../../contract/report.md) to the result. "
            "Before a new read, follow the [query rules](../../../contract/query.md).\n")


def render_endpoint_skill(key, manifest, platform, *, tool_source=None):
    component = manifest["endpoint_skills"][key]
    fields = {"name": component["export_name"], **platform["endpoint_skills"][key],
              "description": component["description"], "version": manifest["source_version"],
              "author": platform["author"]["name"]}
    entry = source_file(component["entry"])
    paths = skill_resource_paths({"resources": ["contract/evidence.md", REPORTING_SOURCE, MCP_SOURCE]})
    files = {destination: path.read_bytes() for path, destination in paths.items()}
    content = endpoint_instructions(entry)
    body = rewrite_resource_links(entry, content, paths, destination="SKILL.md")
    if tool_source:
        body = bind_mcp_operations(body, tool_source)
    files["SKILL.md"] = (frontmatter(fields) + body).encode("utf-8")
    endpoints = [component["endpoint"]]
    if "fallback_endpoint" in component:
        fallback = component["fallback_endpoint"]
        if not fallback or fallback in endpoints or f"`{fallback}`" not in content:
            raise ValueError(f"Invalid fallback endpoint: {key}")
        endpoints.append(fallback)
    files["references/capabilities.json"] = json_bytes({
        "logical_read_endpoints": endpoints,
        "endpoint_ids_are_callable_names": False})
    validate_skill_layout(files)
    return files


def render_workflow(key, manifest, platform):
    """Bundle the workflow and the transitive references used by its data tasks."""
    workflow = manifest["workflows"][key]
    entry = source_file(workflow["entry"])
    permitted = set(entry.parent.glob("*.md"))
    dependencies = workflow["data_skills"]
    data_entries = {source_file(manifest["endpoint_skills"][name]["entry"])
                    for name in dependencies}
    permitted.update(data_entries)
    permitted.update(source_file(relative) for relative in manifest["professional_contracts"])
    permitted.update((source_file(REPORTING_SOURCE), source_file(MCP_SOURCE)))
    permitted.update(entry.parent.glob("*.py"))
    report = manifest["report_skill"]
    report_paths = {source_file(src): dest for src, dest in report["resources"].items()}
    for relative, destination in workflow.get("report_resources", {}).items():
        resource = source_file(relative)
        if not resource.is_relative_to(COMPONENTS / "tools/report"):
            raise ValueError(f"Invalid workflow report resource: {relative}")
        report_paths[resource] = destination
    report_paths[source_file(report["entry"])] = "references/report-guide.md"
    permitted.update(report_paths)
    pending = [entry]
    contents = {}
    while pending:
        path = pending.pop()
        if path in contents:
            continue
        if path not in permitted:
            raise ValueError(f"Unbundled workflow dependency: {path}")
        content = endpoint_instructions(path) if path in data_entries else path.read_text(encoding="utf-8")
        contents[path] = content
        if path.suffix == ".md":
            for _, target in LINKS.findall(content):
                if not target.startswith(("https://", "http://", "#", "mailto:")):
                    pending.append((path.parent / target.split("#", 1)[0]).resolve())

    if data_entries - contents.keys():
        raise ValueError(f"Unreferenced workflow data Skills: {data_entries - contents.keys()}")
    paths = skill_resource_paths({"resources": [str(path.relative_to(COMPONENTS)) for path in contents]})
    for path in contents:
        if path in report_paths and path != source_file(REPORTING_SOURCE):
            paths[path] = report_paths[path]
        elif path.suffix == ".py":
            paths[path] = "scripts/" + path.name
    paths[entry] = "SKILL.md"
    fields = {"name": workflow["export_name"], **platform["workflows"][key],
              "description": workflow["description"], "version": workflow.get("version", manifest["source_version"]),
              "author": platform["author"]["name"]}
    files = {}
    for path, content in contents.items():
        destination = paths[path]
        if path.suffix == ".md":
            content = rewrite_resource_links(path, content, paths, destination=destination)
            if workflow.get("bind_mcp_tools"):
                content = bind_mcp_operations(content, platform["connector"]["source"])
        if path == entry:
            content = frontmatter(fields) + content
        if destination in files:
            raise ValueError(f"Colliding workflow resource: {destination}")
        files[destination] = content.encode("utf-8")
    if "report_example" in workflow:
        files["references/example.json"] = source_file(workflow["report_example"]).read_bytes()
    if "report_tasks" in workflow:
        files["references/report-tasks.json"] = json_bytes(workflow["report_tasks"])
    validate_skill_layout(files)
    return files


def render_report_skill(manifest, platform):
    component = manifest["report_skill"]
    paths = {source_file(path): destination for path, destination in component["resources"].items()}
    entry = source_file(component["entry"])
    fields = {"name": component["export_name"], **platform["report_skill"],
              "description": component["description"], "version": manifest["source_version"],
              "author": platform["author"]["name"]}
    body = rewrite_resource_links(entry, entry.read_text(encoding="utf-8"), paths,
                                  destination="SKILL.md")
    files = {"SKILL.md": (frontmatter(fields) + body).encode("utf-8")}
    for path, destination in paths.items():
        content = path.read_bytes()
        if path.suffix == ".md":
            content = rewrite_resource_links(path, content.decode("utf-8"), paths,
                                             destination=destination).encode("utf-8")
        files[destination] = content
    validate_skill_layout(files)
    return files


def token_schema(platform, localized=False):
    connector = platform["connector"]
    zh = "填写 ZooData API Key，凭证由 WorkBuddy 保存在用户本机。"
    en = "Enter your ZooData API key. WorkBuddy stores credentials locally."
    if localized:
        return {
            "title": {"zh": "连接 ZooData", "en": "Connect ZooData"},
            "description": {"zh": zh, "en": en},
            "docUrl": connector["token_help_url"],
            "docLabel": {"zh": "获取 API Key", "en": "Get an API key"},
            "fields": [{"key": connector["token_key"], "label": "ZooData API Key",
                        "type": "password", "required": True}],
        }
    return {
        "title": "连接 ZooData", "title_en": "Connect ZooData",
        "description": zh, "description_en": en,
        "docUrl": connector["token_help_url"], "docLabel": "获取 API Key",
        "fields": [{"key": connector["token_key"], "label": "ZooData API Key",
                    "type": "password", "required": True}],
    }


def mcp_server(platform, expert=False):
    connector = platform["connector"]
    server = {
        "type": "http" if expert else "streamableHttp",
        "url": connector["mcp_url"],
        "headers": {"Authorization": "Bearer ${" + connector["token_key"] + "}"},
    }
    if expert:
        server["x-workbuddy"] = {
            "displayName": {"zh": connector["name"], "en": connector["name_en"]},
            "description": {"zh": connector["description_zh"],
                            "en": connector["description_en"]},
            "icon": "./avatars/connector.svg",
            "auth": {"type": "token", "tokenSchema": token_schema(platform, localized=True)},
        }
    return {"mcpServers": {connector["source"]: server}}


def render_expert(expert_id, manifest, platform, skills, connector_id):
    expert = manifest["experts"][expert_id]
    fields = platform["experts"][expert_id]
    name = fields["name"]
    workflow_key = expert.get("workflow")
    if workflow_key:
        domains = [workflow_key, *manifest["workflows"][workflow_key]["data_skills"]]
        components = {**manifest["workflows"], **manifest["endpoint_skills"]}
    else:
        domains = expert["primary_professionals"] + expert["optional_professionals"]
        components = manifest["professionals"]
    component_names = {domain: components[domain]["export_name"] for domain in domains}
    sources = {source_file(components[domain]["entry"]): domain for domain in domains}
    path = source_file(expert["configuration"])

    def bind_link(match):
        label, target = match.groups()
        if target.startswith(("https://", "http://", "#", "mailto:")):
            return match.group()
        resolved = (path.parent / target).resolve()
        if resolved in sources:
            return f"{label} (`{component_names[sources[resolved]]}`)"
        raise ValueError(f"Unresolved expert composition link: {target}")

    business = LINKS.sub(bind_link, path.read_text(encoding="utf-8"))
    agent_fields = {key: fields[key] for key in ("name", "description", "displayName", "profession")}
    report_name = manifest["report_skill"]["export_name"]
    if workflow_key:
        workflow_name = component_names[workflow_key]
        agent_fields["skills"] = [workflow_name, report_name]
        binding_lines = ["# Professional Skill composition", "",
                         f"1. Use `{workflow_name}` for the confirmed task. The workflow and report Skill entries and the presentation rules are preloaded. Open only the method needed for a missing measure. Reuse rules already in context.",
                         f"2. Use the workflow's outline for the expert report. Give the findings and requested business interpretation to `{report_name}` for HTML delivery."]
    else:
        agent_fields["skills"] = [component_names[domain] for domain in expert["primary_professionals"]] + [report_name]
        binding_lines = ["# Professional Skill composition", "",
                         "1. Reuse instructions already supplied in this conversation. Read a selected Skill's missing instructions before using its methods; do not reload identical shared rules from each Skill.",
                          "2. Primary analysis Skills and the report-generation Skill are preloaded. Load bundled optional analysis Skills only when needed.",
                          "3. Select a check only if it is approved below and the expert configuration "
                          "allows it for the current question. "
                          "A Skill's larger catalog does not expand this expert's check scope.", ""]
        binding_lines.extend([f"4. Use `{report_name}` to present the completed findings as HTML. The expert's report outline selects the content; the report Skill supplies components, template and generation. It does not acquire evidence or expand the approved analysis tasks.",
                              "", "## Approved Skill tasks", ""])
        for index, domain in enumerate(domains, 1):
            role = "Primary" if domain in expert["primary_professionals"] else "Optional"
            binding_lines.append(f"{index}. {role}: `{component_names[domain]}`")
            checks = ", ".join(f"`{check}`" for check in expert["allowed_checks"][domain])
            binding_lines.append(f"  Approved checks: {checks}")
    combined = []
    delivery_source = source_file("expert/agent-core/delivery.md")
    agent_sources = [source_file(relative) for relative in manifest["agent_sources"]]
    if delivery_source not in agent_sources:
        raise ValueError("Expert composition requires the shared delivery owner")
    combined.extend(path.read_text(encoding="utf-8").strip()
                    for path in agent_sources if path != delivery_source)
    combined.append("\n".join(binding_lines))
    combined.append(business.strip())
    report_path = source_file(REPORTING_SOURCE)
    combined.append(report_path.read_text(encoding="utf-8").strip())
    combined.append(delivery_source.read_text(encoding="utf-8").strip())
    body = frontmatter(agent_fields) + "\n\n".join(combined) + "\n"
    version = manifest["workflows"].get(workflow_key, {}).get("version", manifest["source_version"])
    plugin = {
        "name": name, "version": version,
        "description": fields["description"], "author": platform["author"],
        "agents": [f"./agents/{name}.md"], "expertType": "agent", "agentName": name,
        **{key: fields[key] for key in ("displayName", "profession", "displayDescription",
                                       "categoryId", "tags", "quickPrompts")},
        "avatar": "avatars/expert.png", "plugin": name,
        "defaultInitPrompt": fields["quickPrompts"][0],
        "skills": [f"./skills/{component_names[domain]}" for domain in domains] + [f"./skills/{report_name}"],
        "homepage": platform["homepage"], "license": "MIT",
    }
    files = {f"agents/{name}.md": body.encode("utf-8"),
             "avatars/expert.png": source_file(fields["avatar"]).read_bytes()}
    if workflow_key and "report_tasks" in manifest["workflows"][workflow_key]:
        files[".codebuddy-plugin/report-tasks.json"] = json_bytes(manifest["workflows"][workflow_key]["report_tasks"])
    if connector_id:
        plugin["dependencies"] = {"connectors": [connector_id]}
    else:
        plugin["dependencies"] = {"mcpServers": "./.mcp.json"}
        files[".mcp.json"] = json_bytes(mcp_server(platform, expert=True))
        files["avatars/connector.svg"] = source_file(platform["connector"]["icon"]).read_bytes()
    files[".codebuddy-plugin/plugin.json"] = json_bytes(plugin)
    files["README.md"] = (
        f"# {fields['displayName']['zh']}\n\n{fields['displayDescription']['zh']}\n\n"
        "召唤专家后，按照 WorkBuddy 引导连接 ZooData 并填写 API Key。"
        "也可以提供已有的兼容研究资料；实时查询需要有效的数据连接。\n\n"
        "包含所需专业技能，按问题加载。研究结果保留数据范围与估算口径。\n"
    ).encode("utf-8")
    for domain in domains:
        resources = skills[domain]
        if (domain in manifest["endpoint_skills"] and workflow_key
                and manifest["workflows"][workflow_key].get("bind_mcp_tools")):
            resources = render_endpoint_skill(domain, manifest, platform, tool_source=platform["connector"]["source"])
        for relative, content in resources.items():
            files[f"skills/{component_names[domain]}/{relative}"] = content
    report_files = render_report_skill(manifest, platform)
    if workflow_key:
        report_files["references/example.json"] = skills[workflow_key]["references/example.json"]
    for relative, content in report_files.items():
        files[f"skills/{report_name}/{relative}"] = content
    return files


def render_connector(manifest, platform):
    connector = platform["connector"]
    fields = {key: connector[key] for key in ("source", "name", "name_en", "description",
                                             "description_zh", "description_en",
                                             "examples_zh", "examples_en")}
    fields.update({"name_zh": connector["name"], "type": "mcp", "auth_mode": "token",
                   "version": manifest["source_version"], "minWorkbuddyVersion": "4.24.0"})
    return {
        "connector-meta.json": json_bytes(fields),
        "mcp.json": json_bytes(mcp_server(platform)),
        "token-schema.json": json_bytes(token_schema(platform)),
        "icon.svg": source_file(connector["icon"]).read_bytes(),
    }


def render_packages(connector_id=None, *, include_components=False, mcp_source=None):
    if connector_id is not None and not IDENTIFIER.fullmatch(connector_id):
        raise ValueError("Use the actual published connector ID in kebab-case")
    manifest = read_json(COMPONENTS / "targets.json")
    platform = read_json(COMPONENTS / "workbuddy.json")
    if mcp_source is not None:
        platform["connector"]["source"] = mcp_source
    validate_sources(manifest, platform)
    skills = {domain: render_skill(domain, manifest, platform)
              for domain in manifest["professionals"]}
    for key in manifest["endpoint_skills"]:
        skills[key] = render_endpoint_skill(key, manifest, platform)
    packages = {}
    if include_components:
        for kind in ("professionals", "endpoint_skills"):
            for key, component in manifest[kind].items():
                packages[("skills", component["export_name"])] = skills[key]
        packages[("skills", manifest["report_skill"]["export_name"])] = render_report_skill(manifest, platform)
    for key, workflow in manifest["workflows"].items():
        skills[key] = render_workflow(key, manifest, platform)
        packages[("skills", workflow["export_name"])] = skills[key]
    for expert_id, metadata in platform["experts"].items():
        packages[("experts", metadata["name"])] = render_expert(
            expert_id, manifest, platform, skills, connector_id)
    connector = platform["connector"]
    package_name = connector.get("package_name", connector["source"])
    packages[("connectors", package_name)] = render_connector(manifest, platform)
    return manifest, packages


def unchanged_retired_archives(output, packages):
    """Select obsolete outputs only when the previous build still owns their bytes."""
    previous = output / "build-report.json"
    if not previous.is_file() or previous.is_symlink():
        return []
    current = {f"{kind}/{name}.zip" for kind, name in packages}
    retired = []
    record = read_json(previous)
    if not isinstance(record, dict) or not isinstance(record.get("artifacts"), list):
        return retired
    for item in record["artifacts"]:
        if not isinstance(item, dict):
            continue
        kind, name = item.get("kind"), item.get("name", "")
        relative = item.get("zip")
        if (kind not in {"skills", "experts", "connectors"}
                or not isinstance(name, str) or not IDENTIFIER.fullmatch(name)
                or relative != f"{kind}/{name}.zip" or relative in current):
            continue
        archive = output / relative
        if (archive.is_file() and not archive.is_symlink()
                and archive.resolve().is_relative_to(output)
                and hashlib.sha256(archive.read_bytes()).hexdigest() == item.get("sha256")):
            retired.append(archive)
    return retired


def build(output=None, connector_id=None, *, include_components=False, mcp_source=None):
    output = Path(DEFAULT_OUTPUT if output is None else output).expanduser().resolve()
    archives_only = output == DEFAULT_OUTPUT.resolve()
    if (output.is_relative_to(REPOSITORY) and not archives_only
            or REPOSITORY.is_relative_to(output)):
        raise ValueError("Repository output is allowed only at components/targets (ZIPs only)")
    if output.exists() and (not output.is_dir()
                            or not archives_only and any(output.iterdir())):
        raise ValueError("Output must be a new or empty directory; existing artifacts are never overwritten")
    if archives_only and include_components:
        raise ValueError("Use an external --output directory for standalone component inspection")
    manifest, packages = render_packages(connector_id, include_components=include_components, mcp_source=mcp_source)
    retired = unchanged_retired_archives(output, packages) if archives_only else []
    report = {"version": manifest["source_version"], "platform_publication_performed": False,
              "live_binding_verified": False,
              "unpacked_copies": not archives_only,
              "expert_dependency_mode": "published-connector" if connector_id else "embedded-mcp",
              "published_connector_id": connector_id, "artifacts": []}
    output.mkdir(parents=True, exist_ok=True)
    for (kind, name), files in packages.items():
        root = output / kind / name
        for relative, content in files.items():
            parts = PurePosixPath(relative)
            if parts.is_absolute() or ".." in parts.parts:
                raise ValueError(f"Unsafe generated package path: {relative}")
            if not archives_only:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
        archive = output / kind / f"{name}.zip"
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for relative, content in sorted(files.items()):
                info = zipfile.ZipInfo(f"{name}/{relative}", date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, content)
        report["artifacts"].append({"kind": kind, "name": name,
                                     "zip": str(archive.relative_to(output)),
                                     "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()})
    for archive in retired:
        archive.unlink()
    (output / "build-report.json").write_bytes(json_bytes(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path,
                        help="Defaults to components/targets (ZIPs only, replaces generated archives); "
                             "an external new/empty directory also receives unpacked copies")
    parser.add_argument("--include-components", action="store_true",
                        help="Also export standalone component Skills for inspection in an external output directory")
    parser.add_argument("--connector-id", help="Actual published WorkBuddy connector ID; otherwise embed MCP")
    parser.add_argument("--mcp-source", help="WorkBuddy MCP server name for this build (defaults to workbuddy.json)")
    args = parser.parse_args()
    try:
        report = build(args.output, args.connector_id, include_components=args.include_components, mcp_source=args.mcp_source)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f"WorkBuddy build failed: {error}\n")
    print(f"Built {len(report['artifacts'])} local ZIPs in {args.output.resolve()}; nothing published.")


if __name__ == "__main__":
    main()
