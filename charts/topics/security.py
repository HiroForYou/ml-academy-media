"""
Tema 4.3: seguridad. Topic 4.3: security.

    python charts/topics/security.py --lang es --out <dir>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    DPI, WIDTH_IN, arrow, box, cli, diagram_axes, fit_to, icon_node, place_icon, plt, save,
)

TEXT = {
    "es": {
        "pr_title": "iam:PassRole decide qué rol puede entregar el analista a SageMaker AI",
        "wide": "PassRole con Resource: \"*\"",
        "scoped": "PassRole limitado al ARN aprobado\n+ iam:PassedToService = sagemaker.amazonaws.com",
        "analyst": "Analista\nsagemaker:CreateTrainingJob",
        "admin": "AdminRole\nAdministratorAccess",
        "train": "sm-train-fraud\nrol de ejecución",
        "escalation": "escalada de privilegios",
        "denied": "AccessDenied",
        "perms": "s3:GetObject  fraud-data/train/*\ns3:PutObject  fraud-models/output/*\nkms:Decrypt  fraud-key",
        "job": "Trabajo de entrenamiento\ncon permisos de administrador",
        "pr_note": "Caso de ejemplo · el trabajo usa el rol de ejecución, no las credenciales de quien lo lanza",
        "net_title": "Entrenamiento sin internet: subredes privadas + VPC endpoints + aislamiento de red",
        "vpc": "VPC",
        "subnet": "Subred privada",
        "inst": "Instancia\nde entrenamiento",
        "sg": "Security group: entrada desde sí mismo (entrenamiento distribuido)",
        "route": "Tabla de rutas: sin NAT ni internet gateway",
        "gw": "S3 gateway endpoint\nendpoint policy:\nsolo buckets fraud-*",
        "s3": "Amazon S3\nfraud-data · fraud-models",
        "iface": "Interface endpoints\nPrivateLink, para clientes en la VPC",
        "svcs": "SageMaker API · SageMaker Runtime · bedrock-runtime",
        "internet": "Internet",
        "iso": "EnableNetworkIsolation = True\n\nEl contenedor no hace llamadas\nde red ni recibe credenciales.\n\n"
               "SageMaker AI descarga los datos\ny sube el modelo con el rol de\nejecución, fuera del contenedor.",
        "net_note": "Caso de ejemplo; diagrama simplificado",
        "kms_title": "Paso 3: el AccessDenied venía de la política de la clave, no de la política IAM",
        "req": "sm-train-fraud\nkms:Decrypt sobre fraud-key al leer los datos",
        "trail": "CloudTrail\nel evento muestra el rol, la acción y la clave",
        "both": "Para usar fraud-key, el rol necesita permiso en las dos políticas",
        "iam_pol": "Política IAM del rol\npermite kms:Decrypt y kms:GenerateDataKey sobre fraud-key",
        "key_pol": "Política de la clave fraud-key\nno habilitaba permisos IAM para sm-train-fraud",
        "denied": "AccessDenied",
        "fix_ok": "Corrección: añadir a la política de la clave una declaración solo para sm-train-fraud. "
                  "No se amplía nada más.",
        "fix_bad": "Atajo incorrecto: kms:* o Resource: \"*\". Elimina el error desactivando el control que lo detectó.",
        "kms_note": "Caso de ejemplo; diagrama simplificado",
        "enc_title": "Reposo con tu clave KMS, tránsito con TLS; entre nodos lo activas tú",
        "enc_lane_train": "Entrenamiento",
        "enc_lane_infer": "Inferencia",
        "enc_inst1": "Instancia 1\nvolumen ML",
        "enc_inst2": "Instancia 2\nvolumen ML",
        "enc_s3": "S3 de salida\nartefactos del modelo",
        "enc_app": "Aplicación\nllama a la API",
        "enc_endpoint": "Endpoint\nvolumen ML",
        "enc_vol_key": "VolumeKmsKeyId",
        "enc_out_key": "KmsKeyId en OutputDataConfig",
        "enc_ep_key": "KmsKeyId del endpoint",
        "enc_sse": "SSE-S3 (por defecto) → SSE-KMS → DSSE-KMS",
        "enc_inter": "EnableInterContainerTrafficEncryption\nUDP 500 + ESP 50",
        "enc_inter_note": "sin cifrar por defecto",
        "enc_tls": "TLS 1.2 (1.3 recomendado)",
        "enc_rest": "En reposo: clave KMS del cliente",
        "enc_transit": "En tránsito",
        "enc_note": "Simplificado; KMS no cifra el almacenamiento local de Nitro",
    },
    "en": {
        "pr_title": "iam:PassRole decides which role the analyst can hand to SageMaker AI",
        "wide": "PassRole with Resource: \"*\"",
        "scoped": "PassRole scoped to the approved ARN\n+ iam:PassedToService = sagemaker.amazonaws.com",
        "analyst": "Analyst\nsagemaker:CreateTrainingJob",
        "admin": "AdminRole\nAdministratorAccess",
        "train": "sm-train-fraud\nexecution role",
        "escalation": "privilege escalation",
        "denied": "AccessDenied",
        "perms": "s3:GetObject  fraud-data/train/*\ns3:PutObject  fraud-models/output/*\nkms:Decrypt  fraud-key",
        "job": "Training job\nwith administrator permissions",
        "pr_note": "Worked example · the job uses the execution role, not the launcher's credentials",
        "net_title": "Training with no internet: private subnets + VPC endpoints + network isolation",
        "vpc": "VPC",
        "subnet": "Private subnet",
        "inst": "Training\ninstance",
        "sg": "Security group: inbound from itself (distributed training)",
        "route": "Route table: no NAT or internet gateway",
        "gw": "S3 gateway endpoint\nendpoint policy:\nfraud-* buckets only",
        "s3": "Amazon S3\nfraud-data · fraud-models",
        "iface": "Interface endpoints\nPrivateLink, for clients in the VPC",
        "svcs": "SageMaker API · SageMaker Runtime · bedrock-runtime",
        "internet": "Internet",
        "iso": "EnableNetworkIsolation = True\n\nThe container makes no network\ncalls and gets no credentials.\n\n"
               "SageMaker AI downloads the data\nand uploads the model with the\nexecution role, outside the container.",
        "net_note": "Worked example; simplified diagram",
        "kms_title": "Step 3: the AccessDenied came from the key policy, not the IAM policy",
        "req": "sm-train-fraud\nkms:Decrypt on fraud-key while reading the data",
        "trail": "CloudTrail\nthe event shows the role, the action and the key",
        "both": "To use fraud-key, the role needs permission in both policies",
        "iam_pol": "Role's IAM policy\nallows kms:Decrypt and kms:GenerateDataKey on fraud-key",
        "key_pol": "fraud-key key policy\ndid not enable IAM permissions for sm-train-fraud",
        "denied": "AccessDenied",
        "fix_ok": "Fix: add a key policy statement for sm-train-fraud only. Nothing else is widened.",
        "fix_bad": "Wrong shortcut: kms:* or Resource: \"*\". It removes the error by disabling the control that caught it.",
        "kms_note": "Worked example; simplified diagram",
        "enc_title": "At rest with your KMS key, in transit with TLS; between nodes you turn it on",
        "enc_lane_train": "Training",
        "enc_lane_infer": "Inference",
        "enc_inst1": "Instance 1\nML volume",
        "enc_inst2": "Instance 2\nML volume",
        "enc_s3": "Output S3\nmodel artifacts",
        "enc_app": "Application\ncalls the API",
        "enc_endpoint": "Endpoint\nML volume",
        "enc_vol_key": "VolumeKmsKeyId",
        "enc_out_key": "KmsKeyId in OutputDataConfig",
        "enc_ep_key": "Endpoint KmsKeyId",
        "enc_sse": "SSE-S3 (default) → SSE-KMS → DSSE-KMS",
        "enc_inter": "EnableInterContainerTrafficEncryption\nUDP 500 + ESP 50",
        "enc_inter_note": "unencrypted by default",
        "enc_tls": "TLS 1.2 (1.3 recommended)",
        "enc_rest": "At rest: customer KMS key",
        "enc_transit": "In transit",
        "enc_note": "Simplified; KMS does not encrypt Nitro local storage",
    },
}


def _mark(ax, x, y, ok):
    ax.text(x, y, "✓" if ok else "✗", ha="center", va="center", fontsize=13, family="DejaVu Sans",
            color=OK if ok else ACCENT, zorder=6,
            bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=OK if ok else ACCENT, lw=1.2))


# ─── 1. PassRole amplio vs limitado / broad vs scoped PassRole ─────────────────
def chart_passrole_scope(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.9), dpi=DPI)
    # Ajustar antes de dibujar íconos: su proporción depende del tamaño de los ejes.
    # Adjust before drawing icons: their aspect depends on the axes size.
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.05)
    diagram_axes(ax, 16, 9.8)
    for x0, scoped in ((0.1, False), (8.1, True)):
        ax.add_patch(plt.Rectangle((x0, 0.55), 7.8, 8.15, fc="white", ec=RULE, lw=1))
        ax.text(x0 + 0.25, 8.25, t["scoped"] if scoped else t["wide"], fontsize=9, fontweight="bold",
                color=OK if scoped else ACCENT, va="top")
        icon_node(ax, x0 + 1.5, 5.55, 4.8, 1.2, "aws/user", t["analyst"], size=8.6, desc_size=7.4)
        icon_node(ax, x0 + 0.2, 2.75, 3.6, 1.2, "aws/iam-role", t["admin"], edge=ACCENT, fill="#fbeef0", size=8.4,
                  desc_size=7.2)
        icon_node(ax, x0 + 4.0, 2.75, 3.6, 1.2, "aws/iam-role", t["train"], edge=OK, fill="#eaf4ee", size=8.4,
                  desc_size=7.2)
        arrow(ax, (x0 + 3.3, 5.5), (x0 + 2.0, 4.0), color=ACCENT if not scoped else GRAY, lw=1.6)
        arrow(ax, (x0 + 4.5, 5.5), (x0 + 5.8, 4.0), color=OK, lw=1.6)
        _mark(ax, x0 + 2.65, 4.75, not scoped)
        _mark(ax, x0 + 5.15, 4.75, True)
        if scoped:
            ax.text(x0 + 2.0, 2.3, t["denied"], ha="center", fontsize=8.8, color=ACCENT, fontweight="bold",
                    va="top")
            ax.text(x0 + 5.8, 2.55, t["perms"].replace("  ", " "), ha="center", va="top", fontsize=6.8,
                    color=INK_SOFT, family="monospace", linespacing=1.5)
        else:
            ax.text(x0 + 2.2, 2.5, t["escalation"], ha="left", fontsize=8.8, color=ACCENT, fontweight="bold",
                    va="top")
            icon_node(ax, x0 + 0.2, 0.8, 5.0, 1.05, "aws/sagemaker-train", t["job"], edge=ACCENT, fill="white",
                      size=8, desc_size=7, desc_color=ACCENT)
            arrow(ax, (x0 + 2.0, 2.7), (x0 + 2.0, 1.9), color=ACCENT)
    ax.set_title(t["pr_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    fig.text(0.99, 0.01, t["pr_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "passrole-scope")


# ─── 2. Red privada / private network ──────────────────────────────────────────
def chart_private_network(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 5.4), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.04)
    diagram_axes(ax, 16, 10.8)
    # VPC
    ax.add_patch(plt.Rectangle((0.2, 2.2), 10.6, 7.9, fc="white", ec=INK_SOFT, lw=1.4))
    place_icon(ax, "aws/vpc", 0.75, 9.6, 0.75)
    ax.text(1.3, 9.6, t["vpc"], fontsize=10, fontweight="bold", color=INK, va="center")
    for i, x in enumerate((0.6, 5.6)):
        ax.add_patch(plt.Rectangle((x, 5.55), 4.8, 3.5, fc=SURFACE, ec=RULE, lw=1))
        ax.text(x + 0.2, 8.7, f"{t['subnet']} {i + 1}", fontsize=8.6, color=INK_SOFT, va="center")
        icon_node(ax, x + 0.75, 6.25, 3.3, 1.45, "aws/sagemaker-train", t["inst"], edge=INK_SOFT, fill="white",
                  size=8.4, title_lines=2)
    ax.add_patch(plt.Rectangle((1.1, 5.95), 9.3, 2.05, fill=False, ec=AMBER, lw=1.4, ls=(0, (4, 2))))
    arrow(ax, (4.7, 6.97), (6.3, 6.97), color=AMBER, style="<|-|>")
    # Debajo de las subredes: el texto cruza ambas. Below the subnets: the label spans both.
    ax.text(6.0, 5.15, t["sg"], ha="center", va="center", fontsize=7.6, color=INK_SOFT)
    ax.text(5.6, 4.55, t["route"], fontsize=8.2, color=ACCENT, va="center")

    # S3 gateway endpoint -> S3
    icon_node(ax, 0.6, 2.45, 4.4, 1.6, "aws/vpc-endpoints", t["gw"], edge=OK, fill="#eaf4ee", size=8.2,
              desc_size=7.4, desc_color=OK)
    icon_node(ax, 0.6, 0.15, 4.4, 1.35, "aws/s3", t["s3"], edge=OK, fill="white", size=8.6, desc_size=7.6)
    arrow(ax, (2.1, 2.4), (2.1, 1.55), color=OK, lw=1.6, style="<|-|>")
    arrow(ax, (2.3, 6.2), (2.1, 4.1), color=OK, lw=1.4)

    # Interface endpoints
    icon_node(ax, 5.6, 2.55, 5.0, 1.4, "aws/privatelink", t["iface"], edge=INK_SOFT, fill="white", size=8.2,
              desc_size=7.2)
    ax.text(8.1, 1.6, t["svcs"], ha="center", fontsize=7.8, color=INK_SOFT, va="center")
    arrow(ax, (8.1, 2.5), (8.1, 1.85), color=MUTED)

    # Internet tachado / Internet crossed out
    icon_node(ax, 12.2, 7.0, 3.3, 1.3, "aws/internet", t["internet"], edge=GRAY, fill="white", size=9.5,
              color=MUTED)
    arrow(ax, (10.9, 7.65), (12.1, 7.65), color=GRAY, lw=1.4)
    _mark(ax, 11.5, 7.65, False)

    # Aislamiento de red / network isolation
    ax.text(11.2, 5.6, t["iso"], fontsize=7.6, color=INK,
            va="top", linespacing=1.45,
            bbox=dict(boxstyle="round,pad=0.5", fc="#fff6e0", ec=AMBER, lw=1))
    ax.set_title(t["net_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    fig.text(0.99, 0.01, t["net_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "private-training-network")


# ─── 3. Diagnóstico del AccessDenied del ejemplo / the example's AccessDenied ──
def chart_key_policy_fix(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.7), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.05)
    diagram_axes(ax, 16, 9.4)
    icon_node(ax, 0.2, 6.2, 4.5, 1.6, "aws/sagemaker-train", t["req"], edge=INK_SOFT, fill="white", size=8.6,
              desc_size=7.6)
    icon_node(ax, 0.2, 3.7, 4.5, 1.6, "aws/cloudtrail", t["trail"], edge=RULE, fill=SURFACE, size=8.6,
              desc_size=7.6)

    ax.text(5.6, 8.55, t["both"], fontsize=8.6, color=INK_SOFT, va="center")
    icon_node(ax, 5.6, 6.2, 5.0, 1.6, "aws/iam-role", t["iam_pol"], edge=OK, fill="#eaf4ee", size=8.6,
              desc_size=7.6)
    icon_node(ax, 5.6, 3.7, 5.0, 1.6, "aws/kms", t["key_pol"], edge=ACCENT, fill="#fbeef0", size=8.6,
              desc_size=7.6)
    arrow(ax, (4.75, 7.0), (5.55, 7.0), color=INK_SOFT)
    arrow(ax, (4.75, 6.75), (5.55, 4.75), color=INK_SOFT)
    _mark(ax, 11.15, 7.0, True)
    _mark(ax, 11.15, 4.5, False)

    ax.text(13.6, 5.75, t["denied"], ha="center", va="center", fontsize=10.5, fontweight="bold", color="white",
            bbox=dict(boxstyle="round,pad=0.55", fc=ACCENT, ec=ACCENT))
    arrow(ax, (11.65, 4.5), (12.4, 5.4), color=ACCENT, lw=1.6)

    box(ax, 0.2, 0.75, 7.6, 1.4, t["fix_ok"], edge=OK, fill="#eaf4ee", size=8.8, color=INK)
    box(ax, 8.2, 0.75, 7.6, 1.4, t["fix_bad"], edge=ACCENT, fill="white", size=8.8, color=INK)
    _mark(ax, 0.5, 2.6, True)
    _mark(ax, 8.5, 2.6, False)

    ax.set_title(t["kms_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    fig.text(0.99, 0.01, t["kms_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "key-policy-fix")


# ─── 4. Mapa de cifrado / encryption map ────────────────────────────────────────
def chart_encryption_map(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 5.0), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.04)
    diagram_axes(ax, 16, 10)
    red, amber = ACCENT, AMBER

    def key_chip(x, y, w, text):
        # Caja de clave: ícono de KMS a la izquierda y el parámetro centrado en el resto.
        # Key chip: KMS icon on the left and the parameter centred in the rest.
        box(ax, x, y, w, 0.75, "", edge=red, fill="#fbeef0", lw=1.2)
        place_icon(ax, "aws/kms", x + 0.5, y + 0.375, 0.58)
        txt = ax.text(x + 1.0 + (w - 1.0) / 2, y + 0.375, text, ha="center", va="center", fontsize=8.2, color=INK,
                      fontweight="bold", zorder=5)
        fit_to(txt, w - 1.25)

    ax.text(0.2, 9.55, t["enc_lane_train"], fontsize=9.4, fontweight="bold", color=MUTED, va="center")
    icon_node(ax, 0.2, 6.9, 4.6, 1.5, "aws/sagemaker-train", t["enc_inst1"], edge=INK_SOFT, fill="white", size=8.8,
              desc_size=7.8)
    icon_node(ax, 6.0, 6.9, 4.6, 1.5, "aws/sagemaker-train", t["enc_inst2"], edge=INK_SOFT, fill="white", size=8.8,
              desc_size=7.8)
    icon_node(ax, 11.5, 6.9, 4.3, 1.5, "aws/s3", t["enc_s3"], edge=INK_SOFT, fill="white", size=8.8, desc_size=7.8)
    arrow(ax, (4.9, 7.65), (5.9, 7.65), color=amber, lw=2.0, style="<|-|>")
    arrow(ax, (10.7, 7.65), (11.4, 7.65), color=MUTED, lw=1.5)
    inter = ax.text(5.4, 9.25, t["enc_inter"], fontsize=7.8, color=INK, ha="center", va="center", linespacing=1.4,
                    bbox=dict(boxstyle="round,pad=0.4", fc="#fff6e0", ec=amber, lw=1))
    ax.text(5.4, 8.55, t["enc_inter_note"], fontsize=7.6, color=INK_SOFT, ha="center", va="center", style="italic")
    key_chip(0.2, 5.7, 10.4, t["enc_vol_key"])
    key_chip(11.5, 5.7, 4.3, t["enc_out_key"])
    ax.text(13.65, 5.2, t["enc_sse"], fontsize=7.6, color=INK_SOFT, ha="center", va="center")

    ax.text(0.2, 4.35, t["enc_lane_infer"], fontsize=9.4, fontweight="bold", color=MUTED, va="center")
    icon_node(ax, 0.2, 2.2, 4.0, 1.5, "aws/client", t["enc_app"], edge=INK_SOFT, fill="white", size=8.8,
              desc_size=7.8)
    icon_node(ax, 8.2, 2.2, 4.6, 1.5, "aws/sagemaker-model", t["enc_endpoint"], edge=INK_SOFT, fill="white",
              size=8.8, desc_size=7.8)
    arrow(ax, (4.3, 2.95), (8.1, 2.95), color=amber, lw=2.0)
    ax.text(6.2, 3.45, t["enc_tls"], fontsize=7.8, color=INK, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="#fff6e0", ec=amber, lw=1))
    key_chip(8.2, 1.2, 4.6, t["enc_ep_key"])

    ax.add_patch(plt.Rectangle((0.2, 0.18), 0.35, 0.35, fc="#fbeef0", ec=red, lw=1.2))
    ax.text(0.8, 0.36, t["enc_rest"], fontsize=7.8, color=INK_SOFT, va="center")
    ax.add_patch(plt.Rectangle((6.4, 0.18), 0.35, 0.35, fc="#fff6e0", ec=amber, lw=1.2))
    ax.text(7.0, 0.36, t["enc_transit"], fontsize=7.8, color=INK_SOFT, va="center")

    ax.set_title(t["enc_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    fig.text(0.99, 0.012, t["enc_note"], ha="right", fontsize=7.6, color=MUTED)
    save(fig, out, "encryption-map")


CHARTS = [chart_passrole_scope, chart_private_network, chart_key_policy_fix, chart_encryption_map]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
