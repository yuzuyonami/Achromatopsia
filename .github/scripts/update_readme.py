import json
import os
import re
import subprocess
import tomllib

TOML = ".github/repo-descriptions.toml"


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True)


def parse_github(url):
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$", url.strip())
    return m.groups() if m else None


# 1. Daftar repo: repo utama + semua submodule
entries = []  # (name, url)

slug = os.environ.get("GITHUB_REPOSITORY")
if slug:
    self_url = f"https://github.com/{slug}"
else:
    self_url = sh("git", "remote", "get-url", "origin").stdout.strip()
parsed = parse_github(self_url)
if parsed:
    entries.append((parsed[1], f"https://github.com/{parsed[0]}/{parsed[1]}"))

out = sh("git", "config", "-f", ".gitmodules",
         "--get-regexp", r"^submodule\..*\.url$").stdout
for line in out.splitlines():
    key, url = line.split(" ", 1)
    name = key[len("submodule."):-len(".url")]
    entries.append((name, url.strip()))

# 2. Baca TOML, tambahkan nama yang belum ada (deskripsi dikosongkan)
custom = {}
if os.path.exists(TOML):
    with open(TOML, "rb") as f:
        custom = tomllib.load(f)

missing = [n for n, _ in entries if n not in custom]
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
]

for name, url in entries:
    p = parse_github(url)
    if not p:
        rows.append(f"| {name} | Unknown | {custom.get(name) or '-'} |")
        continue
    owner, repo = p
    link = f"[{name}](https://github.com/{owner}/{repo})"

    r = sh("gh", "api", f"repos/{owner}/{repo}")
    if r.returncode == 0:
        d = json.loads(r.stdout)
        desc = (custom.get(name) or d.get("description") or "-").replace("|", "/")
        rows.append(f"| {link} | Public | {desc} |")
    else:
        desc = (custom.get(name) or "Private repository").replace("|", "/")
        rows.append(f"| {link} | Private 🔒 | {desc} |")

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
