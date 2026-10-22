"""
Renderiza gráficos y videos en ES y EN y los copia al sitio web.
Renders charts and videos in ES and EN and copies them to the website.

    python scripts/render_all.py                 # todo / everything
    python scripts/render_all.py --only charts   # solo gráficos / charts only
    python scripts/render_all.py --no-sync       # no copiar al web / don't copy to the web

Gráficos / charts: charts/images/<course>/<topic>/<name>.<lang>.png   (en el repo / committed)
Videos:            output/<course>/<topic>/<name>.<lang>.mp4           (local, .gitignore)
Web:               ../ml-academy-web/public/media/<course>/<topic>/<name>.<lang>.<ext>
"""

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_MEDIA = ROOT.parent / "ml-academy-web" / "public" / "media"
LANGS = ["es", "en"]

# Videos por tema: nombre publicado -> clase de Manim. Videos per topic: published name -> Manim class.
VIDEOS = {
    ("aws-ml-engineer-associate", "data-quality-bias"): {
        "dq-pipeline": "DQPipeline",
        "stratified-split": "StratifiedSplit",
        "smote": "Smote",
    },
}

# Los gráficos de make_charts.py pertenecen a este tema. Charts in make_charts.py belong to this topic.
CHART_TOPIC = ("aws-ml-engineer-associate", "data-quality-bias")


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True)


CHART_IMAGES = ROOT / "charts" / "images"
VIDEO_OUTPUT = ROOT / "output"


def render_charts(lang):
    out = CHART_IMAGES / CHART_TOPIC[0] / CHART_TOPIC[1]
    out.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "output" / "_charts" / lang
    run([sys.executable, ROOT / "charts" / "make_charts.py", "--lang", lang, "--out", tmp])
    for png in tmp.glob("*.png"):
        shutil.move(png, out / f"{png.stem}.{lang}.png")


def render_videos(lang):
    for (course, topic), scenes in VIDEOS.items():
        scene_file = ROOT / "videos" / course / topic / "scenes.py"
        out = VIDEO_OUTPUT / course / topic
        for name, cls in scenes.items():
            run([sys.executable, ROOT / "scripts" / "render_video.py", "--lang", lang, "--file", scene_file,
                 "--scene", cls, "--out", out / f"{name}.{lang}.mp4"])


def sync():
    # Copia gráficos (charts/images) y videos (output) al web. Copies charts and videos to the web.
    for src in (CHART_IMAGES, VIDEO_OUTPUT):
        if not src.exists():
            continue
        for course_dir in src.iterdir():
            if course_dir.name.startswith("_") or not course_dir.is_dir():
                continue
            for topic_dir in course_dir.iterdir():
                if topic_dir.name.startswith("_") or not topic_dir.is_dir():
                    continue
                dest = WEB_MEDIA / course_dir.name / topic_dir.name
                dest.mkdir(parents=True, exist_ok=True)
                for f in topic_dir.iterdir():
                    if f.is_file() and f.suffix in (".png", ".mp4"):
                        shutil.copy2(f, dest / f.name)
                        print(f"  -> {dest / f.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=["charts", "videos"])
    parser.add_argument("--no-sync", action="store_true")
    args = parser.parse_args()

    start = time.time()
    for lang in LANGS:
        if args.only != "videos":
            render_charts(lang)
        if args.only != "charts":
            render_videos(lang)
    if not args.no_sync:
        sync()
    print(f"done in {time.time() - start:.0f}s")


if __name__ == "__main__":
    main()
