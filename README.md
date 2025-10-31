# 📦 Sistema de Logística Simplificado

Sistema de simulação de fluxo logístico para recebimento de pedidos, cálculo de rotas e atualização de status. Desenvolvido de forma didática como trabalho acadêmico.

## 🚀 Funcionalidades

- **📋 Recebimento de Pedidos** - Cadastro de novos pedidos com produtos e endereço
- **🗺️ Cálculo de Rotas** - Definição do galpão mais próximo do cliente
- **🔄 Atualização de Status** - Acompanhamento do status do pedido
- **💾 Armazenamento** - Base de dados em memória para simulação

## 🏗️ Arquitetura
sistema-logistica/
├── sistema_logistica.py # Arquivo principal
└── README.md # Documentação

text

## 📋 Fluxo do Sistema

1. **Submeter Pedido** → Recebe dados do cliente e produtos
2. **Calcular Rota** → Encontra galpão mais próximo baseado no estado
3. **Atualizar Status** → Marca pedido como despachado

## 🛠️ Tecnologias

- **Python 3.8+**
- **Dataclasses** para modelos de dados
- **UUID** para geração de IDs únicos
- **Random** para dados de teste aleatórios

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior instalado

### Execução
```bash
# Clone ou baixe o arquivo
python sistema_logistica.py
Opções do Menu
text
1. Testar fluxo completo (automático) - Dados aleatórios
2. Testar fluxo completo (manual) - Entrada personalizada  
3. Ver pedidos cadastrados - Lista todos os pedidos
4. Limpar base de dados - Remove todos os pedidos
5. Sair - Encerra o sistema
🎯 Exemplo de Uso
python
# Fluxo automático
>>> Escolha opção 1
📦 Recebendo novo pedido...
✅ Pedido a1b2c3d4 salvo - Valor: R$1.250,00
🗺️ Calculando melhor rota...
✅ Rota calculada - Galpão: galpao_sp
🔄 Atualizando status...
✅ Pedido despachado!
🗂️ Estrutura de Dados
Pedido
python
{
    "id": "a1b2c3d4",
    "cliente_id": "cli_12345",
    "produtos": [...],
    "endereco": {...},
    "status": "despachado",
    "galpao": "galpao_sp"
}
Galpões Disponíveis
galpao_sp - São Paulo

galpao_rj - Rio de Janeiro

galpao_mg - Belo Horizonte

galpao_rs - Porto Alegre

galpao_pr - Curitiba

🧪 Testes
O sistema inclui:

✅ Geração automática de dados de teste

✅ Validação de estados brasileiros

✅ Cálculo correto de valores totais

✅ Atribuição inteligente de galpões

📊 Status do Pedido
recebido - Pedido cadastrado no sistema

rota_calculada - Galpão definido

despachado - Pedido enviado para entrega

👥 Desenvolvimento
Projeto desenvolvido para fins educacionais, demonstrando:

Conceitos de programação orientada a objetos

Estruturação de sistemas logísticos

Manipulação de dados e estados

Interface de linha de comando (CLI)

📝 Licença
Este projeto é para fins educacionais e acadêmicos.

