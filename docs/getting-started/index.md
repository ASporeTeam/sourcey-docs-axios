# Getting started {#getting-started}



## Install {#install}


```bash
npm install axios@1.21.0
```


## Make a request {#make-a-request}


```typescript
import axios from "axios";

const response = await axios.get("https://api.example.com/users");
console.log(response.status);   // number
console.log(response.data);     // parsed body
console.log(response.headers);  // response headers
```

`axios.get(url, config)` is a thin wrapper around `axios.request(config)` with
`method: "get"` — see [request helpers](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/functions/index.md).


## Create an instance {#create-an-instance}


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


## Handle errors {#handle-errors}


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

See [errors](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/errors/index.md) for the full code list.


## Cancel a request {#cancel-a-request}


```typescript
const controller = new AbortController();
const promise = api.get("/slow", { signal: controller.signal });
controller.abort();  // rejects with AxiosError code ERR_CANCELED
```

The legacy `CancelToken` API is still supported — see
[cancellation](https://asporeteam.github.io/sourcey-docs-axios/docs/guides/cancellation/index.md).


## Next steps {#next-steps}


- [Request helpers](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/functions/index.md)
- [Instance API](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/instance/index.md)
- [Request config](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/config/index.md)
- [Interceptors](https://asporeteam.github.io/sourcey-docs-axios/docs/guides/interceptors/index.md)
- [Adapters](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/adapters/index.md)
