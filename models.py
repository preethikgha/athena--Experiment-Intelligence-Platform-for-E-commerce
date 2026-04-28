import pandas as pd

df = pd.read_csv("events.csv")
users = pd.read_csv("user_assignments.csv")

df = df.merge(users, on="visitorid")

# ── Model A: Purchase popularity (conservative) ───────────
# recommends top 10 most PURCHASED items globally
top_items_a = (df[df["event"] == "transaction"]
               .groupby("itemid")
               .size()
               .sort_values(ascending=False)
               .head(10)
               .index.tolist())

# ── Model B: Engagement popularity (broader signal) ───────
# recommends top 10 most VIEWED+CARTED items

weight_map = {"view": 1, "addtocart": 3, "transaction": 5}
df["weight"] = df["event"].map(weight_map)

top_items_b = (df.groupby("itemid")["weight"]
               .sum()
               .sort_values(ascending=False)
               .head(10)
               .index.tolist())

print("Model A top 10 (purchase-based):", top_items_a)
print("Model B top 10 (engagement-based):", top_items_b)
print("\nOverlap between models:", len(set(top_items_a) & set(top_items_b)), "items")


control_df = df[df["variant"] == "control"].copy()
control_df["rec_relevant"] = control_df["itemid"].isin(set(top_items_a))

treatment_df = df[df["variant"] == "treatment"].copy()
treatment_df["rec_relevant"] = treatment_df["itemid"].isin(set(top_items_b))

control_df.to_csv("control_events.csv", index=False)
treatment_df.to_csv("treatment_events.csv", index=False)
print("\nSaved control_events.csv and treatment_events.csv")
