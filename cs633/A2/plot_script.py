import os
import matplotlib.pyplot as plt

folder = r"C:\Users\cavlc\OneDrive\Desktop\^^\Acads\cs633\A2\output"

Ps = [32, 48, 64, 96]

data_120 = {p: [] for p in Ps}
data_240 = {p: [] for p in Ps}

def extract_time(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        return float(lines[-1])

# Read files
for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue

    parts = filename.split('_')
    p = int(parts[1][1:])
    n = int(parts[2][1:])

    filepath = os.path.join(folder, filename)
    t = extract_time(filepath)

    if n == 120:
        data_120[p].append(t)
    elif n == 240:
        data_240[p].append(t)

# Ensure correct order
for p in Ps:
    data_120[p].sort()
    data_240[p].sort()

# Plot
positions = [1, 2, 3, 4]

plt.figure(figsize=(9,6))

box1 = plt.boxplot([data_120[p] for p in Ps],
                   positions=[x - 0.2 for x in positions],
                   widths=0.3)

box2 = plt.boxplot([data_240[p] for p in Ps],
                   positions=[x + 0.2 for x in positions],
                   widths=0.3)

plt.xticks(positions, ['32', '48', '64', '96'])
plt.xlabel('Number of Processes (P)')
plt.ylabel('Time (seconds)')
plt.title('Execution Time vs Processes')

plt.legend([box1["boxes"][0], box2["boxes"][0]], ['120³', '240³'])

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

plt.savefig("final_plot.png", dpi=300)
plt.show()
