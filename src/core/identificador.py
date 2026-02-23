# src/core/identificador.py
"""
Módulo responsável por identificar qual modelo de planilha deve ser usado.
"""
import pandas as pd
from src.models.modelo_curva_abc import ModeloCurvaABC
from src.models.modelo_entradas import ModeloEntradas
from src.models.modelo_estoque import ModeloEstoque

class IdentificadorModelos:
    """Classe que identifica automaticamente o modelo da planilha"""
    
    def __init__(self):
        self.modelos = [
            ModeloCurvaABC(),
            ModeloEntradas(),
            ModeloEstoque(),
        ]
    
    def identificar(self, caminho_arquivo):
        """
        Identifica qual modelo de planilha deve ser usado.
        
        Args:
            caminho_arquivo: Caminho completo para o arquivo Excel
            
        Returns:
            tuple: (modelo, dataframe_completo) ou (None, None) se não identificado
        """
        try:
            print(f"\n🔍 Identificando arquivo: {caminho_arquivo}")
            
            # Ler apenas as primeiras 20 linhas para identificação
            df_amostra = pd.read_excel(caminho_arquivo, nrows=20)
            
            print(f"📊 Amostra: {df_amostra.shape[0]} linhas x {df_amostra.shape[1]} colunas")
            
            # Testar cada modelo
            for modelo in self.modelos:
                try:
                    if modelo.identificar(df_amostra):
                        print(f"✅ Modelo identificado: {modelo.nome}")
                        # Ler o arquivo completo
                        df_completo = pd.read_excel(caminho_arquivo)
                        return modelo, df_completo
                except Exception as e:
                    print(f"⚠️ Erro ao testar {modelo.nome}: {e}")
                    continue
            
            print("❌ Nenhum modelo identificado para este arquivo")
            return None, None
            
        except Exception as e:
            print(f"❌ Erro ao identificar arquivo: {e}")
            return None, None
    
    def identificar_com_df(self, df):
        """
        Identifica o modelo a partir de um DataFrame já carregado.
        
        Args:
            df: DataFrame do pandas
            
        Returns:
            ModeloBase or None: O modelo identificado ou None
        """
        try:
            for modelo in self.modelos:
                try:
                    if modelo.identificar(df):
                        print(f"✅ Modelo identificado: {modelo.nome}")
                        return modelo
                except:
                    continue
            return None
        except Exception as e:
            print(f"❌ Erro ao identificar: {e}")
            return None
    
    def listar_modelos(self):
        """Retorna lista com nomes de todos os modelos disponíveis"""
        return [modelo.nome for modelo in self.modelos]
    
    def get_modelo_por_nome(self, nome):
        """Retorna um modelo específico pelo nome"""
        for modelo in self.modelos:
            if modelo.nome.lower() == nome.lower():
                return modelo
        return None