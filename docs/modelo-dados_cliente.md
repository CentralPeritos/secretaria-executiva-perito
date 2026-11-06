# Modelo de `dados_cliente.md` (ficha do caso)

Fica na raiz de cada pasta de caso. Campo sem informação = `NAO_CONFIRMADO`. Nunca preencha por suposição.

```markdown
---
cliente: NOME DE QUEM CONTRATA
cpf_cnpj: NAO_CONFIRMADO
telefone: NAO_CONFIRMADO
email: NAO_CONFIRMADO
atuacao: ATE            # ATE, ATJ, PERITO...
contraparte: NOME DA PARTE CONTRÁRIA / BANCO
advogado: NAO_CONFIRMADO
numero_processo: NAO_CONFIRMADO
contratos:               # um por pasta de caso
  - numero: NAO_CONFIRMADO
    tipo: NAO_CONFIRMADO
etapa: 00 - PARA ORÇAMENTO
datas:
  abertura: AAAA-MM-DD   # igual à data do nome da pasta
---

# Histórico

| Data recebimento | Origem | O que é | Emissão do documento | Arquivo |
|---|---|---|---|---|
| AAAA-MM-DD | e-mail de fulano | contrato | AAAA-MM-DD | 2026.11.06 - CTR - CONTRATO.pdf |

# Pendências
- 
```
