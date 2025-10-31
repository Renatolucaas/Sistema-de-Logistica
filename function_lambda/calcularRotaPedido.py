import json
from data.database import buscar_pedido, atualizar_status, calcular_galpao_proximo

def handler(event, context):
    print("🗺️ Calculando melhor rota...")
    
    pedido_id = event['pedido_id']
    estado = event['estado']
    
    # Calcular galpão mais próximo
    galpao_ideal = calcular_galpao_proximo(estado)
    
    # Atualizar pedido
    atualizar_status(pedido_id, "rota_calculada", galpao_ideal)
    
    pedido = buscar_pedido(pedido_id)
    
    print(f"✅ Rota calculada para pedido {pedido_id}")
    print(f"🏭 Galpão atribuído: {galpao_ideal}")
    
    return {
        'pedido_id': pedido_id,
        'galpao': galpao_ideal,
        'status': 'rota_calculada',
        'cliente_id': event['cliente_id']
    }