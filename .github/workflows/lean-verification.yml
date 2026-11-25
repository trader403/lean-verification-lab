# Lean 4 Verification Lab — Core-only starter

This directory is a minimal Lean 4 project intended to provide a reproducible starting point for formal verification experiments. It currently uses Lean `leanprover/lean4:v4.36.0` and has no Mathlib dependency.

## Current verified state

The GitHub Actions workflow at `.github/workflows/lean-verification.yml` has completed successfully for commit `94abbd54526d1089d60176abfb757dc36d2433ea`:

- Source preflight scanned two Lean files and reported no `sorry`, `admit`, or explicit `axiom` declarations.
- `lake check-build` succeeded.
- `lake build Proofs` compiled `Proofs.Main` (the log reported `Built Proofs.Main`).
- The Lean action's build step also succeeded.
- `#print axioms FormalProject.identity_implication` reported that the theorem does not depend on any axioms.

Run evidence: <https://github.com/trader403/lean-verification-lab/actions/runs/45548463076>

This is an environment smoke test, not a research result. The theorem is elementary, and its formalization has not received an independent semantic review. A successful build establishes that Lean accepted the elaborated proof term; it does not establish that a future formalization faithfully captures an intended informal theorem.

## Repository layout

The repository root contains the GitHub Actions workflow under `.github/workflows/lean-verification.yml`. This project directory contains:

- `lean-toolchain` — exact Lean toolchain pin.
- `lakefile.lean` — Lake package and default `Proofs` library target.
- `lake-manifest.json` — generated Lake dependency lock/manifest; commit it so dependency resolution is reproducible.
- `Proofs/Main.lean` — minimal smoke-test theorem and its `#print axioms` command.
- `scripts/audit_lean.py` — conservative source/configuration preflight; not a Lean kernel verifier.
- `schemas/verification-report.schema.json` — schema for machine-readable verification records.
- `examples/` — illustrative reports and templates. A report marked as an example is not evidence of a successful run unless it identifies a real commit and run.

## Reproduce locally

From this directory, with elan and the pinned Lean toolchain installed:

```sh
python scripts/audit_lean.py --root . --report preflight-report.json
lake check-build
lake build Proofs
```

The GitHub Actions workflow runs the same preflight and explicit Lake checks, then runs the Lean action build. It archives the preflight report and generated manifest as workflow artifacts.

## Evidence levels

1. **Source preflight:** text-based screening only; it can miss syntactic or semantic cases and must not be described as proof verification.
2. **Lake/Lean build:** Lean elaborates and kernel-checks the generated declarations in the pinned environment.
3. **Axiom dependency inspection:** `#print axioms` reports the axioms used by a named theorem; the output must be retained and reviewed against a project-specific policy.
4. **Formalization review:** a separate review checks that definitions, assumptions, and conclusions match the intended mathematical claim.
5. **Independent checking:** an independent checker or separately reproduced verification path is additional evidence, not currently provided by this starter.

Do not collapse these evidence levels into a single unqualified “verified” status.

## Adding Mathlib later

Keep the current Core-only baseline stable. When Mathlib is needed, first select a revision compatible with the pinned Lean toolchain, add it explicitly to `lakefile.lean`, run `lake update`, and commit the resulting `lake-manifest.json`. Do not use a floating dependency revision for reproducibility-sensitive experiments.

## Source integrity manifest

`MANIFEST.sha256.json` covers the files inside this project directory, using paths relative to this directory. The manifest intentionally excludes itself to avoid a recursive hash. The repository-level GitHub Actions workflow is outside this manifest's scope; Git commits provide its version history.

Verify the manifest locally:

```sh
python scripts/verify_manifest.py --root .
```

The verifier checks each listed file's existence, byte length, and SHA-256 digest, and rejects duplicate paths, absolute paths, and path traversal. It is an integrity check for the listed source snapshot, not a proof checker or a substitute for Git commit signatures.
