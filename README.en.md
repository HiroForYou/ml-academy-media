# ML Academy — media

[Español](README.md) · **English**

This project generates the figures and short videos that illustrate [ML Academy](../ml-academy-web) topics:
- Static charts with matplotlib.
- 6–12 second animations with [Manim Community](https://www.manim.community/), silent and loopable.

Every asset is generated in Spanish and English.

**Charts** are stored in the repository, in `charts/images/`. **Videos** are local only for now: they are not uploaded to any repository or to YouTube.

## Requirements

- Python 3.10 or later.
- **For videos, a LaTeX distribution** (MiKTeX on Windows, TeX Live on macOS or Linux): formulas are written with `MathTex`. If MiKTeX asks to install packages, turn on automatic installation: `initexmf --set-config-value=[MPM]AutoInstall=1`.
- Charts don't need LaTeX: their formulas use matplotlib mathtext with the Computer Modern font.
- No system ffmpeg needed: Manim bundles PyAV.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    ·    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Render and sync

```bash
python scripts/render_all.py                  # charts + videos, ES and EN, then copy to the web
python scripts/render_all.py --only charts    # charts only (seconds)
python scripts/render_all.py --only videos    # videos only (~1 minute)
python scripts/render_all.py --no-sync        # don't copy to the web
```

1. Charts are generated in `charts/images/<course>/<topic>/` (in the repository). Videos are generated in `output/<course>/<topic>/`, which is gitignored.
2. They are then copied to `../ml-academy-web/public/media/<course>/<topic>/`, a folder the web ignores in git.
3. The web's `Figure` component only shows an asset when the file exists, so the site works the same without them.

## Structure

```text
charts/make_charts.py                     # one function per chart; text in TEXT[lang]
charts/images/<course>/<topic>/           # generated PNGs (ES and EN)
videos/<course>/<topic>/scenes.py         # Manim scenes; text in TEXT based on MLA_LANG
scripts/render_video.py                   # renders one scene through Manim's API
scripts/render_all.py                     # runs everything and syncs to the web
```

`render_video.py` uses Manim's Python API instead of the CLI. The CLI turns the file path into a regular expression and fails when the path contains parentheses, such as `C:\Users\Name(Org)\...`.

## Naming convention

The web depends on this format:

```text
public/media/<course>/<topic>/<name>.<es|en>.<png|mp4>
```

| Topic | Charts (PNG, 1600 px, white background) | Videos (MP4 H.264, 1280×720, 30 fps) |
|---|---|---|
| `aws-ml-engineer-associate/data-quality-bias` | `class-imbalance`, `bias-ci-dpl`, `outliers-iqr`, `imbalance-metrics` | `dq-pipeline`, `stratified-split`, `smote` |

## Add media for a new topic

1. **Charts:** add a `chart_<name>(t, out)` function to `charts/make_charts.py` that saves `<name>.png`, and add it to `CHARTS`. For a different topic, adjust `CHART_TOPIC` in `render_all.py`; as it grows, split charts into one file per topic.
2. **Videos:** create `videos/<course>/<topic>/scenes.py` with a per-language `TEXT` dict, and register `name → Class` in `VIDEOS` in `render_all.py`.
3. Run `python scripts/render_all.py`.
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
