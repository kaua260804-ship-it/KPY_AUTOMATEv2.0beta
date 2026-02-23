# src/models/modelo_curva_abc.py
"""
Modelo para processar relatórios de Curva ABC por Loja.
"""
import pandas as pd
from src.models.base import ModeloBase

class ModeloCurvaABC(ModeloBase):
    """Modelo específico para Curva ABC por Loja"""
    
    def __init__(self):
        super().__init__()
        self.nome = "Curva ABC por Loja"
        self.descricao = "Processa relatórios de vendas com cabeçalho na linha 4"
    
    def identificar(self, df):
        """
        Verifica se a planilha é do tipo Curva ABC.
        Procura por "Código" e "Loja:" nas primeiras linhas.
        """
        try:
            # Pega as primeiras 10 linhas da primeira coluna
            primeiras_linhas = df.iloc[:10, 0].astype(str).str.lower()
            
            # Verifica se tem "código" e "loja:"
            tem_codigo = any('código' in str(x).lower() for x in primeiras_linhas)
            tem_loja = any('loja:' in str(x).lower() for x in primeiras_linhas)
            
            return tem_codigo and tem_loja
        except:
            return False
    
    def _is_valid_product(self, x):
        """Verifica se uma linha corresponde a um produto válido"""
        try:
            val = str(x).strip()
            if val == '' or val == 'nan' or pd.isna(x) or val == 'None':
                return False
            if not val[0].isdigit():
                return False
            val_num = val.replace(',', '.')
            float(val_num)
            return True
        except:
            return False
    
    def processar(self, df):
        """
        Processa o relatório de Curva ABC por Loja.
        """
        try:
            # PASSO 1: Organizar os dados (cabeçalho na linha 4)
            linha_cabecalho = 4
            df_dados = df.iloc[linha_cabecalho:].copy()
            df_dados.columns = df_dados.iloc[0]
            df_dados = df_dados.iloc[1:].reset_index(drop=True)
            
            # PASSO 2: Criar colunas para loja
            df_dados['Loja_Codigo'] = ''
            df_dados['Loja_Nome'] = ''
            
            # PASSO 3: Preencher loja para cada produto
            loja_atual_codigo = ''
            loja_atual_nome = ''
            
            for i in range(len(df_dados)):
                valor_codigo = str(df_dados.iloc[i, 0])
                
                if 'Loja:' in valor_codigo:
                    codigo_loja = df_dados.iloc[i, 1]
                    nome_loja = df_dados.iloc[i, 2]
                    
                    loja_atual_codigo = str(codigo_loja) if pd.notna(codigo_loja) else ''
                    loja_atual_nome = str(nome_loja) if pd.notna(nome_loja) else ''
                else:
                    df_dados.loc[i, 'Loja_Codigo'] = loja_atual_codigo
                    df_dados.loc[i, 'Loja_Nome'] = loja_atual_nome
            
            # PASSO 4: Remover linhas que são loja
            df_limpo = df_dados[~df_dados.iloc[:, 0].astype(str).str.contains('Loja:', na=False)].copy()
            
            # PASSO 5: Remover linhas onde a primeira coluna não é número
            mask_produto = df_limpo.iloc[:, 0].apply(self._is_valid_product)
            df_limpo = df_limpo[mask_produto].copy()
            df_limpo = df_limpo.reset_index(drop=True)
            
            # PASSO 6: Converter colunas para número
            colunas_para_converter = ['Código', 'Qtd', 'Total R$', 'Loja_Codigo']
            for coluna in colunas_para_converter:
                if coluna in df_limpo.columns:
                    df_limpo[coluna] = df_limpo[coluna].astype(str).str.replace(',', '.')
                    df_limpo[coluna] = pd.to_numeric(df_limpo[coluna], errors='coerce')
            
            self.df_original = df
            self.df_processado = df_limpo
            return df_limpo
            
        except Exception as e:
            raise Exception(f"Erro no processamento: {str(e)}")
    
    def _formatar_br(self, valor, tipo='moeda'):
        """Formata números no padrão brasileiro"""
        if pd.isna(valor) or valor == '':
            return ''
        
        try:
            valor_float = float(valor)
            
            if tipo == 'moeda':
                return f"R$ {valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            elif tipo == 'inteiro':
                return f"{int(valor_float)}"
            elif tipo == 'decimal_3':
                return f"{valor_float:,.3f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            elif tipo == 'decimal_2':
                return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            else:
                return str(valor_float).replace('.', ',')
        except:
            return str(valor)
    
    def get_resumo(self, df_processado):
        """Gera resumo formatado em colunas"""
        if df_processado is None:
            return "Nenhum dado processado"
        
        resumo_lines = []
        
        # Totais gerais
        num_produtos = df_processado['Código'].nunique()
        num_lojas = df_processado['Loja_Nome'].nunique()
        qtd_total = df_processado['Qtd'].sum()
        fat_total = df_processado['Total R$'].sum()
        
        resumo_lines.append(f"📦 Total de produtos únicos: {self._formatar_br(num_produtos, 'inteiro')}")
        resumo_lines.append(f"🏪 Total de lojas: {self._formatar_br(num_lojas, 'inteiro')}")
        resumo_lines.append(f"📊 Quantidade total: {self._formatar_br(qtd_total, 'decimal_3')}")
        resumo_lines.append(f"💰 Faturamento total: {self._formatar_br(fat_total, 'moeda')}")
        resumo_lines.append("")
        resumo_lines.append("=" * 95)
        resumo_lines.append("")
        
        # Tabela de lojas
        resumo_lines.append("🏢 LOJAS (faturamento e quantidade):")
        resumo_lines.append("")
        
        # Cabeçalho da tabela em colunas
        cabecalho = f"{'LOJA':<35} {'QUANTIDADE':>20} {'FATURAMENTO':>25}"
        resumo_lines.append(cabecalho)
        resumo_lines.append("-" * 85)
        
        # Agrupa por loja
        lojas = df_processado.groupby('Loja_Nome').agg({
            'Qtd': 'sum',
            'Total R$': 'sum'
        }).sort_values('Total R$', ascending=False)
        
        for loja, row in lojas.iterrows():
            if pd.notna(loja) and loja != '':
                loja_nome = str(loja).strip()
                # Formata a linha com as colunas
                linha = f"{loja_nome:<35} {self._formatar_br(row['Qtd'], 'decimal_3'):>20} {self._formatar_br(row['Total R$'], 'moeda'):>25}"
                resumo_lines.append(linha)
        
        return "\n".join(resumo_lines)
    
    def get_preview(self, df_processado, linhas=20):
        """Gera preview formatado com colunas centralizadas e espaçamento"""
        if df_processado is None:
            return "Nenhum dado processado"
        
        preview_lines = []
        preview_lines.append("=" * 120)
        preview_lines.append(f"PRIMEIRAS {linhas} LINHAS:")
        preview_lines.append("=" * 120)
        preview_lines.append("")
        
        # Seleciona colunas para preview
        cols_preview = ['Código', 'Produto', 'Qtd', 'Total R$', 'Loja_Nome']
        df_preview = df_processado[cols_preview].head(linhas).copy()
        
        # Define larguras fixas para cada coluna
        larguras = {
            'Código': 8,
            'Produto': 55,
            'Qtd': 15,
            'Total R$': 18,
            'Loja_Nome': 15
        }
        
        # Cabeçalho centralizado
        cabecalho = ""
        for col in cols_preview:
            cabecalho += f"{col:^{larguras[col]}} "
        preview_lines.append(cabecalho)
        preview_lines.append("-" * len(cabecalho))
        
        # Linhas de dados
        for _, row in df_preview.iterrows():
            linha = ""
            for col in cols_preview:
                valor = row[col]
                if col == 'Código':
                    texto = self._formatar_br(valor, 'inteiro')
                elif col == 'Qtd':
                    texto = self._formatar_br(valor, 'decimal_3')
                elif col == 'Total R$':
                    texto = self._formatar_br(valor, 'moeda')
                else:
                    texto = str(valor)[:larguras[col]-2] + '..' if len(str(valor)) > larguras[col]-2 else str(valor)
                
                # Centraliza o texto na largura da coluna
                linha += f"{texto:^{larguras[col]}} "
            preview_lines.append(linha)
        
        return "\n".join(preview_lines)