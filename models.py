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

    def init_objects(self):
        def temp(obj, tam_max):
            if type(obj) != list:
                return [-1 for _ in range(tam_max)]
            elif len(obj) < (tam_max):
                [obj.append(-1) for _ in range(tam_max - len(obj))]
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
        achou = False
        for i, chave in enumerate(self.chaves):
            if self.is_folha == False:
                if target < chave or chave == -1:
                    return self.filhos[i]
                if i == len(self.chaves) - 1:
                    return self.filhos[i + 1]
            if target == chave:
                achou = True
                break
                
        return achou



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

    
