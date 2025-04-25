#!/bin/bash

GT="Data/TUM/rgbd_dataset_freiburg3_long_office_household/groundtruth.txt"
EST_DIR="results/results_tum/office"
OUT_DIR="evo_eval/office"
mkdir -p "$OUT_DIR"

for f in $EST_DIR/result_*.txt
do
  fname=$(basename "$f" .txt)

  # APE
  evo_ape tum $GT $f -as \
    --save_results "$OUT_DIR/${fname}_APE.zip" \
    --save_plot "$OUT_DIR/${fname}_APE.pdf" \
    --plot --plot_mode xz

  # RPE（完整 SE3）
  evo_rpe tum $GT $f -as \
    --save_results "$OUT_DIR/${fname}_RPE.zip" \
    --save_plot "$OUT_DIR/${fname}_RPE.pdf" \
    --plot --plot_mode xyz

  # RPE（姿态角度误差）
  evo_rpe tum $GT $f -r angle_deg -as \
    --save_results "$OUT_DIR/${fname}_RPE_ANGLE.zip" \
    --save_plot "$OUT_DIR/${fname}_RPE_ANGLE.pdf" \
    --plot

  echo "Finished: $fname"
done
