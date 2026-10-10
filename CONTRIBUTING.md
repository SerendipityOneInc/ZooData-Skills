# Contributing to ZooData Skills

Thanks for your interest in contributing! We keep things simple.

## Ways to Contribute

- 🐛 **Report bugs** — [Open a bug report](https://github.com/SerendipityOneInc/ZooData-Skills/issues/new?template=bug_report.md)
- 💡 **Suggest features** — [Open a feature request](https://github.com/SerendipityOneInc/ZooData-Skills/issues/new?template=feature_request.md)
- 📝 **Improve docs** — Fix typos, clarify instructions, add examples
- 🔧 **Improve skills** — Enhance SKILL.md files, add scenarios, improve the CLI

## Getting Started

1. Fork the repo
2. Create a branch: `git checkout -b my-feature`
3. Make your changes
4. Test your changes (see below)
5. Commit: `git commit -m "feat: add new search scenario"`
6. Push: `git push origin my-feature`
7. Open a Pull Request

## Local Branch Hygiene

To avoid divergence from `origin/main` (e.g. if your previous branch was
squash-merged, your local SHA differs from the merged SHA on `main`):

```bash
# Always start from a fresh main
git checkout main
git fetch origin
git reset --hard origin/main   # safe — discards stale local commits whose
                               # content has already been merged on origin
git checkout -b feat/my-thing
```

## Shared ZooData Runtime Files

The canonical runtime files are:

- `zoodata/scripts/zoodata.py`
- `zoodata/references/cli-contract.md`
- `zoodata/references/analysis-contract.md`

Each active `amazon-*` skill has synced local copies of the shared CLI files at the
matching `scripts/` and `references/` paths so the skill remains independently
publishable. The shared analysis contract is currently adopted by
`amazon-keyword-traffic-analysis` and `amazon-market-analysis`; its copies are
synced into those two skills by the same mechanism. Retired source directories
do not contain a `SKILL.md` entrypoint, so skill installers, publishers, and
this distribution step do not discover them. **Never edit copies
directly** — sync is enforced at three layers:

1. **Local pre-commit hook** — auto-syncs copies when canonical is staged.
   Install once per clone: `bash scripts/install-hooks.sh`
2. **`scripts/sync-scripts.sh`** — mirrors each canonical file to its enrolled
   skill copies.
   `--check` performs a read-only release check and fails on a missing or
   byte-different copy. Normal sync refuses to overwrite a divergent copy
   without the canonical-source managed-copy marker.
3. **CI check** (`.github/workflows/shared-files-distribution.yml`) — every PR
   runs the read-only check; missing or mismatched copies block release even
   when a skill change forgot to update the canonical file or local copy.

The canonical files own their respective managed-copy headers and content.
`analysis-contract.md` is the highest repository-owned runtime prompt for
skills that adopt it. Skill-specific instructions may extend or narrow it but
must not duplicate, weaken, or override it. Each adopting skill's `SKILL.md`
remains the domain responsibility map and names the local owners of API facts,
semantics, scenarios, procedures, and rendering. Add skills to the enrolled
list only as their local ownership map is migrated and reviewed.

## Testing Your Changes

### For Skill files (SKILL.md, references/)

- Ensure markdown renders correctly on GitHub
- Check that all links work
- Verify examples are accurate

### For CLI (zoodata.py)

```bash
# Set your API key
export ZOODATA_API_KEY='hms_live_xxx'

# Test basic commands
python amazon-analysis/scripts/zoodata.py products --keyword "test" --mode beginner
python amazon-analysis/scripts/zoodata.py categories --keyword "electronics"
```

## Skill Specification Ownership

Each skill's `SKILL.md` is that skill's runtime router and module-responsibility
manifest. It must define the trigger and loading path, route requests to any
bundled modules, declare the owner of each policy class used by the skill, and
state the non-negotiable runtime boundaries shared by those modules. Keep it
concise: it may declare ownership and dispatch, but must not absorb the detailed
contracts, procedures, semantics, scenarios, or repository-maintenance process
owned elsewhere.

Every bundled reference, scenario, script-facing instruction, and other skill
module must follow the ownership map declared by its own `SKILL.md`.
Cross-module references are allowed; copying or redefining another module's
contract is not. Split a cross-cutting statement into the owner-specific parts
declared by that skill instead of placing the whole rule in multiple files.

Human reviewers and automated consistency checks must read the affected
`SKILL.md` first and review every bundled module strictly against its declared
responsibility. They must flag foreign definitions, duplicated policy, and
downstream overrides; they must not invent a parallel ownership model in the
review program. A change to the ownership map is an architectural change and
must be reviewed as such, not silently adjusted to make another file or test
pass. This repository-level contract constrains what a `SKILL.md` may own; it
does not define or duplicate any skill's domain-specific policy.

If a change exposes an inseparable conflict between owner contracts, stop and
request a maintainer decision in the issue or pull request. Do not silently
change a top-level contract, combine competing rules, or invent a fallback.
Keep this repository-maintenance process out of runtime skill instructions and
user-facing reports. Add or update consistency tests to enforce both ownership
and the absence of maintenance-language leakage.

## Skill Diagnosis and Repair

Use this process when a skill produces the wrong behavior, stops prematurely,
omits required evidence, or repeatedly needs user correction.

### 1. Understand the design before proposing a fix

Read the affected skill's complete `SKILL.md`, its responsibility map, and the
shared contracts and workflow modules governing the reported behavior. Follow
the loading and precedence chain through acquisition, interpretation, output,
and continuation. Inspect relevant scripts and tests to compare the declared
design with actual capabilities. A keyword search locates candidates; read the
surrounding rules and their callers before deciding what to change.

### 2. Trace the observed behavior to its cause

State the user's intended outcome and the observed deviation. Trace the path
from input or tool result through classification, workflow decision, and
user-facing behavior. Identify the controlling file, rule, and supporting
implementation evidence; distinguish verified causes from hypotheses.

- Determine whether the defect is in a rule, rule precedence, missing routing,
  implementation, or available capability.
- Check whether the Agent followed a harmful rule correctly or failed to follow
  an adequate rule. These require different repairs.
- Use the reported run and local artifacts first. Repeating paid acquisition
  is justified only when it resolves a named uncertainty needed for the repair.
- Do not start by tuning retries, rewriting code, or adding instructions merely
  because those changes appear related to the symptom.

### 3. Choose the owner and scope

Apply **Skill Specification Ownership** above. Place a general rule in its
existing shared owner and domain-specific behavior in its domain owner. Check
all consumers of a shared rule, including callers that have not adopted newer
contracts. State the cause, chosen owner, affected consumers, and intended
behavior before editing. An ownership change requires explicit architectural
review; an incident alone does not justify a new abstraction or global policy.

### 4. Make the smallest complete repair

Fix the controlling rule and any downstream instruction that would still
prevent the intended behavior. Preserve one policy source and use references
from callers. Update managed copies through the repository's sync mechanism.
Change executable code when the required capability is missing or incorrect;
instructions must not promise behavior the available tools cannot perform.

Check the full path, including successful, recoverable, terminal, partial,
paginated, and composite outcomes where applicable. For automatic recovery,
define who acts, what evidence is retained, how work resumes, and when recovery
stops. Keep routine execution decisions with the Agent while preserving user
authorization, cost limits, evidence identity, and persistent-state boundaries.
Avoid replacing one premature stop with an unbounded retry or repeated user
confirmation loop. Keep unrelated findings separate from the repair.

### 5. Verify behavior and integration

Review the original failure scenario against the revised instruction chain,
plus relevant neighboring cases such as normal success, exhausted recovery,
and partial completion. Run the affected ownership, routing, and consistency
checks; check shared-file distribution when shared sources change. Add focused
regression coverage for meaningful behavior or ownership invariants rather than
merely requiring the new wording. Do not weaken tests just to accept a patch.

Distinguish static checks, mocked execution, Agent scenario evaluation, and live
validation. Passing text-consistency tests alone does not demonstrate that an
Agent will complete the real workflow. Use live calls only when necessary and
within the task's authorization and cost boundaries.

### 6. Report the result and its limits

Summarize the root cause, rule ownership, changed behavior, affected scope,
actual verification, and remaining capability gaps. Distinguish local changes,
commits, published packages, and installed copies; editing repository sources
does not update an already installed skill. Follow the PR description rules
when preparing the review handoff.

## Command Allowlists

Every `amazon-*` skill declares its permitted CLI command set on exactly one
declaration line in its `SKILL.md` ("This skill allows ..." or "The bundled
manifest allows exactly ..."), and bundles the same set in
`scripts/allowed-commands.json`, which the shared CLI enforces at runtime.
`tests/test_zoodata.py::TestCommandAllowlist` asserts the declaration line and
the manifest match exactly, in both directions. When adding or removing a
routed command, update the declaration line and the manifest together — never
widen a manifest just to silence the test without also changing the skill's
declared scope. The marker phrases "This skill allows" and "The bundled
manifest allows exactly" are reserved for that single declaration line: do not
use either phrase in other SKILL.md prose, or the exactly-one-declaration
assertion fails.

## Commit Convention

We use conventional commits:

- `feat:` — New feature or scenario
- `fix:` — Bug fix
- `docs:` — Documentation only
- `refactor:` — Code restructuring
- `chore:` — Maintenance tasks

## Code Style

- **Python**: Follow PEP 8, stdlib only (no pip dependencies)
- **Markdown**: Use ATX-style headers (`#`), fenced code blocks with language tags

## Questions?

- Join our [Discord](https://discord.gg/YfDFU9BDp5)
- [Open an Issue](https://github.com/SerendipityOneInc/ZooData-Skills/issues)

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
