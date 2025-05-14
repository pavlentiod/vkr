from src.core.registry import register
import cv2
import numpy as np


@register("wls")
def apply_wls_filter(disparity, left, lambda_val=12000.0, sigma_color=3.5, **kwargs):
    """
    Применение WLS-фильтра к карте диспаратности с использованием направляющего изображения.

    Parameters:
        disparity : np.ndarray — входная карта диспаратности (float32)
        left : np.ndarray — направляющее изображение (grayscale или RGB)
        lambda_val : float — параметр сглаживания (обычно 8000–10000)
        sigma_color : float — чувствительность к краю (обычно 1.0–2.0)

    Returns:
        np.ndarray — отфильтрованная карта диспаратности (float32)
    """
    # Приведение к 16-битному виду для работы с OpenCV WLS
    disp_scaled = (disparity * 16).astype(np.int16)
    left_gray = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY) if len(left.shape) == 3 else left

    # Создание фильтра и применение
    wls_filter = cv2.ximgproc.createDisparityWLSFilterGeneric(False)
    wls_filter.setLambda(lambda_val)
    wls_filter.setSigmaColor(sigma_color)

    filtered = wls_filter.filter(disp_scaled, left_gray)
    return filtered.astype(np.float32) / 16.0
