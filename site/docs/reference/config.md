---
title: "Request config"
description: "Every axios request configuration option and the default value from the pinned source."
---


# Request config

Every request helper accepts a config object. The default values below are
parsed from `lib/defaults/index.js` in the pinned commit `e6b79d9cef79`.

| Option | Default |
|---|---|
| `transitional` | `transitionalDefaults` |
| `adapter` | `['xhr', 'http', 'fetch']` |
| `transformRequest` | `[` |
| `transformResponse` | `[` |
| `timeout` | `0` |
| `xsrfCookieName` | `'XSRF-TOKEN'` |
| `xsrfHeaderName` | `'X-XSRF-TOKEN'` |
| `maxContentLength` | `-1` |
| `maxBodyLength` | `-1` |
| `env` | `{` |
| `validateStatus` | `function validateStatus(status) {` |
| `headers` | `{` |

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
