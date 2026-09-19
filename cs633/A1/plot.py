import pandas as pd
import matplotlib.pyplot as plt

# Read timing data
df = pd.read_csv("timing_data.txt", sep=r"\s+")

# Separate data sizes
M_values = [262144, 1048576]
P_values = [8, 16, 32]

# Prepare boxplot data
box_data = []
positions = []

position_offset = 0.2

for i, P in enumerate(P_values):
    for j, M in enumerate(M_values):
        subset = df[(df["P"] == P) & (df["M"] == M)]["time"]
        box_data.append(subset.values)
        
        # Position adjustment for side-by-side boxes
        if j == 0:
            positions.append(i + 1 - position_offset)
        else:
            positions.append(i + 1 + position_offset)

# Create figure
plt.figure(figsize=(10,6))

# Draw boxplots
bp = plt.boxplot(
    box_data,
    positions=positions,
    widths=0.3,
    patch_artist=True
)

# Color boxes
colors = ["lightblue", "lightgreen"] * len(P_values)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# Labels
plt.xticks([1,2,3], P_values)
plt.xlabel("Number of Processes (P)")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time vs Process Count")

# Legend
plt.plot([], [], color="lightblue", label="M = 262144")
plt.plot([], [], color="lightgreen", label="M = 1048576")
plt.legend()

plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("plot.png", dpi=300)
plt.show()
