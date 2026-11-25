# Lean 4 verification starter — Core-only smoke project

This is a ready-to-push minimal Lean 4 project. It uses the stable Lean toolchain `leanprover/lean4:v4.36.0` and does not depend on Mathlib. The GitHub Actions workflow installs Lean on a hosted runner, runs a source preflight, builds the project, and archives logs.

> Important: this package has **not** been compiled in the current ChatGPT container. A green GitHub Actions run is required before claiming that the project builds.

## What to do

1. Create a new empty GitHub repository, preferably private, named `lean-verification-lab` (do not add a README, license, or `.gitignore` during creation).
2. Upload the **contents of this folder** to the repository root. The root must directly contain `lean-toolchain`, `lakefile.lean`, `Proofs/`, `scripts/`, and `.github/`.
3. Commit the upload. GitHub Actions should start automatically. If it does not, open the repository's **Actions** tab and run **Lean verification** using **Run workflow**.
4. Open the workflow run. Confirm that `Source preflight` and `Build project` both pass. Download `lean-verification-evidence` from the run's Artifacts section to preserve the logs.

Uploading the ZIP file itself to the repository is not sufficient; GitHub Actions needs the extracted files at the repository root.

## Project contents

- `lean-toolchain`: exact Lean version pin.
- `lakefile.lean`: Lake package and `Proofs.Main` library target.
- `Proofs/Main.lean`: tiny smoke-test theorem and `#print axioms` check.
- `.github/workflows/lean.yml`: CI build and evidence archive.
- `scripts/audit_lean.py`: conservative text preflight for `sorry`, `admit`, explicit `axiom` declarations, and placeholder toolchains.
- `schemas/verification-report.schema.json`: report schema for later research tasks.
- `examples/VERIFICATION_REPORT.example.json`: illustrative `not_run` report, not an actual result.

## Evidence levels

1. **Source preflight** is a text scan, not proof checking.
2. **`lake build` passed** means the project compiled with the pinned Lean toolchain in that CI run.
3. **`#print axioms`** displays the axioms used by the smoke-test theorem. For research theorems, this must be run on each key theorem and reviewed against an explicit allowlist.
4. **Formalization review** must separately check that Lean definitions, hypotheses, and conclusions faithfully represent the original mathematical claim.

A green build alone does not establish mathematical correctness or semantic fidelity.

## Adding Mathlib later

Do not add a floating `master` dependency. Select a Mathlib revision compatible with the pinned Lean toolchain, declare it in `lakefile.lean`, run `lake update` intentionally, and commit the generated `lake-manifest.json`. The current starter is intentionally Core-only so the first CI test remains small and isolates the Lean environment from Mathlib dependency setup.
