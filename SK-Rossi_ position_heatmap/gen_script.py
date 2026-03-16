import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap

MAP_PATH = "base-images/lotus.png"
OUT_DIR  = "C:/Code/VLT-Lotus-Analysis/SK-Rossi_ position_heatmap/Heatmaps"


zones = {
  "C Mound": (0.277, 0.622),
  "C Door": (0.327, 0.566),
  "C Hall": (0.132, 0.332),
  "C Site": (0.139, 0.448),
  "C Gravel": (0.387, 0.261),
  "C Bend": (0.075, 0.502),
  "C Main": (0.173, 0.54),
  "C Link": (0.356, 0.371),
  "C Waterfall": (0.271, 0.452),
  "C Lobby": (0.321, 0.762),
  "A Root": (0.694, 0.642),
  "A Drop": (0.907, 0.231),
  "A Stairs": (0.742, 0.337),
  "A Main": (0.733, 0.474),
  "A Tree": (0.861, 0.468),
  "A Door": (0.834, 0.527),
  "A Site": (0.855, 0.396),
  "A Link": (0.609, 0.471),
  "A Hut": (0.855, 0.322),
  "A Top": (0.795, 0.264),
  "A Rubble": (0.84, 0.602),
  "A Lobby": (0.669, 0.73),
  "B Site": (0.466, 0.44),
  "B Upper": (0.563, 0.371),
  "B Main": (0.436, 0.551),
  "B Pillars": (0.479, 0.668),
  "Attacker Spawn": (0.521, 0.828),
  "Defender Spawn": (0.611, 0.178),
}

kills_raw = {
    "C Mound": 9, "C Door": 2, "C Hall": 2, "C Site": 4,
    "C Gravel": 0, "C Bend": 0, "C Main": 6, "A Root": 4,
    "A Drop": 2, "C Link": 1, "B Main": 2, "B Site": 1,
    "A Stairs": 2, "A Main": 1, "A Tree": 2, "C Lobby": 1,
}
deaths_raw = {
    "B Main": 3, "A Door": 2, "C Site": 5, "C Hall": 4,
    "C Main": 5, "C Gravel": 2, "C Mound": 2, "C Bend": 1,
    "B Upper": 1, "B Pillars": 1, "Attacker Spawn": 1,
    "Defender Spawn": 1, "A Tree": 3, "A Main": 2, "A Site": 2,
    "B Site": 2, "A Rubble": 1, "A Stairs": 2, "A Root": 1,
    "C Lobby": 1, "A Lobby": 1, "C Waterfall": 1,
}

def make_gaussian_grid(data_dict, W, H, sigma_frac=0.09):
    grid = np.zeros((H, W), dtype=float)
    sigma = min(W, H) * sigma_frac
    xs = np.arange(W)
    ys = np.arange(H)
    XX, YY = np.meshgrid(xs, ys)
    for zone, val in data_dict.items():
        if not val or zone not in zones:
            continue
        fx, fy = zones[zone]
        cx, cy = fx * W, fy * H
        gauss = np.exp(-((XX - cx)**2 + (YY - cy)**2) / (2 * sigma**2))
        grid += gauss * val
    return grid

def add_labels(ax, data_dict, W, H):
    for zone, val in data_dict.items():
        if not isinstance(val, (int, float)) or val == 0 or zone not in zones:
            continue
        fx, fy = zones[zone]
        label = f"+{val}" if val > 0 else str(val)
        ax.text(fx * W, fy * H, label,
                color='white', fontsize=8.5, fontweight='bold',
                ha='center', va='center', zorder=5,
                bbox=dict(boxstyle='round,pad=0.18', fc='#000000', alpha=0.55, ec='none'))

map_img = Image.open(MAP_PATH).convert("RGBA")
W, H = map_img.size

# Colormaps
kill_cmap = LinearSegmentedColormap.from_list("kills", [
    (0.0, (0.125, 0.784, 0.698, 0.0)),
    (0.3, (0.125, 0.784, 0.698, 0.45)),
    (1.0, (0.050, 0.900, 0.780, 0.95)),
], N=256)

death_cmap = LinearSegmentedColormap.from_list("deaths", [
    (0.0, (0.820, 0.235, 0.216, 0.0)),
    (0.3, (0.820, 0.235, 0.216, 0.45)),
    (1.0, (0.950, 0.150, 0.120, 0.95)),
], N=256)

kd_cmap = LinearSegmentedColormap.from_list("kd", [
    (0.00, (0.95,  0.15, 0.12, 0.92)),
    (0.38, (0.82,  0.24, 0.22, 0.40)),
    (0.50, (0.00,  0.00, 0.00, 0.00)),
    (0.62, (0.125, 0.78, 0.70, 0.40)),
    (1.00, (0.05,  0.90, 0.78, 0.92)),
], N=512)

# Grids
grid_k = make_gaussian_grid(kills_raw, W, H)
grid_d = make_gaussian_grid(deaths_raw, W, H)

kd_dict = {}
for z in set(list(kills_raw) + list(deaths_raw)):
    kd_dict[z] = kills_raw.get(z, 0) - deaths_raw.get(z, 0)

grid_pos = make_gaussian_grid({z: v for z, v in kd_dict.items() if v > 0}, W, H)
grid_neg = make_gaussian_grid({z: abs(v) for z, v in kd_dict.items() if v < 0}, W, H)
mx = max(grid_pos.max(), grid_neg.max(), 1e-9)
grid_kd_norm = ((grid_pos - grid_neg) / mx + 1) / 2

def render(grid, cmap, vmin, vmax, title, label_data, outname):
    fig, ax = plt.subplots(figsize=(11, 11), dpi=130)
    fig.patch.set_facecolor("#0b0b0b")
    ax.set_facecolor("#0b0b0b")

    ax.imshow(map_img, extent=[0, W, H, 0], zorder=1)
    ax.imshow(grid, cmap=cmap, vmin=vmin, vmax=vmax,
              extent=[0, W, H, 0], interpolation='bilinear',
              alpha=1.0, zorder=2)

    add_labels(ax, label_data, W, H)

    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    ax.set_title(title, color="white", fontsize=14, fontweight="bold",
                 pad=8, loc="left", fontfamily="monospace")
    ax.text(0.01, 0.985, "SK ROSSI  ·  LOTUS", transform=ax.transAxes,
            color="#888888", fontsize=8.5, va="top", fontfamily="monospace")

    out = f"{OUT_DIR}/{outname}"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.06, facecolor="#0b0b0b")
    plt.close(fig)
    print(f"Saved {out}")

render(grid_k, kill_cmap, 0, grid_k.max(),
       "KILL HEATMAP", kills_raw, "rossi_kills.png")

render(grid_d, death_cmap, 0, grid_d.max(),
       "DEATH HEATMAP", deaths_raw, "rossi_deaths.png")

render(grid_kd_norm, kd_cmap, 0, 1,
       "K/D OVERLAY  [ teal = net +  |  red = net − ]",
       kd_dict, "rossi_kd_overlay.png")

print("All done.")