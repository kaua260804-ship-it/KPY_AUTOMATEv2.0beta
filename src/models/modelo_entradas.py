# src/models/modelo_entradas.py
"""
Modelo para processar relatórios de Entradas de Produtos por Grupo do SGE.
VERSÃO FINAL - COM PREVIEW PERFEITAMENTE ALINHADO
"""
import pandas as pd
from src.models.base import ModeloBase
from src.config.compradores import get_comprador

class ModeloEntradas(ModeloBase):
    def __init__(self):
        super().__init__()
        self.nome = "Entradas por Grupo"
    
    def identificar(self, df):
        try:
            primeiras_linhas = df.iloc[:5, 0].astype(str).str.lower()
            return any('entradas produtos por grupo' in x for x in primeiras_linhas)
        except:
            return False
    
    def _is_numero(self, valor):
        """Verifica se o valor parece um número (código de produto)"""
        try:
            if pd.isna(valor):
                return False
            val = str(valor).strip()
            if not val or val in ['nan', 'None', '']:
                return False
            return val[0].isdigit()
        except:
            return False
    
    def _formatar_br(self, valor):
        """Formata número no padrão brasileiro"""
        try:
            if pd.isna(valor) or valor == '':
                return "0,00"
            if isinstance(valor, str):
                valor = valor.replace('.', '').replace(',', '.')
            return f"{float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return str(valor)
    
    def processar(self, df):
        """
        Processa o relatório de Entradas por Grupo.
        """
        try:
            print("\n" + "="*60)
            print("INICIANDO PROCESSAMENTO")
            print("="*60)
            
            todos_dados = []
            
            # Valores atuais de categoria e grupo
            cat_codigo = ""
            cat_nome = ""
            grupo_codigo = ""
            grupo_nome = ""
            
            # VAI LINHA POR LINHA
            for i in range(len(df)):
                # Pega a primeira coluna
                primeira = df.iloc[i, 0] if pd.notna(df.iloc[i, 0]) else ""
                primeira_str = str(primeira).strip()
                
                # CASO 1: Encontrou CATEGORIA
                if 'Categoria:' in primeira_str:
                    # Pega os valores nas posições fixas
                    if df.shape[1] > 2:
                        cat_codigo = str(df.iloc[i, 1]).lstrip('0') if pd.notna(df.iloc[i, 1]) else ""
                        cat_nome = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ""
                    if df.shape[1] > 5:
                        grupo_codigo = str(df.iloc[i, 4]).lstrip('0') if pd.notna(df.iloc[i, 4]) else ""
                        grupo_nome = str(df.iloc[i, 5]) if pd.notna(df.iloc[i, 5]) else ""
                    
                    print(f"📁 Linha {i}: Categoria {cat_codigo}-{cat_nome}, Grupo {grupo_codigo}-{grupo_nome}")
                
                # CASO 2: Encontrou PRODUTO (começa com número)
                elif self._is_numero(primeira):
                    # Coletar TODAS as colunas (12 colunas)
                    linha_produto = []
                    
                    # Colunas 0 a 11
                    for j in range(12):
                        if j < df.shape[1]:
                            val = df.iloc[i, j] if pd.notna(df.iloc[i, j]) else ""
                            linha_produto.append(str(val).strip())
                        else:
                            linha_produto.append("")
                    
                    # Adicionar as 5 colunas extras
                    linha_produto.append(cat_codigo)      # Codigo Categoria
                    linha_produto.append(cat_nome)        # Categoria
                    linha_produto.append(grupo_codigo)    # Codigo Grupo
                    linha_produto.append(grupo_nome)      # Grupo
                    linha_produto.append('')              # Comprador (será preenchido depois)
                    
                    todos_dados.append(linha_produto)
            
            print(f"\n📦 Total de produtos encontrados: {len(todos_dados)}")
            
            if not todos_dados:
                print("❌ Nenhum produto encontrado")
                return pd.DataFrame()
            
            # NOMES DAS COLUNAS
            colunas_base = [
                'Codigo', 'Produto', 'Peças', 'Qtd', 'Unid', 
                'Custo Md', 'Total', 'Pr. Vda', 'Markup', 'Margem', 'Ult.Ent.'
            ]
            
            # Verificar se a coluna 11 tem dados
            col11_tem_dados = any(len(row) > 11 and row[11].strip() for row in todos_dados)
            
            if col11_tem_dados:
                colunas = colunas_base + ['Col11'] + ['Codigo Categoria', 'Categoria', 'Codigo Grupo', 'Grupo', 'Comprador']
            else:
                # Remove a col11 de todas as linhas
                todos_dados = [row[:11] + row[12:] for row in todos_dados]
                colunas = colunas_base + ['Codigo Categoria', 'Categoria', 'Codigo Grupo', 'Grupo', 'Comprador']
            
            # Criar DataFrame
            df_final = pd.DataFrame(todos_dados, columns=colunas)
            
            # ===== PREENCHER COMPRADOR BASEADO NO GRUPO =====
            if 'Grupo' in df_final.columns:
                df_final['Comprador'] = df_final['Grupo'].apply(get_comprador)
                print(f"✅ Coluna 'Comprador' preenchida com sucesso!")
            
            # ===== CONVERSÕES PARA NÚMEROS =====
            
            # Converter Código para inteiro
            if 'Codigo' in df_final.columns:
                df_final['Codigo'] = pd.to_numeric(df_final['Codigo'], errors='coerce').fillna(0).astype(int)
            
            # Converter colunas numéricas
            colunas_numericas = ['Qtd', 'Total', 'Custo Md', 'Pr. Vda', 'Markup', 'Margem', 'Peças']
            for col in colunas_numericas:
                if col in df_final.columns:
                    df_final[col] = df_final[col].astype(str).str.replace(',', '.')
                    df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
            
            # Converter códigos de categoria e grupo para inteiro
            if 'Codigo Categoria' in df_final.columns:
                df_final['Codigo Categoria'] = pd.to_numeric(df_final['Codigo Categoria'], errors='coerce').fillna(0).astype(int)
            
            if 'Codigo Grupo' in df_final.columns:
                df_final['Codigo Grupo'] = pd.to_numeric(df_final['Codigo Grupo'], errors='coerce').fillna(0).astype(int)
            
            # Converter data
            if 'Ult.Ent.' in df_final.columns:
                try:
                    df_final['Ult.Ent.'] = pd.to_datetime(df_final['Ult.Ent.'], format='%d/%m/%y', errors='coerce')
                    df_final['Ult.Ent.'] = df_final['Ult.Ent.'].dt.strftime('%d/%m/%Y')
                except:
                    try:
                        df_final['Ult.Ent.'] = pd.to_datetime(df_final['Ult.Ent.'], errors='coerce')
                        df_final['Ult.Ent.'] = df_final['Ult.Ent.'].dt.strftime('%d/%m/%Y')
                    except:
                        pass
            
            # Remover códigos 0
            df_final = df_final[df_final['Codigo'] != 0].reset_index(drop=True)
            
            # ===== REORDENAR COLUNAS CONFORME SOLICITADO =====
            ordem_desejada = [
                'Codigo', 'Produto', 'Categoria', 'Grupo', 'Comprador',
                'Qtd', 'Unid', 'Custo Md', 'Total', 'Pr. Vda',
                'Markup', 'Margem', 'Ult.Ent.', 'Peças',
                'Codigo Categoria', 'Codigo Grupo'
            ]
            
            # Verificar quais colunas existem no DataFrame
            colunas_existentes = [col for col in ordem_desejada if col in df_final.columns]
            
            # Adicionar Col11 se existir (no final)
            if 'Col11' in df_final.columns:
                colunas_existentes.append('Col11')
            
            # Reordenar
            df_final = df_final[colunas_existentes]
            
            print(f"\n✅ PROCESSADO: {len(df_final)} produtos")
            print(f"📊 Colunas: {list(df_final.columns)}")
            
            self.df_processado = df_final
            return df_final
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def get_resumo(self, df):
        """Gera resumo formatado com categorias, grupos e compradores"""
        if df is None or len(df) == 0:
            return "Nenhum dado processado"
        
        linhas = []
        
        # Estatísticas gerais
        linhas.append("📊 RESUMO GERAL")
        linhas.append("-" * 90)
        linhas.append(f"📦 Total de produtos: {len(df)}")
        
        if 'Codigo' in df.columns:
            linhas.append(f"📦 Produtos únicos: {df['Codigo'].nunique()}")
        
        if 'Qtd' in df.columns:
            qtd_total = df['Qtd'].sum()
            linhas.append(f"📊 Quantidade total: {self._formatar_br(qtd_total)}")
        
        if 'Total' in df.columns:
            valor_total = df['Total'].sum()
            linhas.append(f"💰 Valor total: R$ {self._formatar_br(valor_total)}")
        
        # Por CATEGORIA
        if 'Categoria' in df.columns:
            linhas.append("\n📁 POR CATEGORIA")
            linhas.append("-" * 90)
            for cat, qtd in df['Categoria'].value_counts().items():
                if cat and str(cat).strip():
                    valor_cat = df[df['Categoria'] == cat]['Total'].sum() if 'Total' in df.columns else 0
                    linhas.append(f"  {cat:<30} {qtd:>6} produtos  R$ {self._formatar_br(valor_cat):>15}")
        
        # Por GRUPO (TODOS)
        if 'Grupo' in df.columns:
            linhas.append("\n📁 POR GRUPO")
            linhas.append("-" * 90)
            
            # Agrupar por grupo e somar
            grupos = df.groupby('Grupo').agg({
                'Codigo': 'count',
                'Total': 'sum' if 'Total' in df.columns else lambda x: 0
            }).sort_values('Codigo', ascending=False)
            
            for grupo, row in grupos.iterrows():
                if grupo and str(grupo).strip():
                    linhas.append(f"  {grupo[:35]:<35} {int(row['Codigo']):>6} produtos  R$ {self._formatar_br(row['Total']):>15}")
        
        # Por COMPRADOR
        if 'Comprador' in df.columns:
            linhas.append("\n👤 POR COMPRADOR")
            linhas.append("-" * 90)
            
            # Agrupar por comprador
            compradores = df.groupby('Comprador').agg({
                'Codigo': 'count',
                'Total': 'sum' if 'Total' in df.columns else lambda x: 0
            }).sort_values('Codigo', ascending=False)
            
            for comp, row in compradores.iterrows():
                if comp != 'NÃO MAPEADO':
                    linhas.append(f"  {comp:<20} {int(row['Codigo']):>6} produtos  R$ {self._formatar_br(row['Total']):>15}")
            
            # Mostrar não mapeados se houver
            nao_mapeados = df[df['Comprador'] == 'NÃO MAPEADO']
            if len(nao_mapeados) > 0:
                linhas.append(f"\n⚠️ GRUPOS NÃO MAPEADOS:")
                for grupo in nao_mapeados['Grupo'].unique():
                    qtd_grupo = len(nao_mapeados[nao_mapeados['Grupo'] == grupo])
                    valor_grupo = nao_mapeados[nao_mapeados['Grupo'] == grupo]['Total'].sum() if 'Total' in df.columns else 0
                    linhas.append(f"  - {grupo}: {qtd_grupo} produtos (R$ {self._formatar_br(valor_grupo)})")
        
        return "\n".join(linhas)
    
    def get_preview(self, df, linhas=20):
        """Gera preview formatado com colunas perfeitamente alinhadas"""
        if df is None or len(df) == 0:
            return "Nenhum dado processado"
        
        # Selecionar colunas para preview
        cols_preview = []
        col_map = {}
        
        if 'Codigo' in df.columns:
            cols_preview.append('Codigo')
            col_map['Codigo'] = 'Código'
        if 'Produto' in df.columns:
            cols_preview.append('Produto')
            col_map['Produto'] = 'Produto'
        if 'Qtd' in df.columns:
            cols_preview.append('Qtd')
            col_map['Qtd'] = 'Qtd'
        if 'Total' in df.columns:
            cols_preview.append('Total')
            col_map['Total'] = 'Total'
        if 'Ult.Ent.' in df.columns:
            cols_preview.append('Ult.Ent.')
            col_map['Ult.Ent.'] = 'Últ.Ent.'
        if 'Grupo' in df.columns:
            cols_preview.append('Grupo')
            col_map['Grupo'] = 'Grupo'
        if 'Comprador' in df.columns:
            cols_preview.append('Comprador')
            col_map['Comprador'] = 'Comprador'
        
        if not cols_preview:
            return df.head(linhas).to_string(index=False)
        
        # Criar cópia para preview
        df_preview = df[cols_preview].head(linhas).copy()
        
        # Formatar números
        if 'Qtd' in df_preview.columns:
            df_preview['Qtd'] = df_preview['Qtd'].apply(lambda x: self._formatar_br(x))
        
        if 'Total' in df_preview.columns:
            df_preview['Total'] = df_preview['Total'].apply(lambda x: self._formatar_br(x))
        
        # Renomear colunas para exibição
        df_preview = df_preview.rename(columns=col_map)
        
        # Definir larguras FIXAS para cada coluna
        larguras = {
            'Código': 8,
            'Produto': 45,
            'Qtd': 10,
            'Total': 15,
            'Últ.Ent.': 12,
            'Grupo': 25,
            'Comprador': 15
        }
        
        # Função para truncar texto com ellipsis
        def truncar(texto, tamanho):
            texto = str(texto)
            if len(texto) <= tamanho:
                return texto
            return texto[:tamanho-3] + "..."
        
        # Criar linhas formatadas
        linhas_preview = []
        
        # Cabeçalho
        cabecalho = ""
        for col in df_preview.columns:
            largura = larguras.get(col, 15)
            cabecalho += f"{col:<{largura}} "
        linhas_preview.append(cabecalho)
        
        # Linha separadora
        linhas_preview.append("-" * len(cabecalho))
        
        # Linhas de dados
        for _, row in df_preview.iterrows():
            linha = ""
            for col in df_preview.columns:
                valor = str(row[col]) if pd.notna(row[col]) else ""
                largura = larguras.get(col, 15)
                
                # Truncar produto se necessário
                if col == 'Produto':
                    valor = truncar(valor, largura)
                
                linha += f"{valor:<{largura}} "
            linhas_preview.append(linha)
        
        return "\n".join(linhas_preview)