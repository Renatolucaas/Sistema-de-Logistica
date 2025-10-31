import json
from data.database import buscar_pedido, atualizar_status

def handler(event, context):
    print("🔄 Atualizando status do pedido...")
    
    pedido_id = event['pedido_id']
    galpao = event['galpao']
    
    # Atualizar para status final
    atualizar_status(pedido_id, "despachado", galpao)
    
    pedido = buscar_pedido(pedido_id)
    
    print(f"✅ Pedido {pedido_id} despachado!")
    print(f"📋 Status final: {pedido['status']}")
    print(f"🏭 Galpão: {pedido['galpao']}")
    
    return {
        'pedido_id': pedido_id,
        'status': 'despachado',
        'galpao': galpao,
        'mensagem': f'Pedido {pedido_id} foi despachado do galpão {galpao}'
    }