"""
Sistema de Logística Simplificado
Fluxo: Receber Pedido → Calcular Rota → Atualizar Status
"""

import json
import uuid
import random
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# ========== MODELOS DE DADOS ==========
@dataclass
class Endereco:
    cep: str
    rua: str
    numero: str
    cidade: str
    estado: str

@dataclass
class Produto:
    id: str
    nome: str
    quantidade: int
    preco: float

@dataclass
class Pedido:
    id: str
    cliente_id: str
    produtos: List[Produto]
    endereco: Endereco
    status: str = "recebido"
    galpao: Optional[str] = None
    data_criacao: str = None
    
    def __post_init__(self):
        if self.data_criacao is None:
            self.data_criacao = datetime.now().isoformat()
    
    def valor_total(self):
        return sum(p.quantidade * p.preco for p in self.produtos)

# ========== BANCO DE DADOS SIMULADO ==========
pedidos_db = {}
galpoes_db = {
    "galpao_sp": {"cidade": "São Paulo", "capacidade": 1000},
    "galpao_rj": {"cidade": "Rio de Janeiro", "capacidade": 800},
    "galpao_mg": {"cidade": "Belo Horizonte", "capacidade": 600},
    "galpao_rs": {"cidade": "Porto Alegre", "capacidade": 500},
    "galpao_pr": {"cidade": "Curitiba", "capacidade": 550}
}

def salvar_pedido(pedido: Pedido):
    pedidos_db[pedido.id] = {
        'id': pedido.id,
        'cliente_id': pedido.cliente_id,
        'produtos': [p.__dict__ for p in pedido.produtos],
        'endereco': pedido.endereco.__dict__,
        'status': pedido.status,
        'galpao': pedido.galpao,
        'data_criacao': pedido.data_criacao
    }
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

def calcular_galpao_proximo(estado: str):
    mapeamento = {
        "SP": "galpao_sp",
        "RJ": "galpao_rj", 
        "MG": "galpao_mg",
        "RS": "galpao_rs",
        "PR": "galpao_pr"
    }
    return mapeamento.get(estado, "galpao_sp")

# ========== FUNÇÕES PRINCIPAIS ==========
def submeter_pedido(event):
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

def calcular_rota(event):
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

def atualizar_status_pedido(event):
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

# ========== EVENTOS DE EXEMPLO ==========
def criar_evento_exemplo():
    """Cria um evento de pedido com dados aleatórios"""
    
    # Dados variáveis para testes
    estados = ["SP", "RJ", "MG", "RS", "PR"]
    produtos_exemplo = [
        {"id": "prod_001", "nome": "Smartphone", "preco": 1500.00},
        {"id": "prod_002", "nome": "Tablet", "preco": 800.00},
        {"id": "prod_003", "nome": "Notebook", "preco": 2500.00},
        {"id": "prod_004", "nome": "Fone de Ouvido", "preco": 150.00},
        {"id": "prod_005", "nome": "Carregador", "preco": 50.00},
        {"id": "prod_006", "nome": "Mouse", "preco": 80.00},
        {"id": "prod_007", "nome": "Teclado", "preco": 120.00},
        {"id": "prod_008", "nome": "Monitor", "preco": 900.00}
    ]
    
    # Escolher produtos aleatórios
    num_produtos = random.randint(1, 4)
    produtos_selecionados = random.sample(produtos_exemplo, num_produtos)
    
    # Adicionar quantidade aleatória
    for produto in produtos_selecionados:
        produto = produto.copy()  # Criar cópia para não modificar o original
        produto["quantidade"] = random.randint(1, 3)
    
    estado = random.choice(estados)
    cidades = {
        "SP": "São Paulo", 
        "RJ": "Rio de Janeiro", 
        "MG": "Belo Horizonte", 
        "RS": "Porto Alegre", 
        "PR": "Curitiba"
    }
    
    return {
        "body": {
            "cliente_id": f"cli_{random.randint(10000, 99999)}",
            "produtos": produtos_selecionados,
            "endereco": {
                "cep": f"{random.randint(10000, 99999)}-{random.randint(100, 999)}",
                "rua": f"Rua {random.choice(['das Flores', 'Principal', 'Comercial', 'Industrial'])}",
                "numero": str(random.randint(1, 1000)),
                "cidade": cidades[estado],
                "estado": estado
            }
        }
    }

# ========== TESTE DO SISTEMA ==========
def testar_fluxo_completo():
    """Testa o fluxo completo do sistema com dados aleatórios"""
    print("🚀 INICIANDO TESTE DO SISTEMA DE LOGÍSTICA\n")
    
    # 1. Submeter pedido
    evento_pedido = criar_evento_exemplo()
    resultado_pedido = submeter_pedido(evento_pedido)
    print(f"📦 Pedido criado: {resultado_pedido['pedido_id']}\n")
    
    # 2. Calcular rota
    resultado_rota = calcular_rota(resultado_pedido)
    print(f"🗺️ Rota calculada: {resultado_rota['galpao']}\n")
    
    # 3. Atualizar status
    resultado_final = atualizar_status_pedido(resultado_rota)
    print(f"✅ {resultado_final['mensagem']}\n")
    
    # 4. Mostrar dados finais
    pedido_final = buscar_pedido(resultado_pedido['pedido_id'])
    print("📊 DADOS FINAIS DO PEDIDO:")
    print(f"   ID: {pedido_final['id']}")
    print(f"   Cliente: {pedido_final['client_id']}")
    print(f"   Status: {pedido_final['status']}")
    print(f"   Galpão: {pedido_final['galpao']}")
    
    valor_total = sum(p['preco'] * p['quantidade'] for p in pedido_final['produtos'])
    print(f"   Valor Total: R${valor_total:.2f}")
    
    print(f"   Produtos: {len(pedido_final['produtos'])} itens")
    for produto in pedido_final['produtos']:
        print(f"     - {produto['nome']} (x{produto['quantidade']}) - R${produto['preco']:.2f} cada")
    
    print("\n🎉 FLUXO CONCLUÍDO COM SUCESSO!")

def mostrar_pedidos():
    """Mostra todos os pedidos cadastrados"""
    print("\n📋 PEDIDOS CADASTRADOS:")
    print("=" * 50)
    
    if not pedidos_db:
        print("Nenhum pedido cadastrado.")
        return
    
    for pedido_id, pedido in pedidos_db.items():
        valor_total = sum(p['preco'] * p['quantidade'] for p in pedido['produtos'])
        print(f"🆔 {pedido_id}")
        print(f"   👤 Cliente: {pedido['cliente_id']}")
        print(f"   📍 Status: {pedido['status']}")
        print(f"   🏭 Galpão: {pedido.get('galpao', 'Não atribuído')}")
        print(f"   💰 Valor: R${valor_total:.2f}")
        print(f"   📅 Data: {pedido['data_criacao'][:16]}")
        print(f"   🚚 Endereço: {pedido['endereco']['cidade']}-{pedido['endereco']['estado']}")
        print("   ──────────────────────────")

def limpar_base_dados():
    """Limpa todos os pedidos da base"""
    global pedidos_db
    pedidos_db = {}
    print("🗑️ Base de dados limpa!")

# ========== MENU PRINCIPAL ==========
def main():
    print("🔧 SISTEMA DE LOGÍSTICA - MENU PRINCIPAL")
    print("=" * 40)
    
    while True:
        print("\nOpções:")
        print("1. Testar fluxo completo (automático)")
        print("2. Testar fluxo completo (manual)")
        print("3. Ver pedidos cadastrados")
        print("4. Limpar base de dados")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            testar_fluxo_completo()
        
        elif opcao == "2":
            # Pedir dados manualmente
            print("\n📝 Dados do Pedido:")
            cliente_id = input("ID do Cliente: ") or "cli_12345"
            estado = input("Estado (SP/RJ/MG/RS/PR): ").upper() or "SP"
            
            if estado not in ["SP", "RJ", "MG", "RS", "PR"]:
                print("❌ Estado inválido! Usando SP como padrão.")
                estado = "SP"
            
            evento_manual = {
                "body": {
                    "cliente_id": cliente_id,
                    "produtos": [
                        {
                            "id": "prod_manual",
                            "nome": "Produto Manual",
                            "quantidade": 1,
                            "preco": 100.0
                        }
                    ],
                    "endereco": {
                        "cep": "00000-000",
                        "rua": "Rua Manual",
                        "numero": "123",
                        "cidade": "Cidade Manual",
                        "estado": estado
                    }
                }
            }
            
            resultado_pedido = submeter_pedido(evento_manual)
            resultado_rota = calcular_rota(resultado_pedido)
            resultado_final = atualizar_status_pedido(resultado_rota)
            
            print(f"\n✅ Processo concluído: {resultado_final['mensagem']}")
        
        elif opcao == "3":
            mostrar_pedidos()
        
        elif opcao == "4":
            confirmacao = input("Tem certeza que deseja limpar todos os pedidos? (s/N): ")
            if confirmacao.lower() == 's':
                limpar_base_dados()
            else:
                print("Operação cancelada.")
        
        elif opcao == "5":
            print("👋 Saindo do sistema...")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()