import pandas as pd
import numpy as np
from scipy import stats

control_df = pd.read_csv("control_events.csv")
treatment_df = pd.read_csv("treatment_events.csv")

def compute_metrics(df):
    users = df.groupby("visitorid").agg(
        viewed=("event", lambda x: (x == "view").sum()),
        carted=("event", lambda x: (x == "addtocart").sum()),
        purchased=("event", lambda x: (x == "transaction").sum())
    ).reset_index()

    users["ctr"]          = (users["viewed"] > 0).astype(int)
    users["cart_rate"]    = (users["carted"] > 0).astype(int)
    users["purchase_rate"] = (users["purchased"] > 0).astype(int)
    return users

control_users   = compute_metrics(control_df)
treatment_users = compute_metrics(treatment_df)

metrics = ["ctr", "cart_rate", "purchase_rate"]
alpha   = 0.05
bonferroni_alpha = alpha / len(metrics)

print(f"{'Metric':<18} {'Control':>10} {'Treatment':>10} {'Lift':>8} {'p-value':>10} {'Significant':>12}")
print("-" * 72)

results = {}
for m in metrics:
    c = control_users[m].values
    t = treatment_users[m].values

    _, p = stats.ttest_ind(c, t)
    lift = (t.mean() / c.mean() - 1) * 100
    sig  = p < bonferroni_alpha

    results[m] = {
        "control_mean":   c.mean(),
        "treatment_mean": t.mean(),
        "lift_pct":       lift,
        "p_value":        p,
        "significant":    bool(sig)
    }

    print(f"{m:<18} {c.mean():>10.4f} {t.mean():>10.4f} {lift:>+7.2f}% {p:>10.4f} {'✅ YES' if sig else '❌ NO':>12}")

print(f"\nBonferroni corrected alpha: {bonferroni_alpha:.4f}")

import json
with open("ab_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved ab_results.json")