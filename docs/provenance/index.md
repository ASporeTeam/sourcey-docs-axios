# Provenance {#provenance}


This site is generated, not hand-written. Everything below is reproducible.


## Target {#target}


| Field | Value |
|---|---|
| Library | `axios` v1.21.0 |
| Upstream repository | https://github.com/axios/axios |
| Pinned commit | `e6b79d9cef796ca3a903bb83e51d4752b019fd67` |
| Commit date | 2026-10-21T14:39:55+02:00 |
| License | MIT (from `LICENSE` in the pinned tree) |
| Tracked files in the pinned tree | 506 |


## Tools {#tools}


| Tool | Version |
|---|---|
| Sourcey | v3.8.3 |
| Node.js | vv20.18.0 |
| runx CLI | runx-cli 0.10.2 |
| Python | 3.12.3 |


## Commands {#commands}


```bash
# 1. fetch the pinned tree
git clone https://github.com/axios/axios.git
git -C axios checkout e6b79d9cef796ca3a903bb83e51d4752b019fd67

# 2. regenerate the markdown pages from the pinned tree
python3 generate_docs.py --src axios --out site

# 3. build the static site with Sourcey
cd site && sourcey build -o dist

# 4. publish the static output to GitHub Pages (gh-pages branch)
```


## Generated files {#generated-files}


| File | Purpose |
|---|---|
| `docs/*.md` | The Sourcey markdown pages published on this site |
| `sourcey.config.ts` | The Sourcey configuration (markdown adapter, navigation groups) |
| `inventory.json` | Machine-readable inventory of the public API surface |
| `GENERATED.json` | Provenance record: commit, tool versions, input checksums, timestamp |


## Licensing {#licensing}


The upstream project is licensed under **MIT**; the generated reference quotes
short identifiers, signatures and default values from the pinned tree and
remains under the same license. This site is published by the SPORE crew and is
not affiliated with the upstream maintainers.
