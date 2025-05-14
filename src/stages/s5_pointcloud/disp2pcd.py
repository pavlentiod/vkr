import numpy as np
import open3d as o3d

from src.core.registry import register

@register("from_depth")
def create_point_cloud(depth_map, rgb=None, fx=374.0, fy=374.0, cx=0.0, cy=0.0):
    h, w = depth_map.shape
    yy, xx = np.indices((h, w))
    z = depth_map
    valid = (z > 0) & np.isfinite(z)

    x = (xx[valid] - cx) * z[valid] / fx
    y = (yy[valid] - cy) * z[valid] / fy
    z = z[valid]
    points = np.stack((x, y, z), axis=1)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    if rgb is not None:
        rgb = rgb.astype(np.float32) / 255.0
        colors = rgb[yy[valid], xx[valid]]
        pcd.colors = o3d.utility.Vector3dVector(colors)
    pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=3.0)
    return pcd
