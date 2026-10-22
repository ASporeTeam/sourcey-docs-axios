# Interceptors {#interceptors}


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


## Order of execution {#order-of-execution}


- Request interceptors run in **reverse** order of registration (last added, first called).
- Response interceptors run in **registration** order.

Both are managed by `InterceptorManager` (`lib/core/InterceptorManager.js`).
An interceptor can be removed with the `id` returned by `use()`.


## Related {#related}


- [Instance API](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/instance/index.md)
- [Errors](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/errors/index.md)
