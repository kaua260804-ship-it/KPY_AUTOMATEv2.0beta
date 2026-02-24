# src/config/media_vendas.py
"""
Arquivo com a média de vendas de todas as lojas.
Versão 2.1.0 - Com sistema de logs integrado
"""
import pandas as pd
import os
from src.utils.helpers import get_resource_path
from src.utils.logger import info, error, warning, debug

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
            info(f"📁 Carregando média de vendas de: {caminho}")
            
            if os.path.exists(caminho):
                self._df = pd.read_excel(caminho)
                info(f"✅ Média de vendas carregada: {len(self._df)} linhas")
                debug(f"📊 Colunas disponíveis: {list(self._df.columns)}")
                
                # Verificar se as colunas necessárias existem
                colunas_necessarias = ['Código', 'Loja', 'Qtd']
                colunas_faltando = [col for col in colunas_necessarias if col not in self._df.columns]
                
                if colunas_faltando:
                    warning(f"⚠️ Colunas faltando no arquivo de média: {colunas_faltando}")
                else:
                    debug("✅ Todas as colunas necessárias estão presentes")
                    
            else:
                warning(f"⚠️ Arquivo de média de vendas NÃO encontrado em: {caminho}")
                self._df = pd.DataFrame(columns=['Código', 'Loja', 'Qtd'])
                
        except Exception as e:
            error(f"❌ Erro ao carregar média de vendas: {e}")
            self._df = pd.DataFrame(columns=['Código', 'Loja', 'Qtd'])
    
    def get_df(self):
        """Retorna o DataFrame com as médias de vendas"""
        # Se estiver vazio, tenta carregar novamente
        if self._df is None or len(self._df) == 0:
            warning("⚠️ DataFrame vazio, tentando recarregar...")
            self._carregar_dados()
        
        # Garantir que nunca retorna None
        if self._df is None:
            error("❌ DataFrame permanece None, criando DataFrame vazio")
            self._df = pd.DataFrame(columns=['Código', 'Loja', 'Qtd'])
        
        return self._df
    
    def get_media_por_produto_loja(self, codigo, loja):
        """
        Retorna a média de vendas para um produto específico em uma loja.
        
        Args:
            codigo: Código do produto
            loja: Nome da loja
            
        Returns:
            float: Média de vendas ou 0 se não encontrado
        """
        df = self.get_df()
        
        if df is None or len(df) == 0:
            debug(f"📊 DataFrame vazio, retornando 0 para {codigo} - {loja}")
            return 0
        
        try:
            # Converter para string para comparação segura
            codigo_str = str(codigo).strip()
            loja_str = str(loja).strip().upper()
            
            # Filtrar por código e loja
            filtro = df[
                (df['Código'].astype(str).str.strip() == codigo_str) & 
                (df['Loja'].astype(str).str.strip().str.upper() == loja_str)
            ]
            
            if len(filtro) > 0:
                valor = float(filtro.iloc[0]['Qtd'])
                debug(f"📊 Média encontrada: {codigo} - {loja} = {valor}")
                return valor
            else:
                debug(f"📊 Média NÃO encontrada: {codigo} - {loja}")
                return 0
                
        except Exception as e:
            error(f"❌ Erro ao buscar média para {codigo} - {loja}: {e}")
            return 0
    
    def get_media_por_produto(self, codigo):
        """
        Retorna a média de vendas para um produto em todas as lojas.
        
        Args:
            codigo: Código do produto
            
        Returns:
            float: Média de vendas ou 0 se não encontrado
        """
        df = self.get_df()
        
        if df is None or len(df) == 0:
            debug(f"📊 DataFrame vazio, retornando 0 para {codigo}")
            return 0
        
        try:
            codigo_str = str(codigo).strip()
            
            filtro = df[df['Código'].astype(str).str.strip() == codigo_str]
            
            if len(filtro) > 0:
                valor = float(filtro['Qtd'].mean())
                debug(f"📊 Média global para {codigo}: {valor} (baseado em {len(filtro)} lojas)")
                return valor
            else:
                debug(f"📊 Média global NÃO encontrada para {codigo}")
                return 0
                
        except Exception as e:
            error(f"❌ Erro ao buscar média global para {codigo}: {e}")
            return 0
    
    def get_estatisticas(self):
        """
        Retorna estatísticas sobre os dados de média de vendas.
        
        Returns:
            dict: Dicionário com estatísticas
        """
        df = self.get_df()
        
        if df is None or len(df) == 0:
            return {
                'total_registros': 0,
                'total_produtos': 0,
                'total_lojas': 0,
                'media_global': 0
            }
        
        try:
            stats = {
                'total_registros': len(df),
                'total_produtos': df['Código'].nunique() if 'Código' in df.columns else 0,
                'total_lojas': df['Loja'].nunique() if 'Loja' in df.columns else 0,
                'media_global': float(df['Qtd'].mean()) if 'Qtd' in df.columns else 0,
                'minimo': float(df['Qtd'].min()) if 'Qtd' in df.columns else 0,
                'maximo': float(df['Qtd'].max()) if 'Qtd' in df.columns else 0
            }
            
            info(f"📊 Estatísticas da média de vendas: {stats['total_registros']} registros, "
                 f"{stats['total_produtos']} produtos, {stats['total_lojas']} lojas")
            
            return stats
            
        except Exception as e:
            error(f"❌ Erro ao calcular estatísticas: {e}")
            return {
                'total_registros': len(df),
                'total_produtos': 0,
                'total_lojas': 0,
                'media_global': 0
            }

# Singleton para uso em todo o sistema
media_vendas = MediaVendas()

# Função de conveniência para acesso rápido
def get_media_vendas():
    """Retorna a instância singleton de MediaVendas"""
    return media_vendas