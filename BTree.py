# ============================================================
# Trabalho Prático T1 - Estruturas de Dados e PAA - 2026/2
# Nome: Mateus Ferreira Ferraz
# Matrícula: 2026230173
# ============================================================

from Node import Node
import os
from auxiliar import get_node, write_node, split_node, insert_promoted, get_node_data, get_predecessor, min_keys, set_node_data, fix_underflow, handle_root_underflow


class BTree():
    def __init__(self, ordem_arvore, bin_file):
        self.ordem_arvore = ordem_arvore
        self.bin_file = bin_file


    def search(self, target):
        node_layout = Node(-1, self.ordem_arvore)
        tam_node = node_layout.tamanho

        with open(self.bin_file, "rb") as f:
            node = node_layout.from_bytes(f.read(tam_node))

            # faz a busca decendo nos filhos até achar a chave
            search_output = False
            while search_output == False:
                search_output, next_node_id = node.search_keys(target)

                # se o loop não parou e o nó é folha, pode parar a busca
                if node.is_folha:
                    break

                offset = next_node_id * tam_node
                f.seek(offset)
                node = node_layout.from_bytes(f.read(tam_node))

            return search_output, node.node_id

    

    def insert(self, key, value):
        #se não existe arquivo bin, cria e escreve a raiz
        if not os.path.exists(self.bin_file):
            with open(self.bin_file, "wb") as f:
                raiz = Node(node_id=0, ordem=self.ordem_arvore, is_folha=True)
                raiz.insert(key, value)

                f.write(raiz.to_bytes())
                return

        search_output, id = self.search(key)

        # se achou, pega o nó, sobreescreve o novo registro e substitui no arquivo
        if search_output:
            node = get_node(id, self.bin_file, self.ordem_arvore)
            id_to_update = node.chaves.index(key)
            node.registros[id_to_update] = value
            
            write_node(node, self.bin_file)
            return

        # mesmo se ultrapassar o limite, insere a chave/valor no nó (mas não escreve no arquivo)
        node = get_node(id, self.bin_file, self.ordem_arvore)
        node.insert(key, value)
        chaves_len = sum([1 for i in node.chaves if i != -1])

        # Caso base
        if chaves_len <= self.ordem_arvore - 1:
            write_node(node, self.bin_file)
            return


        # Caso sem espaço
        result = split_node(node, self.bin_file)

        # split da raiz
        if result is None:
            return

        promoted_key, promoted_record, left_id, right_id = result

        # se não é raiz, é preciso propagar recursivamente aos pais até "caber"
        insert_promoted(node.pai, promoted_key, promoted_record, left_id, right_id, self.bin_file, self.ordem_arvore)


    def remove(self, key):
        search_output, id = self.search(key)
        if not search_output:
            print("Essa chave não existe na árvore")
            return

        node = get_node(id, self.bin_file, self.ordem_arvore)
        idx_remove = node.chaves.index(key)

        chaves, registros, filhos = get_node_data(node)

        # chave em nó interno
        if not node.is_folha:

            # encontra o predecessor na subárvore esquerda
            left_child = get_node(filhos[idx_remove], self.bin_file, self.ordem_arvore)

            pred_key, pred_record, pred_id = get_predecessor(left_child, self.bin_file, self.ordem_arvore)

            # substitui a chave e o registro no nó interno
            chaves[idx_remove] = pred_key
            registros[idx_remove] = pred_record

            set_node_data(node, chaves, registros, filhos)
            write_node(node, self.bin_file)

            # remove o predecessor da folha onde ele estava
            node = get_node(pred_id, self.bin_file, self.ordem_arvore)
            chaves, registros, filhos = get_node_data(node)

            idx_remove = chaves.index(pred_key)


        # caso base
        chaves.pop(idx_remove)
        registros.pop(idx_remove)

        set_node_data(node, chaves, registros, [])
        write_node(node, self.bin_file)

        # caso tenha underflow no nó, função para consertar
        if node.node_id != 0 and len(chaves) < min_keys(self.ordem_arvore):
            fix_underflow(node, self.bin_file, self.ordem_arvore)

        # se o nó for raiz
        elif node.node_id == 0 and not node.is_folha:
            handle_root_underflow(node, self.bin_file, self.ordem_arvore)


    def get_altura(self, node):
        altura = 1
        while len([f for f in node.filhos if f == -1]) < len(node.filhos):
            node = get_node(node.filhos[0], self.bin_file, self.ordem_arvore)
            altura += 1

        return altura

    def print_tree(self, output_file):
        raiz = get_node(0, self.bin_file, self.ordem_arvore)

        altura_arvore = self.get_altura(raiz)

        larguras = {}
        for a in range(altura_arvore):
            larguras[a] = []

        def get_tree(node, bin_file, ordem_arvore, altura):
            larguras[altura].append([c for c in node.chaves if c != -1])

            filhos = [f_id for f_id in node.filhos if f_id != -1]
            for filho in filhos:
                next_node = get_node(filho, bin_file, ordem_arvore)
                get_tree(next_node, bin_file, ordem_arvore, altura + 1)

        get_tree(raiz, self.bin_file, self.ordem_arvore, 0)

        def write(keys):
            output = '[ ]'
            form_str = ''.join([f'key: {k}, ' for k in keys])
            return output.replace(' ', form_str)

        with open(output_file, 'a') as file:
            for _, v in larguras.items():
                file.write(f'{write(v)}\n')