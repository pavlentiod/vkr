import cv2
import numpy as np

from src.core.registry import register


@register("bilateral")
def apply_bilateral_filter(depth_map, d=9, sigmaColor=75, sigmaSpace=75, **kwargs):
    depth_norm = depth_map.copy()
    depth_norm[~np.isfinite(depth_norm)] = 0
    depth_norm = cv2.normalize(depth_norm, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    filtered = cv2.bilateralFilter(depth_norm, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
    return filtered.astype(np.float32)
