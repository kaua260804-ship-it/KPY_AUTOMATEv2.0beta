# src/relatorios/base_relatorio.py
"""
Classe base para todos os relatórios.
"""
from abc import ABC, abstractmethod

class RelatorioBase(ABC):
    """Classe base abstrata para relatórios"""
    
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
    
    @abstractmethod
    def gerar(self, df_combinado):
        """
        Gera o relatório a partir do DataFrame combinado.
        Retorna uma string com o preview e os dados processados.
        """
        pass
    
    def get_preview(self, df_combinado):
        """Gera preview do relatório (pode ser sobrescrito)"""
        return self.gerar(df_combinado)