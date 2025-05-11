import cv2
import numpy as np
from src.core.registry import register

@register("ncc")
def compute_disparity(left, right, num_disparities=64, block_size=9, **kwargs):
    stereo = cv2.StereoBM_create(numDisparities=num_disparities, blockSize=block_size)
    disp = stereo.compute(left, right).astype(np.float32) / 16.0
    return disp
