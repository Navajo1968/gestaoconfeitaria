#!/usr/bin/env python3
"""
Sistema de Gestão de Confeitaria
Bakery Management System - Main Application

Interface de linha de comando para gerenciar a confeitaria.
"""

from datetime import datetime, timedelta
from database import Database
from models import Produto, Cliente, Pedido, ItemPedido, Estoque, StatusPedido


class SistemaConfeitaria:
    """Classe principal do sistema de gestão"""
    
    def __init__(self):
        self.db = Database()
    
    def menu_principal(self):
        """Exibe o menu principal"""
        while True:
            print("\n" + "="*50)
            print("   SISTEMA DE GESTÃO DE CONFEITARIA")
            print("="*50)
            print("\n1. Gerenciar Produtos")
            print("2. Gerenciar Clientes")
            print("3. Gerenciar Pedidos")
            print("4. Gerenciar Estoque")
            print("5. Relatórios")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.menu_produtos()
            elif opcao == "2":
                self.menu_clientes()
            elif opcao == "3":
                self.menu_pedidos()
            elif opcao == "4":
                self.menu_estoque()
            elif opcao == "5":
                self.menu_relatorios()
            elif opcao == "0":
                print("\nEncerrando o sistema. Até logo!")
                break
            else:
                print("\nOpção inválida!")
    
    # ==================== MENU PRODUTOS ====================
    
    def menu_produtos(self):
        """Menu de gerenciamento de produtos"""
        while True:
            print("\n" + "-"*50)
            print("   GERENCIAR PRODUTOS")
            print("-"*50)
            print("\n1. Listar produtos")
            print("2. Adicionar produto")
            print("3. Atualizar produto")
            print("4. Excluir produto")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.listar_produtos()
            elif opcao == "2":
                self.adicionar_produto()
            elif opcao == "3":
                self.atualizar_produto()
            elif opcao == "4":
                self.excluir_produto()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        produtos = self.db.listar_produtos()
        if not produtos:
            print("\nNenhum produto cadastrado.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Nome':<30} {'Preço':<12} {'Tempo (min)':<12}")
        print("="*80)
        for p in produtos:
            print(f"{p.id:<5} {p.nome:<30} R$ {p.preco:<9.2f} {p.tempo_preparo_minutos:<12}")
        print("="*80)
    
    def adicionar_produto(self):
        """Adiciona um novo produto"""
        print("\n--- Adicionar Produto ---")
        nome = input("Nome: ").strip()
        descricao = input("Descrição: ").strip()
        preco = float(input("Preço (R$): ").strip())
        tempo = int(input("Tempo de preparo (minutos): ").strip())
        
        produto = Produto(None, nome, descricao, preco, tempo)
        produto_id = self.db.criar_produto(produto)
        print(f"\nProduto criado com ID: {produto_id}")
    
    def atualizar_produto(self):
        """Atualiza um produto existente"""
        self.listar_produtos()
        produto_id = int(input("\nID do produto a atualizar: ").strip())
        
        produto = self.db.obter_produto(produto_id)
        if not produto:
            print("\nProduto não encontrado!")
            return
        
        print(f"\nDados atuais - Nome: {produto.nome}, Preço: R$ {produto.preco:.2f}")
        nome = input("Novo nome (Enter para manter): ").strip() or produto.nome
        descricao = input("Nova descrição (Enter para manter): ").strip() or produto.descricao
        preco_str = input("Novo preço (Enter para manter): ").strip()
        preco = float(preco_str) if preco_str else produto.preco
        tempo_str = input("Novo tempo de preparo (Enter para manter): ").strip()
        tempo = int(tempo_str) if tempo_str else produto.tempo_preparo_minutos
        
        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco
        produto.tempo_preparo_minutos = tempo
        self.db.atualizar_produto(produto)
        print("\nProduto atualizado com sucesso!")
    
    def excluir_produto(self):
        """Exclui um produto"""
        self.listar_produtos()
        produto_id = int(input("\nID do produto a excluir: ").strip())
        
        confirma = input("Tem certeza? (s/n): ").strip().lower()
        if confirma == 's':
            self.db.excluir_produto(produto_id)
            print("\nProduto excluído com sucesso!")
    
    # ==================== MENU CLIENTES ====================
    
    def menu_clientes(self):
        """Menu de gerenciamento de clientes"""
        while True:
            print("\n" + "-"*50)
            print("   GERENCIAR CLIENTES")
            print("-"*50)
            print("\n1. Listar clientes")
            print("2. Adicionar cliente")
            print("3. Atualizar cliente")
            print("4. Excluir cliente")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.listar_clientes()
            elif opcao == "2":
                self.adicionar_cliente()
            elif opcao == "3":
                self.atualizar_cliente()
            elif opcao == "4":
                self.excluir_cliente()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        clientes = self.db.listar_clientes()
        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Nome':<30} {'Telefone':<15} {'Email':<30}")
        print("="*80)
        for c in clientes:
            email = c.email or "-"
            print(f"{c.id:<5} {c.nome:<30} {c.telefone:<15} {email:<30}")
        print("="*80)
    
    def adicionar_cliente(self):
        """Adiciona um novo cliente"""
        print("\n--- Adicionar Cliente ---")
        nome = input("Nome: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("Email (opcional): ").strip() or None
        endereco = input("Endereço (opcional): ").strip() or None
        
        cliente = Cliente(None, nome, telefone, email, endereco)
        cliente_id = self.db.criar_cliente(cliente)
        print(f"\nCliente criado com ID: {cliente_id}")
    
    def atualizar_cliente(self):
        """Atualiza um cliente existente"""
        self.listar_clientes()
        cliente_id = int(input("\nID do cliente a atualizar: ").strip())
        
        cliente = self.db.obter_cliente(cliente_id)
        if not cliente:
            print("\nCliente não encontrado!")
            return
        
        print(f"\nDados atuais - Nome: {cliente.nome}, Telefone: {cliente.telefone}")
        nome = input("Novo nome (Enter para manter): ").strip() or cliente.nome
        telefone = input("Novo telefone (Enter para manter): ").strip() or cliente.telefone
        email = input("Novo email (Enter para manter): ").strip() or cliente.email
        endereco = input("Novo endereço (Enter para manter): ").strip() or cliente.endereco
        
        cliente.nome = nome
        cliente.telefone = telefone
        cliente.email = email
        cliente.endereco = endereco
        self.db.atualizar_cliente(cliente)
        print("\nCliente atualizado com sucesso!")
    
    def excluir_cliente(self):
        """Exclui um cliente"""
        self.listar_clientes()
        cliente_id = int(input("\nID do cliente a excluir: ").strip())
        
        confirma = input("Tem certeza? (s/n): ").strip().lower()
        if confirma == 's':
            self.db.excluir_cliente(cliente_id)
            print("\nCliente excluído com sucesso!")
    
    # ==================== MENU PEDIDOS ====================
    
    def menu_pedidos(self):
        """Menu de gerenciamento de pedidos"""
        while True:
            print("\n" + "-"*50)
            print("   GERENCIAR PEDIDOS")
            print("-"*50)
            print("\n1. Listar pedidos")
            print("2. Criar novo pedido")
            print("3. Ver detalhes do pedido")
            print("4. Atualizar status do pedido")
            print("5. Excluir pedido")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.listar_pedidos()
            elif opcao == "2":
                self.criar_pedido()
            elif opcao == "3":
                self.ver_detalhes_pedido()
            elif opcao == "4":
                self.atualizar_status_pedido()
            elif opcao == "5":
                self.excluir_pedido()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
    
    def listar_pedidos(self):
        """Lista todos os pedidos"""
        pedidos = self.db.listar_pedidos()
        if not pedidos:
            print("\nNenhum pedido cadastrado.")
            return
        
        print("\n" + "="*90)
        print(f"{'ID':<5} {'Cliente ID':<12} {'Data Entrega':<20} {'Status':<15} {'Valor':<12}")
        print("="*90)
        for p in pedidos:
            data_entrega = p.data_entrega.strftime("%d/%m/%Y %H:%M")
            print(f"{p.id:<5} {p.cliente_id:<12} {data_entrega:<20} {p.status.value:<15} R$ {p.valor_total:<9.2f}")
        print("="*90)
    
    def criar_pedido(self):
        """Cria um novo pedido"""
        print("\n--- Criar Novo Pedido ---")
        
        # Seleciona o cliente
        self.listar_clientes()
        cliente_id = int(input("\nID do cliente: ").strip())
        
        cliente = self.db.obter_cliente(cliente_id)
        if not cliente:
            print("\nCliente não encontrado!")
            return
        
        # Data de entrega
        dias = int(input("Dias até a entrega (ex: 2 para daqui 2 dias): ").strip())
        data_entrega = datetime.now() + timedelta(days=dias)
        
        observacoes = input("Observações (opcional): ").strip() or None
        
        # Cria o pedido
        pedido = Pedido(None, cliente_id, datetime.now(), data_entrega, 
                       StatusPedido.PENDENTE, observacoes)
        
        # Adiciona itens ao pedido
        self.listar_produtos()
        print("\nAdicionar itens ao pedido:")
        
        while True:
            produto_id = input("\nID do produto (0 para finalizar): ").strip()
            if produto_id == "0":
                break
            
            produto_id = int(produto_id)
            produto = self.db.obter_produto(produto_id)
            if not produto:
                print("Produto não encontrado!")
                continue
            
            quantidade = int(input("Quantidade: ").strip())
            obs_item = input("Observações do item (opcional): ").strip() or None
            
            item = ItemPedido(None, None, produto_id, quantidade, produto.preco, obs_item)
            pedido.adicionar_item(item)
            print(f"Item adicionado: {produto.nome} x{quantidade} = R$ {item.subtotal:.2f}")
        
        if pedido.itens:
            pedido_id = self.db.criar_pedido(pedido)
            print(f"\nPedido criado com ID: {pedido_id}")
            print(f"Valor total: R$ {pedido.valor_total:.2f}")
        else:
            print("\nPedido cancelado (sem itens).")
    
    def ver_detalhes_pedido(self):
        """Exibe os detalhes de um pedido"""
        pedido_id = int(input("\nID do pedido: ").strip())
        pedido = self.db.obter_pedido(pedido_id)
        
        if not pedido:
            print("\nPedido não encontrado!")
            return
        
        cliente = self.db.obter_cliente(pedido.cliente_id)
        
        print("\n" + "="*70)
        print(f"PEDIDO #{pedido.id}")
        print("="*70)
        print(f"Cliente: {cliente.nome} (ID: {cliente.id})")
        print(f"Telefone: {cliente.telefone}")
        print(f"Data do pedido: {pedido.data_pedido.strftime('%d/%m/%Y %H:%M')}")
        print(f"Data de entrega: {pedido.data_entrega.strftime('%d/%m/%Y %H:%M')}")
        print(f"Status: {pedido.status.value}")
        if pedido.observacoes:
            print(f"Observações: {pedido.observacoes}")
        
        print("\nITENS:")
        print("-"*70)
        for item in pedido.itens:
            produto = self.db.obter_produto(item.produto_id)
            print(f"  {produto.nome} x{item.quantidade} - R$ {item.preco_unitario:.2f} cada = R$ {item.subtotal:.2f}")
            if item.observacoes:
                print(f"    Obs: {item.observacoes}")
        
        print("-"*70)
        print(f"VALOR TOTAL: R$ {pedido.valor_total:.2f}")
        print("="*70)
    
    def atualizar_status_pedido(self):
        """Atualiza o status de um pedido"""
        self.listar_pedidos()
        pedido_id = int(input("\nID do pedido: ").strip())
        
        print("\nStatus disponíveis:")
        print("1. Pendente")
        print("2. Em Produção")
        print("3. Pronto")
        print("4. Entregue")
        print("5. Cancelado")
        
        opcao = input("\nNovo status: ").strip()
        
        status_map = {
            "1": StatusPedido.PENDENTE,
            "2": StatusPedido.EM_PRODUCAO,
            "3": StatusPedido.PRONTO,
            "4": StatusPedido.ENTREGUE,
            "5": StatusPedido.CANCELADO
        }
        
        if opcao in status_map:
            self.db.atualizar_status_pedido(pedido_id, status_map[opcao])
            print("\nStatus atualizado com sucesso!")
        else:
            print("\nOpção inválida!")
    
    def excluir_pedido(self):
        """Exclui um pedido"""
        self.listar_pedidos()
        pedido_id = int(input("\nID do pedido a excluir: ").strip())
        
        confirma = input("Tem certeza? (s/n): ").strip().lower()
        if confirma == 's':
            self.db.excluir_pedido(pedido_id)
            print("\nPedido excluído com sucesso!")
    
    # ==================== MENU ESTOQUE ====================
    
    def menu_estoque(self):
        """Menu de gerenciamento de estoque"""
        while True:
            print("\n" + "-"*50)
            print("   GERENCIAR ESTOQUE")
            print("-"*50)
            print("\n1. Listar estoque")
            print("2. Adicionar item")
            print("3. Atualizar quantidade")
            print("4. Itens com estoque baixo")
            print("5. Excluir item")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.listar_estoque()
            elif opcao == "2":
                self.adicionar_item_estoque()
            elif opcao == "3":
                self.atualizar_quantidade_estoque()
            elif opcao == "4":
                self.listar_estoque_baixo()
            elif opcao == "5":
                self.excluir_item_estoque()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
    
    def listar_estoque(self):
        """Lista todos os itens de estoque"""
        itens = self.db.listar_estoque()
        if not itens:
            print("\nNenhum item no estoque.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Nome':<30} {'Qtd Atual':<15} {'Qtd Mínima':<15} {'Status':<10}")
        print("="*80)
        for item in itens:
            status = "⚠️ BAIXO" if item.precisa_reposicao else "OK"
            qtd = f"{item.quantidade_atual} {item.unidade_medida}"
            qtd_min = f"{item.quantidade_minima} {item.unidade_medida}"
            print(f"{item.id:<5} {item.nome:<30} {qtd:<15} {qtd_min:<15} {status:<10}")
        print("="*80)
    
    def adicionar_item_estoque(self):
        """Adiciona um novo item ao estoque"""
        print("\n--- Adicionar Item ao Estoque ---")
        nome = input("Nome do item: ").strip()
        unidade = input("Unidade de medida (kg, l, un, etc): ").strip()
        quantidade = float(input("Quantidade atual: ").strip())
        quantidade_min = float(input("Quantidade mínima: ").strip())
        
        item = Estoque(None, nome, unidade, quantidade, quantidade_min)
        item_id = self.db.criar_item_estoque(item)
        print(f"\nItem criado com ID: {item_id}")
    
    def atualizar_quantidade_estoque(self):
        """Atualiza a quantidade de um item"""
        self.listar_estoque()
        item_id = int(input("\nID do item: ").strip())
        
        item = self.db.obter_item_estoque(item_id)
        if not item:
            print("\nItem não encontrado!")
            return
        
        print(f"\nQuantidade atual: {item.quantidade_atual} {item.unidade_medida}")
        nova_quantidade = float(input("Nova quantidade: ").strip())
        
        self.db.atualizar_quantidade_estoque(item_id, nova_quantidade)
        print("\nQuantidade atualizada com sucesso!")
    
    def listar_estoque_baixo(self):
        """Lista itens com estoque baixo"""
        itens = self.db.listar_estoque()
        itens_baixos = [item for item in itens if item.precisa_reposicao]
        
        if not itens_baixos:
            print("\n✓ Todos os itens estão com estoque adequado!")
            return
        
        print("\n" + "="*70)
        print("   ⚠️  ITENS COM ESTOQUE BAIXO")
        print("="*70)
        for item in itens_baixos:
            print(f"ID {item.id}: {item.nome}")
            print(f"  Quantidade atual: {item.quantidade_atual} {item.unidade_medida}")
            print(f"  Quantidade mínima: {item.quantidade_minima} {item.unidade_medida}")
            print()
    
    def excluir_item_estoque(self):
        """Exclui um item de estoque"""
        self.listar_estoque()
        item_id = int(input("\nID do item a excluir: ").strip())
        
        confirma = input("Tem certeza? (s/n): ").strip().lower()
        if confirma == 's':
            self.db.excluir_item_estoque(item_id)
            print("\nItem excluído com sucesso!")
    
    # ==================== MENU RELATÓRIOS ====================
    
    def menu_relatorios(self):
        """Menu de relatórios"""
        while True:
            print("\n" + "-"*50)
            print("   RELATÓRIOS")
            print("-"*50)
            print("\n1. Pedidos por status")
            print("2. Resumo de vendas")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.relatorio_pedidos_status()
            elif opcao == "2":
                self.relatorio_vendas()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
    
    def relatorio_pedidos_status(self):
        """Relatório de pedidos agrupados por status"""
        print("\n" + "="*70)
        print("   RELATÓRIO: PEDIDOS POR STATUS")
        print("="*70)
        
        for status in StatusPedido:
            pedidos = self.db.listar_pedidos(status)
            print(f"\n{status.value.upper()}: {len(pedidos)} pedido(s)")
            
            if pedidos:
                for p in pedidos:
                    cliente = self.db.obter_cliente(p.cliente_id)
                    print(f"  - Pedido #{p.id}: {cliente.nome}, Entrega: {p.data_entrega.strftime('%d/%m/%Y')}, Valor: R$ {p.valor_total:.2f}")
    
    def relatorio_vendas(self):
        """Relatório de vendas"""
        pedidos = self.db.listar_pedidos()
        
        if not pedidos:
            print("\nNenhum pedido registrado.")
            return
        
        total_vendas = sum(p.valor_total for p in pedidos)
        pedidos_entregues = [p for p in pedidos if p.status == StatusPedido.ENTREGUE]
        total_entregue = sum(p.valor_total for p in pedidos_entregues)
        
        print("\n" + "="*70)
        print("   RELATÓRIO: RESUMO DE VENDAS")
        print("="*70)
        print(f"\nTotal de pedidos: {len(pedidos)}")
        print(f"Pedidos entregues: {len(pedidos_entregues)}")
        print(f"Valor total de todos os pedidos: R$ {total_vendas:.2f}")
        print(f"Valor total de pedidos entregues: R$ {total_entregue:.2f}")
        
        # Produtos mais vendidos
        produtos_vendidos = {}
        for pedido in pedidos:
            for item in pedido.itens:
                if item.produto_id not in produtos_vendidos:
                    produtos_vendidos[item.produto_id] = 0
                produtos_vendidos[item.produto_id] += item.quantidade
        
        if produtos_vendidos:
            print("\nProdutos mais vendidos:")
            for produto_id, quantidade in sorted(produtos_vendidos.items(), 
                                                 key=lambda x: x[1], reverse=True)[:5]:
                produto = self.db.obter_produto(produto_id)
                print(f"  - {produto.nome}: {quantidade} unidades")


def main():
    """Função principal"""
    print("\nBem-vindo ao Sistema de Gestão de Confeitaria!")
    sistema = SistemaConfeitaria()
    sistema.menu_principal()


if __name__ == "__main__":
    main()
