import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
import sys
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
MAP_PATH = "base-images/lotus.png" 

ZONE_NAMES = [
    "C Mound",
    "C Door",
    "C Hall",
    "C Site",
    "C Gravel",
    "C Bend",
    "C Main",
    "C Link",
    "C Waterfall",
    "C Lobby",
    "A Root",
    "A Drop",
    "A Stairs",
    "A Main",
    "A Tree",
    "A Door",
    "A Site",
    "A Link",
    "A Hut",
    "A Top",
    "A Rubble",
    "A Lobby",
    "B Site",
    "B Upper",
    "B Main",
    "B Pillars",
    "Attacker Spawn",
    "Defender Spawn",
]
# ─────────────────────────────────────────────────────────────────────────────

if not os.path.exists(MAP_PATH):
    print(f"\n[ERROR] Map image not found: '{MAP_PATH}'")
    print("        Update MAP_PATH at the top of this script.\n")
    sys.exit(1)

img = Image.open(MAP_PATH).convert("RGBA")
W, H = img.size

state = {
    "index": 0,
    "clicks": {},   # zone_name -> (x_pct, y_pct)
    "dot": None,
    "label": None,
}

fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor("#0b0b0b")
ax.set_facecolor("#0b0b0b")
ax.imshow(img, extent=[0, W, H, 0])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")

# Instruction text at top
instruction = ax.text(
    0.5, 0.98, "", transform=ax.transAxes,
    color="white", fontsize=12, fontweight="bold",
    ha="center", va="top",
    bbox=dict(boxstyle="round,pad=0.4", fc="#000000", alpha=0.7, ec="#444444")
)

# Progress counter bottom-left
progress = ax.text(
    0.01, 0.01, "", transform=ax.transAxes,
    color="#888888", fontsize=9, va="bottom", fontfamily="monospace"
)

# Already-placed dots list
placed_dots = []
placed_labels = []

def update_prompt():
    idx = state["index"]
    total = len(ZONE_NAMES)
    if idx < total:
        zone = ZONE_NAMES[idx]
        instruction.set_text(f"Click  →  {zone}")
        progress.set_text(f"{idx + 1} / {total}  |  press 'u' to undo last")
    else:
        instruction.set_text("✓ All zones done!  Close window to print results.")
        progress.set_text(f"{total} / {total}  complete")
    fig.canvas.draw_idle()

def onclick(event):
    if event.inaxes != ax:
        return
    if event.xdata is None or event.ydata is None:
        return
    idx = state["index"]
    if idx >= len(ZONE_NAMES):
        return

    zone = ZONE_NAMES[idx]
    x_pct = round(event.xdata / W, 3)
    y_pct = round(event.ydata / H, 3)
    state["clicks"][zone] = (x_pct, y_pct)
    state["index"] += 1

    # Draw a dot + label on the map
    dot, = ax.plot(event.xdata, event.ydata, 'o',
                   color="#20c8b2", markersize=7, zorder=10)
    lbl = ax.text(event.xdata + W * 0.012, event.ydata - H * 0.012,
                  zone, color="white", fontsize=7.5, fontweight="bold",
                  zorder=11,
                  bbox=dict(boxstyle="round,pad=0.15", fc="#000000",
                            alpha=0.6, ec="none"))
    placed_dots.append(dot)
    placed_labels.append(lbl)

    print(f"  \"{zone}\": ({x_pct}, {y_pct}),")
    update_prompt()

def onkey(event):
    if event.key == 'u':
        # Undo last click
        if state["index"] == 0:
            return
        state["index"] -= 1
        last_zone = ZONE_NAMES[state["index"]]
        state["clicks"].pop(last_zone, None)
        if placed_dots:
            placed_dots.pop().remove()
        if placed_labels:
            placed_labels.pop().remove()
        print(f"  [undo] removed  \"{last_zone}\"")
        update_prompt()

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', onkey)

print("\n" + "="*55)
print("  ZONE COORDINATE PICKER  —  SK Rossi · Lotus")
print("="*55)
print(f"  Map : {MAP_PATH}  ({W}×{H} px)")
print(f"  Zones to place : {len(ZONE_NAMES)}")
print("  Controls : click = place zone | u = undo")
print("="*55 + "\n")
print("zones = {")

update_prompt()
plt.tight_layout(pad=0)
plt.show()

# ── Print final dict after window closes ─────────────────────────────────────
print("}\n")
print("="*55)
print(f"  Done — {len(state['clicks'])} / {len(ZONE_NAMES)} zones placed")
print("="*55)

if len(state["clicks"]) < len(ZONE_NAMES):
    missing = [z for z in ZONE_NAMES if z not in state["clicks"]]
    print(f"\n  Missing zones ({len(missing)}):")
    for z in missing:
        print(f"    - {z}")

print("\n  Copy the dict above into your heatmap script.\n")