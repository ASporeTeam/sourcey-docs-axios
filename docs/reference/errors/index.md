# Errors {#errors}


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


## Error codes {#error-codes}


Parsed from `lib/core/AxiosError.js` in the pinned commit `e6b79d9cef79`.

| Code | Meaning |
|---|---|
| `ERR_BAD_OPTION` | see the axios error guide |
| `ERR_BAD_OPTION_VALUE` | see the axios error guide |
| `ERR_BAD_REQUEST` | see the axios error guide |
| `ERR_BAD_RESPONSE` | see the axios error guide |
| `ERR_CANCELED` | see the axios error guide |
| `ERR_DEPRECATED` | see the axios error guide |
| `ERR_FORM_DATA_DEPTH_EXCEEDED` | see the axios error guide |
| `ERR_FR_TOO_MANY_REDIRECTS` | see the axios error guide |
| `ERR_INVALID_URL` | see the axios error guide |
| `ERR_NETWORK` | see the axios error guide |
| `ERR_NOT_SUPPORT` | see the axios error guide |


## Predicates {#predicates}


| Helper | Returns |
|---|---|
| `axios.isAxiosError(payload)` | `true` when the payload is an `AxiosError`. |
| `axios.isCancel(value)` | `true` for errors produced by cancellation. |
