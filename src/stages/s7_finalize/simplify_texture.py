from src.core.registry import register


@register("clean")
def finalize_mesh(mesh, remove_isolated=True, simplify=True, target_triangles=100_000, **kwargs):
    if remove_isolated:
        mesh.remove_unreferenced_vertices()
        mesh.remove_degenerate_triangles()
        mesh.remove_duplicated_triangles()
        mesh.remove_duplicated_vertices()

    if simplify:
        mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=target_triangles)

    return mesh
