#!/usr/bin/env python3
"""Validador e gerador do nome padrão de arquivo da Central de Peritos.

Padrão:  AAAA.MM.DD - XXX - NOME_CURTO.ext
  - XXX       = exatamente 3 letras maiúsculas (tipo do documento)
  - NOME_CURTO = poucas palavras, sem dados do cliente
  - nome inteiro (com extensão) <= 60 caracteres
  - caminho completo < 260 caracteres (limite do Windows)

Uso:
  python nome_padrao.py checar "2026.04.02 - PET - INICIAL.pdf"
  python nome_padrao.py gerar --tipo PET --nome "Inicial" --ext pdf [--data 2026.04.02]
"""
import argparse
import re
import sys
import unicodedata
from datetime import date

MAX_NOME = 60
MAX_CAMINHO = 259
PADRAO = re.compile(r"^(\d{4})\.(\d{2})\.(\d{2}) - ([A-Z]{3}) - (.+)\.([A-Za-z0-9]{2,5})$")

# Tipos usuais (3 letras). Outros são aceitos se tiverem 3 letras.
TIPOS = {
    "PET": "petição (inicial, emenda, manifestação)",
    "DEC": "decisão / despacho / liminar",
    "SEN": "sentença",
    "ACO": "acórdão",
    "AGR": "agravo",
    "CON": "contestação",
    "CTR": "contrato",
    "CED": "cédula / CCB",
    "EXT": "extrato / demonstrativo",
    "PRC": "procuração",
    "CER": "certidão",
    "LAU": "laudo",
    "PAR": "parecer",
    "IMP": "impugnação",
    "QUE": "quesitos",
    "CAL": "cálculo / planilha",
    "REC": "recibo",
    "NFS": "nota fiscal de serviço",
    "COM": "comprovante",
    "PRO": "proposta",
    "DOC": "documento diverso",
}

# Fragmentos que NÃO podem aparecer no NOME_CURTO
PROIBIDO = [
    (re.compile(r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}"), "CPF"),
    (re.compile(r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}"), "CNPJ"),
    (re.compile(r"\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}"), "número de processo (CNJ)"),
    (re.compile(r"\bvs?\.?\b", re.I), "'vs' (nome de parte)"),
]


def limpar(texto: str) -> str:
    """Maiúsculas, sem acento, sem caracteres inválidos em nome de arquivo."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r'[\\/:*?"<>|]', " ", t)
    return re.sub(r"\s+", " ", t).strip().upper()


def checar(nome: str, pasta: str = "") -> list[str]:
    erros = []
    m = PADRAO.match(nome)
    if not m:
        erros.append("fora do padrão 'AAAA.MM.DD - XXX - NOME_CURTO.ext'")
        return erros
    ano, mes, dia, tipo, curto, _ext = m.groups()
    try:
        date(int(ano), int(mes), int(dia))
    except ValueError:
        erros.append("data inválida")
    if len(nome) > MAX_NOME:
        erros.append(f"nome com {len(nome)} caracteres (máx. {MAX_NOME})")
    if pasta and len(pasta.rstrip("/\\")) + 1 + len(nome) > MAX_CAMINHO:
        erros.append(f"caminho completo passa de {MAX_CAMINHO} caracteres")
    for rx, rotulo in PROIBIDO:
        if rx.search(curto):
            erros.append(f"NOME_CURTO contém {rotulo}")
    return erros


def gerar(tipo: str, nome: str, ext: str, data: str | None = None) -> str:
    tipo = tipo.upper()
    if not re.fullmatch(r"[A-Z]{3}", tipo):
        raise SystemExit("tipo deve ter exatamente 3 letras")
    d = data or date.today().strftime("%Y.%m.%d")
    final = f"{d} - {tipo} - {limpar(nome)}.{ext.lower().lstrip('.')}"
    erros = checar(final)
    if erros:
        raise SystemExit("nome gerado reprovado: " + "; ".join(erros))
    return final


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("checar")
    c.add_argument("nome")
    c.add_argument("--pasta", default="")
    g = sub.add_parser("gerar")
    g.add_argument("--tipo", required=True)
    g.add_argument("--nome", required=True)
    g.add_argument("--ext", required=True)
    g.add_argument("--data")
    sub.add_parser("tipos")
    a = ap.parse_args()
    if a.cmd == "checar":
        erros = checar(a.nome, a.pasta)
        print("OK" if not erros else "REPROVADO: " + "; ".join(erros))
        return 0 if not erros else 1
    if a.cmd == "gerar":
        print(gerar(a.tipo, a.nome, a.ext, a.data))
        return 0
    for k, v in TIPOS.items():
        print(f"{k}  {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
