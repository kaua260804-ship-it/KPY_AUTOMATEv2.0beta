# src/models/base.py
from abc import ABC, abstractmethod

class ModeloBase(ABC):
    def __init__(self):
        self.nome = "Base"
        self.df_processado = None
    
    @abstractmethod
    def identificar(self, df):
        pass
    
    @abstractmethod
    def processar(self, df):
        pass
    
    def get_resumo(self, df):
        return "Resumo não implementado"
    
    def get_preview(self, df, linhas=20):
        return "Preview não implementado"