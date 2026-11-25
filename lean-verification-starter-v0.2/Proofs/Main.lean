/-
Minimal smoke test. This theorem is only an environment check, not a research result.
-/

namespace FormalProject

theorem identity_implication (P : Prop) : P → P := by
  intro h
  exact h

#print axioms FormalProject.identity_implication

end FormalProject
