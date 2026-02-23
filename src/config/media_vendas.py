# src/config/media_vendas.py
"""
Arquivo com a média de vendas de todas as lojas.
"""
import pandas as pd
import os
from src.utils.helpers import get_resource_path

class MediaVendas:
    """Classe para gerenciar os dados de média de vendas"""
    
    _instance = None
    _df = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._carregar_dados()
        return cls._instance
    
    def _carregar_dados(self):
        """Carrega os dados da planilha de média de vendas"""
        try:
            caminho = get_resource_path("data/media_vendas.xlsx")
            print(f"📁 Carregando média de vendas de: {caminho}")
            
            if os.path.exists(caminho):
                self._df = pd.read_excel(caminho)
                print(f"✅ Média de vendas carregada: {len(self._df)} linhas")
            else:
                print(f"⚠️ Arquivo de média de vendas NÃO encontrado!")
                self._df = pd.DataFrame()
        except Exception as e:
            print(f"❌ Erro ao carregar média de vendas: {e}")
            self._df = pd.DataFrame()
    
    def get_df(self):
        """Retorna o DataFrame com as médias de vendas"""
        # Se estiver vazio, tenta carregar novamente
        if self._df is None or len(self._df) == 0:
            print("⚠️ DataFrame vazio, recarregando...")
            self._carregar_dados()
        return self._df
    
    def get_media_por_produto_loja(self, codigo, loja):
        """
        Retorna a média de vendas para um produto específico em uma loja.
        """
        df = self.get_df()  # Usa o get_df que tenta recarregar
        if df is None or len(df) == 0:
            return 0
        
        filtro = df[
            (df['Código'].astype(str) == str(codigo)) & 
            (df['Loja'].str.upper() == str(loja).upper())
        ]
        
        if len(filtro) > 0:
            return filtro.iloc[0]['Qtd']
        return 0
    
    def get_media_por_produto(self, codigo):
        """
        Retorna a média de vendas para um produto em todas as lojas.
        """
        df = self.get_df()  # Usa o get_df que tenta recarregar
        if df is None or len(df) == 0:
            return 0
        
        filtro = df[df['Código'].astype(str) == str(codigo)]
        if len(filtro) > 0:
            return filtro['Qtd'].mean()
        return 0

# Singleton para uso em todo o sistema
media_vendas = MediaVendas()