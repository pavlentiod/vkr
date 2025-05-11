# === src/core/io.py ===
import numpy as np
import cv2
from pathlib import Path
import open3d as o3d
import json

def save_disparity(disp: np.ndarray, path: Path):
    """
    Сохраняет карту диспаратности в PNG-формате для визуализации.
    Значения масштабируются в диапазон [0, 255].
    """
    disp_norm = disp.copy()
    disp_norm[~np.isfinite(disp_norm)] = 0
    min_val = disp_norm[disp_norm > 0].min() if np.any(disp_norm > 0) else 0
    max_val = disp_norm.max() if np.any(disp_norm > 0) else 1.0

    scaled = ((disp_norm - min_val) / (max_val - min_val + 1e-5)) * 255.0
    scaled = np.clip(scaled, 0, 255).astype(np.uint8)

    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), scaled)

def save_depth(depth, path: Path):
    """
    Сохраняет карту глубины в PNG-формате для визуализации.
    Глубина нормализуется в диапазон [0, 255].
    """
    if isinstance(depth, o3d.geometry.PointCloud):
        print("[WARN] save_depth: получен PointCloud вместо карты глубины — пропуск сохранения")
        return
    depth_norm = np.copy(depth)
    depth_norm[~np.isfinite(depth_norm)] = 0

    if np.max(depth_norm) > 0:
        scaled = (depth_norm / np.max(depth_norm)) * 255.0
    else:
        scaled = depth_norm

    scaled = np.clip(scaled, 0, 255).astype(np.uint8)

    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), scaled)

def save_pointcloud(pcd: o3d.geometry.PointCloud, path: Path):
    """
    Сохраняет облако точек в PLY-формате.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    o3d.io.write_point_cloud(str(path), pcd)

def save_metrics(metrics: dict, path: Path):
    """
    Сохраняет метрики и времена выполнения в JSON-файл.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)


def save_mesh(mesh: o3d.geometry.TriangleMesh, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    o3d.io.write_triangle_mesh(path, mesh)

