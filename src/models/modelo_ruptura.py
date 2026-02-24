# src/models/modelo_ruptura.py
"""
Modelo para gerar relatório de Ruptura combinando Estoque, Curva ABC e Média de Vendas.
Versão 2.1.0 - Com sistema de logs integrado e busca flexível de colunas
"""
import pandas as pd
import numpy as np
from src.models.base import ModeloBase
from src.config.compradores import get_comprador
from src.utils.logger import info, error, warning, debug

class ModeloRuptura(ModeloBase):
    nome = "Ruptura"
    descricao = "Relatório completo de ruptura com análise de estoque e vendas"

    def __init__(self):
        super().__init__()
        self.nome = "Ruptura"
        self.descricao = "Relatório completo de ruptura com análise de estoque e vendas"
        info(f"🔧 Modelo {self.nome} inicializado")
    
    def identificar(self, df):
        """Este modelo não é usado para identificar arquivos"""
        return False

    def _normalizar_codigo(self, codigo):
        """Remove zeros à esquerda e pontos decimais"""
        try:
            if pd.isna(codigo):
                return ""
            # Converter para string e remover parte decimal se houver
            codigo_str = str(codigo).split('.')[0].lstrip('0')
            debug(f"🔢 Código normalizado: {codigo} -> {codigo_str}")
            return codigo_str
        except Exception as e:
            error(f"❌ Erro ao normalizar código {codigo}: {e}")
            return str(codigo)

    def _calcular_dde(self, row):
        """Calcula DDE conforme fórmula do Excel"""
        try:
            estoque = row.get('Estoque_Loja', 0)
            media = row.get('Media_Vendas', 0)
            
            if pd.isna(estoque) or pd.isna(media):
                return ""
            
            # Converter para float
            estoque = float(estoque) if estoque else 0
            media = float(media) if media else 0
            
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
        except Exception as e:
            error(f"❌ Erro ao calcular DDE: {e}")
            return ""
    
    def _status_estoque(self, row):
        """Status do estoque combinando loja e matriz"""
        try:
            estq_loja = row.get('Estoque_Loja', 0)
            estq_matriz = row.get('Estoque_Matriz', 0)
            
            if pd.isna(estq_loja) or pd.isna(estq_matriz):
                return ""
            
            estq_loja = float(estq_loja) if estq_loja else 0
            estq_matriz = float(estq_matriz) if estq_matriz else 0
            
            status_loja = "C/ESTQ LJ" if estq_loja > 0 else "S/ESTQ LJ"
            status_matriz = "C/ESTQ MTZ" if estq_matriz > 0 else "S/ESTQ MTZ"
            
            return f"{status_loja} {status_matriz}"
        except Exception as e:
            error(f"❌ Erro ao calcular status estoque: {e}")
            return ""
    
    def _status_venda(self, row):
        """Status de venda baseado nas vendas do mês"""
        try:
            vendas = row.get('Vendas', 0)
            if pd.isna(vendas) or float(vendas) < 0.000001:
                return "SEM VENDA"
            return "VENDA"
        except Exception as e:
            error(f"❌ Erro ao calcular status venda: {e}")
            return ""
    
    def _status_ruptura(self, row):
        """Identifica se o produto está em ruptura"""
        try:
            media = row.get('Media_Vendas', 0)
            estoque = row.get('Estoque_Loja', 0)
            
            if pd.isna(media) or pd.isna(estoque):
                return "OK"
            
            media = float(media) if media else 0
            estoque = float(estoque) if estoque else 0
            
            if media > 0 and estoque == 0:
                return "RUPTURA"
            return "OK"
        except Exception as e:
            error(f"❌ Erro ao calcular status ruptura: {e}")
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
        info("="*60)
        info("📊 GERANDO RELATÓRIO DE RUPTURA")
        info("="*60)

        # ===== VERIFICAÇÃO CRÍTICA - df_media =====
        if df_media is None:
            warning("⚠️ df_media é None, tentando carregar novamente...")
            try:
                from src.config.media_vendas import media_vendas
                df_media = media_vendas.get_df()
                info(f"📊 DataFrame recarregado: {type(df_media)} com {len(df_media) if df_media is not None else 0} linhas")
            except Exception as e:
                error(f"❌ Erro ao recarregar média: {e}")
                df_media = pd.DataFrame()
        
        if df_media is None:
            error("❌ df_media continua None, criando DataFrame vazio")
            df_media = pd.DataFrame(columns=['Código', 'Loja', 'Qtd'])
        
        if len(df_media) == 0:
            warning("⚠️ df_media está vazio, criando DataFrame vazio")
            df_media = pd.DataFrame(columns=['Código', 'Loja', 'Qtd'])
        
        info(f"📊 df_media final: {len(df_media)} linhas, {len(df_media.columns)} colunas")

        # === 1. NORMALIZAR CÓDIGOS ===
        info("🔧 Normalizando códigos...")
        
        # Estoque (BASE)
        df_estoque = df_estoque.copy()
        info(f"📦 Estoque original: {len(df_estoque)} linhas")
        info(f"📋 Colunas disponíveis no estoque: {list(df_estoque.columns)}")
        
        # Procurar coluna de código no estoque (MAIS FLEXÍVEL)
        col_codigo_estoque = None
        possiveis_nomes = ['codigo', 'código', 'Codigo', 'Código', 'CODIGO', 'CÓDIGO', 'produto_codigo', 'id_produto']
        
        for col in df_estoque.columns:
            col_lower = col.lower().strip()
            for nome in possiveis_nomes:
                if nome.lower() in col_lower or col_lower in nome.lower():
                    col_codigo_estoque = col
                    info(f"   ✅ Coluna de código encontrada: '{col}' (correspondência: '{nome}')")
                    break
            if col_codigo_estoque:
                break
        
        # Se ainda não encontrou, procurar por qualquer coluna que pareça código
        if col_codigo_estoque is None:
            for col in df_estoque.columns:
                # Verificar se a coluna tem muitos números (parece código de produto)
                amostra = df_estoque[col].dropna().astype(str).head(100)
                if len(amostra) > 0:
                    # Contar quantos valores são numéricos
                    numeros = sum(1 for x in amostra if x.replace('.', '').replace('-', '').isdigit())
                    if numeros > len(amostra) * 0.7:  # 70% ou mais são números
                        col_codigo_estoque = col
                        info(f"   ✅ Coluna de código identificada por heurística: '{col}' ({numeros}/{len(amostra)} valores numéricos)")
                        break
        
        if col_codigo_estoque is None:
            error("❌ Não foi possível encontrar coluna de código no estoque")
            error(f"📋 Colunas disponíveis: {list(df_estoque.columns)}")
            raise ValueError(f"Coluna de código não encontrada no estoque. Colunas disponíveis: {list(df_estoque.columns)}")
        
        info(f"   Coluna de código do estoque: '{col_codigo_estoque}'")
        df_estoque['Codigo_Norm'] = df_estoque[col_codigo_estoque].apply(self._normalizar_codigo)
        df_estoque['Cadeamento'] = df_estoque['Codigo_Norm'] + "-" + df_estoque['Loja'].astype(str)
        debug(f"   Exemplos de cadeamento: {df_estoque['Cadeamento'].head(3).tolist()}")
        
        # Curva ABC
        df_curva = df_curva.copy()
        info(f"📊 Curva ABC original: {len(df_curva)} linhas")
        
        # Encontrar coluna de código na curva ABC
        col_codigo_curva = df_curva.columns[0]  # Assume que é a primeira coluna
        info(f"   Coluna de código da curva ABC: '{col_codigo_curva}'")
        
        df_curva['Codigo_Norm'] = df_curva[col_codigo_curva].apply(self._normalizar_codigo)
        df_curva['Cadeamento'] = df_curva['Codigo_Norm'] + "-" + df_curva['Loja_Nome'].astype(str)
        
        # Encontrar coluna de quantidade na curva ABC
        col_qtd_curva = None
        for col in df_curva.columns:
            if 'qtd' in col.lower() or 'quantidade' in col.lower():
                col_qtd_curva = col
                break
        
        if col_qtd_curva is None:
            col_qtd_curva = df_curva.columns[4]  # Assume que é a 5ª coluna (índice 4)
            warning(f"⚠️ Coluna de quantidade não identificada, usando coluna {col_qtd_curva}")
        
        df_curva['Vendas'] = pd.to_numeric(df_curva[col_qtd_curva], errors='coerce').fillna(0)
        
        # Média de Vendas (com verificação de colunas)
        info(f"📈 Média de vendas: {len(df_media)} linhas")
        df_media = df_media.copy()
        
        # Verificar se as colunas necessárias existem
        if 'Código' in df_media.columns:
            df_media['Codigo_Norm'] = df_media['Código'].apply(self._normalizar_codigo)
        else:
            warning("⚠️ Coluna 'Código' não encontrada na média de vendas")
            df_media['Codigo_Norm'] = ""
        
        if 'Loja' in df_media.columns:
            df_media['Cadeamento'] = df_media['Codigo_Norm'] + "-" + df_media['Loja'].astype(str)
        else:
            warning("⚠️ Coluna 'Loja' não encontrada na média de vendas")
            df_media['Cadeamento'] = df_media['Codigo_Norm'] + "-"
        
        if 'Qtd' in df_media.columns:
            df_media['Media_Vendas'] = pd.to_numeric(df_media['Qtd'], errors='coerce').fillna(0)
        else:
            warning("⚠️ Coluna 'Qtd' não encontrada na média de vendas")
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
            info(f"📊 Média agregada: {len(df_media_agg)} grupos únicos")
        else:
            warning("⚠️ Criando DataFrame de média vazio")
            df_media_agg = pd.DataFrame(columns=['Cadeamento', 'Media_Vendas', 'Codigo_Norm'])

        # === 2. IDENTIFICAR MATRIZ ===
        info("🏪 Identificando matriz...")
        nome_matriz = "COMCARNE MATRIZ SAO LUIS"
        
        if nome_matriz in df_estoque['Loja'].values:
            info(f"✅ Matriz encontrada: {nome_matriz}")
            df_matriz = df_estoque[df_estoque['Loja'] == nome_matriz][['Codigo_Norm', 'Estoque_Loja']].copy()
            df_matriz = df_matriz.rename(columns={'Estoque_Loja': 'Estoque_Matriz'})
            
            # Adicionar Estoque_Matriz ao DataFrame principal
            df_estoque = df_estoque.merge(df_matriz, on='Codigo_Norm', how='left')
            df_estoque['Estoque_Matriz'] = df_estoque['Estoque_Matriz'].fillna(0)
            info(f"   Estoque matriz calculado para {len(df_matriz)} produtos")
        else:
            warning(f"⚠️ Matriz '{nome_matriz}' não encontrada")
            df_estoque['Estoque_Matriz'] = 0

        # === 3. JUNTAR DADOS (ESTOQUE COMO BASE) ===
        info("🔄 Juntando dados...")
        
        # Join com Curva ABC (vendas)
        df_temp = pd.merge(
            df_estoque,
            df_curva[['Cadeamento', 'Vendas']],
            on='Cadeamento',
            how='left'
        )
        info(f"   Após join com vendas: {len(df_temp)} linhas")
        
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

        info(f"📊 Total de linhas após joins: {len(df_final)}")

        # === 4. PREENCHER VALORES NULOS ===
        info("📋 Preparando colunas...")
        
        df_final['Vendas'] = df_final['Vendas'].fillna(0)
        df_final['Media_Vendas'] = df_final['Media_Vendas'].fillna(0)
        
        # Verificar quantos produtos têm média
        produtos_com_media = len(df_final[df_final['Media_Vendas'] > 0])
        info(f"   Produtos com média de vendas: {produtos_com_media}")

        # === 5. ADICIONAR COLUNAS CALCULADAS ===
        info("🧮 Calculando colunas derivadas...")
        
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
            # Estatísticas de compradores
            compradores_count = df_final['COMPRADOR'].value_counts()
            info(f"   Compradores identificados: {len(compradores_count)}")
            for comp, qtd in compradores_count.head(3).items():
                debug(f"      {comp}: {qtd} produtos")
        else:
            warning("⚠️ Coluna 'Grupo' não encontrada")
            df_final['COMPRADOR'] = "NÃO MAPEADO"
        
        # RUPTURA
        df_final['RUPTURA'] = df_final.apply(self._status_ruptura, axis=1)
        
        # Colunas em branco
        df_final['Valor Estoque'] = ""
        df_final['Preço'] = ""

        # === 6. ORGANIZAR COLUNAS NA ORDEM SOLICITADA ===
        info("📋 Organizando colunas...")
        
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
            # Converter para numérico, forçando inteiro
            df_final['CÓDIGO'] = pd.to_numeric(df_final['CÓDIGO'], errors='coerce').fillna(0).astype(int)
            info("✅ Coluna CÓDIGO convertida para inteiro")
        
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
                debug(f"   Coluna '{col}' criada vazia")
        
        # Reordenar
        df_final = df_final[colunas_ordem]

        # Estatísticas finais
        total_ruptura = len(df_final[df_final['RUPTURA'] == 'RUPTURA'])
        total_sem_estoque = len(df_final[df_final['ESTQ LOJA'] == 0])
        
        info(f"\n✅ Relatório de Ruptura gerado com sucesso!")
        info(f"📊 Total de linhas: {len(df_final)}")
        info(f"⚠️  Produtos em ruptura: {total_ruptura}")
        info(f"📦 Produtos sem estoque: {total_sem_estoque}")
        
        self.df_processado = df_final
        return df_final

    def get_preview(self, df, linhas=20):
        """Mostra as primeiras linhas formatadas"""
        if df is None or len(df) == 0:
            warning("⚠️ Tentativa de preview com DataFrame vazio")
            return "Nenhum dado processado"
        
        info(f"📋 Gerando preview com {min(linhas, len(df))} linhas")
        
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
            warning("⚠️ Tentativa de resumo com DataFrame vazio")
            return "Nenhum dado processado"
        
        info("📊 Gerando resumo estatístico")
        
        linhas = []
        linhas.append("=" * 60)
        linhas.append("📊 RESUMO DO RELATÓRIO DE RUPTURA")
        linhas.append("=" * 60)
        linhas.append(f"📦 Total de produtos: {len(df)}")
        
        # Produtos em ruptura
        if 'RUPTURA' in df.columns:
            ruptura = len(df[df['RUPTURA'] == 'RUPTURA'])
            perc_ruptura = (ruptura/len(df)*100) if len(df) > 0 else 0
            linhas.append(f"⚠️  Produtos em ruptura: {ruptura} ({perc_ruptura:.1f}%)")
        
        # Produtos sem estoque
        if 'ESTQ LOJA' in df.columns:
            sem_estoque = len(df[df['ESTQ LOJA'] <= 0])
            perc_sem_estoque = (sem_estoque/len(df)*100) if len(df) > 0 else 0
            linhas.append(f"📦 Produtos sem estoque: {sem_estoque} ({perc_sem_estoque:.1f}%)")
        
        # Por comprador
        if 'COMPRADOR' in df.columns:
            linhas.append("\n👤 Por Comprador:")
            for comp, qtd in df['COMPRADOR'].value_counts().head(10).items():
                if comp != "NÃO MAPEADO" and pd.notna(comp):
                    perc = (qtd/len(df)*100)
                    linhas.append(f"   {comp:<20} {qtd:>6} produtos ({perc:.1f}%)")
            
            # Mostrar não mapeados se houver
            nao_mapeados = len(df[df['COMPRADOR'] == 'NÃO MAPEADO'])
            if nao_mapeados > 0:
                perc_nao_mapeados = (nao_mapeados/len(df)*100)
                linhas.append(f"\n⚠️  Grupos não mapeados: {nao_mapeados} produtos ({perc_nao_mapeados:.1f}%)")
        
        # Por categoria (top 5)
        if 'CATEGORIA' in df.columns:
            linhas.append("\n📁 Top 5 Categorias:")
            for cat, qtd in df['CATEGORIA'].value_counts().head(5).items():
                if cat and str(cat).strip():
                    perc = (qtd/len(df)*100)
                    linhas.append(f"   {cat[:30]:<30} {qtd:>6} produtos ({perc:.1f}%)")
        
        # Por loja (top 5)
        if 'LOJA' in df.columns:
            linhas.append("\n🏪 Top 5 Lojas:")
            for loja, qtd in df['LOJA'].value_counts().head(5).items():
                if loja and str(loja).strip():
                    perc = (qtd/len(df)*100)
                    linhas.append(f"   {loja[:30]:<30} {qtd:>6} produtos ({perc:.1f}%)")
        
        info(f"✅ Resumo gerado com {len(linhas)} linhas")
        return "\n".join(linhas)

    def exportar_para_excel(self, df, caminho):
        """Exporta o relatório para Excel com formatação"""
        try:
            info(f"💾 Exportando relatório para: {caminho}")
            
            if df is None or len(df) == 0:
                error("❌ Tentativa de exportar DataFrame vazio")
                return False
            
            # Criar writer do Excel
            with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Ruptura', index=False)
                
                # Ajustar largura das colunas
                worksheet = writer.sheets['Ruptura']
                for i, col in enumerate(df.columns):
                    # Calcular largura máxima
                    max_len = max(
                        df[col].astype(str).map(len).max() if len(df) > 0 else 0,
                        len(str(col))
                    ) + 2
                    # Limitar a 50 caracteres
                    worksheet.column_dimensions[chr(65 + i)].width = min(max_len, 50)
            
            info(f"✅ Relatório exportado com sucesso: {caminho}")
            return True
            
        except Exception as e:
            error(f"❌ Erro ao exportar para Excel: {e}")
            return False