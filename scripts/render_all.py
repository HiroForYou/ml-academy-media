"""
Renderiza gráficos y videos en ES y EN y los copia al sitio web.
Renders charts and videos in ES and EN and copies them to the website.

    python scripts/render_all.py                 # todo / everything
    python scripts/render_all.py --only charts   # solo gráficos / charts only
    python scripts/render_all.py --no-sync       # no copiar al web / don't copy to the web

Salida / output:  output/<course>/<topic>/<name>.<lang>.<ext>
Web:              ../ml-academy-web/public/media/<course>/<topic>/<name>.<lang>.<ext>
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


def render_charts(lang):
    out = ROOT / "output" / CHART_TOPIC[0] / CHART_TOPIC[1]
    out.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "output" / "_charts" / lang
    run([sys.executable, ROOT / "charts" / "make_charts.py", "--lang", lang, "--out", tmp])
    for png in tmp.glob("*.png"):
        shutil.move(png, out / f"{png.stem}.{lang}.png")


def render_videos(lang):
    for (course, topic), scenes in VIDEOS.items():
        scene_file = ROOT / "videos" / course / topic / "scenes.py"
        out = ROOT / "output" / course / topic
        for name, cls in scenes.items():
            run([sys.executable, ROOT / "scripts" / "render_video.py", "--lang", lang, "--file", scene_file,
                 "--scene", cls, "--out", out / f"{name}.{lang}.mp4"])


def sync():
    src = ROOT / "output"
    for course_dir in src.iterdir():
        if course_dir.name.startswith("_"):
            continue
        for topic_dir in course_dir.iterdir():
            if topic_dir.name.startswith("_"):
                continue
            dest = WEB_MEDIA / course_dir.name / topic_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in topic_dir.iterdir():
                if not f.is_file():
                    continue
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
