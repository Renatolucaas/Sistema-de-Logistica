from functions.submeter_pedido import handler as submeter_pedido
from functions.calcular_rota import handler as calcular_rota
from functions.atualizar_status import handler as atualizar_status
import json

def testar_fluxo_completo():
    print("🚀 INICIANDO TESTE DO SISTEMA DE LOGÍSTICA\n")
    
    # 1. Submeter pedido
    with open('events/novo_pedido.json') as f:
        evento_pedido = json.load(f)
    
    resultado_pedido = submeter_pedido(evento_pedido, None)
    print(f"📦 Pedido criado: {resultado_pedido['pedido_id']}\n")
    
    # 2. Calcular rota
    resultado_rota = calcular_rota(resultado_pedido, None)
    print(f"🗺️ Rota calculada: {resultado_rota['galpao']}\n")
    
    # 3. Atualizar status
    resultado_final = atualizar_status(resultado_rota, None)
    print(f"✅ {resultado_final['mensagem']}\n")
    
    print("🎉 FLUXO CONCLUÍDO COM SUCESSO!")

if __name__ == "__main__":
    testar_fluxo_completo()