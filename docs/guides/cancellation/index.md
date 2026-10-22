# Cancellation {#cancellation}



## AbortSignal (recommended) {#abortsignal-recommended}


```typescript
const controller = new AbortController();
const promise = axios.get("/slow", { signal: controller.signal });
controller.abort();
```

An aborted request rejects with an `AxiosError` whose `code` is `ERR_CANCELED`.


## CancelToken (legacy) {#canceltoken-legacy}


```typescript
const source = axios.CancelToken.source();
const promise = axios.get("/slow", { cancelToken: source.token });
source.cancel("Operation canceled by the user.");
```

`CancelToken` is exported from the package root together with `Cancel` and
`CanceledError`. `axios.isCancel(error)` detects a cancellation error.


## Related {#related}


- [Errors](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/errors/index.md)
- [Classes](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/classes/index.md)
