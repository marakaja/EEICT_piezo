import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_path = r'c:\Users\Mara\OneDrive - VUT\Dokumenty\EAGLE\projects\PiezoDriver\Piezo\Trace02.csv'

# Read the CSV flexibly. 
# sep=None and engine='python' tells pandas to automatically guess if it's separated by commas or semicolons
try:
    # Try reading without skipping rows first, or adjust skiprows if your file has a header block
    df = pd.read_csv(csv_path, sep=None, engine='python')
    
    # If the file has metadata rows at the top, pandas might still fail to parse the columns correctly.
    # If your actual data starts on row 4, uncomment the next line and comment the one above:
    # df = pd.read_csv(csv_path, sep=';', skiprows=3) # Often European instruments use ';'
    
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

print("Found columns:", df.columns.tolist())

if len(df.columns) < 3:
    print("Error: Could not find at least 3 columns. The CSV structure might be different.")
    print("Here is the raw first row:")
    print(df.head(1))
    exit()

# Extract columns dynamically
freq_col = df.columns[0]
mag_col = df.columns[1]
phase_col = df.columns[2]

# Ensure data is numeric (sometimes it reads as strings with commas instead of decimal points)
freq = pd.to_numeric(df[freq_col].astype(str).str.replace(',', '.'), errors='coerce')
z_mag = pd.to_numeric(df[mag_col].astype(str).str.replace(',', '.'), errors='coerce')
phase = pd.to_numeric(df[phase_col].astype(str).str.replace(',', '.'), errors='coerce')

# Keep only valid positive-frequency points for log-scale plotting and model evaluation
valid = freq.notna() & z_mag.notna() & phase.notna() & (freq > 0)
freq_plot = freq[valid].to_numpy()
z_mag_plot = z_mag[valid].to_numpy()
phase_plot = phase[valid].to_numpy()

# BVD parameters from identified equivalent circuit (table values)
C0 = 7.03e-9   # F
C1 = 0.53e-9   # F
L1 = 43.85e-3  # H
R1 = 15.20     # Ohm

# Theoretical BVD impedance
omega = 2 * np.pi * freq_plot
z_motional = R1 + 1j * omega * L1 + 1 / (1j * omega * C1)
y_total = 1j * omega * C0 + 1 / z_motional
z_bvd = 1 / y_total
z_bvd_mag = np.abs(z_bvd)
phase_bvd = np.angle(z_bvd, deg=True)

# Split into two charts: phase first, magnitude second
fig, (ax_phase, ax_mag) = plt.subplots(2, 1, figsize=(6, 5), sharex=True)

# Detect resonance frequency from measured phase in selected band
resonance_band = freq_plot < 300e3
if np.any(resonance_band):
    max_phase_idx = np.nanargmax(phase_plot[resonance_band])
    res_freq = freq_plot[resonance_band][max_phase_idx]
else:
    max_phase_idx = np.nanargmax(phase_plot)
    res_freq = freq_plot[max_phase_idx]

# Phase chart (first)
ax_phase.axvline(x=res_freq, color='green', linestyle='-', label='Resonance Frequency', linewidth=0.95)
ax_phase.semilogx(freq_plot, phase_plot, color='tab:red', linewidth=1.5, linestyle='--', label='Phase measured')
ax_phase.semilogx(freq_plot, phase_bvd, color='tab:orange', linewidth=1.2, linestyle='-.', label='Phase BVD theory')
ax_phase.set_ylabel(r'Phase $\theta$ ($^\circ$)')
ax_phase.grid(True, which="both", ls="--", alpha=0.5)
ax_phase.legend(loc='best', fontsize='small')
ax_phase.text(res_freq, ax_phase.get_ylim()[1] * 0.9, f'{res_freq:.1f} Hz', color='green', rotation=90, verticalalignment='top', horizontalalignment='right')

# Magnitude chart (second)
ax_mag.axvline(x=res_freq, color='green', linestyle='-', label='Resonance Frequency', linewidth=0.95)
ax_mag.loglog(freq_plot, z_mag_plot, color='tab:blue', linewidth=1.5, label='|Z| measured')
ax_mag.loglog(freq_plot, z_bvd_mag, color='black', linewidth=1.3, linestyle=':', label='|Z| BVD theory')
ax_mag.set_xlabel('Frequency (Hz)')
ax_mag.set_ylabel(r'Impedance Magnitude $|Z|$ ($\Omega$)')
ax_mag.grid(True, which="both", ls="--", alpha=0.5)
ax_mag.legend(loc='best', fontsize='small')

fig.suptitle('Piezoelectric Actuator Impedance Characteristics')
ax_mag.set_xlim(freq_plot.min(), 300e3)  # Limit x-axis to 300 kHz for better visibility
fig.tight_layout(rect=[0, 0, 1, 0.97])

# Save as PDF for high-quality IEEEtran inclusion
plt.savefig("src/impedance_graph.pdf", format='pdf', bbox_inches='tight')
plt.show()

print("Graph saved successfully!")