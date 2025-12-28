"""
Sistema de Gestão de Confeitaria
Bakery Management System

Este módulo contém as classes de domínio para o sistema de gestão.
"""

from datetime import datetime
from typing import List, Optional
from enum import Enum


class StatusPedido(Enum):
    """Status possíveis de um pedido"""
    PENDENTE = "pendente"
    EM_PRODUCAO = "em_producao"
    PRONTO = "pronto"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class Produto:
    """Representa um produto da confeitaria"""
    
    def __init__(self, id: Optional[int], nome: str, descricao: str, 
                 preco: float, tempo_preparo_minutos: int):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.tempo_preparo_minutos = tempo_preparo_minutos
    
    def __repr__(self):
        return f"Produto(id={self.id}, nome='{self.nome}', preco={self.preco})"


class Cliente:
    """Representa um cliente da confeitaria"""
    
    def __init__(self, id: Optional[int], nome: str, telefone: str, 
                 email: Optional[str] = None, endereco: Optional[str] = None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
    
    def __repr__(self):
        return f"Cliente(id={self.id}, nome='{self.nome}', telefone='{self.telefone}')"


class ItemPedido:
    """Representa um item dentro de um pedido"""
    
    def __init__(self, id: Optional[int], pedido_id: Optional[int], 
                 produto_id: int, quantidade: int, preco_unitario: float,
                 observacoes: Optional[str] = None):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.observacoes = observacoes
    
    @property
    def subtotal(self) -> float:
        """Calcula o subtotal do item"""
        return self.quantidade * self.preco_unitario
    
    def __repr__(self):
        return f"ItemPedido(produto_id={self.produto_id}, quantidade={self.quantidade})"


class Pedido:
    """Representa um pedido de cliente"""
    
    def __init__(self, id: Optional[int], cliente_id: int, 
                 data_pedido: datetime, data_entrega: datetime,
                 status: StatusPedido = StatusPedido.PENDENTE,
                 observacoes: Optional[str] = None):
        self.id = id
        self.cliente_id = cliente_id
        self.data_pedido = data_pedido
        self.data_entrega = data_entrega
        self.status = status
        self.observacoes = observacoes
        self.itens: List[ItemPedido] = []
    
    @property
    def valor_total(self) -> float:
        """Calcula o valor total do pedido"""
        return sum(item.subtotal for item in self.itens)
    
    def adicionar_item(self, item: ItemPedido):
        """Adiciona um item ao pedido"""
        self.itens.append(item)
    
    def __repr__(self):
        return f"Pedido(id={self.id}, cliente_id={self.cliente_id}, status={self.status.value})"


class Estoque:
    """Representa um item de estoque/ingrediente"""
    
    def __init__(self, id: Optional[int], nome: str, unidade_medida: str,
                 quantidade_atual: float, quantidade_minima: float):
        self.id = id
        self.nome = nome
        self.unidade_medida = unidade_medida
        self.quantidade_atual = quantidade_atual
        self.quantidade_minima = quantidade_minima
    
    @property
    def precisa_reposicao(self) -> bool:
        """Verifica se o item precisa de reposição"""
        return self.quantidade_atual <= self.quantidade_minima
    
    def __repr__(self):
        return f"Estoque(id={self.id}, nome='{self.nome}', quantidade={self.quantidade_atual} {self.unidade_medida})"
