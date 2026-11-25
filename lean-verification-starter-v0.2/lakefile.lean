import Lake
open Lake DSL

package «formal-project» where
  -- Add project-specific configuration here.

@[default_target]
lean_lib Proofs where
  srcDir := "."
  roots := #[`Proofs.Main]

-- For Mathlib projects, add a pinned dependency, for example:
-- require mathlib from git
--   "https://github.com/leanprover-community/mathlib4" @ "<PINNED_COMMIT>"
-- Then run `lake update` intentionally and commit lake-manifest.json.
