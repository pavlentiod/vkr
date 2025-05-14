from src.core.registry import register
import open3d as o3d
import numpy as np

@register("marching")
def mesh_marching(depth_map,
                  rgb=None,
                  fx=374.0, fy=374.0, cx=0.0, cy=0.0,
                  voxel_size=0.005, sdf_trunc=0.04, **kwargs):
    """
    Построение цветного mesh через TSDF (имитация Marching Cubes)

    Parameters:
        depth_map : np.ndarray — карта глубины
        rgb : np.ndarray — изображение (BGR/RGB)
        fx, fy, cx, cy : float — параметры камеры
        voxel_size : float — размер вокселя
        sdf_trunc : float — глубина усечения SDF

    Returns:
        open3d.geometry.TriangleMesh
    """
    h, w = depth_map.shape
    camera_intrinsics = o3d.camera.PinholeCameraIntrinsic(w, h, fx, fy, cx, cy)

    # Подготовка depth
    depth_o3d = o3d.geometry.Image((depth_map * 1000.0).astype(np.uint16))  # в мм

    # Подготовка цвета
    if rgb is not None:
        rgb = o3d.geometry.Image((rgb[..., ::-1]).astype(np.uint8))  # RGB → BGR
        color_type = o3d.pipelines.integration.TSDFVolumeColorType.RGB8
    else:
        rgb = o3d.geometry.Image(np.zeros((h, w, 3), dtype=np.uint8))
        color_type = o3d.pipelines.integration.TSDFVolumeColorType.NoColor

    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color=rgb,
        depth=depth_o3d,
        convert_rgb_to_intensity=False,
        depth_scale=1000.0
    )

    # TSDF volume
    volume = o3d.pipelines.integration.ScalableTSDFVolume(
        voxel_length=voxel_size,
        sdf_trunc=sdf_trunc,
        color_type=color_type
    )

    pose = np.identity(4)
    volume.integrate(rgbd, camera_intrinsics, pose)

    mesh = volume.extract_triangle_mesh()
    mesh.compute_vertex_normals()
    return mesh
