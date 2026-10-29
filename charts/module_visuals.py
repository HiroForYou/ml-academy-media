"""Bilingual concept maps for MLA-C02 topics."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

COURSE = "aws-ml-engineer-associate"
INK = "#111114"
MUTED = "#64646e"
ACCENT = "#b3132b"
OK = "#1f7a4d"
SURFACE = "#f3f3f5"
RULE = "#d8d8de"

TOPICS = {
    "data-collection-storage": {
        "es": ("De evento a feature", ["Eventos", "Kinesis", "Amazon S3", "Feature Store"], "Flujo y almacenamiento para entrenamiento"),
        "en": ("From event to feature", ["Events", "Kinesis", "Amazon S3", "Feature Store"], "Streaming and storage for training"),
    },
    "data-transformation-features": {
        "es": ("Preprocesar sin fuga", ["Datos sin\nprocesar", "Dividir", "Ajustar con\nentrenamiento", "Aplicar a\nvalidación e inferencia"], "Aprende parámetros solo con entrenamiento"),
        "en": ("Preprocess without leakage", ["Raw data", "Split", "Fit on\ntraining", "Apply to validation\nand inference"], "Learn parameters from training data only"),
    },
    "modeling-approaches": {
        "es": ("Elegir enfoque de modelado", ["Datos\nestructurados", "ML\nsupervisado", "Documentos\ncambiantes", "RAG + FM"], "Alinea el enfoque con el tipo de dato y la tarea"),
        "en": ("Choose a modeling approach", ["Structured\ndata", "Supervised\nML", "Changing\ndocuments", "RAG + FM"], "Match the approach to the data and task"),
    },
    "training-customization": {
        "es": ("Entrenamiento y generalización", ["Datos de\nentrenamiento", "Entrenar", "Validar y\najustar", "Evaluar en\nprueba"], "Detecta overfitting antes de la evaluación final"),
        "en": ("Training and generalization", ["Training\ndata", "Train", "Validate and\ntune", "Evaluate on\ntest"], "Detect overfitting before final evaluation"),
    },
    "model-evaluation": {
        "es": ("De predicción a decisión", ["Etiquetas y\nbaseline", "Métricas", "Revisar\nsegmentos", "Decisión de\npromoción"], "Mide errores relevantes, no solo accuracy"),
        "en": ("From prediction to decision", ["Labels and\nbaseline", "Metrics", "Review\nsegments", "Promotion\ndecision"], "Measure relevant errors, not accuracy alone"),
    },
    "deployment-infrastructure": {
        "es": ("Elegir patrón de inferencia", ["Respuesta\ninmediata", "Endpoint\ntiempo real", "Solicitud\ngrande", "Inferencia\nasíncrona"], "Usa lotes cuando no se requiere respuesta interactiva"),
        "en": ("Choose an inference pattern", ["Immediate\nresponse", "Real-time\nendpoint", "Large\nrequest", "Async\ninference"], "Use batch when no interactive response is required"),
    },
    "resource-provisioning": {
        "es": ("Capacidad según demanda", ["Medir\ntráfico", "Definir\nmétrica", "Escalar\ncapacidad", "Verificar\ncuotas y latencia"], "Valida picos con pruebas de carga"),
        "en": ("Capacity follows demand", ["Measure\ntraffic", "Choose\nmetric", "Scale\ncapacity", "Check quotas\nand latency"], "Validate peaks with load tests"),
    },
    "mlops-cicd": {
        "es": ("Promoción controlada del modelo", ["Preparar y\nentrenar", "Evaluar\nbaseline", "Registrar\nversión", "Aprobar y\ndesplegar"], "Cada candidato debe superar controles verificables"),
        "en": ("Controlled model promotion", ["Prepare and\ntrain", "Evaluate\nbaseline", "Register\nversion", "Approve and\ndeploy"], "Every candidate must pass verifiable controls"),
    },
    "monitoring-inference": {
        "es": ("Observar y responder", ["Métricas del\nendpoint", "Comparar con\nbaseline", "Investigar\nderiva", "Validar con\netiquetas"], "La deriva inicia una investigación; no demuestra fallo"),
        "en": ("Observe and respond", ["Endpoint\nmetrics", "Compare with\nbaseline", "Investigate\ndrift", "Validate with\nlabels"], "Drift starts an investigation; it does not prove failure"),
    },
    "cost-performance": {
        "es": ("Optimizar con mediciones", ["Carga\nrepresentativa", "Medir costo\ny p95", "Comparar\nconfiguraciones", "Validar calidad\ny requisitos"], "Optimiza costo y latencia sin perder calidad"),
        "en": ("Optimize with measurements", ["Representative\nworkload", "Measure cost\nand p95", "Compare\nconfigurations", "Validate quality\nand objectives"], "Optimize cost and latency without losing quality"),
    },
    "security": {
        "es": ("Límites de acceso del trabajo", ["Identidad\nautorizada", "Rol IAM de\nejecución", "Acceso mínimo\na S3", "Cifrado y\nregistro"], "Permite solo acciones y recursos necesarios"),
        "en": ("Workload access boundaries", ["Authorized\nidentity", "IAM execution\nrole", "Least access\nto S3", "Encryption\nand logging"], "Allow only required actions and resources"),
    },
}


def render(topic: str, lang: str, out: Path) -> None:
    title, labels, footer = TOPICS[topic][lang]
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    ax.text(0.15, 4.95, title, fontsize=18, fontweight="bold", color=INK, va="center")
    ax.text(0.15, 0.38, footer, fontsize=10, color=MUTED, va="center")

    positions = [0.2, 3.15, 6.1, 9.05]
    colors = [SURFACE, SURFACE, "#fff7f7", "#f0f7f3"]
    strokes = [RULE, RULE, ACCENT, OK]
    for index, (x, label, fill, stroke) in enumerate(zip(positions, labels, colors, strokes)):
        box = FancyBboxPatch(
            (x, 2.05), 2.55, 1.32, boxstyle="round,pad=0.06,rounding_size=0.12",
            linewidth=1.6, edgecolor=stroke, facecolor=fill,
        )
        ax.add_patch(box)
        ax.text(x + 1.275, 2.71, label, ha="center", va="center", fontsize=11,
                fontweight="bold" if index >= 2 else "normal", color=INK)
        if index < len(positions) - 1:
            arrow = FancyArrowPatch(
                (x + 2.62, 2.71), (positions[index + 1] - 0.08, 2.71),
                arrowstyle="-|>", mutation_scale=13, linewidth=1.5, color=ACCENT,
            )
            ax.add_patch(arrow)
    fig.tight_layout(pad=0.4)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "concept-map.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", choices=TOPICS, required=True)
    parser.add_argument("--lang", choices=("es", "en"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    render(args.topic, args.lang, args.out)
    print(f"{args.topic} concept map ({args.lang}) -> {args.out}")


if __name__ == "__main__":
    main()
