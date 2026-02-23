# src/models/modelo_estoque.py
"""
Modelo para processar relatórios de Estoque.
"""
import pandas as pd
from src.models.base import ModeloBase

class ModeloEstoque(ModeloBase):
    """Modelo específico para relatórios de Estoque"""
    
    def __init__(self):
        super().__init__()
        self.nome = "Estoque"
        self.descricao = "Processa relatórios de estoque com informações de produtos por loja"
    
    def identificar(self, df):
        """
        Verifica se a planilha é do tipo Estoque.
        Versão robusta que funciona com ou sem cabeçalho.
        """
        try:
            print("\n🔍 VERIFICANDO SE É ESTOQUE...")
            
            # CASO 1: DataFrame já tem colunas com nomes
            colunas = [str(col).strip() for col in df.columns]
            print(f"Colunas: {colunas[:10]}...")
            
            # Verificar se alguma coluna tem os nomes esperados
            for col in colunas:
                if 'Código' in col or 'CODIGO' in col:
                    print(f"✅ Encontrou coluna de código: '{col}'")
                if 'Estoque Loja' in col:
                    print(f"✅ Encontrou 'Estoque Loja': '{col}'")
                if 'Estoque Geral' in col:
                    print(f"✅ Encontrou 'Estoque Geral': '{col}'")
            
            # Verificar se tem as colunas necessárias
            tem_codigo = any('Código' in col or 'CODIGO' in col or 'codigo' in col for col in colunas)
            tem_estoque_loja = any('Estoque Loja' in col for col in colunas)
            tem_estoque_geral = any('Estoque Geral' in col for col in colunas)
            
            if tem_codigo and tem_estoque_loja and tem_estoque_geral:
                print("✅ É ESTOQUE (encontrou colunas)!")
                return True
            
            # CASO 2: DataFrame com colunas numéricas (header=None)
            # Procurar nas primeiras linhas
            for i in range(min(10, len(df))):
                linha = df.iloc[i]
                linha_texto = ' '.join([str(x) for x in linha if pd.notna(x)])
                
                if ('Código' in linha_texto or 'CODIGO' in linha_texto) and \
                   'Estoque Loja' in linha_texto and \
                   'Estoque Geral' in linha_texto:
                    print(f"✅ É ESTOQUE (encontrou na linha {i})!")
                    return True
            
            print("❌ Não é estoque")
            return False
            
        except Exception as e:
            print(f"❌ Erro na identificação: {e}")
            return False
    
    def _is_numero(self, valor):
        """Verifica se o valor parece um número (código de produto)"""
        try:
            if pd.isna(valor):
                return False
            if isinstance(valor, (int, float)):
                return True
            val = str(valor).strip()
            if not val or val in ['nan', 'None', '']:
                return False
            return val[0].isdigit()
        except:
            return False
    
    def _tratar_numero_br(self, valor):
        """Converte número para float"""
        try:
            if pd.isna(valor) or valor == '':
                return 0.0
            if isinstance(valor, (int, float)):
                return float(valor)
            val = str(valor).strip()
            val = val.replace('.', '').replace(',', '.')
            return float(val)
        except:
            return 0.0
    
    def _encontrar_linha_cabecalho(self, df):
        """Encontra a linha onde está o cabeçalho"""
        for i in range(min(30, len(df))):
            linha = df.iloc[i]
            linha_texto = ' '.join([str(x) for x in linha if pd.notna(x)])
            
            if ('Código' in linha_texto or 'CODIGO' in linha_texto) and \
               'Estoque Loja' in linha_texto and \
               'Estoque Geral' in linha_texto:
                return i
        return None
    
    def _extrair_colunas_do_cabecalho(self, linha_cabecalho, df):
        """Extrai os nomes das colunas da linha de cabeçalho"""
        colunas = []
        for j in range(df.shape[1]):
            val = df.iloc[linha_cabecalho, j] if pd.notna(df.iloc[linha_cabecalho, j]) else f"Col{j}"
            colunas.append(str(val).strip())
        return colunas
    
    def _padronizar_nome_coluna(self, nome):
        """Padroniza nomes de colunas"""
        nome = str(nome).strip()
        if 'Código' in nome or 'CODIGO' in nome:
            return 'Codigo'
        if 'Descrição' in nome:
            return 'Descricao'
        if 'Abreviação' in nome:
            return 'Abreviacao'
        if 'Estoque Loja' in nome:
            return 'Estoque_Loja'
        if 'Estoque Geral' in nome:
            return 'Estoque_Geral'
        if 'Unid' in nome:
            return 'Unid'
        if 'Marca' in nome:
            return 'Marca'
        if 'Modelo' in nome:
            return 'Modelo'
        if 'NCM' in nome:
            return 'NCM'
        if 'Referência' in nome:
            return 'Referencia'
        if 'Classificação' in nome:
            return 'Classificacao'
        if 'Categoria' in nome:
            return 'Categoria'
        if 'Grupo' in nome:
            return 'Grupo'
        if 'Sub-grupo' in nome:
            return 'Sub_Grupo'
        if 'Fornec/Razão Social' in nome:
            return 'Fornecedor_Razao'
        if 'Fornec/Nome Fantasia' in nome:
            return 'Fornecedor_Fantasia'
        if 'Linha' in nome:
            return 'Linha'
        if 'Especie' in nome or 'Espécie' in nome:
            return 'Especie'
        if 'LOJA' in nome or 'Loja' in nome:
            return 'Loja'
        return nome.replace(' ', '_').replace('/', '_')
    
    def processar(self, df):
        """
        Processa o relatório de Estoque.
        """
        try:
            print("\n" + "="*60)
            print("INICIANDO PROCESSAMENTO DO ESTOQUE")
            print("="*60)
            
            # Verificar se já tem cabeçalho
            primeiras_colunas = [str(col) for col in df.columns[:5]]
            print(f"Primeiras colunas: {primeiras_colunas}")
            
            tem_cabecalho = any('Código' in col for col in primeiras_colunas)
            
            if not tem_cabecalho:
                print("📋 DataFrame sem cabeçalho, procurando linha de cabeçalho...")
                linha_cab = self._encontrar_linha_cabecalho(df)
                
                if linha_cab is not None:
                    print(f"✅ Cabeçalho encontrado na linha {linha_cab}")
                    
                    # Extrair nomes das colunas
                    colunas = self._extrair_colunas_do_cabecalho(linha_cab, df)
                    print(f"📋 Colunas extraídas: {colunas}")
                    
                    # Criar novo DataFrame com os dados
                    dados = []
                    for i in range(linha_cab + 1, len(df)):
                        primeira = df.iloc[i, 0] if pd.notna(df.iloc[i, 0]) else ""
                        if self._is_numero(primeira):
                            linha_produto = []
                            for j in range(len(colunas)):
                                if j < df.shape[1]:
                                    val = df.iloc[i, j] if pd.notna(df.iloc[i, j]) else ""
                                    linha_produto.append(str(val).strip())
                                else:
                                    linha_produto.append("")
                            dados.append(linha_produto)
                    
                    df = pd.DataFrame(dados, columns=colunas)
                    print(f"📦 DataFrame criado com {len(df)} linhas")
                else:
                    print("❌ Cabeçalho não encontrado")
                    return pd.DataFrame()
            
            # Padronizar nomes das colunas
            novos_nomes = {}
            for col in df.columns:
                novo_nome = self._padronizar_nome_coluna(col)
                if novo_nome != col:
                    novos_nomes[col] = novo_nome
            
            if novos_nomes:
                df.rename(columns=novos_nomes, inplace=True)
                print(f"📋 Colunas padronizadas: {list(df.columns)}")
            
            # Converter colunas numéricas
            if 'Codigo' in df.columns:
                df['Codigo'] = pd.to_numeric(df['Codigo'], errors='coerce').fillna(0).astype(int)
            
            # Converter estoques
            for col in ['Estoque_Loja', 'Estoque_Geral']:
                if col in df.columns:
                    df[col] = df[col].apply(self._tratar_numero_br)
            
            # Remover códigos 0
            if 'Codigo' in df.columns:
                df = df[df['Codigo'] != 0].reset_index(drop=True)
            
            print(f"\n✅ ESTOQUE PROCESSADO: {len(df)} produtos")
            print(f"📊 Colunas: {list(df.columns)}")
            
            self.df_processado = df
            return df
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def get_resumo(self, df):
        """Gera resumo formatado"""
        if df is None or len(df) == 0:
            return "Nenhum dado processado"
        
        linhas = []
        linhas.append("📊 RESUMO DO ESTOQUE")
        linhas.append("-" * 60)
        linhas.append(f"📦 Total de produtos: {len(df)}")
        
        if 'Codigo' in df.columns:
            linhas.append(f"📦 Produtos únicos: {df['Codigo'].nunique()}")
        
        if 'Estoque_Geral' in df.columns:
            total_estoque = df['Estoque_Geral'].sum()
            linhas.append(f"📊 Estoque Geral: {total_estoque:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
        if 'Categoria' in df.columns:
            linhas.append("\n📁 Por Categoria:")
            for cat, qtd in df['Categoria'].value_counts().head(10).items():
                if cat and str(cat).strip():
                    linhas.append(f"  {cat}: {qtd} produtos")
        
        if 'Loja' in df.columns:
            linhas.append("\n🏪 Por Loja:")
            for loja, qtd in df['Loja'].value_counts().head(10).items():
                if loja and str(loja).strip():
                    linhas.append(f"  {loja}: {qtd} produtos")
        
        return "\n".join(linhas)
    
    def get_preview(self, df, linhas=20):
        """Gera preview formatado"""
        if df is None or len(df) == 0:
            return "Nenhum dado processado"
        
        cols = []
        for col in ['Codigo', 'Descricao', 'Estoque_Loja', 'Estoque_Geral', 'Categoria', 'Grupo', 'Loja']:
            if col in df.columns:
                cols.append(col)
        
        if cols:
            return df[cols].head(linhas).to_string(index=False)
        return df.head(linhas).to_string(index=False)