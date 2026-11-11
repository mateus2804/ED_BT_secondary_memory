# Árvore B — Implementação em Python

Implementação de uma **Árvore B** em Python, desenvolvida como trabalho prático da disciplina Estruturas de Dados e Introdução à Análise de Algoritmos (EDPAA).

O projeto utiliza armazenamento em arquivo binário para persistir os nós da árvore, implementando as principais operações de manipulação e manutenção da estrutura.

## Funcionalidades

- **Inserção:** inclusão de chaves e registros, com divisão de nós (*split*) e propagação de chaves promovidas.
- **Busca:** localização de chaves na árvore.
- **Remoção:** exclusão de chaves, com substituição pelo predecessor quando necessário.
- **Redistribuição:** transferência de chaves entre nós irmãos para corrigir situações de *underflow*.
- **Fusão:** combinação de nós quando a redistribuição não é possível.
- **Persistência binária:** armazenamento e recuperação dos nós em arquivo binário.
- **Impressão:** visualização da árvore por níveis.

## Organização do projeto

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada do programa e processamento das operações de entrada. |
| `BTree.py` | Implementação da estrutura da Árvore B e suas operações principais. |
| `Node.py` | Representação e manipulação dos nós da árvore. |
| `auxiliar.py` | Funções auxiliares de persistência, divisão, redistribuição e fusão. |

## Requisitos

- Python 3.
- Não são necessárias bibliotecas externas, considerando a implementação baseada nas bibliotecas padrão do Python.

## Execução

Execute o programa informando os arquivos de entrada e saída:

```bash
python main.py entrada.txt saida.txt
```

Substitua `entrada.txt` pelo arquivo contendo as operações a serem executadas e `saida.txt` pelo arquivo em que os resultados serão registrados.

## Armazenamento

Os nós são armazenados em arquivo binário, utilizando registros de tamanho fixo. Cada nó possui um identificador que permite calcular sua posição no arquivo, possibilitando operações de leitura e escrita diretamente nos respectivos offsets.

## Contexto acadêmico

Projeto desenvolvido para a disciplina **Estruturas de Dados e Introdução à Análise de Algoritmos — 2026/2**.

O trabalho aborda conceitos de árvores balanceadas, manipulação de arquivos binários, organização de estruturas de dados e análise de algoritmos.
