# debug_roda_modelo.py
"""
Debug que RODA O MODELO CURVA ABC e mostra o resultado.
"""
import sys
import os
import pandas as pd

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("="*80)
print("🔥 RODANDO O MODELO CURVA ABC")
print("="*80)

# 1. Importar modelo
from src.models.modelo_curva_abc import ModeloCurvaABC
modelo = ModeloCurvaABC()

# 2. Caminho do arquivo
caminho = r"C:\Users\Compras Fribal\Downloads\VENDAS FEV CONV E FRIOS.xlsx"
print(f"\n📁 Arquivo: {caminho}")

# 3. Ler e processar
df_raw = pd.read_excel(caminho, header=None)
df_processado = modelo.processar(df_raw)

print(f"\n✅ Processado: {len(df_processado)} linhas")
print(f"📋 Colunas: {list(df_processado.columns)}")

# 4. Usar o MÉTODO DO PRÓPRIO MODELO para mostrar
print("\n" + "="*80)
print("📋 PREVIEW PELO PRÓPRIO MODELO:")
print("="*80)
print(modelo.get_preview(df_processado, 5))

# 5. Mostrar os dados de forma simples
print("\n" + "="*80)
print("📋 DADOS SIMPLES:")
print("="*80)

# Pegar as primeiras 5 linhas
for i in range(min(5, len(df_processado))):
    print(f"\nLinha {i}:")
    # Acessar cada coluna que sabemos que existe
    print(f"  Loja: {df_processado.iloc[i]['Loja_Nome']}")
    # As outras colunas estão nas posições 0-10
    print(f"  Código: {df_processado.iloc[i, 0]}")
    print(f"  Produto: {df_processado.iloc[i, 1]}")
    print(f"  Qtd: {df_processado.iloc[i, 4]}")

print("\n" + "="*80)
print("✅ FINALIZADO")
print("="*80)