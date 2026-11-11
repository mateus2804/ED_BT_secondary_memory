# ============================================================
# Trabalho Prático T1 - Estruturas de Dados e PAA - 2026/2
# Nome: Mateus Ferreira Ferraz
# Matrícula: 2026230173
# ============================================================


import argparse
from BTree import BTree


parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument("output", type=str)
args = parser.parse_args()

with open(args.input, 'r') as file:
    ordem_arvore = int(file.readline())
    operacoes = int(file.readline())
    file_name = f'btree_{args.input.split('_')[2].split('.')[0]}.bin'
    arvore = BTree(ordem_arvore=ordem_arvore, bin_file=file_name)

    for i in range(operacoes):
        line = file.readline().strip().split(' ')
        operacao = line[0]
        chave = int(line[1].replace(',', ''))

        if operacao == 'I':
            valor = int(line[2])

            arvore.insert(chave, valor)

        elif operacao == 'R':
            arvore.remove(chave)

        else:
            search_status, _ = arvore.search(chave)
            with open(args.output, 'a') as f:
                if search_status:
                    f.write('O REGISTRO ESTA NA ARVORE!\n')
                else:
                    f.write('O REGISTRO NAO ESTA NA ARVORE!\n')

    arvore.print_tree(args.output)
