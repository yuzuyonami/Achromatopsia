import json
import os
import re
import subprocess
import tomllib

TOML = ".github/repo-descriptions.toml"

# 1. Baca daftar submodule dari .gitmodules
out = subprocess.run(
    ["git", "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.url$"],
    capture_output=True, text=True,
).stdout

subs = []
for line in out.splitlines():
    key, url = line.split(" ", 1)
    name = key[len("submodule."):-len(".url")]
    subs.append((name, url.strip()))

# 2. Baca TOML, lalu tambahkan nama yang belum ada (deskripsi dikosongkan)
custom = {}
if os.path.exists(TOML):
    with open(TOML, "rb") as f:
        custom = tomllib.load(f)

missing = [n for n, _ in subs if n not in custom]
if missing:
    os.makedirs(os.path.dirname(TOML), exist_ok=True)
    needs_newline = False
    if os.path.exists(TOML) and os.path.getsize(TOML) > 0:
        with open(TOML, "rb") as f:
            f.seek(-1, os.SEEK_END)
            needs_newline = f.read(1) != b"\n"
    with open(TOML, "a", encoding="utf-8") as f:
        if needs_newline:
            f.write("\n")
        for n in missing:
            k = n if re.fullmatch(r"[A-Za-z0-9_-]+", n) else json.dumps(n)
            f.write(f'{k} = ""\n')
            custom[n] = ""

# 3. Bangun tabel README
rows = [
    "| Repository | Visibility | Description |",
    "|---|---|---|",
    "| [Achromatopsia](https://github.com/yuzuyonami/Achromatopsia) | Public | "
    "Core structure, monorepo & build orchestrator (you are here) |",
]

for name, url in subs:
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
    if not m:
        rows.append(f"| {name} | Unknown | {custom.get(name) or '-'} |")
        continue
    owner, repo = m.groups()

    r = subprocess.run(["gh", "api", f"repos/{owner}/{repo}"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        d = json.loads(r.stdout)
        desc = (custom.get(name) or d.get("description") or "-").replace("|", "/")
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
