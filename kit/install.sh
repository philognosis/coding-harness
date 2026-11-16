#!/usr/bin/env bash
# Copy the kit into a repository without overwriting anything that exists.
#
#   bash install.sh /path/to/your/repo
set -euo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-}"

if [[ -z "${TARGET}" || ! -d "${TARGET}" ]]; then
  echo "Usage: bash install.sh /path/to/your/repo"
  exit 1
fi

copied=0
skipped=0
while IFS= read -r -d '' file; do
  relative="${file#"${KIT}"/}"
  case "${relative}" in
    install.sh | README.md | gitignore.additions) continue ;;
  esac
  destination="${TARGET}/${relative}"
  if [[ -e "${destination}" ]]; then
    echo "skip   ${relative} (exists)"
    skipped=$((skipped + 1))
  else
    mkdir -p "$(dirname "${destination}")"
    cp "${file}" "${destination}"
    copied=$((copied + 1))
  fi
done < <(find "${KIT}" -type f -not -path "*/.git/*" -print0)

chmod +x "${TARGET}/scripts/check.sh" "${TARGET}"/.claude/hooks/*.py 2>/dev/null || true

# Ignore personal, machine-local agent files.
touch "${TARGET}/.gitignore"
while IFS= read -r line; do
  grep -qxF "${line}" "${TARGET}/.gitignore" || echo "${line}" >> "${TARGET}/.gitignore"
done < "${KIT}/gitignore.additions"

echo
echo "Copied ${copied} file(s), skipped ${skipped}."
echo "Next:"
echo "  1. Fill in AGENTS.md (Project section) and docs/GOALS.md."
echo "  2. Run: python3 scripts/sync_agent_config.py && python3 scripts/codemap.py"
echo "  3. Start a session and run /frame on your next feature."
