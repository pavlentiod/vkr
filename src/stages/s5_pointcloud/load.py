from src.core.registry import register
import open3d as o3d

@register("load")
def load_pointcloud(path: str, **kw):
    """
    Загружает готовый pointcloud.ply и возвращает open3d.geometry.PointCloud.
    Используется, когда первые этапы (SGM/WLS) уже сделаны.
    """
    pcd = o3d.io.read_point_cloud(path)
    if pcd.is_empty():
        raise FileNotFoundError(f"PointCloud is empty or missing: {path}")
    return pcd
