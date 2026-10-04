## 🚀 Quick Start

**The central hub of KOBI Studio.** This repository is the entry point to our projects: it holds the core structure, the build orchestration, and links to every repository that makes up KOBI.

## 📦 Repositories

<!-- REPOS:START -->
| Repository | Visibility | Description |
|---|---|---|
| [Achromatopsia](https://github.com/yuzuyonami/Achromatopsia) | Public | Core structure, monorepo & build orchestrator (you are here) |
| Suffusio | Private | Isi deskripsi singkat di sini |
| Trachoma | Private | Isi deskripsi singkat di sini |
<!-- REPOS:END -->

> New repositories will be added to this table as KOBI grow

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
