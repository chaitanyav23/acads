import os

folder = r"C:\Users\cavlc\OneDrive\Desktop\^^\Acads\cs633\A2\output"

Ps = [32, 48, 64, 96]
Ns = [120, 240]

# Initialize storage
data = {(p, n): [] for p in Ps for n in Ns}

def extract_time(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        return float(lines[-1])  # last line = time

# Read files
for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue

    try:
        parts = filename.split('_')
        p = int(parts[1][1:])   # p32 → 32
        n = int(parts[2][1:])   # n120 → 120

        filepath = os.path.join(folder, filename)
        t = extract_time(filepath)

        data[(p, n)].append(t)

    except Exception as e:
        print(f"Skipping {filename}: {e}")

# Sort runs (optional but clean)
for key in data:
    data[key].sort()

# Write output file
output_file = os.path.join(folder, "timing_data.txt")

with open(output_file, 'w') as f:
    f.write("P   n   run1   run2   run3   run4   run5\n")

    for p in Ps:
        for n in Ns:
            runs = data[(p, n)]
            
            if len(runs) != 5:
                print(f"WARNING: P={p}, n={n} has {len(runs)} runs")

            runs_str = "   ".join(f"{t:.6f}" for t in runs)
            f.write(f"{p}   {n}   {runs_str}\n")

print(f"\nTiming data written to: {output_file}")
