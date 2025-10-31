import json
import boto3
from shared.database.dynamodb import obter_pedido, atualizar_rota
from shared.utils.helpers import calcular_galpao_proximo

sns = boto3.client('sns')

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        
        pedido_id = message['pedido_id']
        cliente_id = message['cliente_id']
        
        # Calcular melhor galpão
        galpao_ideal = calcular_galpao_proximo(cliente_id)
        
        # Atualizar pedido no DynamoDB
        atualizar_rota(pedido_id, galpao_ideal)
        
        # Publicar próximo evento
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789:filaDespachoGalpao',
            Message=json.dumps({
                'pedido_id': pedido_id,
                'galpao': galpao_ideal,
                'status': 'ROTA_DEFINIDA'
            })
        )
    
    return {'status': 'processed'}