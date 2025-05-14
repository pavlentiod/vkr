from src.core.registry import register
import open3d as o3d
import numpy as np


@register("bp")
def mesh_ball_pivoting(pcd,
                       radius: float | None = None,
                       factor: float = 1.5,
                       clean: bool = True,
                       **kwargs):
    """
    Mesh через open3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting.

    Parameters
    ----------
    pcd : open3d.geometry.PointCloud
        Входное облако точек (XYZ[RGB]).
    radius : float | None
        Радиус шара.  Если None — берётся средняя дистанция *d* между точками
        и используется список радиусов  [d, d*factor, d*factor²].
    factor : float
        Мультипликатор для каскадных радиусов, если radius не задан.
    clean : bool
        Чистить ли меш (дубликаты, невостребованные вершины).

    Returns
    -------
    open3d.geometry.TriangleMesh
    """
    # Нормали нужны для BPA
    if not pcd.has_normals():
        pcd.estimate_normals()
        pcd.orient_normals_towards_camera_location()

    # --- выбор радиусов ---
    if radius is None:
        # средняя дистанция между соседними точками
        distances = pcd.compute_nearest_neighbor_distance()
        d = np.mean(distances)
        radii = o3d.utility.DoubleVector([d, d * factor, d * (factor**2)])
    else:
        radii = o3d.utility.DoubleVector([radius, radius * factor, radius * (factor**2)])

    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, radii)

    # перенос цвета
    if pcd.has_colors() and len(pcd.points) == len(mesh.vertices):
        mesh.vertex_colors = pcd.colors

    if clean:
        mesh.remove_duplicated_vertices()
        mesh.remove_degenerate_triangles()
        mesh.remove_duplicated_triangles()
        mesh.remove_unreferenced_vertices()

    mesh.compute_vertex_normals()
    return mesh
