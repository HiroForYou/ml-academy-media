# ML Academy — media

**Español** · [English](README.en.md)

Este proyecto genera las figuras y los videos cortos que ilustran los temas de [ML Academy](../ml-academy-web):
- Gráficos estáticos con matplotlib.
- Animaciones de 6 a 12 segundos con [Manim Community](https://www.manim.community/), sin audio y en bucle.

Cada medio se genera en español y en inglés.

Los **gráficos** se guardan en el repositorio, en `charts/images/`, y también se sincronizan al sitio para el despliegue. Los **videos** se generan localmente en `output/` y se sincronizan a `public/media/` para previsualizarlos; los MP4 no se guardan en Git. Para publicar videos en el sitio se alojarán como no listados cuando esa fase esté disponible.

## Requisitos

- Python 3.10 o superior.
- **Para los videos, una distribución de LaTeX** (MiKTeX en Windows, TeX Live en macOS o Linux): las fórmulas se escriben con `MathTex`. Si MiKTeX pide instalar paquetes, activa la instalación automática: `initexmf --set-config-value=[MPM]AutoInstall=1`.
- Los gráficos no necesitan LaTeX: sus fórmulas usan *mathtext* de matplotlib con la fuente Computer Modern.
- No hace falta ffmpeg del sistema: Manim incluye PyAV.

```bash
# Una sola vez, en la carpeta raíz ml-academy/ (contiene los repositorios).
# Es el mismo entorno global que usan los laboratorios.
python -m venv .venv
# Windows: .venv\Scripts\activate    ·    macOS/Linux: source .venv/bin/activate
pip install -r ml-academy-media/requirements.txt
```

## Generar y sincronizar

```bash
python scripts/render_all.py                  # gráficos + videos, ES y EN, y copia al web
python scripts/render_all.py --only charts    # solo gráficos (segundos)
python scripts/render_all.py --only videos    # solo videos (~1 minuto)
python scripts/render_all.py --no-sync        # no copiar al web
python scripts/render_all.py --topic training-customization   # un solo tema (repetible)
```

1. Los gráficos se generan en `charts/images/<curso>/<tema>/` (en el repositorio). Los videos se generan en `output/<curso>/<tema>/`, que está en `.gitignore`.
2. Los PNG se copian a `../ml-academy-web/public/media/<curso>/<tema>/` y se versionan en el repositorio web. Los MP4 se copian a la misma carpeta local, pero siguen ignorados por Git.
3. El componente `Figure` muestra medios cuando existen; el sitio publicado incluye las figuras y omite los videos locales.

## Estructura

```text
charts/style.py                           # paleta, estilo de matplotlib y utilidades comunes
charts/topics/<tema>.py                   # gráficos de un tema: TEXT[lang] y CHARTS
charts/make_charts.py                     # gráficos del tema 1.3 (expuestos por charts/topics/data-quality-bias.py)
charts/images/<curso>/<tema>/             # PNG generados (ES y EN)
videos/style.py                           # paleta y utilidades comunes de Manim
videos/<curso>/<tema>/scenes.py           # escenas de Manim; VIDEOS = {nombre: Clase}; textos según MLA_LANG
scripts/render_video.py                   # renderiza una escena con la API de Manim
scripts/render_all.py                     # orquesta todo y sincroniza con el web
```

`render_video.py` usa la API de Python de Manim en lugar del CLI. El CLI convierte la ruta del archivo en una expresión regular y falla cuando la ruta contiene paréntesis, como `C:\Users\Nombre(Org)\...`.

`render_all.py` descubre los temas: `charts/topics/*.py` y `videos/<curso>/<tema>/scenes.py`. Los temas que aún no tienen módulo propio usan los generadores genéricos heredados (`charts/module_visuals.py` y `videos/aws-ml-engineer-associate/module-concepts/scenes.py`); elimínalos cuando ningún tema los use.

## Convención de nombres

El web depende de este formato:

```text
public/media/<curso>/<tema>/<nombre>.<es|en>.<png|mp4>
```

| Tema | Gráficos (PNG, 1600 px, fondo blanco) | Videos (MP4 H.264, 1280×720, 30 fps) |
|---|---|---|
| `aws-ml-engineer-associate/data-quality-bias` | `class-imbalance`, `bias-ci-dpl`, `outliers-iqr`, `imbalance-metrics` | `dq-pipeline`, `stratified-split`, `smote` |
| `aws-ml-engineer-associate/data-collection-storage` | `columnar-scan`, `kinesis-hot-shard`, `s3-lifecycle` | `stream-to-s3`, `feature-store-event-time` |
| `aws-ml-engineer-associate/data-transformation-features` | `log-then-scale`, `scalers-outliers`, `chunking-strategies` | `fit-on-train` |
| `aws-ml-engineer-associate/modeling-approaches` | `choose-layer`, `distillation-tradeoff` | `rag-hybrid-filter` |
| `aws-ml-engineer-associate/training-customization` | `early-stopping`, `hpo-strategies`, `spot-checkpoints` | `hyperband` |

## Agregar medios a un tema nuevo

1. **Gráficos:** crea `charts/topics/<tema>.py` con `TEXT` por idioma y funciones `chart_<nombre>(t, out)` que guarden `<nombre>.png`, listadas en `CHARTS` (usa `charts/style.py`).
2. **Videos:** crea `videos/<curso>/<tema>/scenes.py` con `VIDEOS = {"nombre": "Clase"}` y un diccionario `TEXT` por idioma (usa `videos/style.py`).
3. Ejecuta `python scripts/render_all.py --topic <tema>`.
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
