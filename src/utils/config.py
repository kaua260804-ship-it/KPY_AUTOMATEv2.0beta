# src/utils/config.py
"""
Configurações de cores e temas do programa.
"""

# ===== CORES DO TEMA ESCURO (PADRÃO) =====
ESCURO = {
    'menu': "#1a1a1a",
    'fundo': "#2d2d2d",
    'destaque': "#8b0000",
    'texto': "#ffffff",
    'texto_secundario': "#cccccc",
    'entrada': "#3d3d3d",
    'botao_exportar': "#8b0000",
    'botao_limpar': "#666666",
    'botao_filtro': "#4a6da8",
    'macro_emporio': "#5d8c6b",    # Verde
    'macro_mercearia': "#b8860b",   # Dourado
    'macro_outros': "#6a5acd",      # Azul royal
    'scrollbar': "#4d4d4d",
    'scrollbar_trough': "#333333",
}

# ===== CORES DO TEMA CLARO =====
CLARO = {
    'menu': "#e0e0e0",
    'fundo': "#f5f5f5",
    'destaque': "#c62828",
    'texto': "#000000",
    'texto_secundario': "#666666",
    'entrada': "#ffffff",
    'botao_exportar': "#c62828",
    'botao_limpar': "#9e9e9e",
    'botao_filtro': "#1565c0",
    'macro_emporio': "#2e7d32",
    'macro_mercearia': "#b76e1e",
    'macro_outros': "#5e35b1",
    'scrollbar': "#b0b0b0",
    'scrollbar_trough': "#e0e0e0",
}

# ===== LOJAS DESTAQUE =====
LOJAS_DESTAQUE = [
    "CALHAU", "COHAMA", "CURVA DO 90", "EMPORIO FRIBAL TERESINA",
    "EMPORIO IMPERATRIZ", "MERCEARIA MAIOBAO", "MERCEARIA SANTA INES",
    "PENINSULA PTA AREIA", "PONTA D AREIA", "TURU"
]

# ===== MACROS DE FILTRO =====
MACROS = {
    'emporio': [
        "PONTA D AREIA", "CALHAU", "PENINSULA PTA AREIA", "COHAMA",
        "EMPORIO FRIBAL TERESINA", "EMPORIO IMPERATRIZ", "TURU"
    ],
    'mercearia': [
        "CURVA DO 90", "MERCEARIA SANTA INES", "MERCEARIA MAIOBAO"
    ]
}

# ===== CONFIGURAÇÕES DE LAYOUT =====
LAYOUT = {
    'largura_janela': 1400,
    'altura_janela': 900,
    'codigo_largura': 10,
    'produto_largura': 50,
    'qtd_largura': 15,
    'total_largura': 20,
    'loja_largura': 15,
    'preview_total': 115,
}