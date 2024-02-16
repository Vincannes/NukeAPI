import argparse
from pprint import pprint
from io_file import SceneParser


def run(path, export_path=None):
    with open(path, "r") as path_file:
        file_content = path_file.read()

    scene = SceneParser(file_content)
    # pprint(scene.get_dict())

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
        default=None
    )

    args = parser.parse_args()
    path = args.path
    export_path = args.export_path
    run(path, export_path)
