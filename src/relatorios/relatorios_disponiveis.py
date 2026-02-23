# src/relatorios/relatorios_disponiveis.py
"""
Módulo com todos os relatórios disponíveis no sistema.
"""
import pandas as pd
import numpy as np
from src.relatorios.base_relatorio import RelatorioBase
from src.config.media_vendas import media_vendas

class RelatorioRaw(RelatorioBase):
    """Relatório com dados brutos combinados"""
    
    def __init__(self):
        super().__init__(
            nome="📋 Dados Combinados (Raw)",
            descricao="Exibe os dados brutos de todos os arquivos combinados"
        )
    
    def gerar(self, df_combinado):
        if df_combinado is None or len(df_combinado) == 0:
            return "Nenhum dado para gerar relatório"
        
        linhas = []
        linhas.append("=" * 100)
        linhas.append(f"📋 {self.nome}")
        linhas.append("=" * 100)
        linhas.append("")
        linhas.append(f"Total de linhas: {len(df_combinado)}")
        linhas.append(f"Total de colunas: {len(df_combinado.columns)}")
        linhas.append("")
        
        # Mostrar primeiras colunas
        colunas_para_mostrar = []
        for col in ['Codigo', 'Código', 'Produto', 'Qtd', 'Total', 'Categoria', 'Grupo', 'Comprador']:
            if col in df_combinado.columns:
                colunas_para_mostrar.append(col)
        
        if colunas_para_mostrar:
            preview_df = df_combinado[colunas_para_mostrar].head(20)
            linhas.append(preview_df.to_string(index=False))
        else:
            primeiras_cols = df_combinado.columns[:5].tolist()
            preview_df = df_combinado[primeiras_cols].head(20)
            linhas.append(preview_df.to_string(index=False))
        
        return "\n".join(linhas)


class RelatorioVendas(RelatorioBase):
    """Relatório de análise de vendas por loja"""
    
    def __init__(self):
        super().__init__(
            nome="📈 Análise de Vendas por Loja",
            descricao="Analisa vendas agrupadas por loja a partir da Curva ABC"
        )
    
    def gerar(self, df_combinado):
        preview = f"{self.nome}\n"
        preview += "=" * 80 + "\n\n"
        preview += "Em desenvolvimento...\n\n"
        preview += "Este relatório será implementado em breve!\n\n"
        preview += f"Dados disponíveis: {len(df_combinado)} linhas"
        
        return preview


class RelatorioEntradas(RelatorioBase):
    """Relatório de análise de entradas por categoria"""
    
    def __init__(self):
        super().__init__(
            nome="📊 Análise de Entradas por Categoria",
            descricao="Analisa entradas agrupadas por categoria/grupo"
        )
    
    def gerar(self, df_combinado):
        preview = f"{self.nome}\n"
        preview += "=" * 80 + "\n\n"
        preview += "Em desenvolvimento...\n\n"
        preview += "Este relatório será implementado em breve!\n\n"
        preview += f"Dados disponíveis: {len(df_combinado)} linhas"
        
        return preview


class RelatorioComparativo(RelatorioBase):
    """Relatório comparativo entre vendas e entradas"""
    
    def __init__(self):
        super().__init__(
            nome="🔄 Comparativo Vendas x Entradas",
            descricao="Compara dados de vendas com entradas para análise de ruptura"
        )
    
    def gerar(self, df_combinado):
        preview = f"{self.nome}\n"
        preview += "=" * 80 + "\n\n"
        preview += "Em desenvolvimento...\n\n"
        preview += "Este relatório será implementado em breve!\n\n"
        preview += f"Dados disponíveis: {len(df_combinado)} linhas"
        
        return preview


class RelatorioRuptura(RelatorioBase):
    """Relatório de Ruptura (combina Curva ABC, Estoque e Média de Vendas)"""
    
    def __init__(self):
        super().__init__(
            nome="📉 Ruptura - Análise de Disponibilidade",
            descricao="Analisa produtos que estão em ruptura baseado em vendas e estoque"
        )
    
    def _criar_cadeamento(self, codigo, produto, loja):
        """Cria o cadeamento no formato CÓDIGO-PRODUTO-LOJA"""
        return f"{codigo}-{produto}-{loja}"
    
    def _extrair_loja(self, texto):
        """Extrai o nome da loja de uma string"""
        if pd.isna(texto):
            return ""
        return str(texto).strip()
    
    def gerar(self, df_combinado):
        """
        Gera relatório de ruptura.
        """
        if df_combinado is None or len(df_combinado) == 0:
            return "Nenhum dado para gerar relatório"
        
        linhas = []
        linhas.append("=" * 120)
        linhas.append(f"📉 {self.nome}")
        linhas.append("=" * 120)
        linhas.append("")
        
        # Carregar média de vendas
        df_media = media_vendas.get_df()
        if df_media is None or len(df_media) == 0:
            linhas.append("❌ Média de vendas não disponível!")
            linhas.append("   Verifique se o arquivo media_vendas.xlsx está na pasta data/")
            return "\n".join(linhas)
        
        linhas.append(f"✅ Média de vendas carregada: {len(df_media)} registros")
        linhas.append("")
        
        # Identificar os DataFrames de origem
        df_curva = None
        df_estoque = None
        
        # Separar os dados (assumindo que vieram combinados)
        # Vamos tentar identificar pelas colunas
        if 'Loja_Nome' in df_combinado.columns and 'Qtd' in df_combinado.columns:
            df_curva = df_combinado[['Código', 'Produto', 'Qtd', 'Total R$', 'Loja_Nome']].copy()
            df_curva.rename(columns={'Loja_Nome': 'Loja', 'Qtd': 'Vendas_Mes_Atual'}, inplace=True)
        
        if 'Estoque_Loja' in df_combinado.columns:
            cols_estoque = ['Codigo', 'Descricao', 'Estoque_Loja', 'Estoque_Geral', 'Categoria', 'Grupo', 'Loja']
            cols_existentes = [col for col in cols_estoque if col in df_combinado.columns]
            df_estoque = df_combinado[cols_existentes].copy()
            df_estoque.rename(columns={'Codigo': 'Código', 'Descricao': 'Produto'}, inplace=True)
        
        if df_curva is None or df_estoque is None:
            linhas.append("❌ Dados insuficientes para gerar relatório de ruptura.")
            linhas.append("   É necessário ter dados de Curva ABC e Estoque.")
            return "\n".join(linhas)
        
        # Identificar a loja MATRIZ
        matriz_nome = "COMCARNE MATRIZ SAO LUIS"
        
        # Extrair estoque da matriz
        estoque_matriz = {}
        for _, row in df_estoque.iterrows():
            if row['Loja'] == matriz_nome:
                codigo = str(row['Código'])
                estoque_matriz[codigo] = row['Estoque_Loja']
        
        linhas.append(f"🏢 Matriz identificada: {matriz_nome}")
        linhas.append(f"📦 Produtos com estoque na matriz: {len(estoque_matriz)}")
        linhas.append("")
        
        # Criar DataFrame de resultados
        resultados = []
        
        # Processar cada produto da Curva ABC
        for _, venda in df_curva.iterrows():
            codigo = str(venda['Código'])
            produto = venda['Produto']
            loja = venda['Loja']
            vendas_mes = venda['Vendas_Mes_Atual']
            
            # Buscar estoque da loja
            estoque_loja = 0
            estoque_loja_row = df_estoque[
                (df_estoque['Código'].astype(str) == codigo) & 
                (df_estoque['Loja'] == loja)
            ]
            if len(estoque_loja_row) > 0:
                estoque_loja = estoque_loja_row.iloc[0]['Estoque_Loja']
            
            # Buscar estoque da matriz
            estoque_matriz_val = estoque_matriz.get(codigo, 0)
            
            # Buscar categoria e grupo do estoque
            categoria = ""
            grupo = ""
            cat_row = df_estoque[df_estoque['Código'].astype(str) == codigo]
            if len(cat_row) > 0:
                if 'Categoria' in cat_row.columns:
                    categoria = cat_row.iloc[0]['Categoria']
                if 'Grupo' in cat_row.columns:
                    grupo = cat_row.iloc[0]['Grupo']
            
            # Buscar média de vendas mensal
            media_vendas_val = media_vendas.get_media_por_produto_loja(codigo, loja)
            if media_vendas_val == 0:
                media_vendas_val = media_vendas.get_media_por_produto(codigo)
            
            # Criar cadeamento
            cadeamento = self._criar_cadeamento(codigo, produto, loja)
            
            # Adicionar ao resultado
            resultados.append({
                'CATEGORIA': categoria,
                'GRUPO': grupo,
                'Cadeamento': cadeamento,
                'CÓDIGO': codigo,
                'PRODUTO': produto,
                'ESTQ LOJA': estoque_loja,
                'ESTQ MATRIZ': estoque_matriz_val,
                'VENDAS MÊS ATUAL': vendas_mes,
                'MÉDIA VENDA MENSAL': media_vendas_val
            })
        
        # Criar DataFrame de resultados
        df_resultado = pd.DataFrame(resultados)
        
        # Ordenar por categoria e grupo
        if len(df_resultado) > 0:
            df_resultado = df_resultado.sort_values(['CATEGORIA', 'GRUPO', 'PRODUTO'])
        
        # Calcular estatísticas
        total_linhas = len(df_resultado)
        produtos_com_ruptura = len(df_resultado[df_resultado['ESTQ LOJA'] == 0])
        produtos_abaixo_media = len(df_resultado[df_resultado['ESTQ LOJA'] < df_resultado['MÉDIA VENDA MENSAL']])
        
        # Adicionar ao preview
        linhas.append("📊 ESTATÍSTICAS GERAIS:")
        linhas.append(f"   • Total de produtos analisados: {total_linhas}")
        linhas.append(f"   • Produtos em ruptura (estoque 0): {produtos_com_ruptura}")
        linhas.append(f"   • Produtos com estoque abaixo da média: {produtos_abaixo_media}")
        linhas.append("")
        
        # Mostrar preview dos resultados
        linhas.append("📋 PRIMEIRAS 20 LINHAS DO RELATÓRIO DE RUPTURA:")
        linhas.append("-" * 120)
        
        # Formatar números para exibição
        df_preview = df_resultado.head(20).copy()
        for col in ['ESTQ LOJA', 'ESTQ MATRIZ', 'VENDAS MÊS ATUAL', 'MÉDIA VENDA MENSAL']:
            if col in df_preview.columns:
                df_preview[col] = df_preview[col].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
        # Adicionar ao preview
        linhas.append(df_preview.to_string(index=False))
        
        # Salvar o DataFrame para exportação
        self.df_resultado = df_resultado
        
        return "\n".join(linhas)
    
    def get_df_resultado(self):
        """Retorna o DataFrame do resultado para exportação"""
        return getattr(self, 'df_resultado', None)


class RelatorioExemplo(RelatorioBase):
    """Relatório de exemplo (Modelo 1)"""
    
    def __init__(self):
        super().__init__(
            nome="📁 Modelo 1 - Relatório Exemplo",
            descricao="Relatório de exemplo para testes e demonstração"
        )
    
    def gerar(self, df_combinado):
        preview = f"{self.nome}\n"
        preview += "=" * 80 + "\n\n"
        preview += "Este é um relatório de exemplo para testes.\n\n"
        preview += "📊 INFORMAÇÕES DOS DADOS:\n"
        preview += f"• Total de linhas: {len(df_combinado)}\n"
        preview += f"• Total de colunas: {len(df_combinado.columns)}\n"
        preview += f"• Colunas: {', '.join(df_combinado.columns[:10])}\n"
        
        if len(df_combinado.columns) > 10:
            preview += f"• ... e mais {len(df_combinado.columns) - 10} colunas\n"
        
        preview += "\n📈 ESTATÍSTICAS BÁSICAS:\n"
        
        # Tentar mostrar algumas estatísticas
        if 'Qtd' in df_combinado.columns:
            preview += f"• Quantidade total: {df_combinado['Qtd'].sum():,.2f}\n"
        
        if 'Total' in df_combinado.columns:
            preview += f"• Valor total: R$ {df_combinado['Total'].sum():,.2f}\n"
        
        if 'Estoque_Geral' in df_combinado.columns:
            preview += f"• Estoque Geral: {df_combinado['Estoque_Geral'].sum():,.2f}\n"
        
        if 'Codigo' in df_combinado.columns or 'Código' in df_combinado.columns:
            col_cod = 'Codigo' if 'Codigo' in df_combinado.columns else 'Código'
            preview += f"• Produtos únicos: {df_combinado[col_cod].nunique()}\n"
        
        return preview


class GerenciadorRelatorios:
    """Gerencia todos os relatórios disponíveis no sistema"""
    
    def __init__(self):
        self.relatorios = {
            'raw': RelatorioRaw(),
            'exemplo': RelatorioExemplo(),
        }
        
        self.relatorios_condicionais = {
            'vendas': RelatorioVendas(),
            'entradas': RelatorioEntradas(),
            'comparativo': RelatorioComparativo(),
            'ruptura': RelatorioRuptura(),
        }
    
    def get_relatorios_disponiveis(self, tipos_arquivos=None):
        """
        Retorna lista de relatórios disponíveis baseado nos tipos de arquivo.
        
        Args:
            tipos_arquivos: Lista de nomes dos modelos identificados
        """
        relatorios = []  # Removido o raw da lista padrão
        
        if tipos_arquivos:
            tipos_set = set(tipos_arquivos)
            
            # Verificar se tem Curva ABC e Estoque (necessários para Ruptura)
            if "Curva ABC por Loja" in tipos_set and "Estoque" in tipos_set:
                relatorios.append(self.relatorios_condicionais['ruptura'])
        
        # Se não tiver nenhum relatório condicional, mostra apenas o exemplo
        if not relatorios:
            relatorios.append(self.relatorios['exemplo'])
        
        return relatorios
    
    def get_relatorio_por_nome(self, nome):
        """Busca um relatório pelo nome"""
        for relatorio in list(self.relatorios.values()) + list(self.relatorios_condicionais.values()):
            if relatorio.nome == nome:
                return relatorio
        return None
    
    def listar_todos_relatorios(self):
        """Retorna lista com todos os relatórios disponíveis"""
        todos = list(self.relatorios.values()) + list(self.relatorios_condicionais.values())
        return todos