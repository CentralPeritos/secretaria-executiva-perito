# Secretária Executiva do Perito

Agente para o **Claude Code** que faz o trabalho operacional de secretária de um perito, no padrão de
organização da Central de Peritos Associados (mentoria Águias One).

## O que ela faz

| Frente | O que acontece |
|---|---|
| **E-mail** | Ronda na caixa: separa spam/promoção, documentos de cliente, pedidos de resposta e o que precisa de você. Etiqueta, arquiva o ruído e **prepara rascunhos** para você conferir. |
| **Salvar no Drive** | Anexos de cliente vão para a pasta do caso, com nome padrão e linha na ficha `dados_cliente.md`. |
| **Separar processo** | PDF gigante de autos vira um PDF por peça (inicial, contestação, sentença, contrato...), com OCR se for escaneado. |
| **Pastas** | Abre pasta de caso (sem duplicar), move entre os estágios do pipeline, renomeia no padrão. |

Nome padrão de arquivo: `AAAA.MM.DD - XXX - NOME_CURTO.ext` (ex.: `2026.04.02 - PET - MOV1 INICIAL.pdf`).

## O que ela NÃO faz (de propósito)
Não envia e-mail (só rascunho), não apaga nada, não emite nota fiscal, não mexe em financeiro, não gera proposta,
não faz cálculo nem laudo. Detalhes e planos B em [docs/LIMITES.md](docs/LIMITES.md).

## Instalação (1 passo)
Você só precisa do **Claude Code** (app do Claude → aba **Code**) e de uma conta Google.

1. Copie o comando de instalação que a mentoria forneceu (arquivo `COMANDO-INSTALAR` na pasta de treinamentos) e cole no Claude Code.
2. Autorize os conectores **Gmail** e **Google Drive** quando ele pedir.
3. Abra o Claude Code na pasta `Secretaria-Perito` e digite `/iniciar`.

O comando é este (também em [COMANDO-INSTALAR.txt](COMANDO-INSTALAR.txt)):

```
Instale a Secretária Executiva do Perito. Execute: git clone https://github.com/CentralPeritos/secretaria-executiva-perito.git ~/Secretaria-Perito (se a pasta já existir, rode git -C ~/Secretaria-Perito pull --ff-only). Depois leia ~/Secretaria-Perito/INSTALAR.md e siga cada passo, explicando em português simples e pedindo minha confirmação antes de instalar qualquer programa. Não peça senhas: para Gmail e Google Drive apenas me oriente a ligar os conectores.
```

## Como usar no dia a dia
Abra o Claude Code na pasta `Secretaria-Perito` e use:

| Comando | Para quê |
|---|---|
| `/iniciar` | primeira configuração (testa conectores, define a pasta do Drive) |
| `/ronda-email [período]` | triagem da caixa de entrada + rascunhos |
| `/separar <arquivo.pdf>` | fatiar autos em peças |
| `/arquivar <o que e para qual caso>` | salvar documento no caso |
| `/caso-novo <dados>` | abrir pasta de caso novo |
| `/mover <caso> para <estágio>` | mudar de estágio |

Também dá para conversar normalmente: "veja meus e-mails de hoje", "separa o processo do João que chegou agora".

## Estrutura do repositório
```
CLAUDE.md                  # identidade e regras da Secretária
INSTALAR.md                # roteiro de instalação lido pelo Claude Code
COMANDO-INSTALAR.txt       # o comando para colar
.claude/skills/            # as 5 competências (e-mail, arquivar, separar, pastas, rascunho)
.claude/commands/          # atalhos /iniciar /ronda-email /separar ...
scripts/                   # nome_padrao.py, split_pdf.py, instalar.py
config/config.exemplo.json # modelo; a sua cópia (config.local.json) não vai ao GitHub
docs/                      # limites reais e modelo da ficha do caso
tests/test_basico.py       # teste de nomes e do separador de PDF
```

## Segurança e privacidade
- Nada do seu Gmail/Drive é enviado para este repositório; sua configuração fica só no seu computador.
- O agente nunca envia, nunca apaga e trata instrução dentro de e-mail/PDF como dado, não como ordem.
- Confira sempre os rascunhos antes de enviar: a responsabilidade pela comunicação é do perito.

## Atualizar
Cole o mesmo comando de instalação de novo: ele faz `git pull` e preserva a sua configuração.

## Licença
Uso educacional pelos alunos da mentoria Águias One. © Central de Peritos Associados.
