# ML Academy — media

[Español](README.md) · **English**

This project generates the figures and short videos that illustrate [ML Academy](../ml-academy-web) topics:
- Static charts with matplotlib.
- 6–12 second animations with [Manim Community](https://www.manim.community/), silent and loopable.

Every asset is generated in Spanish and English.

**Charts** are stored in the repository, in `charts/images/`, and synced to the site for deployment. **Videos** are generated locally in `output/` and synced to `public/media/` for preview; MP4 files are not stored in Git. Site publication will use unlisted videos when that phase is available.

## Requirements

- Python 3.10 or later.
- **For videos, a LaTeX distribution** (MiKTeX on Windows, TeX Live on macOS or Linux): formulas are written with `MathTex`. If MiKTeX asks to install packages, turn on automatic installation: `initexmf --set-config-value=[MPM]AutoInstall=1`.
- Charts don't need LaTeX: their formulas use matplotlib mathtext with the Computer Modern font.
- No system ffmpeg needed: Manim bundles PyAV.

```bash
# Once, in the root ml-academy/ folder (it contains the repositories).
# This is the same global environment the labs use.
python -m venv .venv
# Windows: .venv\Scripts\activate    ·    macOS/Linux: source .venv/bin/activate
pip install -r ml-academy-media/requirements.txt
```

## Render and sync

```bash
python scripts/render_all.py                  # charts + videos, ES and EN, then copy to the web
python scripts/render_all.py --only charts    # charts only (seconds)
python scripts/render_all.py --only videos    # videos only (~1 minute)
python scripts/render_all.py --no-sync        # don't copy to the web
python scripts/render_all.py --topic training-customization   # a single topic (repeatable)
```

1. Charts are generated in `charts/images/<course>/<topic>/` (in the repository). Videos are generated in `output/<course>/<topic>/`, which is gitignored.
2. PNGs are copied to `../ml-academy-web/public/media/<course>/<topic>/` and versioned in the web repository. MP4s are copied to the same local folder but remain gitignored.
3. The web's `Figure` component renders assets when present; the deployed site includes figures and omits local videos.

## Structure

```text
charts/style.py                           # palette, matplotlib style and shared helpers
charts/topics/<topic>.py                  # one topic's charts: TEXT[lang] and CHARTS
charts/make_charts.py                     # topic 1.3 charts (exposed by charts/topics/data-quality-bias.py)
charts/images/<course>/<topic>/           # generated PNGs (ES and EN)
videos/style.py                           # shared Manim palette and helpers
videos/<course>/<topic>/scenes.py         # Manim scenes; VIDEOS = {name: Class}; text based on MLA_LANG
scripts/render_video.py                   # renders one scene through Manim's API
scripts/render_all.py                     # runs everything and syncs to the web
```

`render_video.py` uses Manim's Python API instead of the CLI. The CLI turns the file path into a regular expression and fails when the path contains parentheses, such as `C:\Users\Name(Org)\...`.

`render_all.py` discovers topics: `charts/topics/*.py` and `videos/<course>/<topic>/scenes.py`. Topics without their own module still use the legacy generic generators (`charts/module_visuals.py` and `videos/aws-ml-engineer-associate/module-concepts/scenes.py`); remove them once no topic uses them.

## Naming convention

The web depends on this format:

```text
public/media/<course>/<topic>/<name>.<es|en>.<png|mp4>
```

| Topic | Charts (PNG, 1600 px, white background) | Videos (MP4 H.264, 1280×720, 30 fps) |
|---|---|---|
| `aws-ml-engineer-associate/data-quality-bias` | `class-imbalance`, `bias-ci-dpl`, `outliers-iqr`, `imbalance-metrics` | `dq-pipeline`, `stratified-split`, `smote` |
| `aws-ml-engineer-associate/data-collection-storage` | `columnar-scan`, `kinesis-hot-shard`, `s3-lifecycle` | `stream-to-s3`, `feature-store-event-time` |
| `aws-ml-engineer-associate/data-transformation-features` | `log-then-scale`, `scalers-outliers`, `chunking-strategies` | `fit-on-train` |
| `aws-ml-engineer-associate/modeling-approaches` | `choose-layer`, `distillation-tradeoff` | `rag-hybrid-filter` |
| `aws-ml-engineer-associate/training-customization` | `early-stopping`, `hpo-strategies`, `spot-checkpoints` | `hyperband` |

## Add media for a new topic

1. **Charts:** create `charts/topics/<topic>.py` with a per-language `TEXT` and `chart_<name>(t, out)` functions that save `<name>.png`, listed in `CHARTS` (use `charts/style.py`).
2. **Videos:** create `videos/<course>/<topic>/scenes.py` with `VIDEOS = {"name": "Class"}` and a per-language `TEXT` dict (use `videos/style.py`).
3. Run `python scripts/render_all.py --topic <topic>`.
4. In the topic's MDX, insert `<Figure name="<name>" … />`.

Chart data must match the topic's theory and lab. For example, `imbalance-metrics` uses the results from `ml-academy-labs`.

## Palette

Matches the site:

| Use | Color |
|---|---|
| Text (ink) | `#111114` |
| Accent | `#b3132b` |
| Correct (ok) | `#1f7a4d` |
| Gray | `#c9c9cf` |
| Surface | `#f3f3f5` |
