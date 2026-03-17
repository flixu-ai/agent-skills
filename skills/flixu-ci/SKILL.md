---
name: flixu-ci
description: Generate CI/CD pipeline configs that auto-translate locale files on push. Use when a developer asks to "automate translations", "add translation to CI", "create GitHub Action for i18n", "auto-translate on push", or "translation pipeline". Also triggers on "continuous localization", "translation PR", or "I don't want to translate manually". Do NOT use for one-time translations (use flixu-translate) or auditing (use translation-qa).
metadata:
  author: Flixu AI
  version: 1.0.0
  category: localization
  tags: [ci-cd, github-actions, gitlab-ci, automation, continuous-localization]
---

# Flixu CI

Generate CI/CD pipeline configurations that automatically translate new or changed strings when code is pushed. Supports GitHub Actions and GitLab CI.

## Bundled tools

- **`scripts/generate_workflow.py`** — Generates workflow files from parameters. Usage: `python scripts/generate_workflow.py --platform github --source messages/en.json --langs "de,fr,es"`. Use `--dry-run` to preview without writing files.

## Instructions

### Step 0: Authenticate

The workflow file can be generated without a key, but the CI runtime needs `FLIXU_API_KEY` as a repository secret.

Run `python shared/scripts/auth.py --check`. If not authenticated, run `python shared/scripts/auth.py` — the login flow validates the key and shows the plan/credits. The developer can then add this key as a CI secret.

### Step 1: Gather requirements

Ask the developer:
1. Where are your source locale files? (e.g., `messages/en.json`)
2. Which languages to translate to? (e.g., `de`, `fr`, `es`)
3. When should translations run? (push to main, every PR, manual dispatch)
4. Separate PR or commit to same branch?
5. Quality threshold to block merging? (e.g., 95% coverage)

Expected output: Answers to all 5 questions.

### Step 2: Generate the workflow

Run `scripts/generate_workflow.py` with the gathered parameters:

```bash
python scripts/generate_workflow.py \
  --platform github \
  --source messages/en.json \
  --langs "de,fr,es" \
  --branches main
```

Expected output: Workflow file written to `.github/workflows/flixu-translate.yml`.

Or for GitLab:
```bash
python scripts/generate_workflow.py \
  --platform gitlab \
  --source messages/en.json \
  --langs "de,fr"
```

### Step 3: Add quality gate (optional)

If the developer wants a quality threshold, add a separate PR quality check workflow. This blocks merges when translation coverage drops below the threshold:

```yaml
- name: Check coverage
  run: |
    SOURCE_KEYS=$(jq -r '[paths(scalars)] | length' "$SOURCE")
    # Compare each locale, fail if below threshold
```

See the templates below for the full workflow.

### Step 4: Configure secrets

| Platform | Where to add `FLIXU_API_KEY` |
|----------|------------------------------|
| GitHub Actions | Settings → Secrets and variables → Actions |
| GitLab CI | Settings → CI/CD → Variables (masked) |

Expected output: Secret added, workflow file committed, first run triggered on next push.

## Examples

### Example 1: GitHub auto-translate

User says: "Create a GitHub Action that auto-translates messages/en.json to de and fr on push to main"

Actions:
1. Run `python scripts/generate_workflow.py --platform github --source messages/en.json --langs "de,fr" --branches main`
2. Script writes `.github/workflows/flixu-translate.yml`
3. Remind developer to add `FLIXU_API_KEY` secret

Result: Workflow file created. On next push to main that changes `en.json`, translations auto-generated and PR created.

### Example 2: GitLab with quality gate

User says: "Set up auto-translation in our GitLab CI with a 95% coverage requirement"

Actions:
1. Run `scripts/generate_workflow.py --platform gitlab --source locales/en.yml --langs "de,fr,es"`
2. Add quality gate job to `.gitlab-ci.yml` that checks coverage threshold
3. Configure `FLIXU_API_KEY` as masked CI/CD variable

Result: Two-stage pipeline: translate on push, block merge if coverage below 95%.

## Troubleshooting

### Error: Workflow runs but no files change

Cause: The `paths` trigger doesn't match the actual source file location.
Solution: Verify the `paths` filter in the workflow matches your actual locale file path.

### Error: API call fails in CI with 401

Cause: `FLIXU_API_KEY` secret not configured or wrong value.
Solution: Add the secret in repository settings. Verify it starts with `flx_`.

### Error: PR created but translations incomplete

Cause: `jq` not available in the CI runner or JSON parsing failed.
Solution: Use a runner image that includes `jq`, or add `apt-get install -y jq` step.
