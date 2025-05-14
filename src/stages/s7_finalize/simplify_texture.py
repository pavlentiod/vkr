from src.core.registry import register
import open3d as o3d
import numpy as np

@register("clean")
def finalize_mesh(mesh, target_triangles=50000, **kwargs):
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.remove_duplicated_vertices()
    mesh.remove_non_manifold_edges()
    mesh.remove_unreferenced_vertices()

    # Кластеризация треугольников
    triangle_clusters, _, _ = mesh.cluster_connected_triangles()
    triangle_clusters = np.asarray(triangle_clusters)

    if len(triangle_clusters) == 0:
        print("[WARNING] No triangle clusters found – returning original mesh.")
        return mesh

    # Удаление всех кластеров кроме самого большого
    cluster_sizes = np.bincount(triangle_clusters)
    if len(cluster_sizes) == 0:
        print("[WARNING] No valid triangle cluster sizes.")
        return mesh

    largest_cluster = cluster_sizes.argmax()
    mask = triangle_clusters != largest_cluster
    mesh.remove_triangles_by_mask(mask)
    mesh.remove_unreferenced_vertices()

    # Упрощение, если слишком много треугольников
    if len(mesh.triangles) > target_triangles:
        mesh = mesh.simplify_quadric_decimation(target_triangles)
        mesh.remove_unreferenced_vertices()

    mesh.compute_vertex_normals()
    return mesh
