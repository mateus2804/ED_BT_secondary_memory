# ============================================================
# Trabalho Prático T1 - Estruturas de Dados e PAA - 2026/2
# Nome: Mateus Ferreira Ferraz
# Matrícula: 2026230173
# ============================================================

import struct
from dataclasses import dataclass, field

@dataclass
class Node():
    node_id: int
    ordem: int
    is_folha: bool = False
    pai: int = -1
    filhos: list = field(default=list)
    chaves: list = field(default=list)
    registros: list = field(default=list)
    formato: str = field(init=False)
    tamanho: int = field(init=False)

    def __post_init__(self):
        self.init_objects()
        self.formato = self.get_format()
        self.tamanho = struct.calcsize(self.formato)

    # Como os objetos tem tamanho fixo no arquivo binário (na minha implementação), pelo limite máximo para uma arvore B de ordem d, eu preencho os vetores com -1
    def init_objects(self):
        def temp(obj, tam_max):
            if not isinstance(obj, list):
                return [-1 for _ in range(tam_max)]
            elif len(obj) < (tam_max):
                obj.extend([-1] * (tam_max- len(obj)))
                return obj
            else:
                return obj

        tam_max_chaves = self.ordem - 1
        tam_max_filhos = tam_max_chaves + 1

        self.chaves = temp(self.chaves, tam_max_chaves)
        self.registros = temp(self.registros, tam_max_chaves)
        self.filhos = temp(self.filhos, tam_max_filhos)

    def get_format(self):
        format_string = '<HH?i'
        for obj in [self.chaves, self.registros, self.filhos]:
            format_string += f'{len(obj)}h'

        return format_string

    def search_keys(self, target):
        chaves = [i for i in self.chaves if i != -1]

        #busca posicao da chave
        pos = 0
        while pos < len(chaves) and chaves[pos] < target:
            pos += 1

        #como a lista de filhos é maior (em 1 espaço) do que a de chaves, evita erro na linha 58 out of index
        if pos >= len(chaves):
            return False, self.filhos[pos]

        #se a chave existir no nó, retorna True e id do próprio nó
        if chaves[pos] == target:
            return True, self.node_id

        # se não, retorna o id do proximo filho
        return False, self.filhos[pos]

    def insert(self, chave, registro):

        chaves = [i for i in self.chaves if i != -1]
        registros = [i for i in self.registros if i != -1]

        pos = 0
        while pos < len(chaves) and chaves[pos] < chave:
            pos += 1

        #insere na a chave numa posicao de modo que as chaves continuam ordenadas
        #insere também o registro para seguir a lógica
        chaves.insert(pos, chave)
        registros.insert(pos, registro)

        
        self.chaves = chaves + [-1] * (len(self.chaves) - len(chaves))
        self.registros = registros + [-1] * (len(self.registros) - len(registros))
 
    def to_bytes(self):
        return struct.pack(self.formato, self.node_id, self.ordem, self.is_folha, self.pai,  *self.chaves, *self.registros, *self.filhos)

    @classmethod
    def from_bytes(cls, dados):
        cabecalho = struct.unpack("<HH?i", dados[:9])

        node_id, ordem, is_folha, pai = cabecalho
        node = cls(node_id, ordem, is_folha, pai)

        valores = struct.unpack(node.formato, dados)

        n_chaves = ordem - 1
        n_registros = ordem - 1
        n_filhos = ordem

        inicio = 4 

        node.chaves = list(valores[inicio:inicio + n_chaves])
        inicio += n_chaves

        node.registros = list(valores[inicio:inicio + n_registros])
        inicio += n_registros

        node.filhos = list(valores[inicio:inicio + n_filhos])

        return node

