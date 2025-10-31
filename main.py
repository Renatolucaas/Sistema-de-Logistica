from src.funcoes.submeterPedido import submeter_pedido
from src.funcoes.calcularRotaPedido import calcular_melhor_rota
from src.funcoes.gerenciarPedido import atualizar_status_pedido

def main():
    # Exemplo de fluxo
    pedido = submeter_pedido(cliente_id="123", produtos=["prod1", "prod2"])
    rota = calcular_melhor_rota(pedido.id)
    atualizar_status_pedido(pedido.id, "DESPACHADO")

if __name__ == "__main__":
    main()