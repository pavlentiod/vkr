import numpy as np

def evaluate_pipeline(pred_disp: np.ndarray, gt_disp: np.ndarray) -> dict:
    """
    Рассчитать метрики качества disparity-карты.

    Parameters
    ----------
    pred_disp : np.ndarray
        Предсказанная карта диспаратности (float32 / float64).
    gt_disp : np.ndarray
        Эталонная (ground-truth) карта диспаратности.

    Returns
    -------
    dict
        rmse        – среднеквадратичная ошибка
        abs_rel     – средняя абсолютная относительная ошибка
        valid_pixels – число пикселей, учтённых в расчёте
    """
    # маска валидных GT-значений: >0 и не NaN/Inf
    mask = (gt_disp > 0) & np.isfinite(gt_disp)
    if not np.any(mask):
        return {"rmse": None, "abs_rel": None, "valid_pixels": 0}

    pred = pred_disp[mask]
    gt   = gt_disp[mask]

    # RMSE = sqrt(mean((pred - gt)^2))
    diff = pred - gt
    rmse = float(np.sqrt(np.mean(diff ** 2)))

    # Abs Rel = mean(|pred - gt| / gt)
    abs_rel = float(np.mean(np.abs(diff) / gt))

    return {
        "rmse": rmse,
        "abs_rel": abs_rel,
        "valid_pixels": int(gt.size)
    }
