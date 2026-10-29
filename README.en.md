# ML Academy — media

[Español](README.md) · **English**

This project generates the figures and short videos that illustrate [ML Academy](../ml-academy-web) topics:
- Static charts with matplotlib.
- Animations of about 25–65 seconds (depending on the amount of text) with [Manim Community](https://www.manim.community/), silent. The pacing leaves time to read each text before the next change.

Every asset is generated in Spanish and English.

**Charts** are stored in the repository, in `charts/images/`, and synced to the site for deployment. **Videos** are generated locally in `output/` (MP4 files are not stored in Git) and published to YouTube as unlisted with `scripts/manage_videos_yt.py`; the site embeds them from `ml-academy-web/src/data/youtube-videos.json`.

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
python scripts/render_all.py --only videos    # videos only (~10 minutes)
python scripts/render_all.py --no-sync        # don't copy to the web
python scripts/render_all.py --topic training-customization   # a single topic (repeatable)
```

1. Charts are generated in `charts/images/<course>/<topic>/` (in the repository). Videos are generated in `output/<course>/<topic>/`, which is gitignored.
2. PNGs are copied to `../ml-academy-web/public/media/<course>/<topic>/` and versioned in the web repository. MP4s are no longer copied to the web: they are uploaded to YouTube (see below).
3. The web's `Figure` component shows the PNGs and, with `video`, embeds the YouTube video recorded in the manifest.

## Publishing the videos on YouTube

`scripts/manage_videos_yt.py` uploads every MP4 in `output/` as an **unlisted** video, adds it to a playlist (also unlisted) per course and writes the IDs to `../ml-academy-web/src/data/youtube-videos.json`. It is idempotent: an already uploaded video with the same SHA-256 is never uploaded again.

```bash
pip install -r requirements.txt               # includes the YouTube API libraries
python scripts/manage_videos_yt.py auth               # once: opens the browser and saves token.json
python scripts/manage_videos_yt.py publish --dry-run  # shows what would be uploaded
python scripts/manage_videos_yt.py publish            # uploads what is missing and updates the manifest
python scripts/manage_videos_yt.py verify             # checks privacy and embeddability on YouTube
python scripts/manage_videos_yt.py                    # interactive menu (list, upload, edit, privacy, delete)
```

- Credentials: put the Google Cloud OAuth file (`client_secret*.json`, *desktop app* type) in this folder, or point `YT_CLIENT_FILE` to it. The script stores `token.json`. Both are in `.gitignore`; never commit them.
- Quota: `videos.insert` costs 1 unit (capped at 100 uploads a day) and each video added to a playlist costs 50 of the 10,000 daily units; all 46 videos fit in one day. If it runs out, the script stops and can be run again.
- If you change a video and re-render it, `publish` warns; with `--replace` it uploads the new version and deletes the old one (YouTube cannot replace the file). The ID changes, so the site must be redeployed afterwards.
- Each video's ES and EN titles are in `videos/youtube-titles.json`. The description comes from the figure caption in the MDX and links to the exact site page where the video appears, with the video's `?lang=`; the site URL is read from `ml-academy-web/astro.config.mjs` (or `ML_ACADEMY_SITE`). `python scripts/manage_videos_yt.py descriptions` reapplies that format to videos already uploaded.

## Structure

```text
assets/icons/{aws,tools}/                 # SVG logos for diagrams (sources and terms in assets/icons/README.md)
charts/style.py                           # palette, matplotlib style and shared helpers (icon_node: box with logo)
charts/topics/<topic>.py                  # one topic's charts: TEXT[lang] and CHARTS
charts/make_charts.py                     # topic 1.3 bias charts (exposed by charts/topics/data-quality-bias.py, which adds dq-rules-flow)
charts/images/<course>/<topic>/           # generated PNGs (ES and EN)
videos/style.py                           # shared Manim palette and helpers
videos/<course>/<topic>/scenes.py         # Manim scenes; VIDEOS = {name: Class}; text based on MLA_LANG
scripts/render_video.py                   # renders one scene through Manim's API
scripts/render_all.py                     # runs everything and syncs to the web
```

`render_video.py` uses Manim's Python API instead of the CLI. The CLI turns the file path into a regular expression and fails when the path contains parentheses, such as `C:\Users\Name(Org)\...`.

`render_all.py` discovers topics: `charts/topics/*.py` and `videos/<course>/<topic>/scenes.py`.

## Naming convention

The web depends on this format for charts, and its YouTube manifest uses the same key without the extension:

```text
public/media/<course>/<topic>/<name>.<es|en>.png          (charts)
output/<course>/<topic>/<name>.<es|en>.mp4                (videos, local)
youtube-videos.json → "<course>/<topic>/<name>.<es|en>"    (YouTube ID)
```

| Topic | Charts (PNG, 1600 px, white background) | Videos (MP4 H.264, 1280×720, 30 fps) |
|---|---|---|
| `aws-ml-engineer-associate/data-quality-bias` | `class-imbalance`, `bias-ci-dpl`, `outliers-iqr`, `imbalance-metrics`, `dq-rules-flow` | `dq-pipeline`, `stratified-split`, `smote` |
| `aws-ml-engineer-associate/data-collection-storage` | `columnar-scan`, `kinesis-hot-shard`, `s3-lifecycle`, `lake-architecture`, `partition-pruning` | `stream-to-s3`, `feature-store-event-time`, `athena-partitions` |
| `aws-ml-engineer-associate/data-transformation-features` | `log-then-scale`, `scalers-outliers`, `chunking-strategies`, `encoding-pca` | `fit-on-train` |
| `aws-ml-engineer-associate/modeling-approaches` | `choose-layer`, `distillation-tradeoff`, `algorithm-map`, `sampling-params` | `rag-hybrid-filter` |
| `aws-ml-engineer-associate/training-customization` | `early-stopping`, `hpo-strategies`, `spot-checkpoints`, `regularization-curves` | `hyperband`, `regularization` |

## Add media for a new topic

1. **Charts:** create `charts/topics/<topic>.py` with a per-language `TEXT` and `chart_<name>(t, out)` functions that save `<name>.png`, listed in `CHARTS` (use `charts/style.py`).
2. **Videos:** create `videos/<course>/<topic>/scenes.py` with `VIDEOS = {"name": "Class"}` and a per-language `TEXT` dict (use `videos/style.py`). Scenes inherit `PacedScene`: they wait the reading time of each new text (`reading_time`), slow transitions down (`SPEED`) and never overlap captions. Short labels (numbers, names of up to `LABEL_WORDS` words) are read alongside the caption on screen, without waiting for it to finish; to leave a moment at the end of a step use `self.beat(s)`, not `self.wait(s)`, which is absorbed by the pending reading time.
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
