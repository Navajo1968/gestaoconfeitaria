"""
Tests for the Bakery Management System
Testes para o Sistema de Gestão de Confeitaria
"""

import unittest
import os
from datetime import datetime, timedelta
from database import Database
from models import Produto, Cliente, Pedido, ItemPedido, Estoque, StatusPedido


class TestModels(unittest.TestCase):
    """Testes para os modelos de domínio"""
    
    def test_produto_creation(self):
        """Testa a criação de um produto"""
        produto = Produto(1, "Bolo de Chocolate", "Delicioso bolo", 50.0, 60)
        self.assertEqual(produto.nome, "Bolo de Chocolate")
        self.assertEqual(produto.preco, 50.0)
    
    def test_cliente_creation(self):
        """Testa a criação de um cliente"""
        cliente = Cliente(1, "João Silva", "11999999999", "joao@email.com")
        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(cliente.telefone, "11999999999")
    
    def test_item_pedido_subtotal(self):
        """Testa o cálculo de subtotal de um item"""
        item = ItemPedido(1, 1, 1, 3, 50.0)
        self.assertEqual(item.subtotal, 150.0)
    
    def test_pedido_valor_total(self):
        """Testa o cálculo do valor total de um pedido"""
        pedido = Pedido(1, 1, datetime.now(), datetime.now() + timedelta(days=1))
        pedido.adicionar_item(ItemPedido(1, 1, 1, 2, 50.0))
        pedido.adicionar_item(ItemPedido(2, 1, 2, 1, 30.0))
        self.assertEqual(pedido.valor_total, 130.0)
    
    def test_estoque_precisa_reposicao(self):
        """Testa a verificação de necessidade de reposição"""
        estoque_ok = Estoque(1, "Farinha", "kg", 10.0, 5.0)
        estoque_baixo = Estoque(2, "Açúcar", "kg", 3.0, 5.0)
        
        self.assertFalse(estoque_ok.precisa_reposicao)
        self.assertTrue(estoque_baixo.precisa_reposicao)


class TestDatabase(unittest.TestCase):
    """Testes para as operações de banco de dados"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.test_db_path = "test_confeitaria.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
    
    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_criar_e_obter_produto(self):
        """Testa criação e obtenção de produto"""
        produto = Produto(None, "Torta de Limão", "Torta fresca", 45.0, 90)
        produto_id = self.db.criar_produto(produto)
        
        produto_obtido = self.db.obter_produto(produto_id)
        self.assertIsNotNone(produto_obtido)
        self.assertEqual(produto_obtido.nome, "Torta de Limão")
        self.assertEqual(produto_obtido.preco, 45.0)
    
    def test_listar_produtos(self):
        """Testa listagem de produtos"""
        self.db.criar_produto(Produto(None, "Produto 1", "Desc 1", 10.0, 30))
        self.db.criar_produto(Produto(None, "Produto 2", "Desc 2", 20.0, 45))
        
        produtos = self.db.listar_produtos()
        self.assertEqual(len(produtos), 2)
    
    def test_atualizar_produto(self):
        """Testa atualização de produto"""
        produto = Produto(None, "Bolo Simples", "Desc", 30.0, 60)
        produto_id = self.db.criar_produto(produto)
        
        produto.id = produto_id
        produto.nome = "Bolo Premium"
        produto.preco = 50.0
        self.db.atualizar_produto(produto)
        
        produto_atualizado = self.db.obter_produto(produto_id)
        self.assertEqual(produto_atualizado.nome, "Bolo Premium")
        self.assertEqual(produto_atualizado.preco, 50.0)
    
    def test_excluir_produto(self):
        """Testa exclusão de produto"""
        produto = Produto(None, "Produto Temp", "Desc", 10.0, 30)
        produto_id = self.db.criar_produto(produto)
        
        self.db.excluir_produto(produto_id)
        produto_obtido = self.db.obter_produto(produto_id)
        self.assertIsNone(produto_obtido)
    
    def test_criar_e_obter_cliente(self):
        """Testa criação e obtenção de cliente"""
        cliente = Cliente(None, "Maria Santos", "11888888888", "maria@email.com")
        cliente_id = self.db.criar_cliente(cliente)
        
        cliente_obtido = self.db.obter_cliente(cliente_id)
        self.assertIsNotNone(cliente_obtido)
        self.assertEqual(cliente_obtido.nome, "Maria Santos")
        self.assertEqual(cliente_obtido.email, "maria@email.com")
    
    def test_criar_pedido_completo(self):
        """Testa criação de um pedido completo com itens"""
        # Cria cliente e produto
        cliente_id = self.db.criar_cliente(Cliente(None, "Pedro", "11777777777"))
        produto_id = self.db.criar_produto(Produto(None, "Bolo", "Desc", 40.0, 60))
        
        # Cria pedido
        pedido = Pedido(None, cliente_id, datetime.now(), 
                       datetime.now() + timedelta(days=2))
        pedido.adicionar_item(ItemPedido(None, None, produto_id, 2, 40.0))
        
        pedido_id = self.db.criar_pedido(pedido)
        
        # Verifica pedido criado
        pedido_obtido = self.db.obter_pedido(pedido_id)
        self.assertIsNotNone(pedido_obtido)
        self.assertEqual(len(pedido_obtido.itens), 1)
        self.assertEqual(pedido_obtido.valor_total, 80.0)
    
    def test_atualizar_status_pedido(self):
        """Testa atualização de status de pedido"""
        cliente_id = self.db.criar_cliente(Cliente(None, "Ana", "11666666666"))
        pedido = Pedido(None, cliente_id, datetime.now(), 
                       datetime.now() + timedelta(days=1))
        pedido_id = self.db.criar_pedido(pedido)
        
        self.db.atualizar_status_pedido(pedido_id, StatusPedido.EM_PRODUCAO)
        
        pedido_obtido = self.db.obter_pedido(pedido_id)
        self.assertEqual(pedido_obtido.status, StatusPedido.EM_PRODUCAO)
    
    def test_listar_pedidos_por_status(self):
        """Testa listagem de pedidos filtrados por status"""
        cliente_id = self.db.criar_cliente(Cliente(None, "Carlos", "11555555555"))
        
        pedido1 = Pedido(None, cliente_id, datetime.now(), 
                        datetime.now() + timedelta(days=1), StatusPedido.PENDENTE)
        pedido2 = Pedido(None, cliente_id, datetime.now(), 
                        datetime.now() + timedelta(days=2), StatusPedido.ENTREGUE)
        
        self.db.criar_pedido(pedido1)
        self.db.criar_pedido(pedido2)
        
        pedidos_pendentes = self.db.listar_pedidos(StatusPedido.PENDENTE)
        pedidos_entregues = self.db.listar_pedidos(StatusPedido.ENTREGUE)
        
        self.assertEqual(len(pedidos_pendentes), 1)
        self.assertEqual(len(pedidos_entregues), 1)
    
    def test_criar_e_obter_estoque(self):
        """Testa criação e obtenção de item de estoque"""
        item = Estoque(None, "Ovos", "dúzia", 10.0, 3.0)
        item_id = self.db.criar_item_estoque(item)
        
        item_obtido = self.db.obter_item_estoque(item_id)
        self.assertIsNotNone(item_obtido)
        self.assertEqual(item_obtido.nome, "Ovos")
        self.assertEqual(item_obtido.quantidade_atual, 10.0)
    
    def test_atualizar_quantidade_estoque(self):
        """Testa atualização de quantidade em estoque"""
        item = Estoque(None, "Leite", "litros", 5.0, 2.0)
        item_id = self.db.criar_item_estoque(item)
        
        self.db.atualizar_quantidade_estoque(item_id, 8.0)
        
        item_atualizado = self.db.obter_item_estoque(item_id)
        self.assertEqual(item_atualizado.quantidade_atual, 8.0)


if __name__ == '__main__':
    unittest.main()
