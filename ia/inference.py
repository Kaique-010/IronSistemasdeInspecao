"""
Inferência de detecção de objetos com YOLO.

Uso:
    python inference.py --imagem <caminho> [--modelo <peso>] [--saida <caminho>] [--conf 0.25]

Imprime um JSON com as detecções e salva a imagem anotada quando --saida é informado.
"""

import argparse
import json
import os

TRADUCAO = {
    "pineapple": "Abacaxi",
    "tomato": "Tomate",
    "person": "Pessoa",
}


def carregar_modelo(peso):
    from ultralytics import YOLO

    return YOLO(peso)


def inferir(peso, imagem, saida, conf=0.25):

    modelo = carregar_modelo(peso)

    resultados = modelo.predict(
        imagem,
        conf=conf,
        verbose=False,
    )

    detecoes = []

    for res in resultados:

        nomes = res.names

        for box in res.boxes:

            cls_id = int(box.cls[0])
            nome_original = nomes[cls_id]

            detecoes.append({
                "nome": TRADUCAO.get(nome_original, nome_original),
                "classe": cls_id,
                "confianca": round(float(box.conf[0]), 4),
                "caixa": [round(float(v), 1) for v in box.xyxy[0].tolist()],
            })

    if saida:

        os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)

        resultados[0].save(saida)

    return {
        "imagem": saida,
        "modelo": peso,
        "total": len(detecoes),
        "detecoes": detecoes,
    }


def main():

    parser = argparse.ArgumentParser(description="Detecção YOLO")

    parser.add_argument("--imagem", required=True)
    parser.add_argument("--modelo", default="yolov8n.pt")
    parser.add_argument("--saida", default=None)
    parser.add_argument("--conf", type=float, default=0.25)

    args = parser.parse_args()

    resultado = inferir(
        args.modelo,
        args.imagem,
        args.saida,
        args.conf,
    )

    print(json.dumps(resultado, ensure_ascii=False))


if __name__ == "__main__":
    main()
