# Form data {#form-data}



## Automatic helpers {#automatic-helpers}


```typescript
await axios.postForm("/profile", { name: "Ada", role: "admin" });
await axios.putForm("/profile/1", { name: "Ada" });
await axios.patchForm("/profile/1", { role: "admin" });
```

The `*Form` helpers detect the payload shape and set the matching
`Content-Type` header.


## Explicit multipart {#explicit-multipart}


```typescript
const form = new FormData();
form.append("file", file);

await axios.post("/upload", form, {
  headers: { "Content-Type": "multipart/form-data" },
});
```


## Explicit urlencoded {#explicit-urlencoded}


```typescript
import qs from "qs";

await axios.post("/login", qs.stringify({ user: "ada" }), {
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
});
```
