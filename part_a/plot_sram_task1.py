import pandas as pd
import matplotlib.pyplot as plt

# Read the space-separated ngspice wrdata output
df = pd.read_csv('read_task1.csv', sep='\\s+', header=None,
                 names=['t1', 'vbl', 't2', 'vblb', 't3', 'vq', 't4', 'vqb'])

plt.figure(figsize=(10, 6))
plt.plot(df['t1']*1e9, df['vbl'], label='BL', linewidth=2)
plt.plot(df['t3']*1e9, df['vblb'], label='BLB', linewidth=2)
plt.plot(df['t1']*1e9, df['vq'], label='Q', linestyle='--')
plt.plot(df['t3']*1e9, df['vqb'], label='QB', linestyle='--')

plt.title('6T SRAM Read Operation')
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)
plt.savefig('sram_read_waveform_task1.png')
print("Plot successfully saved as sram_read_waveform_task1.png")