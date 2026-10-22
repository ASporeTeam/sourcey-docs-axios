---
title: "Getting started"
description: "Install axios and make the first request, with cancellation and error handling."
---


# Getting started

## Install

```bash
npm install axios@1.21.0
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
