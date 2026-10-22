---
title: "Error handling guide"
description: "How to distinguish network failures, timeouts, HTTP errors and cancellations."
---


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
