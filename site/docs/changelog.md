---
title: "Changelog"
description: "Recent axios releases, extracted from the CHANGELOG.md of the pinned commit."
---


# Changelog

Extracted from `CHANGELOG.md` in the pinned commit `e6b79d9cef79` (2026-10-21T14:39:55+02:00).

### v1.19.0 — July 22, 2026
- This release raises the form-data security floor, adds configuration and type-system capabilities, and fixes NO_PROXY matching, interceptor errors, progress reporting, and serialization edge cases.
- ## 🔒 Security Fixes
- - Multipart Form Data: Raised the form-data dependency floor to ^4.0.6, preventing fresh installations from resolving versions affected by the CRLF injection vulnerability GHSA-hmw2-7cc7-3qxx (https://github.com/advisories/GHSA-hmw2-7cc7-3qxx). (#11028)
- ## 🚀 New Features
- - Configuration Extensibility: Preserved own-enumerable symbol-keyed fields through mergeConfig and added a generic params type across public TypeScript declarations, responses, errors,
- adapters, and serializers. (#11043, #11081)
- - Header Parameter Parsing: Added the opt-in AxiosHeaders.parseParameters() parser for quote-aware, RFC-style HTTP parameter parsing while preserving legacy parsing behavior. (#11051)
- - HTTP Status Codes: Added the missing Cloudflare 520 WebServerReturnsAnUnknownError status and matching ESM/CJS declarations. (#11067)
- ## 🐛 Bug Fixes
- - Form Data Conversion: Limited formDataToJSON path splitting to dot and bracket notation, preserving literal punctuation in keys, and removed browser-facing Buffer.from usage from toFormData to avoid unnecessary polyfills. (#11006, #11018)
- - Proxy Bypass: Canonicalized IPv4 shorthand, octal, and hexadecimal forms during NO_PROXY matching and honored * entries within comma- or space-separated bypass lists. (#11029, #11053)
- - Cancellation: Propagated already-aborted input signals immediately when composing abort signals. (#11035)
- - Header Handling: Preserved empty first values for duplicate singleton headers and made AxiosHeaders#getSetCookie() consistently return arrays for present values. (#11036, #11037)
- - URL Handling: Included normalized, safely redacted offending URLs in malformed-protocol errors and removed repeated trailing slashes when combining base URLs. (#11008, #11038)
- - Progress Events: Clamped malformed negative progress values to zero and ensured final Node.js download progress events are delivered before streamed responses close. (#11039, #11040)
- - Error and JSON Serialization: Serialized Set values as arrays in JSON-compatible snapshots and synthesized useful AxiosError messages from otherwise-empty AggregateError instances. (#11044, #11059)
- - Content-Length Enforcement: Corrected base64 data: URL size estimation so maxContentLength is enforced consistently by the HTTP and Fetch adapters. (#11061)
- - Synchronous Interceptors: Prevented requests from being dispatched after synchronous request interceptors fail unless their paired rejection handler resolves successfully. (#11071)
- ## 🔧 Maintenance & Chores
- - Dependencies: Updated development and test tooling, the docs fixture's Axios version, and GitHub Actions integrations including Checkout, Setup Node, Setup Deno, and Zizmor. (#11031, #11055, #11056, #11058, #11079, #11080, #11088, #11089, #11090)
- - Build Outputs: Limited sourcemap generation to published minified bundles, removing broken map references from non-minified builds. (#11054)
- - Form Data Internals: Centralized FormData header handling and made the Node.js adapter tolerate getHeaders() returning undefined under the content-only policy. (#11062)
- - Developer Experience: Ignored common local AI-tooling directories and fixed a constant-reassignment crash when the development sandbox serves its root path. (#11032, #11073)
- - Documentation: Updated sponsor information, clarified that baseURL is not a path-security boundary, scoped provenance claims to attested releases, and corrected the configuration-defaults documentation. (#11041, #11068, #11076, #11078)
- - Publishing: Simplified v1 publishing to use the npm version bundled with Node.js 26 and updated package metadata for the 1.19.0 release. (#11083, #11095)
- ## 🌟 New Contributors
- We are thrilled to welcome our new contributors. Thank you for helping improve Axios:
- - @afonsojramos (#11028)
- - @MahinAnowar (#11006)
- - @yassertawfik4 (#11024)
- - @AnandSundar (#11029)
- - @lin-hongkuan (#11035)
- - @Wali007-lab (#11054)
- - @magicdawn (#11043)
- - @andrewkernel (#11053)
- - @Sagargupta16 (#11059)
- - @Rpaudel379 (#11078)
- - @kobihikri (#11076)
- - @spokodev (#11061)
- - @shaedrich (#11081)
- - @QodeXcli (#11062)
- - @akahoshi1421 (#11067)
- - @TheHonoredOne914 (#11071)
- - @Ahsan1Murtaza (#11073)
- [Full Changelog](https://github.com/axios/axios/compare/v1.18.1...v1.19.0)
### v1.18.0 — June 13, 2026
- This release hardens redirect and URL handling, improves the validateStatus configuration semantics, and includes updates to documentation, dependencies, and release metadata.
- ## 🔒 Security Fixes
- * **Redirect Header Safety:** Added Node HTTP adapter support for stripping caller-specified sensitive headers on cross-origin redirects, helping prevent custom auth headers such as API keys from leaking to another origin. (__#10892__)
- * **URL And Request Hardening:** Rejects malformed `http:` and `https:` URLs that omit `//` with `ERR_INVALID_URL`, while tightening prototype-pollution-safe config reads, stream size limits, FormData depth handling, data URL sizing, and local `NO_PROXY` matching. (__#11000__)
- ## 🐛 Bug Fixes
- * **Status Validation:** Added `transitional.validateStatusUndefinedResolves` so applications can opt in to treating `validateStatus: undefined` like the option was omitted, while `validateStatus: null` remains the explicit way to accept every status. (__#10899__)
- ## 🔧 Maintenance & Chores
- * **Documentation:** Published the v1.17.0 release notes, fixed a changelog typo, clarified the package update PR policy, and marked the `proxy` request config as Node.js-only in the advanced docs. (__#10984__, __#10988__, __#10992__, __#10995__)
- * **Dependencies:** Bumped `@babel/core`, `@babel/preset-env`, `@commitlint/cli`, `@commitlint/config-conventional`, `@rollup/plugin-babel`, `@rollup/plugin-commonjs`, `@vitest/browser`, `@vitest/browser-playwright`, `eslint`, `lint-staged`, `rollup`, `vitest`, and `actions/checkout`. (__#10989__, __#10996__, __#10997__)
- * **Release Metadata:** Prepared the 1.18.0 release by updating package metadata and the runtime `VERSION` value. (__#11003__)
- ## 🌟 New Contributors
- We are thrilled to welcome our new contributors. Thank you for helping improve axios:
- * __@drori12__ (__#10984__)
- * __@eyupcanakman__ (__#10899__)
- * __@Adi-Beker__ (__#10995__)
- [Full Changelog](https://github.com/axios/axios/compare/v1.17.0...v1.18.0)
### v1.17.0 — June 1, 2026
- This release adds Node HTTP zstd decompression, hardens config and release workflows, and fixes authentication, header, proxy, and type-handling regressions.
- ## 🔒 Security Fixes
- * **Config Hardening:** Guarded `socketPath`, `params`, and `paramsSerializer` reads with own-property checks to prevent inherited prototype values from affecting request behavior, including SSRF-sensitive paths. (__#10901__, __#10922__)
- * **Release Publishing:** Switched the publish workflow to npm staged publishing for safer, auditable package releases with provenance. (__#10926__)
- ## 🚀 New Features
- * **HTTP Compression:** Added Node HTTP adapter support for zstd response decompression, with `transitional.advertiseZstdAcceptEncoding` controlling whether `zstd` is advertised in `Accept-Encoding`. (__#6792__, __#10920__)
- ## 🐛 Bug Fixes
- * **Authentication Handling:** Restored Basic auth on same-origin Node redirects while continuing to strip credentials cross-origin, and aligned the fetch adapter with HTTP adapter behavior for URL-embedded Basic auth. (__#10929__, __#10896__)
- * **Proxy TLS:** Preserved user `httpsAgent` TLS options when tunneling HTTPS requests through HTTP CONNECT proxies. (__#10957__)
- * **React Native FormData:** Cleared default `Content-Type` for React Native `FormData` so multipart boundaries can be generated correctly. (__#10898__)
- * **Headers:** Silently skipped empty or whitespace-only header names instead of throwing, matching parsed-header behavior and avoiding React Native response crashes. (__#10875__)
- * **Request Data Merging:** Preserved enumerable symbol keys when cloning plain request data through axios merge logic. (__#10812__)
- * **Bundler Compatibility:** Converted `resolveConfig` from an arrow default export to a named function export to avoid webpack and Babel transform interop failures. (__#10891__)
- * **Types:** Corrected `AxiosHeaders.toJSON()` return types and updated CommonJS `isCancel` typings to narrow to `CanceledError<T>`. (__#10956__, __#10952__)
- * **Build Tooling:** Avoided emitting a null `Authorization` header from the GitHub build helper when `GITHUB_TOKEN` is unset. (__#10931__)
- ## 🔧 Maintenance & Chores
- * **HTTP/2 Internals:** Extracted `Http2Sessions` into its own helper module and added direct unit coverage for session pooling, timeout, and cleanup behavior. (__#10861__)
- * **Package Publishing:** Reduced published package size by switching to a `files` allowlist and dropping unneeded unminified bundle source maps. (__#10939__)
- * **CI and Release Automation:** Added bundle-size reporting, moved reports to the job summary, fixed bundle-size comparison coverage, added Node 26 to the matrix, pinned npm for staged publishing, and prepared the 1.17.0 release. (__#10907__, __#10911__, __#10916__, __#10927__, __#10935__, __#10983__)
- * **Developer Workflow:** Added a dev container and iterated on OpenSpec workflow files before removing them from the release branch. (__#10925__, __#10914__, __#10958__)
- * **Documentation and Policy:** Updated disclosure, contributor, collaboration, threat-model, advanced docs, README badges, release notes, moderator configuration, and project metadata. (__#10890__, __#10889__, __#10921__, __#10945__, __#10905__, __#10933__, __#10915__, __#10887__, __#10955__)
- * **Dependencies:** Bumped Babel tooling, Commitlint, ESLint, Rollup, Globals, Vitest, Playwright, `fs-extra`, `qs`, docs dependencies, and GitHub Actions dependencies including `actions/dependency-review-action` and `zizmorcore/zizmor-action`. (__#10871__, __#10879__, __#10918__, __#10919__, __#10934__, __#10947__, __#10954__, __#10960__)
- ## 🌟 New Contributors
- We are thrilled to welcome our new contributors. Thank you for helping improve axios:
- * __@BasixKOR__ (__#6792__)
- * __@carladams1299-lab__ (__#10861__)
- * __@LaplaceYoung__ (__#10812__)
- * __@JamieMagee__ (__#10939__)
- * __@RonGamzu__ (__#10905__)
- * __@sapirbaruch__ (__#10891__)
- * __@nezukoagent__ (__#10901__)
- * __@devareddy05__ (__#10929__)
- * __@Mohammad-Faiz-Cloud-Engineer__ (__#10922__)
- * __@azandabot__ (__#10931__)
- * __@niksy__ (__#10896__)
- [Full Changelog](https://github.com/axios/axios/compare/v1.16.1...v1.17.0)
### v1.16.1 — May 13, 2026
- This release ships a defence-in-depth fix for prototype pollution in `formDataToJSON`, hardens proxy and CI workflows, restores Webpack 4 compatibility for the fetch adapter, and includes several small bug fixes and maintenance improvements.
- ## 🔒 Security Fixes
- * **Prototype Pollution Defence-in-Depth:** Hardened `formDataToJSON` against already-polluted `Object.prototype` by walking own properties only, so attacker-controlled keys inherited from a poisoned prototype cannot propagate through deserialization. (__#7413__)
- * **Proxy Cleartext Leak:** Fixed an issue where HTTPS request data could be transmitted in cleartext to an HTTP proxy under certain configurations. (__#10858__)
- * **CI Cache Removal:** Removed all GitHub Actions caches as a defence-in-depth measure against cache poisoning vectors in the build pipeline. (__#10882__)
- ## 🐛 Bug Fixes
- * **Data URI Parsing:** Updated the `fromDataURI` regex to match RFC 2397 more strictly, fixing edge cases in `data:` URL handling. (__#10829__)
- * **Unicode Headers:** Preserved Unicode header values when running through request interceptors, so non-ASCII header content is no longer corrupted before dispatch. (__#10850__)
- * **XHR Upload Progress:** Guarded against malformed `ProgressEvent` payloads emitted by some environments during XHR upload, preventing crashes when `loaded` / `total` are missing or invalid. (__#10868__)
- * **Webpack 4 Fetch Adapter:** Fixed an "unexpected token" error caused by syntax in the fetch adapter that Webpack 4 could not parse, restoring compatibility for legacy bundler users. (__#10864__)
- * **Type Definitions:** Made `parseReviver` `context.source` optional in the type definitions to align with the ES2023 specification. (__#10837__)
- * **URL Object Support Reverted:** Reverted the change that allowed passing a `URL` object as `config.url` (originally __#10866__) due to regressions; this support will be reintroduced in a later release once the underlying issues are addressed. (__#10874__)
- ## 🔧 Maintenance & Chores
- * **Cycle Detection Refactor:** Replaced the array-based cycle tracker in `toJSONObject` with a `WeakSet`, improving performance and memory behaviour on large nested structures. (__#10832__)
- * **composeSignals Cleanup:** Refactored `composeSignals` to use a clearer early-return structure, simplifying the cancellation/abort composition path. (__#10844__)
- * **AI Readiness & Repo Docs:** Added `AGENTS.md` and related contributor-guide updates for both human and AI agents, plus post-release documentation improvements. (__#10835__, __#10841__)
- * **Docs Improvements:** Clarified the GET request example, fixed the interceptor `eject` example to reference the correct instance, and corrected the Buzzoid sponsor description in the README. (__#10836__, __#10853__, __#10856__)
- * **Sponsorship Tooling:** Fixed empty sponsor arrays in the sponsor processing script, added the ability to inject additional sponsors, updated the sponsorship link, and added a Twicsy advertisement entry. (__#10843__, __#10859__, __#10869__)
- * **Dependencies:** Bumped `@commitlint/cli` from 20.5.0 to 20.5.2. (__#10846__)

The full upstream changelog lives at
[https://github.com/axios/axios/CHANGELOG.md](https://github.com/axios/axios/blob/e6b79d9cef796ca3a903bb83e51d4752b019fd67/CHANGELOG.md).
