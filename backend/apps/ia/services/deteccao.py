import json
import subprocess
import time
from pathlib import Path

from django.conf import settings


def resolver_caminho_modelo(modelo):

    caminho = Path(modelo)

    if not caminho.is_absolute():
        caminho = Path(settings.IA_DIR) / caminho

    return caminho


def executar_deteccao(imagem, modelo, saida, conf=0.25):

    python = settings.IA_PYTHON
    script = Path(settings.IA_DIR) / "inference.py"

    if not Path(python).exists():
        return {
            "erro": (
                "Python da IA não encontrado. "
                f"Rode o backend na máquina host (não no container) e confira IA_PYTHON: {python}"
            )
        }

    comando = [
        python,
        str(script),
        "--imagem", str(imagem),
        "--modelo", str(modelo),
        "--saida", str(saida),
        "--conf", str(conf),
    ]

    inicio = time.time()

    try:
        processo = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return {"erro": "Tempo limite excedido na inferência."}

    tempo = round(time.time() - inicio, 2)

    if processo.returncode != 0:
        return {
            "erro": (
                processo.stderr.strip()
                or processo.stdout.strip()
                or "Falha ao executar a inferência."
            )
        }

    try:
        dados = json.loads(processo.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {
            "erro": "Resposta inválida do script de inferência.",
            "saida": processo.stdout[-1000:],
        }

    dados["tempo"] = tempo

    return dados
