import pandas as pd
import hashlib

def assign_variant(visitor_id):
    h = int(hashlib.md5(str(visitor_id).encode()).hexdigest(), 16)
    return "control" if h % 2 == 0 else "treatment"

df = pd.read_csv("events.csv")

# assign each unique user to a variant
users = pd.DataFrame(df["visitorid"].unique(), columns=["visitorid"])
users["variant"] = users["visitorid"].apply(assign_variant)

print("Variant split:")
print(users["variant"].value_counts())

# save it
users.to_csv("user_assignments.csv", index=False)
print("\nSaved to user_assignments.csv")