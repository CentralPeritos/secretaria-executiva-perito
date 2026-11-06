#!/usr/bin/env python3
"""Teste ponta a ponta com PDF sintético (sem dados reais). Rode: python3 tests/test_basico.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from nome_padrao import checar, gerar  # noqa: E402

try:
    from reportlab.pdfgen import canvas
except ImportError:
    canvas = None


def py(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


def test_nomes():
    assert checar("2026.04.02 - PET - INICIAL.pdf") == []
    assert checar("2026.04.02 - PETICAO - INICIAL.pdf")  # tipo deve ter 3 letras
    assert checar("2026.04.02 - PET - JOAO SILVA vs BANCO X.pdf")
    assert checar("2026.04.02 - PET - 0001234-56.2026.8.16.0001.pdf")
    assert checar("2026.04.02 - PET - " + "A" * 60 + ".pdf")
    assert gerar("pet", "Contestação", "PDF", "2026.05.01") == "2026.05.01 - PET - CONTESTACAO.pdf"
    print("nomes OK")


def test_split():
    if canvas is None:
        print("split: pulado (reportlab ausente; só para o teste)")
        return
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        pdf = d / "autos.pdf"
        c = canvas.Canvas(str(pdf))
        paginas = [
            "EXCELENTISSIMO SENHOR DOUTOR JUIZ DE DIREITO - ACAO REVISIONAL",
            "continuacao da inicial, pedidos",
            "CONTESTACAO apresentada pelo reu",
            "continuacao da contestacao",
            "SENTENCA julgo procedente",
        ]
        for t in paginas:
            c.drawString(72, 700, t + " " + "texto " * 20)
            c.showPage()
        c.save()
        r = py(RAIZ / "scripts/split_pdf.py", "inspecionar", pdf, "--workdir", d / "w")
        assert '"precisa_ocr": false' in r.stdout, r.stdout + r.stderr
        r = py(RAIZ / "scripts/split_pdf.py", "sugerir", pdf)
        plano = json.loads(r.stdout)["plano_sugerido"]
        assert [p["tipo"] for p in plano] == ["PET", "CON", "SEN"], plano
        (d / "plano.json").write_text(json.dumps(plano))
        r = py(RAIZ / "scripts/split_pdf.py", "cortar", pdf, "--plano", d / "plano.json", "--data", "2026.11.06")
        assert r.returncode == 0, r.stdout + r.stderr
        nomes = sorted(p.name for p in d.glob("2026.*"))
        assert nomes == ["2026.11.06 - CON - CONTESTACAO.pdf", "2026.11.06 - PET - INICIAL.pdf", "2026.11.06 - SEN - SENTENCA.pdf"], nomes
        assert pdf.exists()
        # rodar de novo não sobrescreve
        r = py(RAIZ / "scripts/split_pdf.py", "cortar", pdf, "--plano", d / "plano.json", "--data", "2026.11.06")
        assert r.returncode == 1 and "já existe" in r.stdout
        print("split OK:", nomes)


if __name__ == "__main__":
    test_nomes()
    test_split()
    print("TUDO OK")
