#!/usr/bin/env bash
# One command that says whether the repo is healthy.
# Agents, the Stop hook, pre-push and CI all call this, so "done" means the
# same thing everywhere.
#
#   bash scripts/check.sh           full: lint, format, types, tests, UI build, code map, project rules
#   bash scripts/check.sh --quick   lint, format and types only (seconds)
set -uo pipefail

MODE="${1:-full}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILED=0

step() {
  local label="$1"
  shift
  echo "==> ${label}"
  if ! "$@"; then
    echo "FAILED: ${label}"
    FAILED=1
  fi
}

# Directories that hold a project file, ignoring dependencies and build output.
find_projects() {
  find "${ROOT}" -name "$1" \
    -not -path "*/node_modules/*" -not -path "*/.venv/*" \
    -not -path "*/.next/*" -not -path "*/.git/*" -not -path "*/dist/*" \
    -exec dirname {} \;
}

check_python() {
  local dir="$1"
  cd "${dir}" || return
  step "ruff check (${dir#"${ROOT}"/})" uv run --quiet ruff check .
  step "ruff format (${dir#"${ROOT}"/})" uv run --quiet ruff format --check .
  if grep -q "pyright" pyproject.toml; then
    step "pyright (${dir#"${ROOT}"/})" uv run --quiet pyright
  elif grep -q "mypy" pyproject.toml; then
    step "mypy (${dir#"${ROOT}"/})" uv run --quiet mypy .
  fi
  if [[ "${MODE}" != "--quick" ]] && grep -q "pytest" pyproject.toml; then
    step "pytest (${dir#"${ROOT}"/})" uv run --quiet pytest -q
  fi
}

check_ui() {
  local dir="$1"
  cd "${dir}" || return
  [[ -d node_modules ]] || step "pnpm install (${dir#"${ROOT}"/})" pnpm install --frozen-lockfile
  if grep -q '"lint"' package.json; then
    step "lint (${dir#"${ROOT}"/})" pnpm --silent lint
  fi
  if [[ -f tsconfig.json ]]; then
    step "tsc (${dir#"${ROOT}"/})" pnpm --silent exec tsc --noEmit
  fi
  if [[ "${MODE}" != "--quick" ]]; then
    if grep -q '"test"' package.json; then
      step "test (${dir#"${ROOT}"/})" pnpm --silent test
    fi
    if grep -q '"build"' package.json; then
      step "build (${dir#"${ROOT}"/})" pnpm --silent build
    fi
  fi
}

while IFS= read -r dir; do
  [[ -n "${dir}" ]] && check_python "${dir}"
done < <(find_projects "pyproject.toml")

while IFS= read -r dir; do
  [[ -n "${dir}" ]] && check_ui "${dir}"
done < <(find_projects "package.json")

cd "${ROOT}" || exit 1
if [[ -f scripts/codemap.py ]]; then
  step "code map is current" python3 scripts/codemap.py --check
fi
if [[ -f sgconfig.yml ]] && command -v ast-grep > /dev/null; then
  step "project lint rules" ast-grep scan
fi

if [[ "${FAILED}" -ne 0 ]]; then
  echo "CHECKS FAILED"
  exit 1
fi
echo "ALL CHECKS PASSED (${MODE})"
