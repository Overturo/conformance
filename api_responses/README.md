# Recorded API responses

Every file here is one exchange with the Overturo API, recorded from the real
service and checked against the published OpenAPI document before it was
written. A client test that stubs a response from a recording is testing
against what the API actually sends, not against what the test author
remembered.

- Recordings: 38 across 36 operations
- Published document digest: `23a37f9af0854d50` (the `document` field in every file)

## Layout

One file per operation, named by its `operationId`: `Vouches_show.json`. A
second recording of the same operation — a documented error status or a
variant such as a query flavor — carries a step suffix: `Vouches_show.404.json`,
`AuthorizationReceipts_show.signed.json`.

```json
{
  "operationId": "Vouches_show",
  "request":  { "method": "GET", "path": "/api/v1/vouches/<PREFIX_ID:1>", "headers": { "...": "..." }, "body": null },
  "response": { "status": 200, "headers": { "Content-Type": "application/json; charset=utf-8" }, "body": { "vouch": { "...": "..." } } },
  "document": "23a37f9af0854d50"
}
```

`request.body` is the raw JSON the client sent. `request.query` is present
when the request carried a query string.

## Placeholders

Values that change from one recording run to the next are replaced by
placeholders, so two recordings of the same exchange are byte-identical.

| Placeholder | Stands for |
|---|---|
| `<PREFIX_ID:n>` | A public identifier. The same identifier always maps to the same `n` within one file, so references stay consistent. |
| `2026-01-01T00:00:00Z` | Any timestamp. |
| `<TOKEN>` | A session, consent, or preview token (also in paths). |
| `https://example.com/URL_PLACEHOLDER` | An absolute URL that would carry the serving host and a token (kept URI-shaped). |
| `<SIGNATURE>`, `<PUBLIC_KEY>` | Signature material from the signing key of the recording run. |
| `<NONCE>`, `<CURSOR>`, `<OPAQUE>` | Nonces, pagination cursors, and values with no contract shape. |
| `corpus@example.com` | Any e-mail address. |
| `Bearer ovt_test_token`, `pk_test_corpus` | Credentials. Recordings never carry a live secret. |

A stub built from a recording should widen every placeholder in the path to
one path segment; the loaders shipped with each client do this.

## Consuming a recording

Look a recording up by `operationId` and install its response on your HTTP
double. Each Overturo client ships a loader that does this from a vendored
copy of this directory:

- Ruby: `ApiCorpus.stub!("Vouches_show")` (`spec/support/api_corpus.rb`)
- TypeScript: `corpusResponse("Vouches_show")` (`__tests__/support/corpus.ts`)
- Python: `corpus_route(router, "Vouches_show", BASE)` (`tests/corpus.py`)

## What a recording is not

A recording is a fixed example of a valid response, not the schema. The
published OpenAPI document is the contract; a recording made against an
older document carries a different digest and is regenerated, never patched
by hand.
