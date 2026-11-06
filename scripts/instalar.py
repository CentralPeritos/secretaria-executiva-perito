#!/usr/bin/env python3
"""Prepara o computador para a Secretária Executiva do Perito.

Faz só o que é mecânico e seguro:
  - confere Python 3.9+
  - instala pypdf (para separar PDFs)
  - verifica se existe OCR (ocrmypdf/tesseract) e diz como instalar se faltar
  - cria config/config.local.json a partir do exemplo (se ainda não existir)
  - roda o teste de nomes

Uso:  python3 scripts/instalar.py [--pasta-drive "/caminho/Google Drive/Meus Casos"] [--nome "Dr. Fulano"]
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta-drive", help="pasta local do Google Drive onde ficam os casos")
    ap.add_argument("--nome", help="nome do perito (para assinar rascunhos)")
    a = ap.parse_args()

    if sys.version_info < (3, 9):
        print("ERRO: precisa de Python 3.9 ou mais novo.")
        return 1
    print(f"Python {sys.version.split()[0]} OK")

    try:
        import pypdf  # noqa: F401
        print("pypdf OK")
    except ImportError:
        print("Instalando pypdf...")
        rc = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-q", "pypdf"]).returncode
        if rc != 0:
            rc = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pypdf"]).returncode
        if rc != 0:
            print("ERRO ao instalar pypdf. Rode manualmente: python3 -m pip install pypdf")
            return 1
        print("pypdf instalado")

    if shutil.which("ocrmypdf"):
        print("OCR OK (ocrmypdf)")
    else:
        print("AVISO: OCR não instalado. Só é necessário para PDFs escaneados (imagem).")
        print("  macOS:   brew install ocrmypdf tesseract-lang")
        print("  Windows: use WSL ou peça ao agente para orientar (INSTALAR.md)")
        print("  Linux:   sudo apt install ocrmypdf tesseract-ocr-por")

    cfg = RAIZ / "config" / "config.local.json"
    if not cfg.exists():
        dados = json.loads((RAIZ / "config" / "config.exemplo.json").read_text(encoding="utf-8"))
        if a.pasta_drive:
            dados["pasta_drive_local"] = a.pasta_drive
        if a.nome:
            dados["perito_nome"] = a.nome
        cfg.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Criado {cfg.relative_to(RAIZ)}")
    else:
        print("config.local.json já existe (mantido)")

    rc = subprocess.run([sys.executable, str(RAIZ / "tests" / "test_basico.py")], capture_output=True, text=True)
    print("Teste:", "OK" if rc.returncode == 0 else "FALHOU\n" + rc.stdout + rc.stderr)
    return rc.returncode


if __name__ == "__main__":
    sys.exit(main())
