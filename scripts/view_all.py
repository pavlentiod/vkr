import open3d as o3d
from pathlib import Path
import argparse


def view_all_meshes_separately(scene: str, max_meshes: int = None):
    """
    Для каждой mesh.ply в data/results/<scene> открывает отдельное окно.
    """
    results_dir = Path(f"data/results/{scene}")
    if not results_dir.exists():
        print(f"❌ Директория не найдена: {results_dir}")
        return

    mesh_paths = sorted(results_dir.glob("*/mesh.ply"))
    if not mesh_paths:
        print(f"❌ В папке {results_dir} нет ни одного mesh.ply")
        return

    for i, mesh_path in enumerate(mesh_paths):
        if max_meshes and i >= max_meshes:
            break

        config = mesh_path.parent.name
        mesh = o3d.io.read_triangle_mesh(str(mesh_path))
        if not mesh.has_vertex_normals():
            mesh.compute_vertex_normals()

        if mesh.has_vertex_colors():
            print(f"✓ [{config}] mesh с цветами ({len(mesh.vertex_colors)} вершин)")
        else:
            print(f"⚠️ [{config}] mesh без цветов")

        print(f"Открытие: {mesh_path}")
        o3d.visualization.draw_geometries(
            [mesh],
            window_name=f"{scene} / {config}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scene", required=True, help="Имя сцены (cones, teddy и т.п.)")
    parser.add_argument("-n", "--max", type=int, default=None, help="Максимум моделей для отображения")
    args = parser.parse_args()

    view_all_meshes_separately(args.scene, max_meshes=args.max)
