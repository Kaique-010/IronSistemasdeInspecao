"""
Treinamento do YOLOv8n para detecção de abacaxi e tomate.

Uso:
    python treinar.py [--epocas 40] [--tamanho 320]

Resultado salvo em: ia/runs/detect/abacaxi_tomate/weights/best.pt
"""

import argparse
import os
from pathlib import Path

from ultralytics import YOLO


RAIZ = Path(__file__).resolve().parent

DATASET = RAIZ / "datasets" / "abacaxi_tomate"


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--epocas", type=int, default=40)
    parser.add_argument("--tamanho", type=int, default=320)
    parser.add_argument("--batch", type=int, default=32)

    args = parser.parse_args()

    data = (DATASET / "data.yaml").as_posix()

    modelo = YOLO("yolov8n.pt")

    modelo.train(
        data=data,
        epochs=args.epocas,
        imgsz=args.tamanho,
        batch=args.batch,
        device="cpu",
        workers=0,
        project=(RAIZ / "runs").as_posix(),
        name="abacaxi_tomate",
        exist_ok=True,
    )

    print("Treinamento concluído!")


if __name__ == "__main__":
    main()
