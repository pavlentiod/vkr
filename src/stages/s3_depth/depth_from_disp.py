import numpy as np

from src.core.paths import RAW_DIR
from src.core.registry import register


@register("from_disparity")
def from_disparity(disparity, focal_length=374.0, baseline=0.1, **kwargs):
    # Avoid division by zero
    depth = np.zeros_like(disparity, dtype=np.float32)
    valid = disparity > 0
    depth[valid] = (focal_length * baseline) / disparity[valid]
    return depth
