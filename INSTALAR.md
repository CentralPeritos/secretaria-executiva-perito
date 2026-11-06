# Instalação (feita pelo próprio Claude Code)

> Este arquivo é lido pelo Claude Code quando você cola o comando de instalação. Execute cada passo,
> confirmando o resultado antes do próximo. Fale com o perito em português simples, sem jargão.

## 1. Pasta de instalação
- Pasta: `~/Secretaria-Perito` (Windows: `%USERPROFILE%\Secretaria-Perito`).
- Se não existir: `git clone https://github.com/CentralPeritos/secretaria-executiva-perito.git ~/Secretaria-Perito`
- Se existir: `git -C ~/Secretaria-Perito pull --ff-only` (atualização). **Não apague nada**; a `config/config.local.json` é do perito.
- Se `git` não existir: explique como instalar (git-scm.com) ou baixe o ZIP do repositório e descompacte na pasta.

## 2. Preparar o computador
Rode `python3 scripts/instalar.py` dentro da pasta (no Windows, `python` ou `py -3`).
- Instala `pypdf` (separar PDFs).
- Avisa se falta OCR (só necessário para PDF escaneado). Ofereça instalar se o perito quiser; peça confirmação antes de instalar programas.
- Se falhar, leia a mensagem, corrija a causa e repita só aquele passo.

## 3. Conectar Gmail e Google Drive
O perito precisa autorizar os **conectores** (uma vez, no navegador): Configurações → Conectores → Gmail e Google Drive → Conectar.
Você não pede senha nem token; só orienta e espera a autorização.

## 4. Abrir a Secretária
Diga ao perito, literalmente:
> "Pronto! Agora abra o Claude Code **nesta pasta**: `~/Secretaria-Perito` (no app: Code → selecionar pasta). Depois digite `/iniciar`."

Em seguida, se o perito já estiver na pasta, rode o fluxo de `.claude/commands/iniciar.md`.

## 5. Verificação
- `python3 tests/test_basico.py` termina com `TUDO OK`.
- `config/config.local.json` existe.
- Skills visíveis em `.claude/skills/` (5 pastas).
Só diga que a instalação terminou depois de conferir os três.
