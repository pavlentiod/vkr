import argparse

from scripts.report import make_report
from scripts.run_experiment import run_pipeline
from src.core.paths import CONFIGS_DIR


def run_all(scenes: list[str]):
    config_dir = CONFIGS_DIR
    config_paths = sorted(config_dir.glob("*.yaml"))

    for config_path in config_paths:
        for scene in scenes:
            print(f"\n▶ Запуск: scene={scene}, config={config_path}")
            try:
                run_pipeline(str(config_path).split("\\")[-1].replace(".yaml",""), scene)
            except Exception as e:
                print(f"❌ Ошибка при запуске {scene} + {config_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scenes", nargs="+", required=True, help="Список сцен для запуска")
    args = parser.parse_args()

    run_all(args.scenes)
    make_report()
