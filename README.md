# sourcey-docs-axios

A **Sourcey-generated** API reference for [`axios/axios`](https://github.com/axios/axios),
built by the SPORE crew from a pinned upstream commit.

| | |
|---|---|
| Upstream | https://github.com/axios/axios |
| Pinned commit | see `site/GENERATED.json` |
| License of the upstream project | MIT |
| Generator | Sourcey v3.8.3 (Markdown adapter) |
| Published site | https://asporeteam.github.io/sourcey-docs-axios/docs/ |

This site is **not** affiliated with, endorsed by, or published by the axios
maintainers. Every signature, default value and error code in the reference is
parsed from the pinned upstream tree, so it can be checked against the source.

## Rebuild

```bash
# 1. the pinned upstream tree
git clone https://github.com/axios/axios.git
git -C axios checkout <pinned commit>

# 2. regenerate the markdown pages from that tree
python3 scripts/generate_docs.py --src axios --out site

# 3. build the static site with Sourcey (needs Node >= 22.19)
cd site && npm install sourcey@3.8.3 && npx sourcey build -o dist

# 4. publish
```

## Layout

- `site/docs/**.md` — the Sourcey markdown pages that produce the published site
- `site/sourcey.config.ts` — Sourcey configuration (navigation, theme, site URL)
- `site/inventory.json` — machine-readable inventory of the public API surface
- `site/GENERATED.json` — provenance record (commit, tool versions, input checksums)
- `scripts/generate_docs.py` — the generator that derives the pages from the pinned tree
