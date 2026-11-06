---
name: pastas-e-movimentacao
description: Use para criar, achar, renomear ou mover pasta de caso entre estágios.
---

# Pastas de caso e movimentação entre estágios

## Estrutura
`<Drive>/<pasta_clientes>/<ESTÁGIO>/<AAAA.MM.DD - ATUACAO - CLIENTE vs CONTRAPARTE>/`
Estágios e nomes exatos: `config/config.local.json` → `estagios`. **Copie de lá**; não digite.
O nome da pasta é a chave do caso: errar um caractere cria um caso paralelo.

| Estágio (padrão da Central) | Significado |
|---|---|
| 00 - PARA ORÇAMENTO | pedido chegou, falta proposta |
| 01 - ORÇAMENTO ENVIADO | proposta enviada, aguardando resposta |
| 02 - EM EXECUÇÃO | contratado/pago, em produção |
| 03 - TRABALHO ENTREGUE | entregue e recebido |
| 04 - PROPOSTA RECUSADA | cliente recusou |
| 05 - TRABALHO ENTREGUE A RECEBER | entregue, falta receber |
| 06 - AVULSOS | sem caso formal |

Se o perito usar outros nomes de estágio, vale o que está na config dele.

## 1. Procurar antes de criar (obrigatório)
Busque, nesta ordem, em **todos** os estágios: (1) CPF/CNPJ na ficha `dados_cliente.md`; (2) número do contrato/cédula/processo;
(3) nome do cliente (ignore acento e maiúscula). Registre **qual critério provou** e o valor casado.
- Um candidato com prova → use essa pasta.
- Candidatos sem prova → `NAO_CONFIRMADO`, liste os caminhos completos e pergunte ao perito.
- Nenhum → pode criar, se o cliente real estiver identificado.

## 2. Criar pasta de caso
- Cliente real identificado (nome de quem contrata; **não** o advogado/escritório que indicou, nem o remetente técnico).
- Nome: `AAAA.MM.DD - ATUACAO - CLIENTE vs CONTRAPARTE` (data = abertura). Sem tipo de serviço e sem valor no nome.
- Estágio inicial: `00 - PARA ORÇAMENTO` (ou o que o perito indicar).
- Crie `dados_cliente.md` na raiz da pasta com `docs/modelo-dados_cliente.md`. Campos que você não tem ficam `NAO_CONFIRMADO`.
- Contratos/cédulas diferentes e independentes = pastas de caso diferentes, não subpastas.
- Cliente não identificado → **não cria**; salva em `<pasta_quarentena_nome>` e avisa.

## 3. Mover de estágio
- Mover só com o **fato** confirmado pelo perito (ex.: "proposta enviada" → 01; "cliente pagou/aceitou" → 02; "entreguei" → 03/05; "recusou" → 04).
  **Silêncio ou falta de resposta não move para 04.**
- Use a pasta local do Drive (mover a pasta inteira). Pelo conector só se `drive_pode_mover` for verdadeiro.
- Depois de mover, **releia**: a pasta existe no estágio novo, não existe mais no antigo, e o conteúdo veio inteiro.
- Atualize `etapa` e a data na `dados_cliente.md`.

## 4. Renomear
- Só renomeie pasta para corrigir padrão ou data com **prova documental** (mesmo contrato/CNJ). Semelhança de nome não basta.
- Nunca renomeie ou apague entrega vigente ou documento de cliente sem pedido do perito.

## 5. Duplicata ou pasta errada
Não apague. Renomeie para `_APAGAR - <motivo> - AAAA.MM.DD` e **avise o perito**, que decide a exclusão.

## Nunca
Criar estágio novo, gravar na raiz do Drive, criar pasta sem busca prévia, mover para recusado por silêncio, apagar.
