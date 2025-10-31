import json
import boto3
from shared.database.dynamodb import atualizar_status_pedido, obter_pedido
from shared.utils.constants import STATUS_PEDIDO

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pedidos')

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        
        pedido_id = message['pedido_id']
        galpao = message['galpao']
        
        try:
            # Atualizar status no DynamoDB
            atualizar_status_pedido(
                pedido_id=pedido_id,
                status=STATUS_PEDIDO['DESPACHADO'],
                galpao_atribuido=galpao
            )
            
            # Aqui pode ter lógica adicional:
            # - Notificar cliente
            # - Gerar etiqueta de envio
            # - Integrar com sistema de transporte
            
            print(f"Pedido {pedido_id} gerenciado com sucesso. Galpão: {galpao}")
            
        except Exception as e:
            print(f"Erro ao gerenciar pedido {pedido_id}: {str(e)}")
            # Pode publicar em uma DLQ (Dead Letter Queue) aqui
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Pedidos processados'})
    }