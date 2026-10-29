# ML Academy — media

**Español** · [English](README.en.md)

Este proyecto genera las figuras y los videos cortos que ilustran los temas de [ML Academy](../ml-academy-web):
- Gráficos estáticos con matplotlib.
- Animaciones de unos 25 a 65 segundos (según la cantidad de texto) con [Manim Community](https://www.manim.community/), sin audio. El ritmo deja leer cada texto antes del siguiente cambio.

Cada medio se genera en español y en inglés.

Los **gráficos** se guardan en el repositorio, en `charts/images/`, y también se sincronizan al sitio para el despliegue. Los **videos** se generan localmente en `output/` (los MP4 no se guardan en Git) y se publican en YouTube como no listados con `manage_videos_yt.py`; el sitio los incrusta a partir de `ml-academy-web/src/data/youtube-videos.json`.

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
python scripts/render_all.py --only videos    # solo videos (~10 minutos)
python scripts/render_all.py --no-sync        # no copiar al web
python scripts/render_all.py --topic training-customization   # un solo tema (repetible)
```

1. Los gráficos se generan en `charts/images/<curso>/<tema>/` (en el repositorio). Los videos se generan en `output/<curso>/<tema>/`, que está en `.gitignore`.
2. Los PNG se copian a `../ml-academy-web/public/media/<curso>/<tema>/` y se versionan en el repositorio web. Los MP4 ya no se copian al web: se suben a YouTube (ver más abajo).
3. El componente `Figure` muestra los PNG y, con `video`, incrusta el video de YouTube registrado en el manifiesto.

## Publicar los videos en YouTube

`scripts/manage_videos_yt.py` sube cada MP4 de `output/` como video **no listado**, lo agrega a una lista de reproducción (también no listada) por curso y escribe los IDs en `../ml-academy-web/src/data/youtube-videos.json`. Es idempotente: un video ya subido, con el mismo SHA-256, no se vuelve a subir.

```bash
pip install -r requirements.txt               # incluye las librerías de la API de YouTube
python scripts/manage_videos_yt.py auth               # una sola vez: abre el navegador y guarda token.json
python scripts/manage_videos_yt.py publish --dry-run  # muestra qué se subiría
python scripts/manage_videos_yt.py publish            # sube lo que falte y actualiza el manifiesto
python scripts/manage_videos_yt.py verify             # comprueba en YouTube privacidad e incrustación
python scripts/manage_videos_yt.py                    # menú interactivo (listar, subir, editar, privacidad, eliminar)
```

- Credenciales: coloca el archivo OAuth de Google Cloud (`client_secret*.json`, tipo *aplicación de escritorio*) en esta carpeta, o indica su ruta en `YT_CLIENT_FILE`. El script guarda `token.json`. Ambos están en `.gitignore`; no los subas al repositorio.
- Cuota: `videos.insert` cuesta 1 unidad (tope de 100 subidas al día) y cada video añadido a una lista cuesta 50 de las 10.000 unidades diarias; los 46 videos caben en un día. Si se agota, el script se detiene y se puede relanzar.
- Si cambias un video y vuelves a renderizarlo, `publish` avisa; con `--replace` sube la versión nueva y borra la anterior (YouTube no permite sustituir el archivo). El ID cambia, así que después hay que volver a desplegar el sitio.
- Los títulos en ES y EN de cada video están en `videos/youtube-titles.json`. La descripción sale del pie de figura del MDX y enlaza a la página exacta del sitio donde aparece el video, con `?lang=` del idioma del video; la URL del sitio se toma de `ml-academy-web/astro.config.mjs` (o de `ML_ACADEMY_SITE`). `python scripts/manage_videos_yt.py descriptions` reaplica ese formato a los videos ya subidos.

## Estructura

```text
assets/icons/{aws,tools}/                 # logos SVG de los diagramas (fuentes y términos en assets/icons/README.md)
charts/style.py                           # paleta, estilo de matplotlib y utilidades comunes (icon_node: caja con logo)
charts/topics/<tema>.py                   # gráficos de un tema: TEXT[lang] y CHARTS
charts/make_charts.py                     # gráficos de sesgo del tema 1.3 (los expone charts/topics/data-quality-bias.py, que añade dq-rules-flow)
charts/images/<curso>/<tema>/             # PNG generados (ES y EN)
videos/style.py                           # paleta y utilidades comunes de Manim
videos/<curso>/<tema>/scenes.py           # escenas de Manim; VIDEOS = {nombre: Clase}; textos según MLA_LANG
scripts/render_video.py                   # renderiza una escena con la API de Manim
scripts/render_all.py                     # orquesta todo y sincroniza con el web
```

`render_video.py` usa la API de Python de Manim en lugar del CLI. El CLI convierte la ruta del archivo en una expresión regular y falla cuando la ruta contiene paréntesis, como `C:\Users\Nombre(Org)\...`.

`render_all.py` descubre los temas: `charts/topics/*.py` y `videos/<curso>/<tema>/scenes.py`.

## Convención de nombres

El web depende de este formato para los gráficos, y su manifiesto de YouTube usa la misma clave sin extensión:

```text
public/media/<curso>/<tema>/<nombre>.<es|en>.png          (gráficos)
output/<curso>/<tema>/<nombre>.<es|en>.mp4                (videos, locales)
youtube-videos.json → "<curso>/<tema>/<nombre>.<es|en>"    (ID de YouTube)
```

| Tema | Gráficos (PNG, 1600 px, fondo blanco) | Videos (MP4 H.264, 1280×720, 30 fps) |
|---|---|---|
| `aws-ml-engineer-associate/data-quality-bias` | `class-imbalance`, `bias-ci-dpl`, `outliers-iqr`, `imbalance-metrics`, `dq-rules-flow` | `dq-pipeline`, `stratified-split`, `smote` |
| `aws-ml-engineer-associate/data-collection-storage` | `columnar-scan`, `kinesis-hot-shard`, `s3-lifecycle`, `lake-architecture`, `partition-pruning` | `stream-to-s3`, `feature-store-event-time`, `athena-partitions` |
| `aws-ml-engineer-associate/data-transformation-features` | `log-then-scale`, `scalers-outliers`, `chunking-strategies`, `encoding-pca` | `fit-on-train` |
| `aws-ml-engineer-associate/modeling-approaches` | `choose-layer`, `distillation-tradeoff`, `algorithm-map`, `sampling-params` | `rag-hybrid-filter` |
| `aws-ml-engineer-associate/training-customization` | `early-stopping`, `hpo-strategies`, `spot-checkpoints`, `regularization-curves` | `hyperband`, `regularization` |

## Agregar medios a un tema nuevo

1. **Gráficos:** crea `charts/topics/<tema>.py` con `TEXT` por idioma y funciones `chart_<nombre>(t, out)` que guarden `<nombre>.png`, listadas en `CHARTS` (usa `charts/style.py`).
2. **Videos:** crea `videos/<curso>/<tema>/scenes.py` con `VIDEOS = {"nombre": "Clase"}` y un diccionario `TEXT` por idioma (usa `videos/style.py`). Las escenas heredan de `PacedScene`: esperan el tiempo de lectura de cada texto nuevo (`reading_time`), ralentizan las transiciones (`SPEED`) y nunca superponen subtítulos. Las etiquetas cortas (cifras, nombres de hasta `LABEL_WORDS` palabras) se leen junto con el subtítulo en pantalla, sin esperar a que termine; para dejar un momento al final de un paso usa `self.beat(s)`, no `self.wait(s)`, que queda absorbido por la lectura pendiente.
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
