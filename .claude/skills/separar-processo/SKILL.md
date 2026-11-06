---
name: separar-processo
description: Use para fatiar PDF grande de processo em peças com nome padrão.
---

# Separar processo (autos) em peças

Chegou um PDF monolítico com centenas de páginas. O perito precisa da inicial, contestação, sentença,
contrato etc. como arquivos separados. **Separar é só isso**: não resume o caso, não manda e-mail,
não cria pasta nova.

## Passo a passo (use os scripts, não improvise)

1. **Local do PDF.** Trabalhe com uma cópia local do arquivo se ele estiver só no Drive online.
   O resultado é salvo **na mesma pasta do original**. O original **nunca** é apagado ou alterado.
2. **Inspecionar:**
   `python3 scripts/split_pdf.py inspecionar "<arquivo.pdf>" --workdir .trabalho`
   - `precisa_ocr: true` → o PDF é imagem. Rode `python3 scripts/split_pdf.py ocr "<arquivo.pdf>" --workdir .trabalho`
     e use o `.ocr.pdf` gerado **só para ler o texto**. Se o OCR não estiver instalado: **pare** e avise
     (ver `INSTALAR.md`). Sem OCR a identificação das peças vira adivinhação.
3. **Sugerir:** `python3 scripts/split_pdf.py sugerir "<arquivo.pdf>"` devolve um plano por palavras-chave.
   É só um ponto de partida.
4. **Conferir lendo.** Abra o `.paginas.json` e leia o texto do início de cada peça sugerida e das páginas
   que ficaram de fora (`paginas_nao_cobertas_pelo_plano`). Identifique a peça **pelo texto**, nunca pela
   posição. Autos vêm fora de ordem e com páginas repetidas. Ajuste o plano.
   Peças que interessam: inicial e emendas, contestação/reconvenção, contrato/cédula/aditivos, extratos e
   demonstrativos, laudo e parecer de assistente, impugnação, sentença/acórdão/decisão de liquidação,
   cálculos das partes, despacho que nomeia perito ou fixa honorários.
5. **Gravar o plano** em `.trabalho/plano.json`:
   `[{"pagina_inicial":1,"pagina_final":12,"tipo":"PET","nome":"MOV1 INICIAL"}, ...]`
   Use `MOV<n>` no nome quando o processo eletrônico indicar o movimento. Nome curto, sem dados de parte.
6. **Simular e cortar:**
   `python3 scripts/split_pdf.py cortar "<arquivo.pdf>" --plano .trabalho/plano.json --simular` e depois sem `--simular`.
   O script recusa nome fora do padrão e **não sobrescreve** arquivo existente.
7. **Fechar:** liste a pasta e confira os arquivos criados. Entregue ao perito:
   peças extraídas (arquivo ↔ páginas), páginas **não identificadas** e **páginas ilegíveis** (pendência de legibilidade,
   para ele decidir se pede cópia melhor). Pendência nunca fica em silêncio.

## Pare e avise o perito quando
- o PDF tem mais de um processo, ou uma peça parece de outro cliente (não salve nada);
- o PDF é imagem e não há OCR;
- página ilegível mesmo após OCR (salve a peça mesmo assim e reporte as páginas).

## Nome
`AAAA.MM.DD - XXX - NOME_CURTO.pdf`, data = hoje (data da criação do arquivo gerado), máx. 60 caracteres.
Exemplos: `2026.04.02 - PET - MOV1 INICIAL.pdf`, `2026.05.06 - DEC - LIMINAR.pdf`, `2026.06.22 - ACO - AI.pdf`.
