# src/utils/config.py
"""
Configurações de cores e temas do programa.
Versão 2.2.0 - Com temas personalizados e configurações do usuário
"""
import tkinter as tk

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

# ===== TEMAS PERSONALIZADOS =====
# Cada tema tem cor primária (destaque) e secundária (botão filtro)
TEMAS_PERSONALIZADOS = {
    'Vermelho': {
        'destaque': '#8b0000',
        'secundario': '#a52a2a',
        'nome': 'Vermelho Clássico'
    },
    'Azul': {
        'destaque': '#1e3a8a',
        'secundario': '#2563eb',
        'nome': 'Azul Marinho'
    },
    'Verde': {
        'destaque': '#166534',
        'secundario': '#16a34a',
        'nome': 'Verde Floresta'
    },
    'Roxo': {
        'destaque': '#581c87',
        'secundario': '#7e22ce',
        'nome': 'Roxo Real'
    },
    'Laranja': {
        'destaque': '#9a3412',
        'secundario': '#ea580c',
        'nome': 'Laranja Queimado'
    },
    'Rosa': {
        'destaque': '#831843',
        'secundario': '#db2777',
        'nome': 'Rosa Pink'
    },
    'Ciano': {
        'destaque': '#164e63',
        'secundario': '#0891b2',
        'nome': 'Ciano Profundo'
    },
    'Amarelo': {
        'destaque': '#854d0e',
        'secundario': '#ca8a04',
        'nome': 'Amarelo Mostarda'
    },
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

# ===== FUNÇÃO PARA OBTER TEMA PERSONALIZADO =====
def get_tema_personalizado(nome_tema, tema_base='escuro'):
    """
    Retorna um tema personalizado baseado no tema base (escuro/claro)
    
    Args:
        nome_tema: Nome do tema personalizado (ex: 'Vermelho', 'Azul')
        tema_base: 'escuro' ou 'claro'
    
    Returns:
        dict: Cores do tema personalizado
    """
    # Pegar o tema base
    tema = ESCURO.copy() if tema_base == 'escuro' else CLARO.copy()
    
    # Aplicar cores personalizadas se existirem
    if nome_tema in TEMAS_PERSONALIZADOS:
        cores_personalizadas = TEMAS_PERSONALIZADOS[nome_tema]
        tema['destaque'] = cores_personalizadas['destaque']
        tema['botao_exportar'] = cores_personalizadas['destaque']
        tema['botao_filtro'] = cores_personalizadas['secundario']
        
        # Ajustar cores derivadas
        if tema_base == 'escuro':
            tema['macro_emporio'] = "#5d8c6b"      # Mantém verde
            tema['macro_mercearia'] = "#b8860b"    # Mantém dourado
            tema['macro_outros'] = "#6a5acd"       # Mantém roxo
        else:
            tema['macro_emporio'] = "#2e7d32"
            tema['macro_mercearia'] = "#b76e1e"
            tema['macro_outros'] = "#5e35b1"
    
    return tema

# ===== FUNÇÃO PARA LISTAR TEMAS DISPONÍVEIS =====
def listar_temas_disponiveis():
    """Retorna lista com nomes de todos os temas disponíveis"""
    return list(TEMAS_PERSONALIZADOS.keys())

# ===== FUNÇÃO PARA OBTER INFO DO TEMA =====
def get_info_tema(nome_tema):
    """Retorna informações detalhadas de um tema"""
    if nome_tema in TEMAS_PERSONALIZADOS:
        return TEMAS_PERSONALIZADOS[nome_tema]
    return None

# ===== FUNÇÃO PARA CALCULAR TAMANHO DA JANELA =====
def get_tamanho_janela():
    """
    Calcula o tamanho ideal da janela baseado na resolução da tela
    
    Returns:
        tuple: (largura, altura) em pixels
    """
    # Criar uma janela temporária para pegar as dimensões da tela
    root = tk.Tk()
    root.withdraw()  # Esconder a janela temporária
    
    # Pegar dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    
    # Destruir a janela temporária
    root.destroy()
    
    # Calcular tamanho proporcional (80% da tela, mas com limites)
    largura = int(largura_tela * 0.8)
    altura = int(altura_tela * 0.8)
    
    # Limitar tamanho mínimo e máximo
    largura = max(1000, min(largura, 1600))  # Entre 1000 e 1600 pixels
    altura = max(600, min(altura, 900))      # Entre 600 e 900 pixels
    
    return largura, altura

# ===== CONFIGURAÇÕES DE LAYOUT =====
def get_layout():
    """Retorna as configurações de layout com tamanho dinâmico"""
    largura, altura = get_tamanho_janela()
    return {
        'largura_janela': largura,
        'altura_janela': altura,
        'codigo_largura': 10,
        'produto_largura': 50,
        'qtd_largura': 15,
        'total_largura': 20,
        'loja_largura': 15,
        'preview_total': 115,
    }

# Por compatibilidade, manter LAYOUT como dicionário (mas agora é função)
LAYOUT = get_layout()

# ===== CONFIGURAÇÕES DE FONTE =====
FONTES_DISPONIVEIS = [
    "Arial",
    "Helvetica",
    "Times New Roman",
    "Courier New",
    "Verdana",
    "Tahoma",
    "Segoe UI",
    "Calibri"
]

def get_fonte_padrao():
    """Retorna a fonte padrão do sistema"""
    return "Arial"

# ===== CONFIGURAÇÕES DE MODO COMPACTO =====
MODO_COMPACTO_PADRAO = {
    'largura_minima': 800,
    'altura_minima': 500,
    'ocultar_preview': False,
    'ocultar_resumo': False,
    'tamanho_fonte': 10
}

def get_config_modo_compacto():
    """Retorna configuração padrão do modo compacto"""
    return MODO_COMPACTO_PADRAO.copy()