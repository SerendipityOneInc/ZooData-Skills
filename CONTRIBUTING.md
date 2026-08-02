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

Each `amazon-*` skill has synced local copies at the matching `scripts/` and
`references/` paths so the skill remains independently publishable. **Never
edit copies directly** — sync is enforced at three layers:

1. **Local pre-commit hook** — auto-syncs copies when canonical is staged.
   Install once per clone: `bash scripts/install-hooks.sh`
2. **`scripts/sync-scripts.sh`** — mirrors both canonical files → copies.
   `--check` performs a read-only release check and fails on a missing or
   byte-different copy. Normal sync refuses to overwrite a divergent copy
   without the canonical-source managed-copy marker.
3. **CI check** (`.github/workflows/shared-files-distribution.yml`) — every PR
   runs the read-only check; missing or mismatched copies block release even
   when a skill change forgot to update the canonical file or local copy.

The canonical files own their respective managed-copy headers and content.

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
