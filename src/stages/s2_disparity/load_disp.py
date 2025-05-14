# src/stages/s3_depth/load_disp.py
from src.core.paths import RAW_DIR
from src.core.registry import register
import numpy as np

@register("load_disp")
def load_disp(scene: str, **kw):
    """Просто читает .npy и отдаёт как depth_map."""
    p = RAW_DIR/scene/"sgm_disp.npy"
    return np.load(p)
