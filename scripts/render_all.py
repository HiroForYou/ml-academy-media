"""
Renderiza gráficos y videos en ES y EN y los copia al sitio web.
Renders charts and videos in ES and EN and copies them to the website.

    python scripts/render_all.py                                 # todo / everything
    python scripts/render_all.py --only charts                   # solo gráficos / charts only
    python scripts/render_all.py --topic training-customization  # un tema / one topic
    python scripts/render_all.py --no-sync                       # no copiar al web / don't copy to the web

Descubrimiento / discovery:
  Gráficos / charts: charts/topics/<topic>.py           (TEXT + CHARTS; curso en COURSE, por defecto el de AWS)
  Videos:            videos/<course>/<topic>/scenes.py  (VIDEOS = {"nombre": "Clase"})
  Temas sin módulo propio usan los generadores genéricos heredados (charts/module_visuals.py y
  videos/<course>/module-concepts/scenes.py) mientras existan.
  Topics without their own module fall back to the legacy generic generators while they exist.

Salidas / outputs:
  charts/images/<course>/<topic>/<name>.<lang>.png   (en el repo / committed)
  output/<course>/<topic>/<name>.<lang>.mp4           (local, .gitignore)
  ../ml-academy-web/public/media/<course>/<topic>/<name>.<lang>.<ext>
"""

import argparse
import ast
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_MEDIA = ROOT.parent / "ml-academy-web" / "public" / "media"
CHART_IMAGES = ROOT / "charts" / "images"
VIDEO_OUTPUT = ROOT / "output"
CHART_TOPICS = ROOT / "charts" / "topics"
VIDEO_ROOT = ROOT / "videos"
LANGS = ["es", "en"]
DEFAULT_COURSE = "aws-ml-engineer-associate"

LEGACY_CHARTS = ROOT / "charts" / "module_visuals.py"
LEGACY_SCENES = "module-concepts"


def literal(path, name, default=None):
    """Lee una asignación literal sin importar el módulo. Reads a literal assignment without importing."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and any(getattr(t, "id", None) == name for t in stmt.targets):
            return ast.literal_eval(stmt.value)
    return default


def chart_jobs():
    """{(course, topic): (script, extra_args)}"""
    jobs = {}
    for script in sorted(CHART_TOPICS.glob("*.py")):
        if script.name.startswith("_"):
            continue
        jobs[(literal(script, "COURSE", DEFAULT_COURSE), script.stem)] = (script, [])
    if LEGACY_CHARTS.exists():
        for topic in literal(LEGACY_CHARTS, "TOPICS", {}):
            jobs.setdefault((DEFAULT_COURSE, topic), (LEGACY_CHARTS, ["--topic", topic]))
    return jobs


def video_jobs():
    """{(course, topic): (scene_file, {name: class}, env)}"""
    jobs = {}
    legacy = []
    for course_dir in sorted(p for p in VIDEO_ROOT.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        for topic_dir in sorted(p for p in course_dir.iterdir() if p.is_dir()):
            scenes = topic_dir / "scenes.py"
            if not scenes.exists():
                continue
            if topic_dir.name == LEGACY_SCENES:
                legacy.append((course_dir.name, scenes))
                continue
            jobs[(course_dir.name, topic_dir.name)] = (scenes, literal(scenes, "VIDEOS", {}), {})
    for course, scenes in legacy:
        for topic in literal(scenes, "TOPICS", {}):
            jobs.setdefault((course, topic), (scenes, literal(scenes, "VIDEOS", {}), {"MLA_TOPIC": topic}))
    return jobs


def run(cmd, env=None):
    print("  $", " ".join(str(c) for c in cmd))
    full_env = None
    if env:
        full_env = os.environ.copy()
        full_env.update(env)
    subprocess.run([str(c) for c in cmd], check=True, env=full_env)


def render_charts(lang, topics):
    for (course, topic), (script, extra) in chart_jobs().items():
        if topics and topic not in topics:
            continue
        out = CHART_IMAGES / course / topic
        out.mkdir(parents=True, exist_ok=True)
        tmp = VIDEO_OUTPUT / "_charts" / lang / course / topic
        if tmp.exists():
            shutil.rmtree(tmp)
        run([sys.executable, script, *extra, "--lang", lang, "--out", tmp])
        for png in tmp.glob("*.png"):
            shutil.move(png, out / f"{png.stem}.{lang}.png")


def render_videos(lang, topics):
    for (course, topic), (scene_file, scenes, env) in video_jobs().items():
        if topics and topic not in topics:
            continue
        out = VIDEO_OUTPUT / course / topic
        for name, cls in scenes.items():
            run([sys.executable, ROOT / "scripts" / "render_video.py", "--lang", lang, "--file", scene_file,
                 "--scene", cls, "--out", out / f"{name}.{lang}.mp4"], env)


def sync(topics):
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
                if topics and topic_dir.name not in topics:
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
    parser.add_argument("--topic", action="append", help="id del tema (repetible) / topic id (repeatable)")
    parser.add_argument("--no-sync", action="store_true")
    args = parser.parse_args()

    topics = set(args.topic or [])
    known = {t for _, t in chart_jobs()} | {t for _, t in video_jobs()}
    unknown = topics - known
    if unknown:
        parser.error(f"unknown topic(s): {', '.join(sorted(unknown))}")

    start = time.time()
    for lang in LANGS:
        if args.only != "videos":
            render_charts(lang, topics)
        if args.only != "charts":
            render_videos(lang, topics)
    if not args.no_sync:
        sync(topics)
    print(f"done in {time.time() - start:.0f}s")


if __name__ == "__main__":
    main()
