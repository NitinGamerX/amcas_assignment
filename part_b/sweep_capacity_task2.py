import subprocess
import re
import math
import matplotlib.pyplot as plt

# Capacities to sweep: 256KB to 16MB (in bytes)
capacities_kb = [256, 512, 1024, 2048, 4096, 8192, 16384]
capacities_bytes = [k * 1024 for k in capacities_kb]

access_times = []
log2_capacities = []

print("Running CACTI Capacity Sweep (Task 2)...")
print("-" * 55)

for cap in capacities_bytes:
    # 1. Update the cache.cfg file dynamically using sed
    subprocess.run(['sed', '-i', f's/^-size (bytes).*/-size (bytes) {cap}/', 'cache_task1.cfg'])
    
    # 2. Run CACTI
    result = subprocess.run(['cacti', '-infile', 'cache_task1.cfg'], capture_output=True, text=True)
    
    # 3. Extract the Access time (ns) from the terminal output
    match = re.search(r'Access time \(ns\):\s*([\d.]+)', result.stdout)
    
    if match:
        delay = float(match.group(1))
        access_times.append(delay)
        log2_cap = math.log2(cap)
        log2_capacities.append(log2_cap)
        print(f"Capacity: {cap//1024:>5} KB | log2(Bytes): {log2_cap:>5.1f} | Access Time: {delay:.5f} ns")
    else:
        print(f"Failed to extract data for capacity {cap}")

# 4. Calculate the average delay increase per doubling
slopes = []
for i in range(1, len(access_times)):
    # Since log2(capacity) increases by exactly 1 at each step, 
    # the slope is just the difference in access time.
    slopes.append(access_times[i] - access_times[i-1])

avg_slope_ns = sum(slopes) / len(slopes)
avg_slope_ps = avg_slope_ns * 1000

# 5. Plot the results
plt.figure(figsize=(8, 5))
plt.plot(log2_capacities, access_times, marker='o', linewidth=2, color='b')
plt.title('SRAM L2 Access Time vs. Capacity')
plt.xlabel('$\\log_2$(Capacity in Bytes)')
plt.ylabel('Access Time (ns)')
plt.grid(True, linestyle='--', alpha=0.7)

# Add annotation for the report
plt.annotate(f'Avg Delay Increase per Doubling:\n{avg_slope_ps:.1f} ps', 
             xy=(log2_capacities[-3], access_times[-3]), 
             xytext=(log2_capacities[-5], access_times[-2]),
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6))

plt.tight_layout()
plt.savefig('sram_capacity_sweep_task2.png')
print("-" * 55)
print("Sweep complete! Plot saved as 'sram_capacity_sweep_task2.png'.")
print(f"Average delay increase per doubling: {avg_slope_ps:.1f} picoseconds.")

# 6. Reset config to our 2MB baseline
subprocess.run(['sed', '-i', 's/^-size (bytes).*/-size (bytes) 2097152/', 'cache_task1.cfg'])