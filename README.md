# ML Academy — media

**Español** · [English](README.en.md)

Este proyecto genera las figuras y los videos cortos que ilustran los temas de [ML Academy](../ml-academy-web):
- Gráficos estáticos con matplotlib.
- Animaciones de 6 a 12 segundos con [Manim Community](https://www.manim.community/), sin audio y en bucle.

Cada medio se genera en español y en inglés.

Por ahora todo es **local**: los archivos generados no se suben a ningún repositorio ni a YouTube.

## Requisitos

- Python 3.10 o superior.
- No hace falta LaTeX: las escenas solo usan `Text`.
- No hace falta ffmpeg del sistema: Manim incluye PyAV.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    ·    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Generar y sincronizar

```bash
python scripts/render_all.py                  # gráficos + videos, ES y EN, y copia al web
python scripts/render_all.py --only charts    # solo gráficos (segundos)
python scripts/render_all.py --only videos    # solo videos (~1 minuto)
python scripts/render_all.py --no-sync        # no copiar al web
```

1. Los archivos se generan en `output/<curso>/<tema>/`.
2. Luego se copian a `../ml-academy-web/public/media/<curso>/<tema>/`, una carpeta que el web ignora en git.
3. El componente `Figure` del web solo muestra un medio si el archivo existe, así que el sitio funciona igual sin ellos.

## Estructura

```text
charts/make_charts.py                     # una función por gráfico; textos en TEXT[lang]
videos/<curso>/<tema>/scenes.py           # escenas de Manim; textos en TEXT según MLA_LANG
scripts/render_video.py                   # renderiza una escena con la API de Manim
scripts/render_all.py                     # orquesta todo y sincroniza con el web
```

`render_video.py` usa la API de Python de Manim en lugar del CLI. El CLI convierte la ruta del archivo en una expresión regular y falla cuando la ruta contiene paréntesis, como `C:\Users\Nombre(Org)\...`.

## Convención de nombres

El web depende de este formato:

```text
public/media/<curso>/<tema>/<nombre>.<es|en>.<png|mp4>
```

| Tema | Gráficos (PNG, 1600 px, fondo blanco) | Videos (MP4 H.264, 1280×720, 30 fps) |
|---|---|---|
| `aws-ml-engineer-associate/data-quality-bias` | `class-imbalance`, `bias-ci-dpl`, `outliers-iqr`, `imbalance-metrics` | `dq-pipeline`, `stratified-split`, `smote` |

## Agregar medios a un tema nuevo

1. **Gráficos:** agrega una función `chart_<nombre>(t, out)` en `charts/make_charts.py` que guarde `<nombre>.png`, y añádela a `CHARTS`. Si el tema es distinto, ajusta `CHART_TOPIC` en `render_all.py`; si crece, separa un archivo de gráficos por tema.
2. **Videos:** crea `videos/<curso>/<tema>/scenes.py` con un diccionario `TEXT` por idioma, y registra `nombre → Clase` en `VIDEOS` dentro de `render_all.py`.
3. Ejecuta `python scripts/render_all.py`.
4. En el MDX del tema, inserta `<Figure name="<nombre>" … />`.

Los datos de los gráficos deben coincidir con la teoría y con el laboratorio del tema. Por ejemplo, `imbalance-metrics` usa los resultados de `ml-academy-labs`.

## Paleta

Coincide con el sitio:

| Uso | Color |
|---|---|
| Texto (ink) | `#111114` |
| Acento | `#b3132b` |
| Correcto (ok) | `#1f7a4d` |
| Gris | `#c9c9cf` |
| Superficie | `#f3f3f5` |
