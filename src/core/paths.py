from pathlib import Path

# === Корневые директории ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # VKR/
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"
CONFIGS_DIR = PROJECT_ROOT / "configs"
SUMMARY_PATH = DATA_DIR / "summary.csv"


# === Пути к изображениям и GT ===
def get_left_image_path(scene):
    return RAW_DIR / scene / "left.png"


def get_right_image_path(scene):
    return RAW_DIR / scene / "right.png"


def get_gt_disparity_path(scene):
    return RAW_DIR / scene / "disp0_gt.npy"


# === Пути к результатам ===
def get_scene_result_dir(scene, p="ncc_median"):
    return RESULTS_DIR / f"{scene}" / f"{p}"


def get_pcd_output_path(scene, tag="ncc_median"):
    return get_scene_result_dir(scene, tag) / "pointcloud.ply"


def get_depth_output_path(scene, tag="ncc_median"):
    return get_scene_result_dir(scene, tag) / "depth.png"


def get_disp_output_path(scene, tag="ncc_median"):
    return get_scene_result_dir(scene, tag) / "disp.png"


def get_metrics_path(scene, tag="ncc_median"):
    return get_scene_result_dir(scene, tag) / "metrics.json"
