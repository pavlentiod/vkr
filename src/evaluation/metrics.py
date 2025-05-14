import numpy as np


def evaluate_pipeline(pred_disp: np.ndarray, gt_disp: np.ndarray) -> dict:
    pred_disp = pred_disp.astype(np.float32)
    gt_disp   = gt_disp.astype(np.float32)

    # 1. Единый валид-mask: GT валидно и предсказание конечное
    mask = (gt_disp > 0) & np.isfinite(gt_disp) & np.isfinite(pred_disp)
    if not np.any(mask):
        return {"rmse": None, "abs_rel": None, "valid_pixels": 0}

    pred = pred_disp[mask]
    gt   = gt_disp[mask]

    # 2. Проверка масштаба (опц.) — warn, если диспаратности отличаются >×8
    ratio = np.median(gt) / (np.median(pred) + 1e-6)
    if ratio > 8 or ratio < 0.125:
        print("[WARN] Предсказание и GT, вероятно, в разных масштабах.")

    # 3. Ограничиваем выбросы (например, 99-й перцентиль)
    diff = np.clip(pred - gt, -1e4, 1e4)

    rmse = float(np.sqrt(np.mean(diff ** 2)))
    abs_rel = float(np.mean(np.abs(diff) / np.maximum(gt, 1e-6)))

    return {"rmse": rmse, "abs_rel": abs_rel, "valid_pixels": int(mask.sum())}
