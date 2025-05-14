from src.core.registry import register
import open3d as o3d
import numpy as np

@register("alpha_shape")
def mesh_alpha_shape(pcd,
                     alpha: float = 0.03,
                     clean: bool = True,
                     **kwargs):
    """
    Mesh через open3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape.

    Parameters
    ----------
    pcd : open3d.geometry.PointCloud
        Входное облако точек (XYZ[RGB]).
    alpha : float
        Радиус сферы α-shape. Меньше → «жёстче» поверхность, больше → сглаженнее.
    clean : bool
        Выполнять ли базовую очистку меша (дубликаты / невостребованные вершины).

    Returns
    -------
    open3d.geometry.TriangleMesh
    """
    # подготовка нормалей (α-shape их не требует, но пригодятся позже)
    if not pcd.has_normals():
        pcd.estimate_normals()


    # построение
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)

    # перенос цвета (если был в point cloud)
    if pcd.has_colors() and len(pcd.points) == len(mesh.vertices):
        mesh.vertex_colors = pcd.colors


    # базовая чистка
    # if clean:
    #     mesh.remove_duplicated_vertices()
    #     mesh.remove_degenerate_triangles()
    #     mesh.remove_duplicated_triangles()
    #     mesh.remove_unreferenced_vertices()

    mesh.compute_vertex_normals()
    return mesh
