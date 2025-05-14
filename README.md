# Реконструкция 3D с применением различных алгоритмов и способов фильтрации

## Запуск
```bash
python -m scripts.run_all_experiments -s cones -v
```

Имеет возможность сравнить качество построенной модели(на данном этапе есть только сравнение построенных карт глубины) для разных алгоритмов и способов фильтрации. Наборы этих компонентов описываются в configs.
**Репозиторий автоматизирует сравнение алгоритмов построения 3‑D модели по стереоснимкам.  Pipeline описывается YAML‑файлом, сцена выбирается в CLI аргументах; результаты сохраняются в `data/results/<scene>/<config>/`

## 1. Дерево проекта

```
├── data/               # 
│   ├── raw/            # стереопары + GT disparity
│   └── results/        # artefacts (png, ply, csv)
├── configs/            # YAML‑конфиги
├── scripts/            # Запускаемые скрипты
├── src/                # 
│   ├── core/           # registry, io, paths, timer
│   ├── stages/         # реализованные стадии 1‑7
│   └── evaluation/     # метрики + отчёты
```

### Основные модули `src/stages`

| ID в YAML               | Файл                              | Описание                              |
| ----------------------- | --------------------------------- |---------------------------------------|
| `disparity/ncc`         | `s2_disparity/ncc.py`             | NCC алгоритм построения карты глубины |
| `disparity/sgm`         | `s2_disparity/sgm.py`             | SGM алгоритм построения карты глубины |
| `depth/from_disparity`  | `s3_depth/depth_from_disp.py`     | Реконструкция глубин                  |
| `postproc/median`       | `s4_postproc/median.py`           | 3‑D медианный фильтр                  |
| `postproc/bilateral`    | `s4_postproc/bilateral.py`        | Bilateral фильтр                      |
| `pointcloud/from_depth` | `s5_pointcloud/disp2pcd.py`       | XYZRGB → PLY                          |
| `mesh/poisson`          | `s6_meshing/poisson.py`           | Реконструкция по Пуассону             |
| `finalize/clean`        | `s7_finalize/simplify_texture.py` | Очистка контуров                      |

## 2. Принцип работы

1`run_experiment.py` загружает YAML → строит цепочку функций → сохраняет метрики .
2. Результаты каждого шага сохраняет модуль `core/io.py`; таблица метрик (`metrics.json`) формируется после сравнения с GT.


## 4. Как смотреть результаты

* PNG файлы disparity/depth — `data/results/<scene>/<config>/`.
* Облако точек `pointcloud.ply` и `mesh.ply` открываем в **MeshLab** или **CloudCompare**.
* Времена и RMSE — в `metrics.json`; сводка — `data/summary.csv`.
