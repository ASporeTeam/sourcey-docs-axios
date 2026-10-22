# Request helpers {#request-helpers}


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


### `getAdapter` {#getadapter}


_No doc comment in the pinned source._

```typescript
axios.getAdapter(( adapters: AxiosAdapterConfig | AxiosAdapterConfig[] | undefined ): AxiosAdapter)
```


### `toFormData` {#toformdata}


_No doc comment in the pinned source._

```typescript
axios.toFormData(( sourceObj: object, targetFormData?: GenericFormData, options?: FormSerializerOptions ): GenericFormData)
```


### `formToJSON` {#formtojson}


_No doc comment in the pinned source._

```typescript
axios.formToJSON((form: GenericFormData | GenericHTMLFormElement): object)
```


### `isAxiosError` {#isaxioserror}


_No doc comment in the pinned source._

```typescript
axios.isAxiosError(<T = any, D = any, P = any>( payload: any ): payload is AxiosError<T, D, P>)
```


### `spread` {#spread}


_No doc comment in the pinned source._

```typescript
axios.spread(<T, R>(callback: (...args: T[]) => R): (array: T[]) => R)
```


### `isCancel` {#iscancel}


_No doc comment in the pinned source._

```typescript
axios.isCancel(<T = any, D = any, P = any>(value: any): value is CanceledError<T, D, P>)
```


### `all` {#all}


_No doc comment in the pinned source._

```typescript
axios.all(<T>(values: Array<T | Promise<T>>): Promise<T[]>)
```


### `mergeConfig` {#mergeconfig}


_No doc comment in the pinned source._

```typescript
axios.mergeConfig(<D = any, P = any>( config1: AxiosRequestConfig<D, P>, config2: AxiosRequestConfig<D, P> ): AxiosRequestConfig<D, P>)
```


### `create` {#create}


_No doc comment in the pinned source._

```typescript
axios.create((config?: CreateAxiosDefaults): AxiosInstance)
```


## Related {#related}


- [Instance API](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/instance/index.md) — the same helpers on a configured instance
- [Request config](https://asporeteam.github.io/sourcey-docs-axios/docs/reference/config/index.md) — options accepted by every helper
