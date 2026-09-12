> **Release mirror.** This repository is a read-only snapshot of
> `conformance` 1.0.1, published from Overturo's main
> development repository. Issues and pull requests are welcome here; accepted
> changes are ported upstream and appear in the next release snapshot.
> Security reports: see [SECURITY.md](./SECURITY.md).

# Conformance corpus

Shared fixtures every Overturo client is tested against. Each directory is one corpus:

- `api_responses/` — recorded API exchanges keyed by `operationId`, validated against the published OpenAPI document; what client tests stub (see its README for the placeholder grammar).
- `discovery/` — the flow-disclosure inventory a client decodes before a decision session exists.
- `signed_records/` — signed receipt and record envelopes with fixed key material, for verification round-trips.
- `fixtures/` — authorization decision fixtures for the round-trip conformance check (`test_corpus_roundtrip.py`).
