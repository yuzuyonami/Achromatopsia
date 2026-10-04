import json
import os
import re
import subprocess
import tomllib

# Deskripsi manual (opsional)
custom = {}
if os.path.exists(".github/repo-descriptions.toml"):
    with open(".github/repo-descriptions.toml", "rb") as f:
        custom = tomllib.load(f)

out = subprocess.run(
    ["git", "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.url$"],
    capture_output=True, text=True,
).stdout

rows = [
    "| Repository | Visibility | Description |",
    "|---|---|---|",
    "| [Achromatopsia](https://github.com/yuzuyonami/Achromatopsia) | Public | "
    "Core structure, monorepo & build orchestrator (you are here) |",
]

for line in out.splitlines():
    key, url = line.split(" ", 1)
    name = key[len("submodule."):-len(".url")]
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url.strip())
    if not m:
        rows.append(f"| {name} | Unknown | {custom.get(name, '-')} |")
        continue
    owner, repo = m.groups()

    r = subprocess.run(["gh", "api", f"repos/{owner}/{repo}"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        d = json.loads(r.stdout)
        # Deskripsi manual menang, kalau tidak ada pakai deskripsi dari GitHub
        desc = custom.get(name) or d.get("description") or "-"
        desc = desc.replace("|", "/")
        rows.append(f"| [{name}](https://github.com/{owner}/{repo}) | Public | {desc} |")
    else:
        desc = (custom.get(name) or "Private repository").replace("|", "/")
        rows.append(f"| {name} | Private | {desc} |")

table = "\n".join(rows)

with open("README.md", encoding="utf-8") as f:
    text = f.read()

new = re.sub(
    r"(<!-- REPOS:START -->).*?(<!-- REPOS:END -->)",
    lambda m: f"{m.group(1)}\n{table}\n{m.group(2)}",
    text,
    flags=re.DOTALL,
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new)
