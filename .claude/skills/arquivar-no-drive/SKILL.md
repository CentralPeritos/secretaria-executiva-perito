---
name: arquivar-no-drive
description: Use para salvar anexo ou documento na pasta do caso, com nome padrão.
---

# Arquivar documento na pasta do caso

## Entrada
Um arquivo (anexo de e-mail, PDF que o perito entregou, arquivo já no Drive) e, se souber, o caso.

## Passo a passo
1. **Identifique o caso.** Pelo nome do cliente, CPF/CNPJ, número do contrato ou do processo.
   Procure a pasta nos estágios (`pastas-e-movimentacao`, "busca antes de criar").
   - Achou uma só → siga.
   - Achou duas plausíveis ou nenhuma prova → `NAO_CONFIRMADO`: lista os candidatos para o perito e **para**.
   - Cliente não existe ainda → peça confirmação para abrir o caso (ou, se vier de lead, `00 - PARA ORÇAMENTO`).
2. **Classifique o documento** e escolha as 3 letras (`python3 scripts/nome_padrao.py tipos`).
3. **Gere o nome:** `python3 scripts/nome_padrao.py gerar --tipo CED --nome "CCB" --ext pdf`
   (data = hoje). Se o nome já existe na pasta, **não sobrescreva**: ajuste o NOME_CURTO (ex.: `CCB 2`).
4. **Salve na raiz da pasta do caso** (sem subpasta). Caminhos possíveis, nesta ordem:
   - a. pasta local do Drive (`pasta_drive_local` na config) — escreva/mova o arquivo direto;
   - b. conector do Drive (criar arquivo na pasta do caso), se `drive_pode_criar_arquivo` for verdadeiro;
   - c. se nenhum for possível: salve em `.trabalho/para-subir/` com o nome final já correto e avise o perito para arrastar ao Drive.
   Anexo do Gmail que a ferramenta não consegue baixar: diga qual e-mail e qual anexo, e peça ao perito para baixar.
5. **Registre no `dados_cliente.md`** uma linha: data do recebimento, remetente, o que é, data de emissão do documento
   (essa vai na ficha, nunca no nome). Se o arquivo da ficha não existir, crie a partir de `docs/modelo-dados_cliente.md`.
6. **Releia:** liste a pasta e confirme nome, tamanho > 0 e local. Só então `CONCLUIDO`.

## Não faça
- Não renomeie nem mova arquivo que já estava no Drive sem o perito pedir.
- Não inclua nome de cliente, parte contrária, CPF/CNPJ ou nº de processo no nome do arquivo.
- Não salve na raiz do Drive nem crie subpastas por tipo.
- PDF com mais de um processo, ou peça que parece de outro cliente: não salve, avise o perito.
- PDF grande de processo inteiro: use `separar-processo` antes de arquivar as peças.
