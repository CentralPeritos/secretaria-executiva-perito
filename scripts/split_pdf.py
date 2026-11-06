#!/usr/bin/env python3
"""Separa um PDF de processo (autos) em peças, no nome padrão da Central.

Fluxo (quem decide o que é cada peça é o agente, lendo o texto; o script faz o trabalho mecânico):

  1) inspecionar  -> diz se o PDF tem texto ou é imagem (precisa OCR) e grava texto por página
  2) ocr          -> (só se for imagem) gera cópia pesquisável usando ocrmypdf ou tesseract
  3) sugerir      -> procura, por palavras-chave no texto, onde cada peça parece começar
  4) cortar       -> corta o PDF conforme um plano JSON e salva os arquivos na MESMA pasta

Plano JSON (lista):
  [{"pagina_inicial": 1, "pagina_final": 12, "tipo": "PET", "nome": "MOV1 INICIAL"}, ...]

Regras (herdadas da Central):
  - a data do nome é a data de HOJE (criação do arquivo gerado no corte), não a data de emissão
  - o PDF original nunca é apagado nem alterado
  - tudo é salvo na mesma pasta do original; não cria subpasta
  - nome <= 60 caracteres, sem dados do cliente (veja nome_padrao.py)
  - página sem texto mesmo após OCR é reportada como pendência de legibilidade
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    sys.exit("Falta a biblioteca pypdf. Rode: python3 -m pip install --user pypdf")

sys.path.insert(0, str(Path(__file__).parent))
from nome_padrao import checar, gerar  # noqa: E402

# (tipo, nome curto, padrões que indicam o INÍCIO da peça — primeiras linhas da página)
ASSINATURAS = [
    ("PET", "INICIAL", r"EXCELENT[ÍI]SSIMO.{0,80}(JUIZ|JU[ÍI]ZO)|PETI[ÇC][ÃA]O INICIAL|A[ÇC][ÃA]O (REVISIONAL|DE|ORDIN)"),
    ("CON", "CONTESTACAO", r"CONTESTA[ÇC][ÃA]O|CONTESTA,? PELAS RAZ"),
    ("PET", "REPLICA", r"R[ÉE]PLICA [ÀA] CONTESTA|IMPUGNA[ÇC][ÃA]O [ÀA] CONTESTA"),
    ("SEN", "SENTENCA", r"\bSENTEN[ÇC]A\b|ISTO POSTO,? JULGO|DISPOSITIVO"),
    ("ACO", "ACORDAO", r"AC[ÓO]RD[ÃA]O|EMENTA:"),
    ("AGR", "AGRAVO", r"AGRAVO (DE INSTRUMENTO|INTERNO|REGIMENTAL)"),
    ("DEC", "DECISAO", r"\bDECIS[ÃA]O\b|\bDESPACHO\b|LIMINAR"),
    ("LAU", "LAUDO", r"LAUDO PERICIAL|LAUDO T[ÉE]CNICO"),
    ("PAR", "PARECER ASSISTENTE", r"PARECER (T[ÉE]CNICO|DO ASSISTENTE)"),
    ("IMP", "IMPUGNACAO LAUDO", r"IMPUGNA[ÇC][ÃA]O (AO|DO) LAUDO"),
    ("CED", "CEDULA", r"C[ÉE]DULA (DE )?CR[ÉE]DITO|C\.?C\.?B\.?\b|CONTRATO DE (EMPR[ÉE]STIMO|FINANCIAMENTO|ABERTURA)"),
    ("CTR", "CONTRATO", r"CONTRATO (DE|N[ºO°])|INSTRUMENTO PARTICULAR"),
    ("EXT", "EXTRATO", r"EXTRATO|DEMONSTRATIVO (DE|DO)"),
    ("PRC", "PROCURACAO", r"PROCURA[ÇC][ÃA]O"),
    ("CER", "CERTIDAO", r"CERTID[ÃA]O"),
    ("DEC", "NOMEACAO PERITO", r"NOMEIO.{0,40}PERITO|HONOR[ÁA]RIOS PERICIAIS"),
]


def _texto_paginas(reader: PdfReader) -> list[str]:
    out = []
    for p in reader.pages:
        try:
            out.append((p.extract_text() or "").strip())
        except Exception:
            out.append("")
    return out


def cmd_inspecionar(a) -> int:
    pdf = Path(a.pdf)
    r = PdfReader(str(pdf))
    textos = _texto_paginas(r)
    total = len(textos)
    com_texto = sum(1 for t in textos if len(t) > 40)
    destino = Path(a.saida or pdf.with_suffix(".paginas.json"))
    if a.saida is None:
        destino = Path(a.workdir) / (pdf.stem[:40] + ".paginas.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(
        [{"pagina": i + 1, "texto": t[:3000]} for i, t in enumerate(textos)], ensure_ascii=False), encoding="utf-8")
    pct = 100 * com_texto / total if total else 0
    print(json.dumps({
        "paginas": total, "paginas_com_texto": com_texto, "percentual_texto": round(pct, 1),
        "precisa_ocr": pct < 50, "texto_por_pagina": str(destino),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_ocr(a) -> int:
    pdf = Path(a.pdf)
    saida = Path(a.workdir) / (pdf.stem[:40] + ".ocr.pdf")
    saida.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("ocrmypdf"):
        cmd = ["ocrmypdf", "--skip-text", "-l", a.lang, "--optimize", "0", str(pdf), str(saida)]
        rc = subprocess.run(cmd).returncode
        if rc not in (0, 6):  # 6 = já tinha texto
            print("ocrmypdf falhou (código %s)" % rc, file=sys.stderr)
            return rc
        print(f"PDF pesquisável: {saida}")
        return 0
    sys.stderr.write(
        "OCR indisponível: instale 'ocrmypdf' (veja INSTALAR.md). "
        "Sem OCR a identificação das peças viraria adivinhação — pare e avise o perito.\n")
    return 2


def cmd_sugerir(a) -> int:
    r = PdfReader(a.pdf)
    textos = _texto_paginas(r)
    achados = []
    for i, t in enumerate(textos):
        topo = " ".join(t.split())[:400].upper()
        if not topo:
            continue
        for tipo, nome, rx in ASSINATURAS:
            if re.search(rx, topo):
                achados.append({"pagina_inicial": i + 1, "tipo": tipo, "nome": nome, "evidencia": topo[:120]})
                break
    # páginas seguidas com a mesma peça são continuação, não peça nova
    unidos = []
    for ach in achados:
        if unidos and (unidos[-1]["tipo"], unidos[-1]["nome"]) == (ach["tipo"], ach["nome"]):
            continue
        unidos.append(ach)
    achados = unidos
    # fecha as faixas: cada peça vai até a página anterior à próxima
    total = len(textos)
    plano = []
    for k, ach in enumerate(achados):
        fim = achados[k + 1]["pagina_inicial"] - 1 if k + 1 < len(achados) else total
        plano.append({**ach, "pagina_final": fim})
    sem_texto = [i + 1 for i, t in enumerate(textos) if len(t) <= 40]
    print(json.dumps({"plano_sugerido": plano, "paginas_sem_texto": sem_texto,
                      "aviso": "Sugestão por palavras-chave. O agente DEVE conferir lendo o texto de cada início."},
                     ensure_ascii=False, indent=2))
    return 0


def cmd_cortar(a) -> int:
    pdf = Path(a.pdf)
    plano = json.loads(Path(a.plano).read_text(encoding="utf-8"))
    r = PdfReader(str(pdf))
    total = len(r.pages)
    textos = _texto_paginas(r)
    pasta = pdf.parent
    feitos, ilegiveis, erros = [], [], []
    for item in plano:
        ini, fim = int(item["pagina_inicial"]), int(item["pagina_final"])
        if not (1 <= ini <= fim <= total):
            erros.append(f"faixa inválida {ini}-{fim} (PDF tem {total} páginas)")
            continue
        nome = gerar(item["tipo"], item["nome"], "pdf", a.data)
        destino = pasta / nome
        problemas = checar(nome, str(pasta))
        if problemas:
            erros.append(f"{nome}: {'; '.join(problemas)}")
            continue
        if destino.exists():
            erros.append(f"{nome}: já existe (não sobrescrevo) — ajuste o nome no plano")
            continue
        w = PdfWriter()
        for p in range(ini - 1, fim):
            w.add_page(r.pages[p])
        if not a.simular:
            with open(destino, "wb") as fh:
                w.write(fh)
        feitos.append({"arquivo": nome, "paginas": f"{ini}-{fim}"})
        vazias = [p + 1 for p in range(ini - 1, fim) if len(textos[p]) <= 40]
        if vazias:
            ilegiveis.append({"arquivo": nome, "paginas_sem_texto": vazias})
    cobertas = set()
    for item in plano:
        cobertas.update(range(int(item["pagina_inicial"]), int(item["pagina_final"]) + 1))
    nao_cobertas = [p for p in range(1, total + 1) if p not in cobertas]
    print(json.dumps({"salvos": feitos, "paginas_nao_cobertas_pelo_plano": nao_cobertas, "pendencias_legibilidade": ilegiveis, "erros": erros,
                      "original_preservado": str(pdf), "simulacao": a.simular}, ensure_ascii=False, indent=2))
    return 1 if erros else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nome, fn in (("inspecionar", cmd_inspecionar), ("ocr", cmd_ocr), ("sugerir", cmd_sugerir), ("cortar", cmd_cortar)):
        s = sub.add_parser(nome)
        s.add_argument("pdf")
        s.set_defaults(fn=fn)
        if nome in ("inspecionar", "ocr"):
            s.add_argument("--workdir", default=".trabalho")
        if nome == "inspecionar":
            s.add_argument("--saida")
        if nome == "ocr":
            s.add_argument("--lang", default="por")
        if nome == "cortar":
            s.add_argument("--plano", required=True)
            s.add_argument("--data", help="AAAA.MM.DD (padrão: hoje)")
            s.add_argument("--simular", action="store_true")
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
