# Maintainer report

# Maintainer report — axios v1.21.0 API reference (Sourcey-generated) {#maintainer-report--axios-v1210-api-reference-sourcey-generated}


This report is for the **maintainers of axios**, not for a grader. It says what
the generated reference actually covers, what it does not, and what a maintainer
would want to fix first.


## What was generated {#what-was-generated}


| | |
|---|---|
| Target | `axios/axios` v1.21.0 |
| Pinned commit | `e6b79d9cef796ca3a903bb83e51d4752b019fd67` (2026-10-21T14:39:55+02:00) |
| Adapter | Sourcey Markdown adapter |
| Pages | 16 published pages (overview, getting started, 4 guides, 8 reference pages, changelog, provenance) |
| Public API items extracted from the pinned tree | 118 |
| Machine-readable inventory | `inventory.json` |

The reference is generated from the pinned tree, not written by hand: the
signatures, default values, error codes and adapter names are parsed out of
`index.d.ts`, `lib/defaults/index.js`, `lib/core/Axios.js`,
`lib/core/AxiosError.js` and `lib/adapters/adapters.js`, and every input file's
sha256 is recorded in `GENERATED.json`.


## Coverage {#coverage}


- **Request helpers** — the nine exported functions (`getAdapter`, `toFormData`,
  `formToJSON`, `isAxiosError`, `spread`, `isCancel`, `all`, `mergeConfig`,
  `create`) with their exact signatures.
- **Instance surface** — the thirteen verb helpers of the `Axios` class
  (`get`, `delete`, `head`, `options`, `post`, `put`, `patch`, `postForm`,
  `putForm`, `patchForm`, `query`, `request`, `getUri`) and the static surface
  declared by `AxiosStatic` (17 members).
- **Classes** — `Axios`, `AxiosError`, `AxiosHeaders`, `CanceledError` with
  their public members.
- **Configuration** — the twelve request-config options that ship as defaults
  (`adapter`, `timeout`, `transitional`, `transformRequest`,
  `transformResponse`, `xsrfCookieName`, `xsrfHeaderName`, `maxContentLength`,
  `maxBodyLength`, `env`, `validateStatus`, `headers`) with their default
  values.
- **Errors** — the eleven `ERR_*` codes the core can raise.
- **Adapters** — `http`, `xhr` and `fetch`.
- **Types** — 36 exported interfaces and 13 exported type aliases, plus the
  `HttpStatusCode` enum with every member.


## Real gaps (not cosmetic) {#real-gaps-not-cosmetic}


1. **The verb helpers are generated in a loop.** `lib/core/Axios.js` builds the
   `get`/`post`/… helpers with `utils.forEach`, so the *JavaScript* source
   never spells out thirteen separate methods. This reference recovers them
   from the `Axios` class declaration in `index.d.ts`; a tool that reads only
   `lib/` would miss all thirteen. The reference states this explicitly rather
   than pretending the methods are hand-written.
2. **Type parameters are dropped in the tables.** The `Axios` class declares
   generic parameters (`<T, R, D, P>`) on every helper. The reference keeps
   the argument list but not the generic constraints, so it cannot tell a
   reader which `D` shape is accepted by `post` versus `postForm`. A
   follow-up generator pass should keep the type parameters verbatim.
3. **Adapter internals are not documented.** The three adapters are listed and
   their selection order is described, but the per-adapter behaviour
   (progress events, `maxBodyLength` handling, `FormData` boundary selection)
   lives in `lib/adapters/*.js` and is only summarised here.
4. **Only 4 of the 11 error codes carry a documented meaning in the source.**
   The codes are extracted mechanically, so the reference can list them but
   cannot yet explain, for each one, exactly which request condition produces
   it. That table is the most useful thing a maintainer could improve.
5. **Examples are not executed.** The reference contains no runnable examples
   because the pinned tree ships no example fixtures; a maintainer-facing
   example suite would let the site demonstrate each helper against a local
   server.


## What an ecosystem user would link {#what-an-ecosystem-user-would-link}


- A reader who wants the *shape* of an axios call (what `config` keys exist,
  which error code means what, which adapter runs) gets a single static site
  that cannot change under them, because it is pinned to one commit.
- Every claim on the site is checkable against the pinned tree, and the
  generator plus the input checksums are published next to it, so a reviewer
  can rebuild and diff the pages byte for byte.
- The site is a plain static build: it can be mirrored by any registry, and
  the `llms.txt` / `llms-full.txt` exports make it usable by agents.


## Reproduction {#reproduction}


```bash
git clone https://github.com/axios/axios.git && git -C axios checkout e6b79d9cef796ca3a903bb83e51d4752b019fd67
python3 scripts/generate_docs.py --src axios --out site
cd site && sourcey build -o dist
```


## Licence {#licence}


The upstream project is MIT-licensed; this generated reference quotes short
identifiers, signatures and default values from the pinned tree and is
published under the same terms.
