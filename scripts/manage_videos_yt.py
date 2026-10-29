"""
Gestiona en YouTube los videos de ML Academy: los sube como no listados, los agrega a una lista de
reproducción por curso y registra sus IDs en el sitio (ml-academy-web/src/data/youtube-videos.json).
Manage ML Academy's videos on YouTube: upload them as unlisted, add them to one playlist per course,
and record their IDs for the site (ml-academy-web/src/data/youtube-videos.json).

    python scripts/manage_videos_yt.py                    # menú interactivo / interactive menu
    python scripts/manage_videos_yt.py auth               # autoriza la cuenta (abre el navegador) / authorize the account
    python scripts/manage_videos_yt.py auth --no-browser  # imprime la URL en vez de abrir el navegador / print the URL instead
    python scripts/manage_videos_yt.py publish --dry-run  # muestra qué se subiría, sin subir / show the plan, no upload
    python scripts/manage_videos_yt.py publish            # sube lo que falte / upload what is missing
    python scripts/manage_videos_yt.py publish --only security,mlops-cicd --lang es --limit 3
    python scripts/manage_videos_yt.py verify             # comprueba privacidad e incrustación en YouTube / check privacy and embeddability
    python scripts/manage_videos_yt.py status             # compara archivos locales y manifiesto / compare local files and manifest
    python scripts/manage_videos_yt.py descriptions       # reaplica el formato de descripción a los videos ya subidos / reapply the description format to uploaded videos

Origen de los videos / video source: output/<curso>/<tema>/<nombre>.<es|en>.mp4 (los genera scripts/render_all.py).
Es idempotente: un video ya subido (mismo SHA-256) no se vuelve a subir. Si el archivo cambió, avisa; con
--replace sube la versión nueva y borra la anterior. Idempotent: an uploaded video (same SHA-256) is never
re-uploaded. If the file changed it warns; with --replace it uploads the new one and deletes the old one.

Cuota / quota: videos.insert cuesta 1 unidad (tope de 100 subidas al día) y cada video añadido a una lista
cuesta 50 de las 10.000 unidades diarias. Si se agota, el script se detiene y se puede relanzar al día siguiente.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parents[1]  # carpeta ml-academy-media / ml-academy-media folder
WEB = ROOT.parent / "ml-academy-web"
CONTENT = WEB / "src" / "content" / "courses"
MANIFEST = WEB / "src" / "data" / "youtube-videos.json"
TITLES = ROOT / "videos" / "youtube-titles.json"
OUTPUT = ROOT / "output"
TOKEN_FILE = ROOT / "token.json"  # credencial con refresh token; está en .gitignore / refresh-token credential, gitignored

# Permite subir, listar, actualizar y eliminar videos y listas propias.
# Lets the app upload, list, update and delete the account's own videos and playlists.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

CATEGORY_EDUCATION = "27"
LANG_NAME = {"es": "Español", "en": "English"}


def site_url():
    """URL pública del sitio. Sale de ml-academy-web/astro.config.mjs (el mismo `owner/repo` que usa Astro para `site` y
    `base`), o de la variable ML_ACADEMY_SITE si se define. Public site URL, read from the web's astro.config.mjs (the
    same `owner/repo` Astro uses for `site` and `base`), or from ML_ACADEMY_SITE if set."""
    if os.environ.get("ML_ACADEMY_SITE"):
        return os.environ["ML_ACADEMY_SITE"].rstrip("/")
    config = WEB / "astro.config.mjs"
    match = re.search(r"GITHUB_REPOSITORY \?\? '([^/']+)/([^']+)'", config.read_text(encoding="utf-8")) if config.exists() else None
    if not match:
        raise SystemExit("No pude deducir la URL del sitio de ml-academy-web/astro.config.mjs; define ML_ACADEMY_SITE.")
    owner, repo = match.groups()
    return f"https://{owner.lower()}.github.io/{repo}"


SITE_URL = site_url()
# (enlace, tema, curso, nota final) por idioma / (link line, topic, course, closing note) per language
LABELS = {
    "es": ("Explicación completa en ML Academy:", "Tema", "Curso", "Animación sin audio."),
    "en": ("Full explanation on ML Academy:", "Topic", "Course", "Animation without audio."),
}
HASHTAGS = "#AWS #MachineLearning #MLA_C02"  # YouTube muestra los 3 primeros sobre el título / shows the first 3 above the title
QUOTA_REASONS = {"quotaExceeded", "uploadLimitExceeded", "dailyLimitExceeded", "rateLimitExceeded"}

sys.stdout.reconfigure(encoding="utf-8")


# ─────────────────────────────── autenticación / authentication ───────────────────────────────

def client_file():
    """Archivo OAuth de Google Cloud: YT_CLIENT_FILE, client_secrets.json o client_secret*.json."""
    env = os.environ.get("YT_CLIENT_FILE")
    candidates = [Path(env)] if env else [ROOT / "client_secrets.json", *sorted(ROOT.glob("client_secret*.json"))]
    for path in candidates:
        if path.is_file():
            return path
    raise SystemExit("Falta el archivo OAuth de Google Cloud (client_secret*.json) en ml-academy-media/.")


def autenticar(open_browser=True):
    credentials = None
    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
        except RefreshError:  # token revocado o caducado: se vuelve a autorizar / revoked or expired: re-authorize
            credentials = None
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(client_file()), SCOPES)
        # open_browser=False imprime la URL para pegarla en el navegador que prefieras (p. ej. Brave).
        # open_browser=False prints the URL so you can paste it in the browser you prefer.
        credentials = flow.run_local_server(port=0, open_browser=open_browser)
    TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=credentials)


# ─────────────────────────────── manifiesto / manifest ───────────────────────────────

def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"playlists": {}, "videos": {}}


def save_manifest(manifest):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST.with_suffix(".tmp")
    tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(MANIFEST)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


# ─────────────────────────────── metadatos / metadata ───────────────────────────────

def topic_order(course):
    """(código, id, títulos) de cada tema, en el orden del temario / each topic in syllabus order."""
    syllabus = json.loads((CONTENT / course / "syllabus" / "syllabus.json").read_text(encoding="utf-8"))
    return [(t["code"], t["id"], t["title"]) for d in syllabus["domains"] for t in d["topics"]]


def course_info(course):
    return json.loads((CONTENT / course / "course.json").read_text(encoding="utf-8"))


def find_caption(course, name, lang):
    """Pie de figura del video en el MDX del idioma / the video's figure caption from the language's MDX."""
    pattern = re.compile(r'<Figure\s+name="%s"[^>]*?caption="([^"]*)"' % re.escape(name), re.S)
    for path in sorted((CONTENT / course).glob(f"**/*.{lang}.mdx")):
        match = pattern.search(path.read_text(encoding="utf-8"))
        if match:
            return match.group(1)
    return ""


def describe(caption, course, course_title, badge, topic, page, code, topic_title, lang):
    """Descripción para YouTube. Lo que se ve antes de «más» es la idea del video y el enlace al tema; después, tema y
    curso, la nota de que no tiene audio y tres hashtags. Cada video tiene su propia idea (el pie de figura).
    YouTube description. What shows before "more" is the video's idea and the link to the topic; then topic and
    course, the no-audio note and three hashtags. Each video has its own idea (the figure caption)."""
    link_label, topic_label, course_label, closing = LABELS[lang]
    idea = caption.strip()
    if idea and idea[-1] not in ".!?":
        idea += "."
    course_line = f"{course_title} ({badge})" if badge else course_title
    return clean("\n\n".join(filter(None, [
        idea,
        f"{link_label}\n{SITE_URL}/courses/{course}/topics/{topic}/{page}?lang={lang}",
        f"{topic_label}: {code} {topic_title}\n{course_label}: {course_line}\n{closing}",
        HASHTAGS,
    ])), 5000)


def find_page(course, topic, name, lang):
    """Ruta del sitio donde aparece el video: '' (parte 1), '2/', '3/'... o 'practice/' (ejemplo y cuestionario).
    Mismas reglas que ml-academy-web/src/pages/courses/[course]/topics/[topic]/[...step].astro.
    Site path where the video appears: '' (part 1), '2/', '3/'... or 'practice/' (example and quiz).
    Same rules as the web's topic page route."""
    marker = f'<Figure name="{name}"'
    parts = sorted((CONTENT / course / "theory" / topic).glob(f"part-*.{lang}.mdx"),
                   key=lambda f: int(f.name.split("-")[1].split(".")[0]))
    for path in parts:
        if marker in path.read_text(encoding="utf-8"):
            number = int(path.name.split("-")[1].split(".")[0])
            return "" if number == 1 else f"{number}/"
    example = CONTENT / course / "examples" / f"{topic}.{lang}.mdx"
    if example.exists() and marker in example.read_text(encoding="utf-8"):
        return "practice/" if len(parts) > 1 else ""
    raise SystemExit(f"No encontré la figura de video '{name}' ({lang}) en la teoría ni en el ejemplo de {topic}.")


def clean(text, limit):
    """YouTube no admite < ni > en títulos y descripciones / YouTube disallows < and > in titles and descriptions."""
    return re.sub(r"[<>]", "", text).strip()[:limit]


def discover(only=None, lang=None):
    """Videos locales, en orden de temario / local videos in syllabus order."""
    titles = json.loads(TITLES.read_text(encoding="utf-8"))
    found = []
    for course_dir in sorted(p for p in OUTPUT.iterdir() if p.is_dir() and not p.name.startswith("_")):
        course = course_dir.name
        if not (CONTENT / course / "course.json").exists():
            continue
        info = course_info(course)
        for order, (code, topic, topic_title) in enumerate(topic_order(course)):
            if only and topic not in only:
                continue
            for path in sorted((course_dir / topic).glob("*.mp4")) if (course_dir / topic).is_dir() else []:
                name, video_lang = path.stem.rsplit(".", 1)
                if lang and video_lang != lang:
                    continue
                title = titles.get(name, {}).get(video_lang) or name.replace("-", " ").capitalize()
                caption = find_caption(course, name, video_lang)
                description = describe(caption, course, info["title"][video_lang], info.get("badge", ""), topic,
                                       find_page(course, topic, name, video_lang), code,
                                       topic_title[video_lang], video_lang)
                found.append({
                    "key": f"{course}/{topic}/{name}.{video_lang}", "course": course, "topic": topic, "name": name,
                    "lang": video_lang, "path": path, "order": (order, name, video_lang),
                    "title": clean(f"ML Academy · {title} ({video_lang.upper()})", 100),
                    "description": description,
                    "tags": ["AWS", "MLA-C02", "Machine Learning", "MLOps", "SageMaker", "ML Academy"],
                })
    return sorted(found, key=lambda v: (v["course"], v["order"]))


# ─────────────────────────────── YouTube API ───────────────────────────────

def error_reasons(error):
    """Motivos que devuelve la API (p. ej. quotaExceeded, uploadLimitExceeded) / reasons returned by the API."""
    try:
        return [e.get("reason") for e in json.loads(error.content).get("error", {}).get("errors", [])]
    except (ValueError, AttributeError):
        return []


def is_quota_error(error):
    return bool(set(error_reasons(error)) & QUOTA_REASONS)


def ensure_playlist(youtube, manifest, course):
    """Lista de reproducción no listada del curso; se crea si no existe / the course's unlisted playlist, created if missing."""
    if course in manifest["playlists"]:
        return manifest["playlists"][course]["id"]
    info = course_info(course)
    title = clean(f"ML Academy · {info['title']['es']} ({info.get('badge', '')})", 150)
    page_token = None
    while True:
        response = youtube.playlists().list(part="snippet", mine=True, maxResults=50, pageToken=page_token).execute()
        for item in response.get("items", []):
            if item["snippet"]["title"] == title:
                manifest["playlists"][course] = {"id": item["id"], "title": title}
                save_manifest(manifest)
                return item["id"]
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    created = youtube.playlists().insert(part="snippet,status", body={
        "snippet": {"title": title, "description": clean(
            f"Animaciones cortas de {info['title']['es']}. Videos no listados que se incrustan en ML Academy.", 5000)},
        "status": {"privacyStatus": "unlisted"},
    }).execute()
    manifest["playlists"][course] = {"id": created["id"], "title": title}
    save_manifest(manifest)
    return created["id"]


def upload(youtube, video):
    body = {
        "snippet": {
            "title": video["title"], "description": video["description"], "tags": video["tags"],
            "categoryId": CATEGORY_EDUCATION, "defaultLanguage": video["lang"], "defaultAudioLanguage": video["lang"],
        },
        "status": {"privacyStatus": "unlisted", "embeddable": True, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(str(video["path"]), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        _, response = request.next_chunk(num_retries=3)
    return response


def add_to_playlist(youtube, playlist_id, video_id):
    item = youtube.playlistItems().insert(part="snippet", body={"snippet": {
        "playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video_id}}}).execute()
    return item["id"]


def publish(args):
    only = set(args.only.split(",")) if args.only else None
    videos = discover(only, args.lang)
    manifest = load_manifest()
    pending = []
    for video in videos:
        entry = manifest["videos"].get(video["key"])
        digest = sha256(video["path"])
        video["sha256"] = digest
        if entry and entry["sha256"] == digest:
            continue
        if entry and not args.replace:
            print(f"CAMBIÓ  {video['key']}: el archivo difiere del subido; usa --replace para reemplazarlo.")
            continue
        pending.append(video)
    total_pending = len(pending)
    if args.limit:
        pending = pending[: args.limit]

    print(f"{len(videos)} videos locales · {len(videos) - total_pending} ya publicados o sin cambios · "
          f"{total_pending} por subir" + (f" · se subirán {len(pending)} ahora (--limit)" if len(pending) < total_pending else ""))
    for video in pending:
        size = video["path"].stat().st_size / 1e6
        print(f"  - {video['key']}  ({size:.1f} MB)\n      {video['title']}")
    if args.dry_run or not pending:
        return

    youtube = autenticar(not getattr(args, "no_browser", False))
    uploaded = 0
    for video in pending:
        key = video["key"]
        try:
            playlist = ensure_playlist(youtube, manifest, video["course"])
            print(f"Subiendo {key} ...", flush=True)
            response = upload(youtube, video)
            privacy = response.get("status", {}).get("privacyStatus")
            previous = manifest["videos"].get(key)
            manifest["videos"][key] = {
                "id": response["id"], "sha256": video["sha256"], "privacy": privacy,
                "uploadedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            save_manifest(manifest)  # antes de seguir: si algo falla después, el ID no se pierde / saved first so the ID is never lost
            if privacy != "unlisted":
                raise SystemExit(f"YouTube dejó {key} como '{privacy}' y no como 'unlisted'. Se detiene: revisa el estado "
                                 f"de verificación del proyecto de API en Google Cloud / YouTube API Services.")
            manifest["videos"][key]["playlistItemId"] = add_to_playlist(youtube, playlist, response["id"])
            save_manifest(manifest)
            if previous and args.replace:
                youtube.videos().delete(id=previous["id"]).execute()
                print(f"  reemplazado: se borró la versión anterior ({previous['id']})")
            uploaded += 1
            print(f"  ok  https://www.youtube.com/watch?v={response['id']}  [{privacy}]")
        except HttpError as error:
            if is_quota_error(error):
                print(f"Límite de YouTube alcanzado tras {uploaded} subidas ({', '.join(error_reasons(error))}); "
                      f"vuelve a ejecutar más tarde (es idempotente).")
                return
            raise
    print(f"Listo: {uploaded} videos subidos.")


def refresh_descriptions(args):
    """Actualiza la descripción de los videos ya publicados con el formato actual (conserva título, tags y demás).
    Updates the description of already published videos to the current format (keeps title, tags and the rest)."""
    manifest = load_manifest()
    wanted = {v["key"]: v for v in discover(set(args.only.split(",")) if args.only else None, args.lang)}
    todo = {key: wanted[key] for key in manifest["videos"] if key in wanted}
    if not todo:
        print("No hay videos publicados que actualizar.")
        return
    youtube = None if args.dry_run else autenticar(not getattr(args, "no_browser", False))
    changed = 0
    for key, video in todo.items():
        if args.dry_run:
            print(f"--- {key}\n{video['description']}\n")
            continue
        video_id = manifest["videos"][key]["id"]
        items = youtube.videos().list(part="snippet", id=video_id).execute().get("items", [])
        if not items:
            print(f"FALTA   {key}: el video {video_id} ya no existe en el canal")
            continue
        snippet = items[0]["snippet"]
        if snippet.get("description") == video["description"]:
            continue
        keep = {k: snippet[k] for k in ("title", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage") if k in snippet}
        youtube.videos().update(part="snippet", body={"id": video_id, "snippet": {**keep, "description": video["description"]}}).execute()
        changed += 1
        print(f"  ok  {key}")
    if not args.dry_run:
        print(f"{changed} descripciones actualizadas.")


def verify(args):
    manifest = load_manifest()
    ids = {entry["id"]: key for key, entry in manifest["videos"].items()}
    if not ids:
        print("El manifiesto no tiene videos.")
        return
    youtube = autenticar(not getattr(args, "no_browser", False))
    problems = 0
    seen = set()
    id_list = list(ids)
    for i in range(0, len(id_list), 50):
        response = youtube.videos().list(part="status,snippet", id=",".join(id_list[i:i + 50])).execute()
        for item in response.get("items", []):
            seen.add(item["id"])
            status = item["status"]
            ok = status["privacyStatus"] == "unlisted" and status.get("embeddable") and status["uploadStatus"] == "processed"
            if not ok:
                problems += 1
            print(f"{'ok ' if ok else 'REVISAR'}  {ids[item['id']]}  {status['privacyStatus']}  "
                  f"embeddable={status.get('embeddable')}  {status['uploadStatus']}")
    for missing in sorted(set(ids) - seen):
        problems += 1
        print(f"FALTA   {ids[missing]}  ({missing}) ya no existe en el canal")
    print(f"{len(seen)} de {len(ids)} verificados · {problems} con problemas")


def status(_args):
    manifest = load_manifest()
    local = {v["key"]: v for v in discover()}
    for key, video in local.items():
        entry = manifest["videos"].get(key)
        if not entry:
            state = "sin subir"
        elif entry["sha256"] != sha256(video["path"]):
            state = "CAMBIÓ"
        else:
            state = f"subido  {entry['id']}  [{entry.get('privacy')}]"
        print(f"{state:40s} {key}")
    extra = set(manifest["videos"]) - set(local)
    for key in sorted(extra):
        print(f"{'en manifiesto, sin archivo':40s} {key}")
    print(f"\n{len(local)} locales · {sum(1 for k in local if k in manifest['videos'])} en el manifiesto")


# ─────────────────────────────── menú interactivo / interactive menu ───────────────────────────────

def validar_privacidad():
    while True:
        value = input("Privacidad (private/unlisted/public): ").strip().lower()
        if value in ("private", "unlisted", "public"):
            return value
        print("Valor no válido.")


def obtener_videos(youtube):
    """Obtiene los videos del canal autenticado, paginando resultados."""
    channel = youtube.channels().list(part="contentDetails", mine=True).execute()
    items = channel.get("items", [])
    if not items:
        print("No se encontró un canal para esta cuenta.")
        return []
    playlist_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    videos, page_token = [], None
    while True:
        response = youtube.playlistItems().list(
            part="snippet,contentDetails", playlistId=playlist_id, maxResults=50, pageToken=page_token).execute()
        for item in response.get("items", []):
            videos.append({"id": item["contentDetails"]["videoId"], "title": item["snippet"]["title"]})
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return videos


def listar_videos(youtube):
    videos = obtener_videos(youtube)
    if not videos:
        print("No se encontraron videos.")
        return
    for i, video in enumerate(videos, start=1):
        print(f'{i}. {video["title"]} | ID: {video["id"]}')
        print(f'   https://www.youtube.com/watch?v={video["id"]}')
    print(f"\nTotal: {len(videos)} videos")


def subir_video(youtube):
    path = input("Ruta del video: ").strip().strip('"')
    if not os.path.isfile(path):
        print("No existe el archivo.")
        return
    title = input("Título: ").strip()
    if not title:
        print("El título es obligatorio.")
        return
    description = input("Descripción: ").strip()
    tags = [t.strip() for t in input("Etiquetas separadas por comas: ").split(",") if t.strip()]
    privacy = validar_privacidad()
    body = {
        "snippet": {"title": title, "description": description, "tags": tags, "categoryId": CATEGORY_EDUCATION},
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(path, mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        progress, response = request.next_chunk(num_retries=3)
        if progress:
            print(f"Subiendo: {progress.progress() * 100:.1f}%")
    print("Subida completada.")
    print(f"ID: {response['id']}\nhttps://www.youtube.com/watch?v={response['id']}")


def obtener_video(youtube, video_id):
    items = youtube.videos().list(part="snippet,status", id=video_id).execute().get("items", [])
    return items[0] if items else None


def actualizar_metadatos(youtube):
    video_id = input("ID del video: ").strip()
    video = obtener_video(youtube, video_id)
    if not video:
        print("Video no encontrado o no accesible.")
        return
    old = video["snippet"]
    print(f'Título actual: {old.get("title", "")}')
    title = input("Nuevo título (Enter para conservar): ").strip()
    description = input("Nueva descripción (Enter para conservar): ").strip()
    tags_text = input("Nuevas etiquetas separadas por comas (Enter para conservar): ").strip()
    category = input(f'Categoría (Enter para conservar {old.get("categoryId", CATEGORY_EDUCATION)}): ').strip()
    snippet = {  # se reconstruye el snippet conservando los campos existentes / rebuilt keeping existing fields
        "title": title or old["title"],
        "categoryId": category or old.get("categoryId", CATEGORY_EDUCATION),
        "description": description or old.get("description", ""),
        "tags": [t.strip() for t in tags_text.split(",") if t.strip()] if tags_text else old.get("tags", []),
    }
    youtube.videos().update(part="snippet", body={"id": video_id, "snippet": snippet}).execute()
    print("Metadatos actualizados.")


def cambiar_privacidad(youtube):
    video_id = input("ID del video: ").strip()
    video = obtener_video(youtube, video_id)
    if not video:
        print("Video no encontrado o no accesible.")
        return
    print("Privacidad actual:", video.get("status", {}).get("privacyStatus"))
    privacy = validar_privacidad()
    status_body = dict(video["status"], privacyStatus=privacy)  # conserva embeddable y demás / keeps embeddable etc.
    youtube.videos().update(part="status", body={"id": video_id, "status": status_body}).execute()
    print(f"Privacidad actualizada a: {privacy}")


def eliminar_video(youtube):
    video_id = input("ID del video que deseas eliminar: ").strip()
    video = obtener_video(youtube, video_id)
    if not video:
        print("Video no encontrado o no accesible.")
        return
    print("Video:", video["snippet"]["title"])
    print("Esta acción es permanente.")
    if input("Escribe ELIMINAR para confirmar: ").strip() != "ELIMINAR":
        print("Operación cancelada.")
        return
    youtube.videos().delete(id=video_id).execute()
    print("Video eliminado.")


def menu():
    try:
        youtube = autenticar()
        print("Conectado a YouTube.")
        actions = {"1": listar_videos, "2": subir_video, "3": actualizar_metadatos,
                   "4": cambiar_privacidad, "5": eliminar_video}
        while True:
            print("""
========= YOUTUBE MANAGER =========
1. Listar videos del canal
2. Subir video
3. Actualizar título, descripción y etiquetas
4. Cambiar privacidad
5. Eliminar video
0. Salir
""")
            option = input("Selecciona una opción: ").strip()
            if option == "0":
                break
            if option not in actions:
                print("Opción no válida.")
                continue
            try:
                actions[option](youtube)
            except HttpError as error:
                print("Error de YouTube API:", error)
            except (OSError, ValueError) as error:
                print("Error:", error)
    except HttpError as error:
        print("Error de autenticación o API:", error)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawTextHelpFormatter)
    sub = parser.add_subparsers(dest="command")
    auth = sub.add_parser("auth", help="autoriza la cuenta y guarda token.json")
    pub = sub.add_parser("publish", help="sube los videos que falten y actualiza el manifiesto del sitio")
    pub.add_argument("--dry-run", action="store_true", help="muestra el plan sin subir ni autenticar")
    pub.add_argument("--only", help="temas separados por comas, p. ej. security,mlops-cicd")
    pub.add_argument("--lang", choices=["es", "en"])
    pub.add_argument("--limit", type=int, help="máximo de videos a subir en esta ejecución")
    pub.add_argument("--replace", action="store_true", help="sube la versión nueva de un video cambiado y borra la anterior")
    ver = sub.add_parser("verify", help="comprueba en YouTube privacidad e incrustación de los videos del manifiesto")
    for cmd in (auth, pub, ver):
        cmd.add_argument("--no-browser", action="store_true", help="imprime la URL de autorización en vez de abrir el navegador")
    sub.add_parser("status", help="compara los archivos locales con el manifiesto")
    desc = sub.add_parser("descriptions", help="actualiza la descripción de los videos ya publicados al formato actual")
    desc.add_argument("--dry-run", action="store_true", help="muestra las descripciones sin tocar YouTube")
    desc.add_argument("--only", help="temas separados por comas")
    desc.add_argument("--lang", choices=["es", "en"])
    desc.add_argument("--no-browser", action="store_true", help="imprime la URL de autorización en vez de abrir el navegador")
    args = parser.parse_args()

    if args.command == "auth":
        youtube = autenticar(not args.no_browser)
        channel = youtube.channels().list(part="snippet", mine=True).execute().get("items", [])
        print("Autorizado:", channel[0]["snippet"]["title"] if channel else "(sin canal)")
    elif args.command == "publish":
        publish(args)
    elif args.command == "verify":
        verify(args)
    elif args.command == "status":
        status(args)
    elif args.command == "descriptions":
        refresh_descriptions(args)
    else:
        menu()


if __name__ == "__main__":
    main()
