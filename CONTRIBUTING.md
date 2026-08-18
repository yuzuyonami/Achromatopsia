# Contributing to Achromatopsia

Thanks for your interest in this project! It started as a small collaborative build tool between friends, and has grown into **Kobi Build Bootstrapper** — the build orchestration tool behind KOBI Studio's tooling.

## Before You Start

- This repo covers the **public build tool** (SCons project generation, config management, godot-cpp handling, etc). Core internal application logic lives in a private submodule and isn't open for outside contribution.
- Please open an issue or reach out before starting large changes, so we can align on direction first.

## How to Contribute

1. Fork the repository
2. Create a branch for your change (`git checkout -b fix/build-flag-issue`)
3. Make your changes
4. Test that the tool still runs cleanly and generates valid SCons files
5. Commit with a clear message describing what and why
6. Open a Pull Request against `main`

## Code Style

- Keep the CLI/TUI logic readable and commented, especially anything non-obvious in the SCons generation or godot-cpp handling.
- Avoid introducing new dependencies unless discussed first.

## License & Sharing Changes Back

This project is licensed under **GPL-3.0**, which allows others to use, copy, and modify it freely — including for private use. In return, if you distribute a modified version of this project (e.g. sharing your fork or a build derived from it), the license requires that your source code changes also be made available under the same terms.

In short: fork it, edit it, build on it — just share improvements to *this* project back with the community under the same license, so everyone benefits from each other's changes.

See [`LICENSE`](./LICENSE) for full terms.

## Questions

Open an issue if anything here is unclear, or if you want to discuss an idea before building it.
