# ============================================================
# Trabalho Prático T1 - Estruturas de Dados e PAA - 2026/2
# Nome: Mateus Ferreira Ferraz
# Matrícula: 2026230173
# ============================================================


from Node import Node
import os
import math

# retorna limite minimo da arvore
def min_keys(ordem_arvore):
    return math.ceil(ordem_arvore / 2) - 1

# a partir do ultimo nó no bin, gera o próximo id
def get_next_id(bin_file, ordem_arvore):
    node_layout = Node(-1, ordem_arvore)

    return os.path.getsize(bin_file) // node_layout.tamanho

# busca o nó no arquivo bin
def get_node(id, bin_file, ordem_arvore):
    node_layout = Node(-1, ordem_arvore)
    tam_node = node_layout.tamanho

    with open(bin_file, "rb") as f:
        offset = id * tam_node
        f.seek(offset)
        return node_layout.from_bytes(f.read(tam_node))

# escreve o nó no arquivo bin
def write_node(node, bin_file):
    node_id = node.node_id
    tam_node = node.tamanho

    with open(bin_file, "r+b") as f:
        offset = node_id * tam_node
        f.seek(offset)
        f.write(node.to_bytes())

# as duas próximas funções são para transformar as listas no formato definido e a operação contrária (pegar a lista no formato definido e tirar os placeholdders -1)

def set_node_data(node, keys, records, children):
    node.chaves = keys + [-1] * (node.ordem - 1 - len(keys))
    node.registros = records + [-1] * (node.ordem - 1 - len(records))
    node.filhos = children + [-1] * (node.ordem - len(children))

def get_node_data(node):
    chaves = [k for k in node.chaves if k != -1]
    registros = [r for r in node.registros if r != -1]
    filhos = [c for c in node.filhos if c != -1]

    return chaves, registros, filhos

# atualiza o atributo pai de cada nó filho para o atual
def update_children_parent(node, bin_file):
    if node.is_folha:
        return

    for child_id in node.filhos:
        if child_id != -1:
            child = get_node(child_id, bin_file, node.ordem)
            child.pai = node.node_id
            write_node(child, bin_file)


# no momento da inserção, caso o nó a ser inserido esteja cheio, a mediana é promovida ao nó pai e as duas metade são divididos em dois nós
def split_node(node, bin_file, keys=None, records=None, children=None):
    next_id = get_next_id(bin_file, node.ordem)

    if keys is None:
        keys = [k for k in node.chaves if k != -1]

    if records is None:
        records = [r for r in node.registros if r != -1]

    if children is None:
        children = [c for c in node.filhos if c != -1]

    median = (len(keys) - 1) // 2

    promoted_key = keys[median]
    promoted_record = records[median]

    left_keys = keys[:median]
    left_records = records[:median]

    right_keys = keys[median + 1:]
    right_records = records[median + 1:]

    if node.is_folha:
        left_children = []
        right_children = []
    else:
        left_children = children[:median + 1]
        right_children = children[median + 1:]

    # caso o nó seja raiz
    if node.pai == -1:
        left_id = next_id
        right_id = next_id + 1

        left_node = Node(
            node_id=left_id,
            ordem=node.ordem,
            is_folha=node.is_folha,
            pai=node.node_id,
            filhos=left_children,
            chaves=left_keys,
            registros=left_records
        )

        right_node = Node(
            node_id=right_id,
            ordem=node.ordem,
            is_folha=node.is_folha,
            pai=node.node_id,
            filhos=right_children,
            chaves=right_keys,
            registros=right_records
        )

        # Atualizar os pais dos filhos
        update_children_parent(left_node, bin_file)
        update_children_parent(right_node, bin_file)

        write_node(left_node, bin_file)
        write_node(right_node, bin_file)

        # A raiz permanece com o mesmo ID
        root = Node(
            node_id=node.node_id,
            ordem=node.ordem,
            is_folha=False,
            pai=-1,
            filhos=[left_id, right_id],
            chaves=[promoted_key],
            registros=[promoted_record]
        )

        write_node(root, bin_file)

        return

    # nó que não é raiz
    right_node = Node(
        node_id=next_id,
        ordem=node.ordem,
        is_folha=node.is_folha,
        pai=node.pai,
        filhos=right_children,
        chaves=right_keys,
        registros=right_records
    )

    set_node_data(node, left_keys, left_records, left_children)

    update_children_parent(node, bin_file)
    update_children_parent(right_node, bin_file)

    write_node(node, bin_file)
    write_node(right_node, bin_file)

    return promoted_key, promoted_record, node.node_id, right_node.node_id


# atualiza o nó pai que recebe a mediana promovida no nó filho dividido (até o achar um pai que não esteja cheio)
def insert_promoted(parent_id, key, record, left_id, right_id, bin_file, ordem_arvore):

    parent = get_node(parent_id, bin_file, ordem_arvore)
    keys, records, children = get_node_data(parent)

    # localiza a posição do filho esquerdo
    pos = children.index(left_id)

    # insere a chave e o registro na posição correspondente
    keys.insert(pos, key)
    records.insert(pos, record)

    # insere o novo filho à direita
    children.insert(pos + 1, right_id)

    # verifica se o nó está cheio. se não estiver, apenas atualiza as listas do pai e escreve
    if len(keys) <= ordem_arvore - 1:
        set_node_data(parent, keys, records, children)
        write_node(parent, bin_file)

        return

    # O pai também está cheio, mesmo processo de divisão
    result = split_node(parent, bin_file, keys, records, children)

    # Se o pai não era raiz, propagar a mediana
    if result is not None:
        promoted_key, promoted_record, left_id, right_id = result

        insert_promoted(parent.pai, promoted_key, promoted_record, left_id, right_id, bin_file, ordem_arvore)



def get_predecessor(node, bin_file, ordem_arvore):
    while not node.is_folha:
        filhos = [c for c in node.filhos if c != -1]

        node = get_node(filhos[-1], bin_file, ordem_arvore)

    chaves = [c for c in node.chaves if c != -1]
    registros = [r for r in node.registros if r != -1]

    return chaves[-1], registros[-1], node.node_id


# as duas próximas funções são usadas quando um dos nós tem menos chaves que o minimo, mas um nó irmão tem chaves além do minimo 

def get_left(node, parent, left_sibling, pos, bin_file):
    node_keys, node_records, node_children = get_node_data(node)
    parent_keys, parent_records, parent_children = get_node_data(parent)
    left_keys, left_records, left_children = get_node_data(left_sibling)

    # separador do pai desce para o nó deficitário
    node_keys.insert(0, parent_keys[pos - 1])
    node_records.insert(0, parent_records[pos - 1])

    # maior chave do irmão sobe para o pai
    parent_keys[pos - 1] = left_keys.pop()
    parent_records[pos - 1] = left_records.pop()

    # se os nós forem internos, transfere também o último filho
    if not node.is_folha:
        moved_child = left_children.pop()
        node_children.insert(0, moved_child)

        child = get_node(moved_child, bin_file, node.ordem)
        child.pai = node.node_id
        write_node(child, bin_file)

    set_node_data(node, node_keys, node_records, node_children)
    set_node_data(left_sibling, left_keys, left_records, left_children)
    set_node_data(parent, parent_keys, parent_records, parent_children)

    write_node(node, bin_file)
    write_node(left_sibling, bin_file)
    write_node(parent, bin_file)


def get_right(node, parent, right_sibling, pos, bin_file):
    node_keys, node_records, node_children = get_node_data(node)
    parent_keys, parent_records, parent_children = get_node_data(parent)
    right_keys, right_records, right_children = get_node_data(right_sibling)

    # separador do pai desce para o nó deficitário
    node_keys.append(parent_keys[pos])
    node_records.append(parent_records[pos])

    # menor chave do irmão sobe para o pai
    parent_keys[pos] = right_keys.pop(0)
    parent_records[pos] = right_records.pop(0)

    # se os nós forem internos, transferir também o primeiro filho
    if not node.is_folha:
        moved_child = right_children.pop(0)
        node_children.append(moved_child)

        child = get_node(moved_child, bin_file, node.ordem)
        child.pai = node.node_id
        write_node(child, bin_file)

    set_node_data(node, node_keys, node_records, node_children)
    set_node_data(right_sibling, right_keys, right_records, right_children)
    set_node_data(parent, parent_keys, parent_records, parent_children)

    write_node(node, bin_file)
    write_node(right_sibling, bin_file)
    write_node(parent, bin_file)

# caso não exista irmão com mais chaves que o minimo, funde

def merge_left(node, parent, left_sibling, pos, bin_file):
    node_keys, node_records, node_children = get_node_data(node)
    parent_keys, parent_records, parent_children = get_node_data(parent)
    left_keys, left_records, left_children = get_node_data(left_sibling)

    # a chave separadora do pai desce
    separator_key = parent_keys.pop(pos - 1)
    separator_record = parent_records.pop(pos - 1)

    # fundir: irmão esquerdo + separador + nó atual
    merged_keys = left_keys + [separator_key] + node_keys
    merged_records = left_records + [separator_record] + node_records
    merged_children = left_children + node_children

    set_node_data(left_sibling, merged_keys, merged_records, merged_children)

    # remove o ponteiro do nó incorporado
    parent_children.pop(pos)

    set_node_data(parent, parent_keys, parent_records, parent_children)

    # atualizar os pais dos filhos incorporados
    update_children_parent(left_sibling, bin_file)

    write_node(left_sibling, bin_file)
    write_node(parent, bin_file)

    return parent


def merge_right(node, parent, right_sibling, pos, bin_file):
    node_keys, node_records, node_children = get_node_data(node)
    parent_keys, parent_records, parent_children = get_node_data(parent)
    right_keys, right_records, right_children = get_node_data(right_sibling)

    # a chave separadora do pai desce
    separator_key = parent_keys.pop(pos)
    separator_record = parent_records.pop(pos)

    # fundir: nó atual + separador + irmão direito
    merged_keys = node_keys + [separator_key] + right_keys
    merged_records = node_records + [separator_record] + right_records
    merged_children = node_children + right_children

    set_node_data(node, merged_keys, merged_records, merged_children)

    # remove o ponteiro do irmão incorporado
    parent_children.pop(pos + 1)

    set_node_data(parent, parent_keys, parent_records, parent_children)

    update_children_parent(node, bin_file)

    write_node(node, bin_file)
    write_node(parent, bin_file)

    return parent


def handle_root_underflow(root, bin_file, ordem_arvore):
    keys, records, children = get_node_data(root)

    # raiz ainda possui chaves
    if len(keys) > 0:
        return

    # raiz vazia e sem filhos: árvore vazia
    if len(children) == 0:
        root.is_folha = True
        set_node_data(root, [], [], [])
        write_node(root, bin_file)
        return

    # raiz com um único filho: reduzir a altura da árvore
    if len(children) == 1:
        child = get_node(children[0], bin_file, ordem_arvore)

        child_keys, child_records, child_children = get_node_data(child)

        root.is_folha = child.is_folha
        root.pai = -1

        set_node_data(root, child_keys, child_records, child_children)
        update_children_parent(root, bin_file)
        write_node(root, bin_file)


# função que coordena as anteriores para "consertar" o underflow (nós com menos registros que o minimo d/2 - 1)
def fix_underflow(node, bin_file, ordem_arvore):
    min_k = min_keys(ordem_arvore)

    keys, _, _ = get_node_data(node)

    # não há underflow
    if len(keys) >= min_k:
        return

    # raiz
    if node.node_id == 0:
        handle_root_underflow(node, bin_file, ordem_arvore)
        return

    parent = get_node(node.pai, bin_file, ordem_arvore)

    parent_keys, parent_records, parent_children = get_node_data(parent)

    pos = parent_children.index(node.node_id)

    left_sibling = None
    right_sibling = None

    if pos > 0:
        left_sibling = get_node(parent_children[pos - 1], bin_file, ordem_arvore)

    if pos < len(parent_children) - 1:
        right_sibling = get_node(parent_children[pos + 1], bin_file, ordem_arvore)

    # tenta empréstimo do irmão esquerdo
    if left_sibling is not None:
        left_keys, _, _ = get_node_data(left_sibling)

        if len(left_keys) > min_k:
            get_left(node, parent, left_sibling, pos, bin_file)
            return

    # tenta empréstimo do irmão direito
    if right_sibling is not None:
        right_keys, _, _ = get_node_data(right_sibling)

        if len(right_keys) > min_k:
            get_right(node, parent, right_sibling, pos, bin_file)
            return

    # nenhum irmão pode emprestar: realizar fusão
    if left_sibling is not None:
        parent = merge_left(node, parent, left_sibling, pos, bin_file)

    elif right_sibling is not None:
        parent = merge_right(node, parent, right_sibling, pos, bin_file)

    # verificar se o pai também sofreu underflow. se sofreu, chama recursivamente
    fix_underflow(parent, bin_file, ordem_arvore)


