from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Endereco:
    cep: str
    rua: str
    numero: str
    cidade: str
    estado: str

@dataclass
class Produto:
    id: str
    nome: str
    quantidade: int
    preco: float

@dataclass
class Pedido:
    id: str
    cliente_id: str
    produtos: List[Produto]
    endereco: Endereco
    status: str = "recebido"
    galpao: Optional[str] = None
    data_criacao: str = None
    
    def __post_init__(self):
        if self.data_criacao is None:
            self.data_criacao = datetime.now().isoformat()
    
    def valor_total(self):
        return sum(p.quantidade * p.preco for p in self.produtos)