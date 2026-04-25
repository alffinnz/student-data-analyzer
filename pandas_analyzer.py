import pandas as pd

# -------------------------------
# Load CSV
# -------------------------------
try:
    df = pd.read_csv("students.csv")
except FileNotFoundError:
    print("❌ students.csv not found")
    exit()

# -------------------------------
# Add Total & Average
# -------------------------------
df["Total"] = df["Maths"] + df["Science"] + df["English"]
df["Average"] = df["Total"] / 3

# -------------------------------
# Grade Function
# -------------------------------
def get_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 50:
        return "C"
    else:
        return "Fail"

df["Grade"] = df["Average"].apply(get_grade)

# -------------------------------
# Display All Students
# -------------------------------
print("\n--- ALL STUDENTS ---")
print(df.to_string(index=False))

# -------------------------------
# Top Student
# -------------------------------
top = df.loc[df["Total"].idxmax()]
print("\nTop Student:")
print(f"{top['Name']} ({top['Total']} marks)")

# -------------------------------
# Failed Students
# -------------------------------
failed = df[df["Grade"] == "Fail"]

print("\nFailed Students:")
if failed.empty:
    print("None")
else:
    for name in failed["Name"]:
        print(name)

# -------------------------------
# Class Average
# -------------------------------
class_avg = df["Average"].mean()
print("\nClass Average:", round(class_avg, 2))

# -------------------------------
# Ranked Students
# -------------------------------
print("\n--- RANKED STUDENTS ---")
ranked = df.sort_values(by="Total", ascending=False)
print(ranked[["Name", "Total", "Average", "Grade"]].to_string(index=False))

# -------------------------------
# Save Results
# -------------------------------
df.to_csv("results.csv", index=False)
print("\n✅ Results saved to results.csv")