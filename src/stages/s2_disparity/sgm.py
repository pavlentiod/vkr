import cv2
import numpy as np

from src.core.registry import register


@register("sgm")
def compute_disparity_sgm(left, right, num_disparities=128, block_size=5, **kwargs):
    stereo = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=num_disparities,
        blockSize=block_size,
        P1=8 * 3 * block_size ** 2,
        P2=32 * 3 * block_size ** 2,
        mode=cv2.STEREO_SGBM_MODE_SGBM
    )
    disp = stereo.compute(left, right).astype(np.float32) / 16.0
    return disp