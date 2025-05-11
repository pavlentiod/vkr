import time
from inspect import signature

import cv2
import numpy as np
import yaml

from src.core.io import save_disparity, save_depth, save_pointcloud, save_metrics, save_mesh
from src.core.paths import (
    get_left_image_path, get_right_image_path, get_gt_disparity_path,
    get_disp_output_path, get_depth_output_path, get_pcd_output_path,
    get_metrics_path, get_scene_result_dir, CONFIGS_DIR
)
from src.core.registry import get as get_stage_fn
from src.evaluation.metrics import evaluate_pipeline

# Регистрация стадий
from src.stages.s2_disparity import ncc, sgm
from src.stages.s3_depth import depth_from_disp
from src.stages.s4_postproc import median, bilateral
from src.stages.s5_pointcloud import disp2pcd
from src.stages.s6_meshing.poisson import mesh_from_pointcloud
from src.stages.s7_finalize.simplify_texture import finalize_mesh

# === Отображение выходов по стадии ===
SAVE_HANDLERS = {
    "disparity": lambda result, scene, tag: save_disparity(result, get_disp_output_path(scene, tag)),
    "depth": lambda result, scene, tag: save_depth(result, get_depth_output_path(scene, tag)),
    "pointcloud": lambda result, scene, tag: save_pointcloud(result, get_pcd_output_path(scene, tag)),
    "mesh": lambda result, scene, tag: save_mesh(result, get_scene_result_dir(scene, tag) / "mesh.ply"),
    "finalize": lambda result, scene, tag: save_mesh(result, get_scene_result_dir(scene, tag) / "mesh_final.ply"),
}

STAGE_OUTPUT_KEYS = {
    "disparity": ["disparity"],
    "depth": ["depth", "depth_map"],
    "pointcloud": ["pcd"],
    "mesh": ["mesh"],
    "finalize": ["final_mesh"],
}

def run_pipeline(config: str, scene: str):
    config_path = CONFIGS_DIR / (config + ".yaml")
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    pipeline_cfg = cfg["pipeline"]
    tag = str(config_path).split("/")[-1].split(".")[0]
    result_dir = get_scene_result_dir(scene, config)
    print("RESULTS", scene, config)
    result_dir.mkdir(parents=True, exist_ok=True)

    left = cv2.imread(str(get_left_image_path(scene)), cv2.IMREAD_GRAYSCALE)
    right = cv2.imread(str(get_right_image_path(scene)), cv2.IMREAD_GRAYSCALE)
    rgb = cv2.imread(str(get_left_image_path(scene)))

    if left is None or right is None:
        raise FileNotFoundError(f"Не найдены изображения для сцены: {scene}")

    data = {"left": left, "right": right, "rgb": rgb}
    times = {}

    for step in pipeline_cfg:
        stage_id = step["stage"]
        stage, stage_key = stage_id.split("/")
        fn = get_stage_fn(stage_key)
        params = step.get("params", {})

        sig = signature(fn)
        needed_args = sig.parameters.keys()
        call_args = {arg:data[arg] for arg in needed_args if arg in data}

        call_args.update(params)

        t0 = time.time()
        result = fn(**call_args)
        t1 = time.time()
        print(f"[{stage_id}] done in {t1 - t0:.2f} sec")
        times[stage_id] = round(t1 - t0, 4)

        # Обновляем ключи результата
        for key in STAGE_OUTPUT_KEYS.get(stage, []):
            data[key] = result

        # Сохраняем результат
        if stage in SAVE_HANDLERS:
            SAVE_HANDLERS[stage](result, scene, config)

    metrics = {}
    gt_path = get_gt_disparity_path(scene)
    if gt_path.exists() and "disparity" in data:
        disp_gt = np.load(gt_path)
        metrics = evaluate_pipeline(data["disparity"], disp_gt)

    save_metrics({"metrics": metrics, "times": times}, get_metrics_path(scene, config))
    print(f"✓ Завершено: {scene} ({tag})")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, required=True, help="YAML-файл с описанием pipeline")
    parser.add_argument("-s", "--scene", type=str, required=True, help="Имя сцены (папка в data/raw)")
    args = parser.parse_args()
    run_pipeline(args.config, args.scene)
