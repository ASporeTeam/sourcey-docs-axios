# Adapters {#adapters}


An adapter is the transport layer axios uses to send a request. The default
adapter is chosen per environment: `xhr` in the browser, `http` in Node.

| Adapter |
|---|
| `http` | adapter |
| `xhr` | adapter |
| `fetch` | adapter |


## Custom adapter {#custom-adapter}


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

Adapters are listed in `lib/adapters/adapters.js` in the pinned commit `e6b79d9cef79`.
