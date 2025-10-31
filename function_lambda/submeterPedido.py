import json
import uuid
from data.database import salvar_pedido
from data.models import Pedido, Produto, Endereco

def handler(event, context):
    print("📦 Recebendo novo pedido...")
    
    # Extrair dados do pedido
    body = event.get('body', {})
    
    # Criar objetos do pedido
    endereco = Endereco(
        cep=body['endereco']['cep'],
        rua=body['endereco']['rua'],
        numero=body['endereco']['numero'],
        cidade=body['endereco']['cidade'],
        estado=body['endereco']['estado']
    )
    
    produtos = [
        Produto(
            id=p['id'],
            nome=p['nome'],
            quantidade=p['quantidade'],
            preco=p['preco']
        ) for p in body['produtos']
    ]
    
    # Criar pedido
    pedido = Pedido(
        id=str(uuid.uuid4())[:8],
        cliente_id=body['cliente_id'],
        produtos=produtos,
        endereco=endereco
    )
    
    # Salvar no banco
    salvar_pedido(pedido)
    
    print(f"✅ Pedido {pedido.id} salvo - Valor: R${pedido.valor_total():.2f}")
    
    # Retornar evento para próxima função
    return {
        'pedido_id': pedido.id,
        'cliente_id': pedido.cliente_id,
        'estado': endereco.estado,
        'valor_total': pedido.valor_total(),
        'status': 'recebido'
    }