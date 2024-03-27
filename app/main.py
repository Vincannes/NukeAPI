import argparse
from pprint import pprint
from io_file import SceneDict


def run(path, export_path=None):

    scene = SceneDict(path) 
    # pprint([data for i in SceneDict(path) .get_nodes() for name, data in i.items() if isinstance(data, dict) and data.get("Class") == "Group"])
    # print(len(scene.get_nodes()))
    # pprint(scene.errors)
    # pprint(scene.get_inputs())
    pprint([data for i in scene.get_inputs().get("current_scene") for name, data in i.items() if name == "ASSET_CONFOCADRE1"])


    if export_path:
        print(export_path)
        scene.export_to_file(export_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Nuke API")
    parser.add_argument(
        "path",
        type=str,
        help="Path to the path.",
    )

    parser.add_argument(
        "export_path",
        type=str,
        help="Path to the export file as json.",
        default=None,
        # required=False
    )

    args = parser.parse_args()
    path = args.path
    export_path = args.export_path
    run(path, export_path)
