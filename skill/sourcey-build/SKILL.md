---
name: sourcey-build
description: Rebuild the Sourcey-generated axios reference from the pinned upstream tree, verify the published site answers from outside, and seal both facts into one runx receipt.
---

# Sourcey build (native, model-free)

Three recorded steps, no model in the loop:

1. `build` — run the generator and the Sourcey build for the pinned axios tree.
2. `verify` — fetch the published site from outside and record what answered.
3. `attest` — bind the build, the published URL and their digests into the receipt.

Everything the receipt claims is a step output, so `runx verify <receipt-id>`
recomputes it.
