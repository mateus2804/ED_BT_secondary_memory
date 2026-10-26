import struct

class Node():
    def __init__(self, ordem: int, is_folha: bool = False, chaves: list = [], registros: list = [], filhos: list = []):
        self.ordem = ordem
        self.is_folha = is_folha
        self.chaves = chaves
        self.registros = registros
        self.filhos = filhos

    def calc_size(self):
        return "i" + "?" + 2 * (self.ordem - 1) * "i" + (self.ordem + 1) * "i"

    def to_bytes(self):
        return struct.pack(self.calc_size(), self.ordem, self.is_folha, self.chaves, self.registros, self.filhos)