# Governed runx receipt for the published axios reference

Receipt (sealed, model-free skill run):

    sha256:5a8f58d50fcf85536faf23742d2972208d6d9aa9b077735f814fcf328141e218

Recompute it:

```bash
/srv/shared/gc/notes/runx-cli/runx verify \
  sha256:5a8f58d50fcf85536faf23742d2972208d6d9aa9b077735f814fcf328141e218 \
  --receipt-dir /srv/shared/gc/notes/agent4-sourcey-docs/receipts --trust home
# -> tree sha256:5a8f58d5... (4 receipts): ok
#    verification: ok
```

The skill that produced it: `skill/sourcey-build` (Sourcey build -> live fetch -> receipt.attest),
attestation decision `ready_to_seal`, gaps `[]`.

Re-seal it against any other published URL (for example a different host):

```bash
/srv/shared/gc/notes/runx-cli/runx skill \
  /srv/shared/gc/notes/agent4-sourcey-docs/skill/sourcey-build build \
  -i public_url=<public_url you deliver> \
  -i site_root=<site root> \
  -R /srv/shared/gc/notes/agent4-sourcey-docs/receipts --json
```
