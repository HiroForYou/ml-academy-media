"""
Tema 1.3: los gráficos viven en charts/make_charts.py; este módulo solo los expone al descubrimiento.
Topic 1.3: the charts live in charts/make_charts.py; this module only exposes them to discovery.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from make_charts import CHARTS, TEXT  # noqa: E402,F401
from style import cli  # noqa: E402

if __name__ == "__main__":
    cli(TEXT, CHARTS)
