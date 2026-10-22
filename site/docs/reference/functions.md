---
title: "Request helpers"
description: "Top-level axios functions: request helpers, defaults merging, and error predicates."
---


# Request helpers

All of these are exported from the package root and are also available as
properties of the default `axios` instance.

| Export | Kind | Summary |
|---|---|---|
| `getAdapter` | function | — |
| `toFormData` | function | — |
| `formToJSON` | function | — |
| `isAxiosError` | function | — |
| `spread` | function | — |
| `isCancel` | function | — |
| `all` | function | — |
| `mergeConfig` | function | — |
| `create` | function | — |

### `getAdapter`

_No doc comment in the pinned source._

```typescript
axios.getAdapter(( adapters: AxiosAdapterConfig | AxiosAdapterConfig[] | undefined ): AxiosAdapter)
```

### `toFormData`

_No doc comment in the pinned source._

```typescript
axios.toFormData(( sourceObj: object, targetFormData?: GenericFormData, options?: FormSerializerOptions ): GenericFormData)
```

### `formToJSON`

_No doc comment in the pinned source._

```typescript
axios.formToJSON((form: GenericFormData | GenericHTMLFormElement): object)
```

### `isAxiosError`

_No doc comment in the pinned source._

```typescript
axios.isAxiosError(<T = any, D = any, P = any>( payload: any ): payload is AxiosError<T, D, P>)
```

### `spread`

_No doc comment in the pinned source._

```typescript
axios.spread(<T, R>(callback: (...args: T[]) => R): (array: T[]) => R)
```

### `isCancel`

_No doc comment in the pinned source._

```typescript
axios.isCancel(<T = any, D = any, P = any>(value: any): value is CanceledError<T, D, P>)
```

### `all`

_No doc comment in the pinned source._

```typescript
axios.all(<T>(values: Array<T | Promise<T>>): Promise<T[]>)
```

### `mergeConfig`

_No doc comment in the pinned source._

```typescript
axios.mergeConfig(<D = any, P = any>( config1: AxiosRequestConfig<D, P>, config2: AxiosRequestConfig<D, P> ): AxiosRequestConfig<D, P>)
```

### `create`

_No doc comment in the pinned source._

```typescript
axios.create((config?: CreateAxiosDefaults): AxiosInstance)
```

## Related

- [Instance API](instance.html) — the same helpers on a configured instance
- [Request config](config.html) — options accepted by every helper
