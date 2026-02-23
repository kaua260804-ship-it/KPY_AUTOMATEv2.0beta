# src/models/modelo_ruptura.py
"""
Modelo para gerar relatório de Ruptura combinando Estoque, Curva ABC e Média de Vendas.
"""
import pandas as pd
import numpy as np
from src.models.base import ModeloBase
from src.config.compradores import get_comprador

class ModeloRuptura(ModeloBase):
    nome = "Ruptura"
    descricao = "Relatório completo de ruptura com análise de estoque e vendas"

    def __init__(self):
        super().__init__()
        self.nome = "Ruptura"
        self.descricao = "Relatório completo de ruptura com análise de estoque e vendas"
    
    def identificar(self, df):
        """Este modelo não é usado para identificar arquivos"""
        return False

    def _normalizar_codigo(self, codigo):
        """Remove zeros à esquerda e pontos decimais"""
        try:
            if pd.isna(codigo):
                return ""
            return str(codigo).split('.')[0].lstrip('0')
        except:
            return str(codigo)

    def _calcular_dde(self, row):
        """Calcula DDE conforme fórmula do Excel"""
        estoque = row.get('Estoque_Loja', 0)
        media = row.get('Media_Vendas', 0)
        
        if pd.isna(estoque) or pd.isna(media):
            return ""
        
        if estoque == 0 and media == 0:
            return "Estoque e venda zerados"
        elif estoque == 0:
            return "Estoque zerado"
        elif media == 0:
            return "Sem venda"
        else:
            dias = (estoque / media) * 30
            if dias >= 30:
                meses = int(dias // 30)
                return f"{meses} mês(es)"
            else:
                return f"{int(dias)} dia(s)"
    
    def _status_estoque(self, row):
        """Status do estoque combinando loja e matriz"""
        estq_loja = row.get('Estoque_Loja', 0)
        estq_matriz = row.get('Estoque_Matriz', 0)
        
        if pd.isna(estq_loja) or pd.isna(estq_matriz):
            return ""
        
        status_loja = "C/ESTQ LJ" if estq_loja > 0 else "S/ESTQ LJ"
        status_matriz = "C/ESTQ MTZ" if estq_matriz > 0 else "S/ESTQ MTZ"
        
        return f"{status_loja} {status_matriz}"
    
    def _status_venda(self, row):
        """Status de venda baseado nas vendas do mês"""
        vendas = row.get('Vendas', 0)
        if pd.isna(vendas) or vendas < 0.000001:
            return "SEM VENDA"
        return "VENDA"
    
    def _status_ruptura(self, row):
        """Identifica se o produto está em ruptura"""
        media = row.get('Media_Vendas', 0)
        estoque = row.get('Estoque_Loja', 0)
        
        if pd.isna(media) or pd.isna(estoque):
            return "OK"
        
        if media > 0 and estoque == 0:
            return "RUPTURA"
        return "OK"
    
    def processar(self, df_estoque, df_curva, df_media):
        """
        Gera o relatório de ruptura completo.
        
        Args:
            df_estoque: DataFrame do estoque
            df_curva: DataFrame da Curva ABC
            df_media: DataFrame da média de vendas (pode ser None)
        
        Returns:
            DataFrame com todas as colunas do relatório
        """
        print("\n" + "="*60)
        print("📊 GERANDO RELATÓRIO DE RUPTURA")
        print("="*60)

        # ===== VERIFICAÇÃO CRÍTICA - df_media =====
        if df_media is None:
            print("⚠️ df_media é None, tentando carregar novamente...")
            try:
                from src.config.media_vendas import media_vendas
                df_media = media_vendas.get_df()
                print(f"📊 DataFrame recarregado: {type(df_media)}")
            except Exception as e:
                print(f"❌ Erro ao recarregar média: {e}")
                df_media = pd.DataFrame()
        
        if df_media is None:
            print("❌ df_media continua None, criando DataFrame vazio")
            df_media = pd.DataFrame(columns=['Código', 'Loja', 'Qtd'])
        
        if len(df_media) == 0:
            print("⚠️ df_media está vazio, criando DataFrame vazio")
            df_media = pd.DataFrame(columns=['Código', 'Loja', 'Qtd'])
        
        print(f"📊 df_media final: {len(df_media)} linhas, {len(df_media.columns)} colunas")

        # === 1. NORMALIZAR CÓDIGOS ===
        print("🔧 Normalizando códigos...")
        
        # Estoque (BASE)
        df_estoque = df_estoque.copy()
        
        # Procurar coluna de código no estoque
        col_codigo_estoque = None
        for col in df_estoque.columns:
            if 'codigo' in col.lower():
                col_codigo_estoque = col
                break
        
        if col_codigo_estoque is None:
            raise ValueError("Não foi possível encontrar coluna de código no estoque")
        
        print(f"   Coluna de código do estoque: '{col_codigo_estoque}'")
        df_estoque['Codigo_Norm'] = df_estoque[col_codigo_estoque].apply(self._normalizar_codigo)
        df_estoque['Cadeamento'] = df_estoque['Codigo_Norm'] + "-" + df_estoque['Loja'].astype(str)
        
        # Curva ABC
        df_curva = df_curva.copy()
        df_curva['Codigo_Norm'] = df_curva.iloc[:, 0].apply(self._normalizar_codigo)
        df_curva['Cadeamento'] = df_curva['Codigo_Norm'] + "-" + df_curva['Loja_Nome'].astype(str)
        df_curva['Vendas'] = pd.to_numeric(df_curva.iloc[:, 4], errors='coerce').fillna(0)
        
        # Média de Vendas (com verificação de colunas)
        df_media = df_media.copy()
        
        # Verificar se as colunas necessárias existem
        if 'Código' in df_media.columns:
            df_media['Codigo_Norm'] = df_media['Código'].apply(self._normalizar_codigo)
        else:
            print("⚠️ Coluna 'Código' não encontrada na média de vendas")
            df_media['Codigo_Norm'] = ""
        
        if 'Loja' in df_media.columns:
            df_media['Cadeamento'] = df_media['Codigo_Norm'] + "-" + df_media['Loja'].astype(str)
        else:
            print("⚠️ Coluna 'Loja' não encontrada na média de vendas")
            df_media['Cadeamento'] = df_media['Codigo_Norm'] + "-"
        
        if 'Qtd' in df_media.columns:
            df_media['Media_Vendas'] = pd.to_numeric(df_media['Qtd'], errors='coerce').fillna(0)
        else:
            print("⚠️ Coluna 'Qtd' não encontrada na média de vendas")
            df_media['Media_Vendas'] = 0
        
        # Agrupar média por cadeamento
        if len(df_media) > 0 and 'Cadeamento' in df_media.columns:
            df_media_agg = df_media.groupby('Cadeamento', as_index=False).agg({
                'Media_Vendas': 'mean',
                'Codigo_Norm': 'first',
                'Loja': 'first' if 'Loja' in df_media.columns else None
            })
            # Remover colunas None
            df_media_agg = df_media_agg.dropna(axis=1, how='all')
        else:
            print("⚠️ Criando DataFrame de média vazio")
            df_media_agg = pd.DataFrame(columns=['Cadeamento', 'Media_Vendas', 'Codigo_Norm'])

        # === 2. IDENTIFICAR MATRIZ ===
        print("🏪 Identificando matriz...")
        nome_matriz = "COMCARNE MATRIZ SAO LUIS"
        
        if nome_matriz in df_estoque['Loja'].values:
            print(f"✅ Matriz encontrada: {nome_matriz}")
            df_matriz = df_estoque[df_estoque['Loja'] == nome_matriz][['Codigo_Norm', 'Estoque_Loja']].copy()
            df_matriz = df_matriz.rename(columns={'Estoque_Loja': 'Estoque_Matriz'})
            
            # Adicionar Estoque_Matriz ao DataFrame principal
            df_estoque = df_estoque.merge(df_matriz, on='Codigo_Norm', how='left')
            df_estoque['Estoque_Matriz'] = df_estoque['Estoque_Matriz'].fillna(0)
        else:
            print(f"⚠️ Matriz '{nome_matriz}' não encontrada")
            df_estoque['Estoque_Matriz'] = 0

        # === 3. JUNTAR DADOS (ESTOQUE COMO BASE) ===
        print("🔄 Juntando dados...")
        
        # Join com Curva ABC (vendas)
        df_temp = pd.merge(
            df_estoque,
            df_curva[['Cadeamento', 'Vendas']],
            on='Cadeamento',
            how='left'
        )
        
        # Join com Média de Vendas
        if len(df_media_agg) > 0:
            df_final = pd.merge(
                df_temp,
                df_media_agg[['Cadeamento', 'Media_Vendas']],
                on='Cadeamento',
                how='left'
            )
        else:
            df_final = df_temp.copy()
            df_final['Media_Vendas'] = 0

        print(f"📊 Total de linhas: {len(df_final)}")

        # === 4. PREENCHER VALORES NULOS ===
        print("📋 Preparando colunas...")
        
        df_final['Vendas'] = df_final['Vendas'].fillna(0)
        df_final['Media_Vendas'] = df_final['Media_Vendas'].fillna(0)

        # === 5. ADICIONAR COLUNAS CALCULADAS ===
        print("🧮 Calculando colunas derivadas...")
        
        # DDE
        df_final['DDE'] = df_final.apply(self._calcular_dde, axis=1)
        
        # Status do Estoque
        df_final['STATUS DO ESTOQUE'] = df_final.apply(self._status_estoque, axis=1)
        
        # VENDA
        df_final['VENDA'] = df_final.apply(self._status_venda, axis=1)
        
        # COMPRADOR (baseado no grupo)
        if 'Grupo' in df_final.columns:
            df_final['COMPRADOR'] = df_final['Grupo'].apply(
                lambda x: get_comprador(x) if pd.notna(x) and x != '' else "NÃO MAPEADO"
            )
        else:
            df_final['COMPRADOR'] = "NÃO MAPEADO"
        
        # RUPTURA
        df_final['RUPTURA'] = df_final.apply(self._status_ruptura, axis=1)
        
        # Colunas em branco
        df_final['Valor Estoque'] = ""
        df_final['Preço'] = ""

        # === 6. ORGANIZAR COLUNAS NA ORDEM SOLICITADA ===
        print("📋 Organizando colunas...")
        
        # Mapear nomes das colunas existentes
        mapeamento = {
            'Categoria': 'CATEGORIA',
            'Grupo': 'GRUPO',
            'Codigo_Norm': 'CÓDIGO',
            'Descricao': 'PRODUTO',
            'Estoque_Loja': 'ESTQ LOJA',
            'Estoque_Matriz': 'ESTQ MATRIZ',
            'Vendas': 'VENDAS MÊS ATUAL',
            'Media_Vendas': 'MÉDIA VENDA MENSAL',
            'Loja': 'LOJA',
            'Sub_Grupo': 'Subgrupo',
            'Fornecedor_Razao': 'Forn'
        }
        
        df_final = df_final.rename(columns=mapeamento)
        
        # Garantir que CÓDIGO seja número inteiro
        if 'CÓDIGO' in df_final.columns:
            df_final['CÓDIGO'] = pd.to_numeric(df_final['CÓDIGO'], errors='coerce').fillna(0).astype(int)
            print("✅ Coluna CÓDIGO convertida para inteiro")
        
        # Lista de colunas na ordem desejada
        colunas_ordem = [
            'CATEGORIA',
            'GRUPO',
            'CÓDIGO',
            'PRODUTO',
            'ESTQ LOJA',
            'ESTQ MATRIZ',
            'VENDAS MÊS ATUAL',
            'MÉDIA VENDA MENSAL',
            'DDE',
            'LOJA',
            'STATUS DO ESTOQUE',
            'VENDA',
            'COMPRADOR',
            'RUPTURA',
            'Valor Estoque',
            'Preço',
            'Subgrupo',
            'Forn'
        ]
        
        # Garantir que todas as colunas existam
        for col in colunas_ordem:
            if col not in df_final.columns:
                df_final[col] = ""
        
        # Reordenar
        df_final = df_final[colunas_ordem]

        print(f"\n✅ Relatório de Ruptura gerado com sucesso!")
        print(f"📊 Total de linhas: {len(df_final)}")
        print(f"📊 Produtos com ruptura: {len(df_final[df_final['RUPTURA'] == 'RUPTURA'])}")
        
        self.df_processado = df_final
        return df_final

    def get_preview(self, df, linhas=20):
        """Mostra as primeiras linhas formatadas"""
        if df is None or len(df) == 0:
            return "Nenhum dado processado"
        
        # Formatar números para exibição
        df_preview = df.head(linhas).copy()
        
        for col in ['ESTQ LOJA', 'ESTQ MATRIZ', 'VENDAS MÊS ATUAL', 'MÉDIA VENDA MENSAL']:
            if col in df_preview.columns:
                df_preview[col] = df_preview[col].apply(
                    lambda x: f"{float(x):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notna(x) and x != '' else ""
                )
        
        return df_preview.to_string(index=False)

    def get_resumo(self, df):
        """Gera resumo estatístico do relatório"""
        if df is None or len(df) == 0:
            return "Nenhum dado processado"
        
        linhas = []
        linhas.append("📊 RESUMO DO RELATÓRIO DE RUPTURA")
        linhas.append("-" * 60)
        linhas.append(f"📦 Total de produtos: {len(df)}")
        
        # Produtos em ruptura
        if 'RUPTURA' in df.columns:
            ruptura = len(df[df['RUPTURA'] == 'RUPTURA'])
            linhas.append(f"⚠️ Produtos em ruptura: {ruptura}")
        
        # Produtos sem estoque
        if 'ESTQ LOJA' in df.columns:
            sem_estoque = len(df[df['ESTQ LOJA'] <= 0])
            linhas.append(f"📦 Produtos sem estoque: {sem_estoque}")
        
        # Por comprador
        if 'COMPRADOR' in df.columns:
            linhas.append("\n👤 Por Comprador:")
            for comp, qtd in df['COMPRADOR'].value_counts().head(10).items():
                if comp != "NÃO MAPEADO" and pd.notna(comp):
                    linhas.append(f"  {comp}: {qtd} produtos")
        
        return "\n".join(linhas)