import open3d as o3d
from pathlib import Path
import argparse


def view_mesh(scene: str, config: str):
    mesh_path = Path(f"data/results/{scene}/{config}/mesh.ply")

    if not mesh_path.exists():
        print(f"❌ Mesh-файл не найден: {mesh_path}")
        return

    mesh = o3d.io.read_triangle_mesh(str(mesh_path))
    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()

    if mesh.has_vertex_colors():
        print(f"✓ Цвета присутствуют: {len(mesh.vertex_colors)} точек окрашено")
    else:
        print("❌ Цвета отсутствуют в mesh")

    print(f"✓ Загрузка: {mesh_path}")
    o3d.visualization.draw_geometries([mesh], window_name=f"{scene} / {config}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scene", required=True, help="Имя сцены (cones, teddy и т.п.)")
    parser.add_argument("-c", "--config", required=True, help="Имя конфига (sgm_poisson, sgm_marching и т.п.)")
    args = parser.parse_args()

    view_mesh(args.scene, args.config)
