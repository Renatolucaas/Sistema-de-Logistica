import json
from .models import Pedido

# Simula um banco de dados em memória
pedidos_db = {}
galpoes_db = {
    "galpao_sp": {"cidade": "São Paulo", "capacidade": 1000},
    "galpao_rj": {"cidade": "Rio de Janeiro", "capacidade": 800},
    "galpao_mg": {"cidade": "Belo Horizonte", "capacidade": 600}
}

def salvar_pedido(pedido: Pedido):
    pedidos_db[pedido.id] = pedido.__dict__
    return pedido.id

def buscar_pedido(pedido_id: str):
    return pedidos_db.get(pedido_id)

def atualizar_status(pedido_id: str, novo_status: str, galpao: str = None):
    if pedido_id in pedidos_db:
        pedidos_db[pedido_id]['status'] = novo_status
        if galpao:
            pedidos_db[pedido_id]['galpao'] = galpao
        return True
    return False

def listar_galpoes():
    return galpoes_db

def calcular_galpao_proximo(estado: str):
    # Lógica simples de proximidade baseada no estado
    mapeamento = {
        "SP": "galpao_sp",
        "RJ": "galpao_rj", 
        "MG": "galpao_mg"
    }
    return mapeamento.get(estado, "galpao_sp")