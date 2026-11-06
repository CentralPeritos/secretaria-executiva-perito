---
description: Primeira configuração da Secretária (conectores, pasta do Drive, nome, teste)
---

Faça a configuração inicial desta Secretária Executiva, conversando com o perito em português, uma pergunta por vez.

1. Rode `python3 scripts/instalar.py` e mostre o resultado em linguagem simples (OCR faltando só importa para PDF escaneado).
2. Pergunte: nome completo do perito (para a assinatura), e-mail principal.
3. **Conectores.** Verifique quais ferramentas de Gmail e Google Drive você tem nesta sessão.
   - Se faltar o Gmail ou o Drive: explique como ligar em Configurações → Conectores (Gmail e Google Drive) e peça para autorizar. Pare aqui até estar ligado.
   - Teste de leitura segura: liste 1 thread do Gmail e pesquise 1 arquivo no Drive.
   - Teste o que cada conector **consegue fazer** e anote em `config/config.local.json` → `ferramentas`
     (`gmail_pode_criar_rascunho`, `gmail_pode_etiquetar`, `gmail_pode_baixar_anexo`, `drive_pode_criar_arquivo`,
     `drive_pode_mover`, `drive_pode_renomear` = true/false). Não envie e-mail nem apague nada para testar; para rascunho,
     crie um rascunho de teste com assunto "TESTE SECRETARIA" para o próprio perito e peça que o apague.
4. **Pasta dos casos.** Pergunte se o perito usa o aplicativo **Google Drive para computador** (pasta local sincronizada).
   - Sim → peça o caminho da pasta onde ficam os clientes (ex.: `~/Google Drive/Meu Drive/00 - CLIENTES`) e grave em `pasta_drive_local`. Confira que existe.
   - Não → explique que sem a pasta local o movimento de pastas e o salvamento de anexos ficam limitados (ver `docs/LIMITES.md`) e recomende instalar.
5. **Estrutura.** Se a pasta de clientes já tem estágios, mostre o que existe e pergunte se quer usar os nomes dele (ajuste `estagios`).
   Se está vazia, ofereça criar os 7 estágios padrão da Central, listando antes o que vai criar. Só crie após o "sim".
6. Mostre o resumo da configuração e como usar: `/ronda-email`, `/separar`, `/arquivar`, `/mover`, `/caso-novo`.
