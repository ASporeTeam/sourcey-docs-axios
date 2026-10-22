# Classes {#classes}


Exported classes in the pinned commit `e6b79d9cef79`.

| Class | Members | Summary |
|---|---|---|
| `AxiosHeaders` | 31 | — |
| `AxiosError` | 1 | — |
| `CanceledError` | 0 | — |
| `Axios` | 13 | — |


## `AxiosHeaders` {#axiosheaders}


_Class exported from the pinned source._

| Member | Returns | Summary |
|---|---|---|
| `set` | `AxiosHeaders` | — |
| `get` | `AxiosHeaderParameters` | — |
| `has` | `boolean` | — |
| `delete` | `boolean` | — |
| `clear` | `boolean` | — |
| `normalize` | `AxiosHeaders` | — |
| `concat` | `AxiosHeaders` | — |
| `toJSON` | `Record<string, string>` | — |
| `from` | `AxiosHeaders` | — |
| `parseParameters` | `AxiosHeaderParameters` | — |
| `accessor` | `AxiosHeaders` | — |
| `setContentType` | `AxiosHeaders` | — |
| `getContentType` | `RegExpExecArray | null` | — |
| `hasContentType` | `boolean` | — |
| `setContentLength` | `AxiosHeaders` | — |
| `getContentLength` | `RegExpExecArray | null` | — |
| `hasContentLength` | `boolean` | — |
| `setAccept` | `AxiosHeaders` | — |
| `getAccept` | `RegExpExecArray | null` | — |
| `hasAccept` | `boolean` | — |
| `setUserAgent` | `AxiosHeaders` | — |
| `getUserAgent` | `RegExpExecArray | null` | — |
| `hasUserAgent` | `boolean` | — |
| `setContentEncoding` | `AxiosHeaders` | — |
| `getContentEncoding` | `RegExpExecArray | null` | — |
| `hasContentEncoding` | `boolean` | — |
| `setAuthorization` | `AxiosHeaders` | — |
| `getAuthorization` | `RegExpExecArray | null` | — |
| `hasAuthorization` | `boolean` | — |
| `getSetCookie` | `string[]` | — |
| `toString` | `string` | — |


#### `set` {#set}


_No doc comment in the pinned source._

```typescript
set(headerName?: string, value?: AxiosHeaderValue, rewrite?: boolean | AxiosHeaderMatcher): AxiosHeaders
```


#### `get` {#get}


_No doc comment in the pinned source._

```typescript
get(headerName: string, parser: typeof AxiosHeaders.parseParameters): AxiosHeaderParameters
```


#### `has` {#has}


_No doc comment in the pinned source._

```typescript
has(header: string, matcher?: AxiosHeaderMatcher): boolean
```


#### `delete` {#delete}


_No doc comment in the pinned source._

```typescript
delete(header: string | string[], matcher?: AxiosHeaderMatcher): boolean
```


#### `clear` {#clear}


_No doc comment in the pinned source._

```typescript
clear(matcher?: AxiosHeaderMatcher): boolean
```


#### `normalize` {#normalize}


_No doc comment in the pinned source._

```typescript
normalize(format: boolean): AxiosHeaders
```


#### `concat` {#concat}


_No doc comment in the pinned source._

```typescript
concat(...targets: Array<AxiosHeaders | RawAxiosHeaders | string | undefined | null>): AxiosHeaders
```


#### `toJSON` {#tojson}


_No doc comment in the pinned source._

```typescript
toJSON(asStrings: true): Record<string, string>
```


#### `from` {#from}


_No doc comment in the pinned source._

```typescript
staticfrom(thing?: AxiosHeaders | RawAxiosHeaders | string): AxiosHeaders
```


#### `parseParameters` {#parseparameters}


_No doc comment in the pinned source._

```typescript
staticparseParameters(value: AxiosHeaderValue): AxiosHeaderParameters
```


#### `accessor` {#accessor}


_No doc comment in the pinned source._

```typescript
staticaccessor(header: string | string[]): AxiosHeaders
```


#### `setContentType` {#setcontenttype}


_No doc comment in the pinned source._

```typescript
setContentType(value: ContentType, rewrite?: boolean | AxiosHeaderMatcher): AxiosHeaders
```


#### `getContentType` {#getcontenttype}


_No doc comment in the pinned source._

```typescript
getContentType(parser?: RegExp): RegExpExecArray | null
```


#### `hasContentType` {#hascontenttype}


_No doc comment in the pinned source._

```typescript
hasContentType(matcher?: AxiosHeaderMatcher): boolean
```


#### `setContentLength` {#setcontentlength}


_No doc comment in the pinned source._

```typescript
setContentLength(value: AxiosHeaderValue, rewrite?: boolean | AxiosHeaderMatcher): AxiosHeaders
```


#### `getContentLength` {#getcontentlength}


_No doc comment in the pinned source._

```typescript
getContentLength(parser?: RegExp): RegExpExecArray | null
```


#### `hasContentLength` {#hascontentlength}


_No doc comment in the pinned source._

```typescript
hasContentLength(matcher?: AxiosHeaderMatcher): boolean
```


#### `setAccept` {#setaccept}


_No doc comment in the pinned source._

```typescript
setAccept(value: AxiosHeaderValue, rewrite?: boolean | AxiosHeaderMatcher): AxiosHeaders
```


#### `getAccept` {#getaccept}


_No doc comment in the pinned source._

```typescript
getAccept(parser?: RegExp): RegExpExecArray | null
```


#### `hasAccept` {#hasaccept}


_No doc comment in the pinned source._

```typescript
hasAccept(matcher?: AxiosHeaderMatcher): boolean
```


#### `setUserAgent` {#setuseragent}


_No doc comment in the pinned source._

```typescript
setUserAgent(value: AxiosHeaderValue, rewrite?: boolean | AxiosHeaderMatcher): AxiosHeaders
```


#### `getUserAgent` {#getuseragent}


_No doc comment in the pinned source._

```typescript
getUserAgent(parser?: RegExp): RegExpExecArray | null
```


#### `hasUserAgent` {#hasuseragent}


_No doc comment in the pinned source._

```typescript
hasUserAgent(matcher?: AxiosHeaderMatcher): boolean
```


#### `setContentEncoding` {#setcontentencoding}


_No doc comment in the pinned source._

```typescript
setContentEncoding(value: AxiosHeaderValue, rewrite?: boolean | AxiosHeaderMatcher): AxiosHeaders
```


#### `getContentEncoding` {#getcontentencoding}


_No doc comment in the pinned source._

```typescript
getContentEncoding(parser?: RegExp): RegExpExecArray | null
```


#### `hasContentEncoding` {#hascontentencoding}


_No doc comment in the pinned source._

```typescript
hasContentEncoding(matcher?: AxiosHeaderMatcher): boolean
```


#### `setAuthorization` {#setauthorization}


_No doc comment in the pinned source._

```typescript
setAuthorization(value: AxiosHeaderValue, rewrite?: boolean | AxiosHeaderMatcher): AxiosHeaders
```


#### `getAuthorization` {#getauthorization}


_No doc comment in the pinned source._

```typescript
getAuthorization(parser?: RegExp): RegExpExecArray | null
```


#### `hasAuthorization` {#hasauthorization}


_No doc comment in the pinned source._

```typescript
hasAuthorization(matcher?: AxiosHeaderMatcher): boolean
```


#### `getSetCookie` {#getsetcookie}


_No doc comment in the pinned source._

```typescript
getSetCookie(): string[]
```


#### `toString` {#tostring}


_No doc comment in the pinned source._

```typescript
toString(): string
```


## `AxiosError` {#axioserror}


_Class exported from the pinned source._

| Member | Returns | Summary |
|---|---|---|
| `from` | `AxiosError<T, D, P>` | — |


#### `from` {#from-1}


_No doc comment in the pinned source._

```typescript
staticfrom(error: Error | unknown, code?: string, config?: InternalAxiosRequestConfig<D, P>, request?: any, response?: AxiosResponse<T, D, {}, P>, customProps?: object): AxiosError<T, D, P>
```


## `CanceledError` {#cancelederror}


_Class exported from the pinned source._

| Member | Returns | Summary |
|---|---|---|




## `Axios` {#axios}


_Class exported from the pinned source._

| Member | Returns | Summary |
|---|---|---|
| `getUri` | `string` | — |
| `request` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `get` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `delete` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `head` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `options` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `post` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `put` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `patch` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `postForm` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `putForm` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `patchForm` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |
| `query` | `Promise<AxiosResponseResult<T, R, D, P>>` | — |


#### `getUri` {#geturi}


_No doc comment in the pinned source._

```typescript
getUri(config?: AxiosRequestConfig): string
```


#### `request` {#request}


_No doc comment in the pinned source._

```typescript
request(config: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `get` {#get-1}


_No doc comment in the pinned source._

```typescript
get(url: string, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `delete` {#delete-1}


_No doc comment in the pinned source._

```typescript
delete(url: string, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `head` {#head}


_No doc comment in the pinned source._

```typescript
head(url: string, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `options` {#options}


_No doc comment in the pinned source._

```typescript
options(url: string, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `post` {#post}


_No doc comment in the pinned source._

```typescript
post(url: string, data?: D, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `put` {#put}


_No doc comment in the pinned source._

```typescript
put(url: string, data?: D, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `patch` {#patch}


_No doc comment in the pinned source._

```typescript
patch(url: string, data?: D, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `postForm` {#postform}


_No doc comment in the pinned source._

```typescript
postForm(url: string, data?: D, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `putForm` {#putform}


_No doc comment in the pinned source._

```typescript
putForm(url: string, data?: D, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `patchForm` {#patchform}


_No doc comment in the pinned source._

```typescript
patchForm(url: string, data?: D, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```


#### `query` {#query}


_No doc comment in the pinned source._

```typescript
query(url: string, data?: D, config?: AxiosRequestConfig<D, P>): Promise<AxiosResponseResult<T, R, D, P>>
```
