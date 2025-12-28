"""
Database layer for the bakery management system
Camada de banco de dados para o sistema de gestão
"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from models import Produto, Cliente, Pedido, ItemPedido, Estoque, StatusPedido


class Database:
    """Gerencia a conexão e operações com o banco de dados"""
    
    def __init__(self, db_path: str = "gestao_confeitaria.db"):
        self.db_path = db_path
        self.criar_tabelas()
    
    def get_connection(self):
        """Cria uma conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def criar_tabelas(self):
        """Cria as tabelas do banco de dados se não existirem"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                tempo_preparo_minutos INTEGER NOT NULL
            )
        ''')
        
        # Tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT,
                endereco TEXT
            )
        ''')
        
        # Tabela de pedidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                data_pedido TEXT NOT NULL,
                data_entrega TEXT NOT NULL,
                status TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        # Tabela de itens de pedido
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        
        # Tabela de estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                unidade_medida TEXT NOT NULL,
                quantidade_atual REAL NOT NULL,
                quantidade_minima REAL NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ==================== PRODUTOS ====================
    
    def criar_produto(self, produto: Produto) -> int:
        """Cria um novo produto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, preco, tempo_preparo_minutos)
            VALUES (?, ?, ?, ?)
        ''', (produto.nome, produto.descricao, produto.preco, produto.tempo_preparo_minutos))
        produto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return produto_id
    
    def obter_produto(self, produto_id: int) -> Optional[Produto]:
        """Obtém um produto pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Produto(row['id'], row['nome'], row['descricao'], 
                          row['preco'], row['tempo_preparo_minutos'])
        return None
    
    def listar_produtos(self) -> List[Produto]:
        """Lista todos os produtos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos ORDER BY nome')
        rows = cursor.fetchall()
        conn.close()
        
        return [Produto(row['id'], row['nome'], row['descricao'],
                       row['preco'], row['tempo_preparo_minutos'])
                for row in rows]
    
    def atualizar_produto(self, produto: Produto):
        """Atualiza um produto existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produtos 
            SET nome = ?, descricao = ?, preco = ?, tempo_preparo_minutos = ?
            WHERE id = ?
        ''', (produto.nome, produto.descricao, produto.preco, 
              produto.tempo_preparo_minutos, produto.id))
        conn.commit()
        conn.close()
    
    def excluir_produto(self, produto_id: int):
        """Exclui um produto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conn.commit()
        conn.close()
    
    # ==================== CLIENTES ====================
    
    def criar_cliente(self, cliente: Cliente) -> int:
        """Cria um novo cliente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, telefone, email, endereco)
            VALUES (?, ?, ?, ?)
        ''', (cliente.nome, cliente.telefone, cliente.email, cliente.endereco))
        cliente_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cliente_id
    
    def obter_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Obtém um cliente pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Cliente(row['id'], row['nome'], row['telefone'],
                          row['email'], row['endereco'])
        return None
    
    def listar_clientes(self) -> List[Cliente]:
        """Lista todos os clientes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY nome')
        rows = cursor.fetchall()
        conn.close()
        
        return [Cliente(row['id'], row['nome'], row['telefone'],
                       row['email'], row['endereco'])
                for row in rows]
    
    def atualizar_cliente(self, cliente: Cliente):
        """Atualiza um cliente existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clientes 
            SET nome = ?, telefone = ?, email = ?, endereco = ?
            WHERE id = ?
        ''', (cliente.nome, cliente.telefone, cliente.email, cliente.endereco, cliente.id))
        conn.commit()
        conn.close()
    
    def excluir_cliente(self, cliente_id: int):
        """Exclui um cliente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        conn.commit()
        conn.close()
    
    # ==================== PEDIDOS ====================
    
    def criar_pedido(self, pedido: Pedido) -> int:
        """Cria um novo pedido com seus itens"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insere o pedido
        cursor.execute('''
            INSERT INTO pedidos (cliente_id, data_pedido, data_entrega, status, observacoes)
            VALUES (?, ?, ?, ?, ?)
        ''', (pedido.cliente_id, pedido.data_pedido.isoformat(), 
              pedido.data_entrega.isoformat(), pedido.status.value, pedido.observacoes))
        pedido_id = cursor.lastrowid
        
        # Insere os itens do pedido
        for item in pedido.itens:
            cursor.execute('''
                INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario, observacoes)
                VALUES (?, ?, ?, ?, ?)
            ''', (pedido_id, item.produto_id, item.quantidade, item.preco_unitario, item.observacoes))
        
        conn.commit()
        conn.close()
        return pedido_id
    
    def obter_pedido(self, pedido_id: int) -> Optional[Pedido]:
        """Obtém um pedido completo pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Busca o pedido
        cursor.execute('SELECT * FROM pedidos WHERE id = ?', (pedido_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        pedido = Pedido(
            row['id'], row['cliente_id'],
            datetime.fromisoformat(row['data_pedido']),
            datetime.fromisoformat(row['data_entrega']),
            StatusPedido(row['status']),
            row['observacoes']
        )
        
        # Busca os itens do pedido
        cursor.execute('SELECT * FROM itens_pedido WHERE pedido_id = ?', (pedido_id,))
        item_rows = cursor.fetchall()
        
        for item_row in item_rows:
            item = ItemPedido(
                item_row['id'], item_row['pedido_id'], item_row['produto_id'],
                item_row['quantidade'], item_row['preco_unitario'], item_row['observacoes']
            )
            pedido.adicionar_item(item)
        
        conn.close()
        return pedido
    
    def listar_pedidos(self, status: Optional[StatusPedido] = None) -> List[Pedido]:
        """Lista todos os pedidos, opcionalmente filtrando por status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM pedidos WHERE status = ? ORDER BY data_entrega', 
                          (status.value,))
        else:
            cursor.execute('SELECT * FROM pedidos ORDER BY data_entrega')
        
        rows = cursor.fetchall()
        pedidos = []
        
        for row in rows:
            pedido = Pedido(
                row['id'], row['cliente_id'],
                datetime.fromisoformat(row['data_pedido']),
                datetime.fromisoformat(row['data_entrega']),
                StatusPedido(row['status']),
                row['observacoes']
            )
            
            # Busca os itens do pedido
            cursor.execute('SELECT * FROM itens_pedido WHERE pedido_id = ?', (row['id'],))
            item_rows = cursor.fetchall()
            
            for item_row in item_rows:
                item = ItemPedido(
                    item_row['id'], item_row['pedido_id'], item_row['produto_id'],
                    item_row['quantidade'], item_row['preco_unitario'], item_row['observacoes']
                )
                pedido.adicionar_item(item)
            
            pedidos.append(pedido)
        
        conn.close()
        return pedidos
    
    def atualizar_status_pedido(self, pedido_id: int, novo_status: StatusPedido):
        """Atualiza o status de um pedido"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE pedidos SET status = ? WHERE id = ?', 
                      (novo_status.value, pedido_id))
        conn.commit()
        conn.close()
    
    def excluir_pedido(self, pedido_id: int):
        """Exclui um pedido e seus itens"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM itens_pedido WHERE pedido_id = ?', (pedido_id,))
        cursor.execute('DELETE FROM pedidos WHERE id = ?', (pedido_id,))
        conn.commit()
        conn.close()
    
    # ==================== ESTOQUE ====================
    
    def criar_item_estoque(self, item: Estoque) -> int:
        """Cria um novo item de estoque"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO estoque (nome, unidade_medida, quantidade_atual, quantidade_minima)
            VALUES (?, ?, ?, ?)
        ''', (item.nome, item.unidade_medida, item.quantidade_atual, item.quantidade_minima))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id
    
    def obter_item_estoque(self, item_id: int) -> Optional[Estoque]:
        """Obtém um item de estoque pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Estoque(row['id'], row['nome'], row['unidade_medida'],
                          row['quantidade_atual'], row['quantidade_minima'])
        return None
    
    def listar_estoque(self) -> List[Estoque]:
        """Lista todos os itens de estoque"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque ORDER BY nome')
        rows = cursor.fetchall()
        conn.close()
        
        return [Estoque(row['id'], row['nome'], row['unidade_medida'],
                       row['quantidade_atual'], row['quantidade_minima'])
                for row in rows]
    
    def atualizar_quantidade_estoque(self, item_id: int, nova_quantidade: float):
        """Atualiza a quantidade de um item de estoque"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE estoque SET quantidade_atual = ? WHERE id = ?', 
                      (nova_quantidade, item_id))
        conn.commit()
        conn.close()
    
    def excluir_item_estoque(self, item_id: int):
        """Exclui um item de estoque"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM estoque WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
