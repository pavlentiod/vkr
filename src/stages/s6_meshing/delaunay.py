from src.core.registry import register
import open3d as o3d
import numpy as np
from scipy.spatial import Delaunay

@register("delaunay")
def mesh_delaunay(pcd: o3d.geometry.PointCloud, **kwargs):
    """
    Построение треугольной сетки по 2.5D проекции с использованием Delaunay.
    Работает с уже готовым облаком точек (pcd).

    Parameters:
        pcd : open3d.geometry.PointCloud — входное облако точек с координатами XYZ
        kwargs : не используется

    Returns:
        mesh : open3d.geometry.TriangleMesh — полученная треугольная сетка
    """
    if len(pcd.points) < 3:
        raise ValueError("Недостаточно точек для построения меша.")

    points = np.asarray(pcd.points)
    x, y, z = points[:, 0], points[:, 1], points[:, 2]

    # Используем только x, y для Delaunay (2.5D)
    tri = Delaunay(np.vstack((x, y)).T)

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(points)
    mesh.triangles = o3d.utility.Vector3iVector(tri.simplices)

    # Цвета, если есть
    if pcd.has_colors():
        mesh.vertex_colors = pcd.colors

    mesh.compute_vertex_normals()
    return mesh
