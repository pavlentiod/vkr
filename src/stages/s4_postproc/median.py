from scipy.ndimage import median_filter
from src.core.registry import register

@register("median")
def apply_median_filter(depth_map, size=5, **kwargs):
    return median_filter(depth_map, size=size)
