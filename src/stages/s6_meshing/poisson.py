from src.core.registry import register
import open3d as o3d

@register("poisson")
def mesh_from_pointcloud(pcd, depth=7, scale=1.1, linear_fit=False, clean=True, **kwargs):
    """
    Построение треугольной сетки методом Poisson Surface Reconstruction с передачей цвета.
    """
    # Очистка выбросов (опционально)
    if clean:
        pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

    # Проверка и ориентация нормалей
    if not pcd.has_normals():
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30))
        pcd.orient_normals_towards_camera_location()
    pcd.orient_normals_consistent_tangent_plane(k=30)

    # Построение Poisson-меша
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=depth, scale=scale, linear_fit=linear_fit
    )

    # Обработка цвета (по ближайшим точкам)
    if pcd.has_colors():
        pcd_tree = o3d.geometry.KDTreeFlann(pcd)
        mesh_colors = []
        for v in mesh.vertices:
            _, idx, _ = pcd_tree.search_knn_vector_3d(v, 1)
            mesh_colors.append(pcd.colors[idx[0]])
        mesh.vertex_colors = o3d.utility.Vector3dVector(mesh_colors)

    return mesh
