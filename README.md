# VLT Lotus Analysis

This repository contains a two-part Valorant esports analytics portfolio focusing on Velocity Gaming (VLT 2025) on the map Lotus. It demonstrates a dual-skillset: macro-level team strategy scouting and micro-level Position data visualization using Python.

## Project Structure

### 1. Anti-Strat Report (`Anti-Strat/`)

Contains `Basic-Playstyle-Antistrat.pdf`, a comprehensive strategic breakdown of VLT's highly aggressive composition. The report is broken down into actionable coaching insights:

* **Macro Playstyle & Identity:** Analysis of their fast-paced tendencies.


* **Defense & Attack Setups:** Detailed logging of standard site holds, economy round strategies, and heavy execute patterns.


* **Exploitable Weaknesses:** Targeted anti-stratting recommendations, such as isolating chamber on attack and punishing their C-Door retake habits.



### 2. Player Position Heatmaps (`SK-Rossi_position_heatmap/`)

Contains custom Python scripts and the resulting visual analytics mapping a player's spatial performance across the 3 analyzed matches.

* **`base-images/`**: The clean Lotus map asset.
* **`Heatmaps/`**:
* `rossi_kills.png`: Density heatmap of where the player successfully finds opening picks and trades.
* `rossi_deaths.png`: Density heatmap highlighting vulnerable positions and over-extensions.
* `rossi_kd_overlay.png`: A composite net K/D visualization (teal = net positive, red = net negative) to quickly identify the player's strongest and weakest map zones.


* **Scripts (`gen_script.py`, `helper-script.py`)**: The data processing and plotting logic used to generate the overlays.
