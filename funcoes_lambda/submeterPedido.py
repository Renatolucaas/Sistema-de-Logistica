import json
import boto3
from shared.database.dynamodb import salvar_pedido
from shared.schemas.pedido_schema import validar_pedido

sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Validar pedido
        pedido = validar_pedido(event)
        
        # Salvar no DynamoDB
        pedido_id = salvar_pedido(pedido)
        
        # Publicar no SNS
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789:filaPedido',
            Message=json.dumps({
                'pedido_id': pedido_id,
                'cliente_id': pedido['cliente_id'],
                'produtos': pedido['produtos']
            })
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'pedido_id': pedido_id,
                'message': 'Pedido submetido com sucesso'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }