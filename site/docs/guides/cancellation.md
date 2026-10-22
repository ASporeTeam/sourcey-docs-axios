---
title: "Cancellation"
description: "Cancelling axios requests with AbortSignal and with the legacy CancelToken."
---


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
