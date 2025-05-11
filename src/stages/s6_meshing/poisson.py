from src.core.registry import register
import open3d as o3d


@register("poisson")
def mesh_from_pointcloud(pcd, depth=8, **kwargs):
    if not pcd.has_normals():
        pcd.estimate_normals()
        pcd.normalize_normals()

    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=depth)
    return mesh