# src/stages/s2_disparity/sgm_custom.py
from src.core.registry import register
import numpy as np
import cv2
from .sgm_full import Parameters, Paths, compute_costs, aggregate_costs, select_disparity   # ← импорт функций из вашего «длинного» файла
from ...core.paths import RAW_DIR


@register("sgm")          # перезаписываем прежнюю «sgm»
def compute_disparity_sgm_custom(
        left: np.ndarray,
        right: np.ndarray,
        num_disparities: int = 64,
        P1: int = 10,
        P2: int = 120,
        census_kernel: tuple = (7, 7),
        blur_kernel: tuple = (3, 3),
        **kw):
    """
    Semi-Global Matching (полная Python-реализация Hirschmüller).
    Возврат: float32 disparity (px).
    """
    # 0. Подготовка параметров
    params = Parameters(max_disparity=num_disparities,
                        P1=P1, P2=P2,
                        csize=census_kernel,
                        bsize=blur_kernel)
    paths = Paths()       # 8 направлений

    # 1. Matching-cost (census + Hamming)
    left_cost, right_cost = compute_costs(left, right, params, save_images=False)

    # 2. Aggregation на 8 путях
    left_aggr = aggregate_costs(left_cost, params, paths)

    # 3. WTA
    disp_left = select_disparity(left_aggr).astype(np.float32)

    # 4. Пост-median как в оригинале
    disp_left = cv2.medianBlur(disp_left, blur_kernel[0])

    # 5. Приведём к «float px» (SGM-OpenCV делит на 16)
    # np.save(RAW_DIR/"teddy"/"sgm_disp.npy", disp_left)
    return disp_left
