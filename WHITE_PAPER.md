# Acoustic Air Mover White Paper - REV 5.5

## 1. Abstract
This document outlines the design, simulation model, and control logic for the REV-5.5 Acoustic Air Mover, a solid-state, multi-stage air circulation system combining EHD, acoustic, and mechanical vortex principles.

## 2. System Architecture
* **Stage 1 (EHD):** Ionic wind pre-ionizer.
* **Stage 2 (Acoustic/Mechanical):** Vortex initiation with ultrasonic augmentation.
* **Stage 2.5 (Core Jet):** High-velocity axial jet for vortex stabilization.
* **Stage 3 (Air Amplifier):** Annular ejector with Venturi mixing.
* **Stage 4 (Booster):** Final pressure stage.

## 3. Simulation & Controls
* **Reynolds-Aware Duct Losses:** Dynamic friction factor calculation.
* **Ozone Abatement:** Exponential decay model with catalytic gating.
* **Filter Aging:** Auto-compensation loop scaling power to maintain CFM.

## 4. Simulation Code
The full physics model is available in [simulation.py](./simulation.py).
