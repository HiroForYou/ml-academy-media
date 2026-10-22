"""
Renderiza una escena de Manim con la API de Python (no con el CLI).
Renders one Manim scene through the Python API (not the CLI).

El CLI de Manim compila la ruta del archivo como regex y falla con rutas que contienen
paréntesis; la API evita ese problema. Manim's CLI compiles the file path as a regex and
fails on paths with parentheses; the API avoids that.

    python scripts/render_video.py --lang es --file videos/.../scenes.py --scene Smote --out output/x/smote.es.mp4
"""

import argparse
import importlib.util
import os
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--lang", required=True)
parser.add_argument("--file", required=True)
parser.add_argument("--scene", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()

# El idioma se lee al importar las escenas. The language is read when scenes are imported.
os.environ["MLA_LANG"] = args.lang

from manim import tempconfig  # noqa: E402

spec = importlib.util.spec_from_file_location("scenes", args.file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

out = Path(args.out).resolve()
media_dir = out.parents[2] / "_manim" / args.lang  # output/_manim/<lang>
settings = {
    "pixel_width": 1280,
    "pixel_height": 720,
    "frame_rate": 30,
    "format": "mp4",
    "media_dir": str(media_dir),
    "output_file": out.stem,
    "disable_caching": True,
    "progress_bar": "none",
    "verbosity": "WARNING",
}
with tempconfig(settings):
    scene = getattr(module, args.scene)()
    scene.render()
    rendered = Path(scene.renderer.file_writer.movie_file_path)

out.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(rendered, out)
print(f"{args.scene} -> {out}")
