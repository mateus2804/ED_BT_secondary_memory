import argparse
from models import Node
import os

parser = argparse.ArgumentParser()

parser.add_argument("input", type=str)
parser.add_argument("output", type=str)
args = parser.parse_args()

with open(args.input, 'r') as file:
    arvore_ordem = int(file.readline())
    operacoes = int(file.readline())
    node_id = 0

    for i in range(operacoes):
        line = file.readline().strip().split(' ')
        operacao = line[0]

        if operacao == 'I':
            pass

def search_value(target, bin_file, ordem_arvore=3):
    node_layout = Node(-1, ordem_arvore)
    tam_node = node_layout.tamanho
    with open(bin_file, "rb") as f:
        node = node_layout.from_bytes(f.read(tam_node))

        while node.is_folha == False:
            next_node_id = node.search_keys(target)
            offset = next_node_id * tam_node
            f.seek(offset)
            node = node_layout.from_bytes(f.read(tam_node))

        search_result = node.search_keys(target)
        print(search_result)


search_value(25, 'teste.bin')



# def gerar_arvore_teste(bin_file):
#     ordem = 3

#     raiz = Node(
#         node_id=0,
#         ordem=ordem,
#         is_folha=False,
#         pai=-1,
#         chaves=[20],
#         registros=[200],
#         filhos=[1, 2, -1]
#     )

#     folha_esquerda = Node(
#         node_id=1,
#         ordem=ordem,
#         is_folha=True,
#         pai=0,
#         chaves=[10, 15],
#         registros=[100, 150],
#         filhos=[-1, -1, -1]
#     )

#     folha_direita = Node(
#         node_id=2,
#         ordem=ordem,
#         is_folha=True,
#         pai=0,
#         chaves=[25, 30],
#         registros=[250, 300],
#         filhos=[-1, -1, -1]
#     )

#     # Grava os nós em ordem de ID.
#     with open(bin_file, "wb") as f:
#         for node in [raiz, folha_esquerda, folha_direita]:
#             f.write(node.to_bytes())

# gerar_arvore_teste('teste.bin')
