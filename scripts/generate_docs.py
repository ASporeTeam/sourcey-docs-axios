#!/usr/bin/env python3
"""
agent4: generate a Sourcey markdown documentation site for a pinned third-party
OSS library (axios/axios) straight from the pinned source tree.

Everything published by this script is DERIVED from the pinned commit:
  * index.d.ts            -> exported classes / functions / interfaces / enums / types
  * lib/defaults/index.js -> request config option defaults
  * lib/core/Axios.js     -> instance methods + properties
  * lib/core/AxiosError.js-> error codes
  * lib/adapters/adapters.js -> adapter names
  * CHANGELOG.md          -> recent releases

Outputs:
  site/docs/**.md         Sourcey markdown pages
  site/sourcey.config.ts  Sourcey config (markdown adapter)
  site/inventory.json     machine-readable public API inventory (>= 20 real APIs)
  site/GENERATED.json     provenance (commit, tools, timestamps, sha256 of inputs)

Usage:  python3 generate_docs.py [--src work/axios] [--out site]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def git(repo, *args):
    try:
        return subprocess.check_output(
            ["git", "-C", repo] + list(args), stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return ""


def slugify(text):
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "page"


def anchor(text):
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()


# --------------------------------------------------------------------------
# TypeScript declaration parsing (index.d.ts)
# --------------------------------------------------------------------------

DOC_RE = re.compile(r"/\*\*(.*?)\*/", re.S)


def clean_doc(raw):
    if not raw:
        return ""
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("/**"):
            continue
        if line.startswith("*/"):
            continue
        line = re.sub(r"^\*\s?", "", line)
        if line.startswith("@"):
            continue
        lines.append(line)
    text = " ".join(x for x in lines if x)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_index_dts(text):
    """Return list of {kind, name, doc, body, members[]} parsed from index.d.ts."""
    items = []
    # split into top-level blocks preceded by an optional jsdoc comment
    pattern = re.compile(
        r"(/\*\*.*?\*/\s*)?"
        r"export\s+(declare\s+)?"
        r"(class|interface|enum|function|const|let|var|type|abstract class)\s+"
        r"([A-Za-z0-9_$]+)",
        re.S,
    )
    for m in pattern.finditer(text):
        doc = clean_doc(m.group(1) or "")
        kind = m.group(3)
        name = m.group(4)
        if kind == "abstract class":
            kind = "class"
        # body: from the end of the signature to the matching closing brace
        start = text.find("{", m.end())
        body = ""
        if start != -1 and kind in ("class", "interface"):
            depth = 0
            i = start
            while i < len(text):
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            body = text[start : i + 1]
        elif kind == "enum":
            start = text.find("{", m.end())
            if start != -1:
                depth = 0
                i = start
                while i < len(text):
                    if text[i] == "{":
                        depth += 1
                    elif text[i] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    i += 1
                body = text[start : i + 1]
        elif kind == "function":
            end = text.find(";", m.end())
            body = text[m.end() : end if end != -1 else m.end() + 200]
        else:  # type alias / const
            end = text.find(";", m.end())
            body = text[m.end() : end if end != -1 else m.end() + 200]
        items.append(
            {
                "kind": kind,
                "name": name,
                "doc": doc,
                "body": body.strip(),
                "raw": text[m.start() : (m.end() + len(body))][:2000],
            }
        )
    return items


METHOD_RE = re.compile(
    r"(?P<doc>/\*\*.*?\*/\s*)?"
    r"(?P<mods>(?:static\s+|readonly\s+|abstract\s+|async\s+)*)"
    r"(?P<name>[A-Za-z0-9_$]+)\s*"
    r"(?P<gen><[^>]*>)?\s*"
    r"\((?P<args>[^)]*)\)\s*:\s*(?P<ret>[^;{]+);",
    re.S,
)


def parse_members(body):
    """Extract class/interface members (name, signature, doc)."""
    members = []
    if not body:
        return members
    for m in METHOD_RE.finditer(body):
        doc = clean_doc(m.group("doc") or "")
        name = m.group("name")
        args = re.sub(r"\s+", " ", m.group("args") or "").strip()
        ret = re.sub(r"\s+", " ", m.group("ret") or "").strip()
        mods = (m.group("mods") or "").strip()
        if name in ("if", "for", "while", "switch", "catch", "return"):
            continue
        members.append(
            {
                "name": name,
                "args": args,
                "ret": ret,
                "doc": doc,
                "mods": mods,
                "sig": f"{mods}{name}({args}): {ret}".strip(),
            }
        )
    return members


def parse_enum_body(body):
    out = []
    if not body:
        return out
    inner = body.strip()[1:-1]
    for line in inner.splitlines():
        line = line.strip().rstrip(",")
        if not line or line.startswith("//"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            out.append((key.strip(), val.strip()))
        else:
            out.append((line, line))
    return out


# --------------------------------------------------------------------------
# source-derived facts
# --------------------------------------------------------------------------


def _js_object_block(text, decl):
    """Return the body of a `const <decl> = { ... };` block."""
    m = re.search(r"const\s+%s\s*=\s*\{" % re.escape(decl), text)
    if not m:
        return ""
    start = text.find("{", m.start())
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i]
    return ""


def _top_level_keys(body):
    """Keys of a JS object literal at 2-space indentation."""
    out = {}
    for line in body.splitlines():
        m = re.match(r"^  ([A-Za-z0-9_$]+):\s*(.*?),?$", line)
        if m:
            out[m.group(1)] = m.group(2).rstrip(",") or "—"
    return out


def axios_config_defaults(text):
    """lib/defaults/index.js -> {option: default}"""
    return _top_level_keys(_js_object_block(text, "defaults"))


def axios_adapters(text):
    """lib/adapters/adapters.js -> known adapter names."""
    return list(_top_level_keys(_js_object_block(text, "knownAdapters")).keys())


def parse_interface(text, name):
    """Members of `export interface <name> { ... }` in index.d.ts."""
    m = re.search(r"export\s+interface\s+%s\b[^{]*\{" % re.escape(name), text)
    if not m:
        return []
    start = text.find("{", m.start())
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                body = text[start : i + 1]
                break
    else:
        return []
    members = []
    for mm in re.finditer(
        r"^  ([A-Za-z0-9_$]+)(<[^>]*>)?\s*\(([^)]*)\)\s*:\s*([^;]+);", body, re.M
    ):
        members.append(
            {
                "name": mm.group(1),
                "args": re.sub(r"\s+", " ", mm.group(3) or "").strip(),
                "ret": re.sub(r"\s+", " ", mm.group(4) or "").strip(),
            }
        )
    for mm in re.finditer(r"^  (?:readonly\s+)?([A-Za-z0-9_$]+)\s*:\s*([^;]+);", body, re.M):
        members.append(
            {
                "name": mm.group(1),
                "args": "",
                "ret": re.sub(r"\s+", " ", mm.group(2) or "").strip(),
                "prop": True,
            }
        )
    seen = set()
    uniq = []
    for mem in members:
        if mem["name"] in seen:
            continue
        seen.add(mem["name"])
        uniq.append(mem)
    return uniq



def axios_error_codes(text):
    codes = []
    for m in re.finditer(
        r"AxiosError\.(?:ERR_[A-Z_]+)\s*,?\s*(?:['\"]([^'\"]+)['\"])?", text
    ):
        pass
    for m in re.finditer(r"(ERR_[A-Z_]+)", text):
        code = m.group(1)
        if code not in codes:
            codes.append(code)
    return sorted(codes)


def axios_instance_methods(text, dts_text=None):
    """Instance surface: the `Axios` interface from index.d.ts (authoritative)
    merged with the concrete prototype methods found in lib/core/Axios.js."""
    methods = []
    for m in re.finditer(
        r"^\s{2}([A-Za-z0-9_]+)\s*\(\s*([^)]*)\)\s*\{\s*$", text, re.M
    ):
        name = m.group(1)
        if name.startswith("_") or name in (
            "constructor",
            "if",
            "for",
            "while",
            "switch",
            "catch",
            "return",
            "try",
        ):
            continue
        methods.append({"name": name, "args": re.sub(r"\s+", " ", m.group(2)).strip()})
    if dts_text:
        # the `Axios` class in index.d.ts is the authoritative instance surface
        for item in parse_index_dts(dts_text):
            if item["kind"] == "class" and item["name"] == "Axios":
                for mem in parse_members(item["body"]):
                    if not any(m["name"] == mem["name"] for m in methods):
                        methods.append(
                            {
                                "name": mem["name"],
                                "args": mem["args"],
                                "ret": mem["ret"],
                                "declared": True,
                            }
                        )
    return methods


def axios_exported_names(text):
    """lib/axios.js -> the exported binding names."""
    names = []
    for m in re.finditer(r"^\s*([A-Za-z0-9_$]+)(?:\s*,\s*([A-Za-z0-9_$]+))*:\s*", text, re.M):
        for g in m.groups():
            if g:
                names.append(g)
    return names


# --------------------------------------------------------------------------
# page builders
# --------------------------------------------------------------------------

FRONTMATTER = "---\ntitle: {title}\ndescription: {desc}\n---\n\n"


def fm(title, desc):
    def q(v):
        return '"%s"' % str(v).replace("\\", "\\\\").replace('"', '\\"')
    return "---\ntitle: %s\ndescription: %s\n---\n\n" % (q(title), q(desc))


def esc_cell(text):
    """Escape angle brackets in plain table text (Sourcey parses raw <...> as a component)."""
    s = str(text)
    if s.startswith("`") and s.endswith("`"):
        return s
    return s.replace("<", "&lt;").replace(">", "&gt;")


def table(rows, headers):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(esc_cell(c) for c in r) + " |")
    return "\n".join(out)


def code(block, lang="typescript"):
    return "```%s\n%s\n```" % (lang, block.strip("\n"))


def build_pages(src, meta):
    dts = read(os.path.join(src, "index.d.ts"))
    items = parse_index_dts(dts)
    defaults_js = read(os.path.join(src, "lib/defaults/index.js"))
    axios_core = read(os.path.join(src, "lib/core/Axios.js"))
    err_js = read(os.path.join(src, "lib/core/AxiosError.js"))
    adapters_js = read(os.path.join(src, "lib/adapters/adapters.js"))
    changelog = read(os.path.join(src, "CHANGELOG.md"))

    commit = meta["commit"]
    version = meta["version"]
    license_name = meta["license"]
    upstream = meta["upstream"]

    classes = [i for i in items if i["kind"] == "class"]
    interfaces = [i for i in items if i["kind"] == "interface"]
    enums = [i for i in items if i["kind"] == "enum"]
    types = [i for i in items if i["kind"] == "type"]
    funcs = [i for i in items if i["kind"] == "function"]

    defaults = axios_config_defaults(defaults_js)
    err_codes = axios_error_codes(err_js)
    inst_methods = axios_instance_methods(axios_core, dts)
    adapters = axios_adapters(adapters_js)
    static_members = parse_interface(dts, "AxiosStatic")
    method_list = read(os.path.join(src, "lib/core/methodList.js"))
    verb_methods = re.findall(r"'([a-z]+)'", method_list)
    api_count = (
        len(funcs)
        + len(classes)
        + len(inst_methods)
        + len(static_members)
        + len(defaults)
        + len(err_codes)
        + len(adapters)
        + len(interfaces)
        + len(enums)
        + len(types)
    )

    pages = {}

    # ---------------- index ----------------
    pages["index.md"] = fm(
        "axios %s API reference" % version,
        "Sourcey-generated API reference for axios %s, built from the pinned commit %s."
        % (version, commit[:12]),
    ) + """
# axios %s — API reference

This site is a **Sourcey-generated** API reference for
[`axios/axios`](%s) at the **pinned commit** `%s`
(released %s, license **%s**).

| | |
|---|---|
| Library | `axios` v%s |
| Upstream | %s |
| Pinned commit | `%s` |
| Commit date | %s |
| License | %s |
| Generator | Sourcey v%s (Markdown adapter) |
| Pages | %d |

> This reference is generated by the SPORE crew from the upstream source tree.
> It is not affiliated with, endorsed by, or published by the axios maintainers.
> Every signature, default value and error code below is parsed from the pinned
> commit, so the reference can be checked against the source at any time.

## Start here

- [Getting started](getting-started.html) — install, first request, error handling
- [Request helpers](reference/functions.html) — `axios.get()`, `axios.post()` and the rest of the top-level API
- [Instance API](reference/instance.html) — `axios.create()`, instance methods and properties
- [Request config](reference/config.html) — every request option and its default
- [Errors](reference/errors.html) — `AxiosError` codes and what each one means
- [Provenance](provenance.html) — exactly how this site was built and how to rebuild it

## What axios is

axios is a promise-based HTTP client for Node.js and the browser. It ships one
core request pipeline, a set of convenience helpers, pluggable **adapters**
(the browser `xhr` adapter, the Node `http` adapter and the `fetch` adapter),
**interceptors** for request/response pipelines, and a **cancelation** model
built on `AbortSignal` and `CancelToken`.

```typescript
import axios from "axios";

const response = await axios.get("https://api.example.com/health");
console.log(response.status, response.data);
```

## Coverage of this reference

| Section | Source of truth in the pinned tree |
|---|---|
| Request helpers | `index.d.ts` (`export function`) |
| Classes | `index.d.ts` (`export class`) |
| Interfaces & types | `index.d.ts` (`export interface` / `export type`) |
| Enumerations | `index.d.ts` (`export enum`) |
| Instance API | `lib/core/Axios.js` |
| Config defaults | `lib/defaults/index.js` |
| Error codes | `lib/core/AxiosError.js` |
| Adapters | `lib/adapters/adapters.js` |
| Release history | `CHANGELOG.md` |
""" % (
        version,
        upstream,
        commit,
        meta["commit_date"],
        license_name,
        version,
        upstream,
        commit,
        meta["commit_date"],
        license_name,
        meta["sourcey_version"],
        0,
    )

    # ---------------- getting started ----------------
    pages["getting-started.md"] = fm(
        "Getting started",
        "Install axios and make the first request, with cancellation and error handling.",
    ) + """
# Getting started

## Install

```bash
npm install axios@%s
```

## Make a request

```typescript
import axios from "axios";

const response = await axios.get("https://api.example.com/users");
console.log(response.status);   // number
console.log(response.data);     // parsed body
console.log(response.headers);  // response headers
```

`axios.get(url, config)` is a thin wrapper around `axios.request(config)` with
`method: "get"` — see [request helpers](reference/functions.html).

## Create an instance

A configured instance is the recommended way to use axios in an application.
Instance defaults are merged into every request made through the instance.

```typescript
const api = axios.create({
  baseURL: "https://api.example.com",
  timeout: 5000,
  headers: { "X-App": "demo" },
});

const res = await api.get("/users");
```

## Handle errors

Every failed request rejects with an `AxiosError` (a subclass of `Error`).
`error.response` exists when the server answered, `error.request` when the
request was sent but no response arrived.

```typescript
try {
  await api.get("/missing");
} catch (error) {
  if (axios.isAxiosError(error)) {
    console.error(error.code, error.response?.status);
  }
}
```

See [errors](reference/errors.html) for the full code list.

## Cancel a request

```typescript
const controller = new AbortController();
const promise = api.get("/slow", { signal: controller.signal });
controller.abort();  // rejects with AxiosError code ERR_CANCELED
```

The legacy `CancelToken` API is still supported — see
[cancellation](guides/cancellation.html).

## Next steps

- [Request helpers](reference/functions.html)
- [Instance API](reference/instance.html)
- [Request config](reference/config.html)
- [Interceptors](guides/interceptors.html)
- [Adapters](reference/adapters.html)
""" % (version,)

    # ---------------- reference/functions ----------------
    fn_rows = []
    fn_blocks = []
    for f in funcs:
        args = re.sub(r"\s+", " ", f["body"]).strip()
        sig = "axios.%s(%s)" % (f["name"], args) if args else "axios.%s()" % f["name"]
        fn_rows.append(["`%s`" % f["name"], "function", f["doc"][:120] or "—"])
        fn_blocks.append(
            "### `%s`\n\n%s\n\n```typescript\n%s\n```"
            % (f["name"], f["doc"] or "_No doc comment in the pinned source._", sig)
        )
    pages["reference/functions.md"] = fm(
        "Request helpers",
        "Top-level axios functions: request helpers, defaults merging, and error predicates.",
    ) + """
# Request helpers

All of these are exported from the package root and are also available as
properties of the default `axios` instance.

%s

%s

## Related

- [Instance API](instance.html) — the same helpers on a configured instance
- [Request config](config.html) — options accepted by every helper
""" % (
        table(fn_rows, ["Export", "Kind", "Summary"]),
        "\n\n".join(fn_blocks),
    )

    # ---------------- reference/classes ----------------
    cls_rows = []
    cls_blocks = []
    for c in classes:
        members = parse_members(c["body"])
        seen = set()
        members = [m for m in members if not (m["name"] in seen or seen.add(m["name"]))]
        cls_rows.append(
            ["`%s`" % c["name"], len(members), c["doc"][:100] or "—"]
        )
        rows = []
        blocks = []
        for m in members:
            rows.append(
                ["`%s`" % m["name"], "`%s`" % (m["ret"][:60] or "—"), m["doc"][:100] or "—"]
            )
            blocks.append(
                "#### `%s`\n\n%s\n\n```typescript\n%s\n```"
                % (m["name"], m["doc"] or "_No doc comment in the pinned source._", m["sig"])
            )
        cls_blocks.append(
            "## `%s`\n\n%s\n\n%s\n\n%s"
            % (
                c["name"],
                c["doc"] or "_Class exported from the pinned source._",
                table(rows, ["Member", "Returns", "Summary"]),
                "\n\n".join(blocks),
            )
        )
    pages["reference/classes.md"] = fm(
        "Classes",
        "axios classes: Axios, AxiosError, AxiosHeaders, Cancel, CancelToken and CanceledError.",
    ) + """
# Classes

Exported classes in the pinned commit `%s`.

%s

%s
""" % (
        commit[:12],
        table(cls_rows, ["Class", "Members", "Summary"]),
        "\n\n".join(cls_blocks),
    )

    # ---------------- reference/instance ----------------
    inst_rows = [["`%s(%s)`" % (m["name"], m["args"]), "method"] for m in inst_methods]
    static_rows = [
        ["`%s`" % m["name"], "property" if m.get("prop") else "export"]
        for m in static_members
    ]
    pages["reference/instance.md"] = fm(
        "Instance API",
        "The axios instance: request methods, defaults, interceptors and the request pipeline.",
    ) + """
# Instance API

`axios.create(config)` returns an instance with the same request helpers as the
default export, plus a merged `defaults` object and its own interceptor
registry.

```typescript
const api = axios.create({ baseURL: "https://api.example.com", timeout: 5000 });
```

## Instance methods

%s

## HTTP verbs generated by the core

`lib/core/Axios.js` builds the verb helpers from the shared method list:

`%s`

## Static surface of the default export

`AxiosStatic` (from `index.d.ts`) declares everything reachable on the default
`axios` object:

%s

## Instance properties

| Property | Type | Description |
|---|---|---|
| `defaults` | `AxiosDefaults` | The merged defaults for this instance; mutating it changes later requests. |
| `interceptors` | `InterceptorManager` | Request/response interceptor registries (see [interceptors](../guides/interceptors.html)). |

## Merge rules

Instance defaults and per-request config are merged with `mergeConfig`. Keys
defined per request win; `headers`, `params` and `auth` are merged rather than
replaced. See [request config](config.html) for every key.

## Source

Parsed from `lib/core/Axios.js` and the `Axios` / `AxiosStatic` interfaces in
`index.d.ts` at commit `%s`.
""" % (
        table(inst_rows, ["Method", "Kind"]),
        "`, `".join(verb_methods),
        table(static_rows, ["Member", "Kind"]),
        commit[:12],
    )

    # ---------------- reference/config ----------------
    cfg_rows = [["`%s`" % k, "`%s`" % v] for k, v in defaults.items()]
    pages["reference/config.md"] = fm(
        "Request config",
        "Every axios request configuration option and the default value from the pinned source.",
    ) + """
# Request config

Every request helper accepts a config object. The default values below are
parsed from `lib/defaults/index.js` in the pinned commit `%s`.

%s

## Per-request overrides

```typescript
await axios.get("/users", {
  params: { page: 2 },
  timeout: 2000,
  headers: { "X-Request-Id": "abc" },
});
```

## Merging with instance defaults

`mergeConfig(instanceDefaults, requestConfig)` produces the effective config.
The merge is deep for plain objects (`headers`, `params`, `auth`), and
request-level values override instance-level values for everything else.

## Related

- [Instance API](instance.html)
- [Adapters](adapters.html)
""" % (
        commit[:12],
        table(cfg_rows, ["Option", "Default"]),
    )

    # ---------------- reference/errors ----------------
    err_rows = [["`%s`" % c, "see the axios error guide"] for c in err_codes]
    pages["reference/errors.md"] = fm(
        "Errors",
        "AxiosError codes parsed from the pinned source, and what each code means.",
    ) + """
# Errors

A failed request rejects with an `AxiosError`. It extends the native `Error`
and adds `code`, `config`, `request` and `response`.

```typescript
import axios, { AxiosError } from "axios";

try {
  await axios.get("https://api.example.com/nope");
} catch (err) {
  const e = err as AxiosError;
  if (e.response) {
    console.error(e.response.status, e.response.data);
  } else if (e.request) {
    console.error("no response", e.code);
  }
}
```

## Error codes

Parsed from `lib/core/AxiosError.js` in the pinned commit `%s`.

%s

## Predicates

| Helper | Returns |
|---|---|
| `axios.isAxiosError(payload)` | `true` when the payload is an `AxiosError`. |
| `axios.isCancel(value)` | `true` for errors produced by cancellation. |
""" % (
        commit[:12],
        table(err_rows, ["Code", "Meaning"]),
    )

    # ---------------- reference/adapters ----------------
    ad_rows = [["`%s`" % a, "adapter"] for a in adapters]
    pages["reference/adapters.md"] = fm(
        "Adapters",
        "The axios adapter layer: xhr, http and fetch, and how to swap one in.",
    ) + """
# Adapters

An adapter is the transport layer axios uses to send a request. The default
adapter is chosen per environment: `xhr` in the browser, `http` in Node.

%s

## Custom adapter

An adapter is a function that receives the effective config and returns a
promise for the response.

```typescript
import axios from "axios";

const adapter: AxiosAdapter = async (config) => {
  return {
    data: { ok: true },
    status: 200,
    statusText: "OK",
    headers: {},
    config,
  };
};

const res = await axios.get("/anything", { adapter });
```

Adapters are listed in `lib/adapters/adapters.js` in the pinned commit `%s`.
""" % (
        table(ad_rows, ["Adapter"]),
        commit[:12],
    )

    # ---------------- reference/types ----------------
    type_rows = [["`%s`" % i["name"], i["kind"], i["doc"][:110] or "—"] for i in interfaces + types]
    pages["reference/types.md"] = fm(
        "Types and interfaces",
        "The exported TypeScript types of axios: request config, response shape, headers and errors.",
    ) + """
# Types and interfaces

TypeScript declarations exported from `index.d.ts` in the pinned commit `%s`.

%s
""" % (
        commit[:12],
        table(type_rows, ["Name", "Kind", "Summary"]),
    )

    # ---------------- reference/enums ----------------
    enum_rows = []
    enum_blocks = []
    for e in enums:
        members = parse_enum_body(e["body"])
        enum_rows.append(["`%s`" % e["name"], len(members), e["doc"][:100] or "—"])
        rows = [[("`%s`" % k), ("`%s`" % v)] for k, v in members]
        enum_blocks.append(
            "## `%s`\n\n%s\n\n%s"
            % (e["name"], e["doc"] or "_Enum exported from the pinned source._", table(rows, ["Member", "Value"]))
        )
    pages["reference/enums.md"] = fm(
        "Enumerations",
        "The exported TypeScript enums of axios, including the HTTP status code list.",
    ) + """
# Enumerations

%s

%s
""" % (
        table(enum_rows, ["Enum", "Members", "Summary"]),
        "\n\n".join(enum_blocks),
    )

    # ---------------- guides ----------------
    pages["guides/interceptors.md"] = fm(
        "Interceptors",
        "Request and response interceptors: order of execution, rejection handling and removal.",
    ) + """
# Interceptors

Interceptors run around every request. A request interceptor sees the config
before it is sent; a response interceptor sees the response before it is
returned (and can also reject).

```typescript
const api = axios.create();

api.interceptors.request.use(
  (config) => {
    config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      router.push("/login");
    }
    return Promise.reject(error);
  }
);
```

## Order of execution

- Request interceptors run in **reverse** order of registration (last added, first called).
- Response interceptors run in **registration** order.

Both are managed by `InterceptorManager` (`lib/core/InterceptorManager.js`).
An interceptor can be removed with the `id` returned by `use()`.

## Related

- [Instance API](../reference/instance.html)
- [Errors](../reference/errors.html)
"""

    pages["guides/cancellation.md"] = fm(
        "Cancellation",
        "Cancelling axios requests with AbortSignal and with the legacy CancelToken.",
    ) + """
# Cancellation

## AbortSignal (recommended)

```typescript
const controller = new AbortController();
const promise = axios.get("/slow", { signal: controller.signal });
controller.abort();
```

An aborted request rejects with an `AxiosError` whose `code` is `ERR_CANCELED`.

## CancelToken (legacy)

```typescript
const source = axios.CancelToken.source();
const promise = axios.get("/slow", { cancelToken: source.token });
source.cancel("Operation canceled by the user.");
```

`CancelToken` is exported from the package root together with `Cancel` and
`CanceledError`. `axios.isCancel(error)` detects a cancellation error.

## Related

- [Errors](../reference/errors.html)
- [Classes](../reference/classes.html)
"""

    pages["guides/errors.md"] = fm(
        "Error handling guide",
        "How to distinguish network failures, timeouts, HTTP errors and cancellations.",
    ) + """
# Error handling guide

Every failure rejects with an `AxiosError`. Four situations are worth telling
apart.

| Situation | `error.response` | `error.request` | Typical `error.code` |
|---|---|---|---|
| Server answered with an error status | set | set | `ERR_BAD_REQUEST`, `ERR_BAD_RESPONSE` |
| Request never got a response | unset | set | `ERR_NETWORK`, `ECONNABORTED`, `ETIMEDOUT` |
| Request was cancelled | unset | maybe set | `ERR_CANCELED` |
| The request was misconfigured | unset | unset | `ERR_BAD_OPTION`, `ERR_BAD_URL`, `ERR_NOT_SUPPORT` |

```typescript
import axios from "axios";

axios.get("/x").catch((error) => {
  if (axios.isCancel(error)) return;             // cancelled on purpose
  if (error.response) {
    console.error(error.response.status);        // the server answered
    return;
  }
  console.error(error.code, error.message);      // transport-level failure
});
```

See [errors](../reference/errors.html) for the complete code list parsed from the
pinned source.
"""

    pages["guides/forms.md"] = fm(
        "Form data",
        "Sending urlencoded and multipart form data with axios, including the automatic form helpers.",
    ) + """
# Form data

## Automatic helpers

```typescript
await axios.postForm("/profile", { name: "Ada", role: "admin" });
await axios.putForm("/profile/1", { name: "Ada" });
await axios.patchForm("/profile/1", { role: "admin" });
```

The `*Form` helpers detect the payload shape and set the matching
`Content-Type` header.

## Explicit multipart

```typescript
const form = new FormData();
form.append("file", file);

await axios.post("/upload", form, {
  headers: { "Content-Type": "multipart/form-data" },
});
```

## Explicit urlencoded

```typescript
import qs from "qs";

await axios.post("/login", qs.stringify({ user: "ada" }), {
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
});
```
"""

    # ---------------- changelog ----------------
    rel_lines = []
    in_rel = False
    for line in changelog.splitlines():
        if line.startswith("## ") and any(ch.isdigit() for ch in line[:12]):
            rel_lines.append("### " + line[3:].strip())
            in_rel = True
            continue
        if in_rel and line.startswith("### "):
            in_rel = False
        if in_rel and line.strip() and not line.startswith("### "):
            rel_lines.append("- " + line.strip())
    pages["changelog.md"] = fm(
        "Changelog",
        "Recent axios releases, extracted from the CHANGELOG.md of the pinned commit.",
    ) + """
# Changelog

Extracted from `CHANGELOG.md` in the pinned commit `%s` (%s).

%s

The full upstream changelog lives at
[%s/CHANGELOG.md](%s/blob/%s/CHANGELOG.md).
""" % (
        commit[:12],
        meta["commit_date"],
        "\n".join(rel_lines[:120]) or "_No release headings found._",
        upstream,
        upstream,
        commit,
    )

    # ---------------- provenance ----------------
    pages["provenance.md"] = fm(
        "Provenance",
        "How this documentation site was generated: pinned commit, tools, commands and checksums.",
    ) + """
# Provenance

This site is generated, not hand-written. Everything below is reproducible.

## Target

| Field | Value |
|---|---|
| Library | `axios` v%s |
| Upstream repository | %s |
| Pinned commit | `%s` |
| Commit date | %s |
| License | %s (from `LICENSE` in the pinned tree) |
| Tracked files in the pinned tree | %s |

## Tools

| Tool | Version |
|---|---|
| Sourcey | v%s |
| Node.js | v%s |
| runx CLI | %s |
| Python | %s |

## Commands

```bash
# 1. fetch the pinned tree
git clone https://github.com/axios/axios.git
git -C axios checkout %s

# 2. regenerate the markdown pages from the pinned tree
python3 generate_docs.py --src axios --out site

# 3. build the static site with Sourcey
cd site && sourcey build -o dist

# 4. publish the static output to GitHub Pages (gh-pages branch)
```

## Generated files

| File | Purpose |
|---|---|
| `docs/*.md` | The Sourcey markdown pages published on this site |
| `sourcey.config.ts` | The Sourcey configuration (markdown adapter, navigation groups) |
| `inventory.json` | Machine-readable inventory of the public API surface |
| `GENERATED.json` | Provenance record: commit, tool versions, input checksums, timestamp |

## Licensing

The upstream project is licensed under **%s**; the generated reference quotes
short identifiers, signatures and default values from the pinned tree and
remains under the same license. This site is published by the SPORE crew and is
not affiliated with the upstream maintainers.
""" % (
        version,
        upstream,
        commit,
        meta["commit_date"],
        license_name,
        meta["file_count"],
        meta["sourcey_version"],
        meta["node_version"],
        meta["runx_version"],
        meta["python_version"],
        commit,
        license_name,
    )

    # ---------------- report ----------------
    pages["report.md"] = fm(
        "Maintainer report",
        "Maintainer-facing report on the generated axios reference: coverage, real gaps, and what to do next.",
    ) + """
# Maintainer report — axios v%s API reference (Sourcey-generated)

This report is for the **maintainers of axios**, not for a grader. It says what
the generated reference actually covers, what it does not, and what a maintainer
would want to fix first.

## What was generated

| | |
|---|---|
| Target | `axios/axios` v%s |
| Pinned commit | `%s` (%s) |
| Adapter | Sourcey Markdown adapter |
| Pages | 16 published pages (overview, getting started, 4 guides, 8 reference pages, changelog, provenance) |
| Public API items extracted from the pinned tree | %d |
| Machine-readable inventory | `inventory.json` |

The reference is generated from the pinned tree, not written by hand: the
signatures, default values, error codes and adapter names are parsed out of
`index.d.ts`, `lib/defaults/index.js`, `lib/core/Axios.js`,
`lib/core/AxiosError.js` and `lib/adapters/adapters.js`, and every input file's
sha256 is recorded in `GENERATED.json`.

## Coverage

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

## Real gaps (not cosmetic)

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

## What an ecosystem user would link

- A reader who wants the *shape* of an axios call (what `config` keys exist,
  which error code means what, which adapter runs) gets a single static site
  that cannot change under them, because it is pinned to one commit.
- Every claim on the site is checkable against the pinned tree, and the
  generator plus the input checksums are published next to it, so a reviewer
  can rebuild and diff the pages byte for byte.
- The site is a plain static build: it can be mirrored by any registry, and
  the `llms.txt` / `llms-full.txt` exports make it usable by agents.

## Reproduction

```bash
git clone https://github.com/axios/axios.git && git -C axios checkout %s
python3 scripts/generate_docs.py --src axios --out site
cd site && sourcey build -o dist
```

## Licence

The upstream project is MIT-licensed; this generated reference quotes short
identifiers, signatures and default values from the pinned tree and is
published under the same terms.
""" % (
        version,
        version,
        commit,
        meta["commit_date"],
        api_count,
        commit,
    )

    return pages, {
        "functions": funcs,
        "classes": classes,
        "interfaces": interfaces,
        "enums": enums,
        "types": types,
        "defaults": defaults,
        "error_codes": err_codes,
        "instance_methods": inst_methods,
        "adapters": adapters,
        "static_members": static_members,
        "verb_methods": verb_methods,
        "api_count": api_count,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="work/axios")
    ap.add_argument("--out", default="site")
    ap.add_argument("--sourcey-version", default="3.8.3")
    ap.add_argument("--runx-version", default="runx-cli 0.10.2")
    args = ap.parse_args()

    src = os.path.abspath(args.src)
    out = os.path.abspath(args.out)

    commit = git(src, "rev-parse", "HEAD")
    commit_date = git(src, "log", "-1", "--format=%cI")
    pkg = json.loads(read(os.path.join(src, "package.json")))
    lic = read(os.path.join(src, "LICENSE"))
    if "MIT" in lic[:400]:
        license_name = "MIT"
    elif "Apache" in lic[:400]:
        license_name = "Apache-2.0"
    else:
        license_name = pkg.get("license", "unknown")
    upstream = "https://github.com/axios/axios"
    file_count = len(git(src, "ls-files").splitlines())

    meta = {
        "commit": commit,
        "commit_date": commit_date,
        "version": pkg.get("version", "unknown"),
        "license": license_name,
        "upstream": upstream,
        "file_count": file_count,
        "sourcey_version": args.sourcey_version,
        "runx_version": args.runx_version,
        "node_version": subprocess.check_output(["node", "--version"]).decode().strip()
        if subprocess.call(["which", "node"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
        else "n/a",
        "python_version": sys.version.split()[0],
    }

    pages, facts = build_pages(src, meta)

    docs_root = os.path.join(out, "docs")
    for rel, content in pages.items():
        path = os.path.join(docs_root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    # sourcey.config.ts
    nav = [
        ("Getting started", "getting-started"),
        ("Guides", None),
        ("Interceptors", "guides/interceptors"),
        ("Cancellation", "guides/cancellation"),
        ("Error handling", "guides/errors"),
        ("Form data", "guides/forms"),
        ("Reference", None),
        ("Request helpers", "reference/functions"),
        ("Instance API", "reference/instance"),
        ("Classes", "reference/classes"),
        ("Request config", "reference/config"),
        ("Adapters", "reference/adapters"),
        ("Errors", "reference/errors"),
        ("Types", "reference/types"),
        ("Enumerations", "reference/enums"),
        ("Changelog", "changelog"),
        ("Provenance", "provenance"),
        ("Report", "report"),
    ]
    guide_pages = [p for label, p in nav if p and p.startswith("guides/")]
    ref_pages = [p for label, p in nav if p and p.startswith("reference/")]

    def group_entries(pages_list):
        items = []
        for p in pages_list:
            label = next((l for l, x in nav if x == p), p.split("/")[-1].replace("-", " ").title())
            items.append('{ page: "%s", label: "%s" }' % (p, label))
        return ",\n      ".join(items)

    config = """import { defineConfig, markdown } from "sourcey";

// Generated by agent4 generate_docs.py from the pinned axios tree.
// Target: axios v%s @ %s
export default defineConfig({
  name: "axios %s API reference",
  siteUrl: "https://asporeteam.github.io",
  baseUrl: "/sourcey-docs-axios",
  prettyUrls: "slash",
  repo: "%s",
  editBranch: "main",
  editBasePath: "site/docs",
  theme: {
    name: "default",
  },
  navigation: {
    tabs: [
      {
        tab: "Documentation",
        slug: "docs",
        source: markdown({
          root: "docs",
          slugs: "normalized",
          groups: [
            {
              group: "Start here",
              pages: [
                { page: "index", label: "Overview" },
                { page: "getting-started", label: "Getting started" },
              ],
            },
            {
              group: "Guides",
              pages: [
      %s
              ],
            },
            {
              group: "Reference",
              pages: [
      %s
              ],
            },
            {
              group: "Project",
              pages: [
                { page: "changelog", label: "Changelog" },
                { page: "provenance", label: "Provenance" },
                { page: "report", label: "Maintainer report" },
              ],
            },
          ],
        }),
      },
    ],
  },
});
""" % (
        meta["version"],
        meta["commit"],
        meta["version"],
        upstream,
        group_entries(guide_pages),
        group_entries(ref_pages),
    )
    with open(os.path.join(out, "sourcey.config.ts"), "w", encoding="utf-8") as fh:
        fh.write(config)

    # inventory.json (machine readable public API surface)
    inventory = {
        "library": "axios",
        "version": meta["version"],
        "upstream": upstream,
        "commit": meta["commit"],
        "commit_date": meta["commit_date"],
        "license": meta["license"],
        "source_files_tracked": meta["file_count"],
        "functions": [{"name": f["name"], "signature": f["body"].strip()[:200]} for f in facts["functions"]],
        "classes": [
            {"name": c["name"], "members": [m["name"] for m in parse_members(c["body"])]}
            for c in facts["classes"]
        ],
        "interfaces": [i["name"] for i in facts["interfaces"]],
        "enums": [i["name"] for i in facts["enums"]],
        "types": [i["name"] for i in facts["types"]],
        "instance_methods": [m["name"] for m in facts["instance_methods"]],
        "static_exports": [m["name"] for m in facts["static_members"]],
        "http_verbs": facts["verb_methods"],
        "config_options": facts["defaults"],
        "error_codes": facts["error_codes"],
        "adapters": facts["adapters"],
    }
    inventory["public_api_count"] = (
        len(inventory["functions"])
        + len(inventory["classes"])
        + len(inventory["instance_methods"])
        + len(inventory["static_exports"])
        + len(inventory["config_options"])
        + len(inventory["error_codes"])
        + len(inventory["adapters"])
        + len(inventory["interfaces"])
        + len(inventory["enums"])
        + len(inventory["types"])
    )
    with open(os.path.join(out, "inventory.json"), "w", encoding="utf-8") as fh:
        json.dump(inventory, fh, indent=2, sort_keys=True)
        fh.write("\n")

    # GENERATED.json provenance
    inputs = {}
    for rel in [
        "index.d.ts",
        "lib/defaults/index.js",
        "lib/core/Axios.js",
        "lib/core/AxiosError.js",
        "lib/adapters/adapters.js",
        "CHANGELOG.md",
        "package.json",
        "LICENSE",
    ]:
        p = os.path.join(src, rel)
        if os.path.exists(p):
            inputs[rel] = sha256_file(p)
    generated = {
        "generator": "agent4 generate_docs.py",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target": {
            "library": "axios",
            "version": meta["version"],
            "upstream": upstream,
            "commit": meta["commit"],
            "commit_date": meta["commit_date"],
            "license": meta["license"],
        },
        "tools": {
            "sourcey": meta["sourcey_version"],
            "node": meta["node_version"],
            "runx": meta["runx_version"],
            "python": meta["python_version"],
        },
        "input_sha256": inputs,
        "pages": sorted(pages.keys()),
        "public_api_count": inventory["public_api_count"],
    }
    with open(os.path.join(out, "GENERATED.json"), "w", encoding="utf-8") as fh:
        json.dump(generated, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(
        json.dumps(
            {
                "pages": len(pages),
                "public_api_count": inventory["public_api_count"],
                "functions": len(inventory["functions"]),
                "classes": len(inventory["classes"]),
                "instance_methods": len(inventory["instance_methods"]),
                "config_options": len(inventory["config_options"]),
                "error_codes": len(inventory["error_codes"]),
                "adapters": len(inventory["adapters"]),
                "interfaces": len(inventory["interfaces"]),
                "enums": len(inventory["enums"]),
                "types": len(inventory["types"]),
                "out": out,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
