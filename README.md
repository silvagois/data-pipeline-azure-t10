
## Projeto data-pipeline-azure-t10

- Criação de um pipeline na Azure onde extraia dados de nota fiscal xml de um container/bucket e faça transformações e implementações nas zonas corretas do Data Lake

## ARQUITETURA

- A infra básica foi feita via Terraform, onde foi criado o resource group, storage account, e os containers landing, raw, processing e curated.
- Landing: Seria uma zona transitoria, onde o Data Factory por exemplo fazia a ingestão de um arquivo xml nessa camada, seria feito algumas validações de catalogação de dados e governança, onde esse dado fosse aprovado, iria ser enviado para a camada raw
- Raw: Dado bruto disponível para tratamento ou alguma validação de destes dados
- Processing: Dados tratados ja com dtypes definidos e processos de data quatily
- Curated: Dados processados e enriquecidos com alguma regra de negócio

## OBJETIVO:

- A principio eu ia criar esse pipeline usando azure databricks, porém tive problemas de criação do cluster , por conta da minha , account ser free.
- Mudei a ideia para implementar todo o pipe usando Azure Functions, porém não consegui finalizar o processo, esta incompleto.

- Estou enviando  código caso queiram ainda, analisar o codigo, onde criei as functions no arquivo ultils.py e chamei essas funções no arquivo main.py


# Resultados obtidos:
- Consegui logar na azure via python, coletar um arquivo xml que coloquei no bucket raw, fiz alguns tratamentos de dados para gerar um data frame e salvar na camada processing em formato parquet particionado por year, month e day, porém ao salvar apresentou um erro de "TypeError: quote_from_bytes() expected bytes " Ate o presente momento não consegui resolver esse erro.
- Não consegui fazer os try except no codigo e documentar as funções, mas a ideia era fazer as funções com as exceções e tratamentos de possiveis erros.

- Diretorio context e arquivo transform-info.json, é um arquivo para poder inserir dados que podem ser reaproveitados no codigo, assim facilita a replicação do codigo
- Diretorio notebook, foi onde fiz os testes
- Arquivo Workflow no diretorio .github, era para implementar a automatização do deploy da infra terraform, porém apresentou alguns erros de autenticação com a azure.

