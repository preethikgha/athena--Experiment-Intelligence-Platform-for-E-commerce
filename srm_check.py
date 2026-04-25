import pandas as pd
from scipy.stats import chi2_contingency

users = pd.read_csv("user_assignments.csv")

n_control   = (users["variant"] == "control").sum()
n_treatment = (users["variant"] == "treatment").sum()
total       = n_control + n_treatment

expected_control   = total * 0.5
expected_treatment = total * 0.5

chi2, p_val, _, _ = chi2_contingency([
    [n_control,          n_treatment],
    [expected_control,   expected_treatment]
])

actual_ratio = n_control / total

print("=" * 45)
print("       SAMPLE RATIO MISMATCH CHECK")
print("=" * 45)
print(f"Control users   : {n_control:,}")
print(f"Treatment users : {n_treatment:,}")
print(f"Total users     : {total:,}")
print(f"Actual ratio    : {actual_ratio:.4f} (expected 0.5000)")
print(f"Chi-squared     : {chi2:.4f}")
print(f"p-value         : {p_val:.4f}")
print("-" * 45)

if p_val < 0.01:
    print(" SRM DETECTED — split is not 50/50")
    print("    Results may be unreliable.")
    print("    Investigate assignment logic.")
else:
    print(" NO SRM — split looks healthy")
    print("    Safe to trust experiment results.")

print("=" * 45)