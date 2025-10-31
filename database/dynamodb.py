import boto3
from .models import Pedido
from utils.constants import TABELA_DYNAMODB

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABELA_DYNAMODB['PEDIDOS'])

def atualizar_status_pedido(pedido_id: str, status: str, galpao_atribuido: str = None):
    update_expression = "SET #status = :status"
    expression_values = {':status': status}
    expression_names = {'#status': 'status'}
    
    if galpao_atribuido:
        update_expression += ", galpao_atribuido = :galpao"
        expression_values[':galpao'] = galpao_atribuido
    
    response = table.update_item(
        Key={'pedido_id': pedido_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names,
        ReturnValues='UPDATED_NEW'
    )
    return response