# Limites reais (leia antes de se frustrar)

A Secretária trabalha com **o que os conectores do Claude permitem**. Os conectores mudam com o tempo;
o comando `/iniciar` testa e registra o que funciona na sua conta. Esta tabela mostra o que é esperado e o plano B.

| Tarefa | Ideal | Se o conector não permitir |
|---|---|---|
| Ler e-mail | conector Gmail | — (é o mínimo; sem isso nada funciona) |
| Responder cliente | **rascunho** na thread | texto pronto no chat para você copiar |
| Enviar e-mail | **nunca** — por regra, não por limitação | — |
| Etiquetar / arquivar | conector Gmail | lista no relatório com o que você deve arquivar |
| Baixar anexo | conector Gmail | o relatório diz qual e-mail/anexo; você baixa para a pasta do caso e pede `/arquivar` |
| Salvar arquivo na pasta do caso | pasta local do **Google Drive para computador** | conector do Drive; senão `.trabalho/para-subir/` com nome já correto |
| Mover / renomear pasta | pasta local do Google Drive para computador | conector do Drive; senão a Secretária diz exatamente o que mover |
| Separar PDF | scripts locais (`pypdf`) | — |
| PDF escaneado (imagem) | OCR (`ocrmypdf`) | sem OCR a Secretária **para** e avisa; não adivinha |
| Apagar | **nunca** | — |

## Por que a pasta local do Drive importa
Os conectores leem e criam arquivos, mas mover e renomear pastas e gravar PDFs grandes é muito mais confiável
pela pasta sincronizada do aplicativo **Google Drive para computador**. Recomendado instalar
(drive.google.com/drive/download) e deixar a pasta de clientes disponível offline.

## Fora de escopo (de propósito)
Nota fiscal, financeiro/cobrança, proposta e orçamento automáticos, cálculo pericial e laudo.
A Secretária prepara a casa para você trabalhar; a decisão e a assinatura são suas.

## Privacidade
Os e-mails e documentos lidos passam pelo Claude conforme a sua conta/plano. Dados de clientes ficam no **seu**
Gmail e Drive; este repositório não contém nem coleta nenhum dado seu (a configuração `config.local.json`
fica só no seu computador e não vai para o GitHub).
