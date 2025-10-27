import os
import pandas as pd
from collections import defaultdict

# 📁 Step 1: Set up the folder path and read roster files
folder_path = "roster_data"
all_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])

player_seasons = defaultdict(set)
player_positions = {}

# 🔁 Step 2: Process each roster file
for file in all_files:
    season = int(file.split("_")[1].split(".")[0])
    file_path = os.path.join(folder_path, file)

    try:
        df = pd.read_csv(file_path)

        # Retry with header in second row if necessary
        if "full_name" not in df.columns or "position" not in df.columns:
            df = pd.read_csv(file_path, header=1)

        # Still missing key columns
        if "full_name" not in df.columns or "position" not in df.columns:
            print(f"⚠️ Skipping {file} — missing 'full_name' or 'position' columns.")
            continue
    except Exception as e:
        print(f"❌ Error reading {file}: {e}")
        continue

    for _, row in df.iterrows():
        name = row.get("full_name")
        position = row.get("position")

        if pd.notna(name):
            player_seasons[name].add(season)
            if name not in player_positions and pd.notna(position):
                player_positions[name] = position

# 📊 Step 3: Calculate career lengths
career_lengths = []
for player, seasons in player_seasons.items():
    career_lengths.append({
        "full_name": player,
        "position": player_positions.get(player, "NAN"),
        "career_length": len(seasons)
    })

# 🧩 Step 4: Define grouped position categories
position_groups = {
    "OL": ["C", "G", "T", "OL"],
    "DL": ["DE", "DT", "NT", "DL"],
    "LB": ["OLB", "ILB", "MLB", "LB"],
    "DB": ["CB", "FS", "SS", "S", "DB"],
    "WR": ["WR"],
    "RB": ["RB", "FB"],
    "TE": ["TE"],
    "QB": ["QB"],
    "SP": ["K", "P", "LS", "KR", "PR", "SPEC"]
}

def map_position_group(pos):
    pos = str(pos).upper().strip()
    for group, codes in position_groups.items():
        if pos in codes:
            return group
    return "OTHER"

# 🧮 Step 5: Create DataFrame and group positions
career_df = pd.DataFrame(career_lengths)
career_df["position"] = career_df["position"].str.upper().str.strip()
career_df["position_group"] = career_df["position"].apply(map_position_group)

# ✅ Top 10 Longest Careers
print("\n✅ Top 10 Longest Careers:")
print(career_df.sort_values(by="career_length", ascending=False).head(10))

# 📊 Career length by grouped position
grouped = career_df.groupby("position_group")["career_length"].agg(["count", "mean", "median"]).sort_values("mean", ascending=False)

print("\n📊 Career Length by Position Group:")
print(grouped)
career_df.to_csv("career_summary.csv", index=False)
