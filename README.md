# Achromatopsia

**The central hub of KOBI Studio.** Achromatopsia is the public entry point to our projects:

- **Open tools**: free-to-use tools you can use right away.
- **Repository index**: a map of every KOBI repository, listed below.
- **Ping monitor**: a GitHub Pages status page that watches our web tunnel.
- **Official documents**: documents and notes published by KOBI Studio.

## 🚀 Quick Start

**The central hub of KOBI Studio.** This repository is the entry point to our projects: it holds the core structure, the build orchestration, and links to every repository that makes up KOBI.

## 📦 Repositories

<!-- REPOS:START -->
| Repository | Visibility | Description |
|---|---|---|
| [Achromatopsia](https://github.com/yuzuyonami/Achromatopsia) | Public | KOBI hub: open tools, repository index, tunnel ping monitor, and official docs |
| [Suffusio](https://github.com/yuzuyonami/Suffusio) | Private 🔒 | Private repository |
| [Trachoma](https://github.com/yuzuyonami/Trachoma) | Private 🔒 | Private repository |
<!-- REPOS:END -->

> New repositories will be added to this table as KOBI grow

> Private repositories require access. Contact the maintainers if you need it.

Clone the public repository:

```bash
git clone https://github.com/yuzuyonami/Achromatopsia.git
cd Achromatopsia
```

> **Note:** `Suffusio` and `Trachoma` are private submodules (Kobi Internal System).
> They are skipped automatically and their folders will stay empty.
> Everything else in this repository works without them.

### For maintainers

If you have access to the private repositories:

```bash
git submodule update --checkout --init Suffusio Trachoma
```
