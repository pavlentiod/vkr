import numpy as np
import open3d as o3d

from src.core.registry import register

@register("from_depth")
def create_point_cloud(depth, rgb, fx=374.0, fy=374.0, cx=None, cy=None, **kwargs):
    h, w = depth.shape
    cx = cx or w / 2
    cy = cy or h / 2

    xx, yy = np.meshgrid(np.arange(w), np.arange(h))
    x = (xx - cx) * depth / fx
    y = (yy - cy) * depth / fy
    z = depth

    xyz = np.stack((x, y, z), axis=2).reshape(-1, 3)
    rgb = rgb.reshape(-1, 3) / 255.0

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.colors = o3d.utility.Vector3dVector(rgb)
    return pcd
