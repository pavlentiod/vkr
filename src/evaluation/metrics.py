import numpy as np
from sklearn.metrics import mean_squared_error

def evaluate_pipeline(pred_disp, gt_disp):
    mask = (gt_disp > 0) & np.isfinite(gt_disp)
    pred = pred_disp[mask]
    gt = gt_disp[mask]

    if len(pred) == 0:
        return {"rmse": None, "valid_pixels": 0}

    rmse = np.sqrt(mean_squared_error(gt, pred))
    abs_rel = np.mean(np.abs(gt - pred) / gt)
    return {
        "rmse": float(rmse),
        "abs_rel": float(abs_rel),
        "valid_pixels": int(len(gt))
    }