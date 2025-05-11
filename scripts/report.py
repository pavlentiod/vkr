import json
import pandas as pd

from src.core.paths import RESULTS_DIR, SUMMARY_PATH


def collect_metrics():
    rows = []

    for scene_dir in RESULTS_DIR.iterdir():
        if not scene_dir.is_dir():
            continue

        for config_dir in scene_dir.iterdir():
            metrics_path = config_dir / "metrics.json"
            if not metrics_path.exists():
                continue

            with open(metrics_path) as f:
                metrics_data = json.load(f)

            row = {
                "scene": scene_dir.name,
                "config": config_dir.name,
            }

            # Распаковываем вложенные метрики
            row.update(metrics_data.get("metrics", {}))
            row.update({f"time::{k}": v for k, v in metrics_data.get("times", {}).items()})

            rows.append(row)

    return pd.DataFrame(rows)


def make_report():
    df = collect_metrics()
    if not df.empty:
        SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(SUMMARY_PATH, index=False)
        print(f"✓ Сводная таблица сохранена: {SUMMARY_PATH}")
    else:
        print("⚠️ Нет данных для сводной таблицы.")

