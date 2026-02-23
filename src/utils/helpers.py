# src/utils/helpers.py
"""
Funções auxiliares para formatação e utilitários.
"""
import pandas as pd
import os
import sys

def formatar_br(valor, tipo='moeda'):
    """
    Formata números no padrão brasileiro.
    
    Args:
        valor: Número a ser formatado
        tipo: 'moeda', 'inteiro', 'decimal_3', 'decimal_2', 'decimal_1'
    
    Returns:
        str: Número formatado
    """
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
        elif tipo == 'decimal_1':
            return f"{valor_float:,.1f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            return str(valor_float).replace('.', ',')
    except:
        return str(valor)

def get_resource_path(relative_path):
    """
    Retorna o caminho correto para arquivos, tanto em desenvolvimento quanto no executável.
    
    Args:
        relative_path: Caminho relativo ao diretório base (ex: "data/media_vendas.xlsx")
    
    Returns:
        str: Caminho absoluto correto
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
        print(f"📦 Rodando como executável, _MEIPASS: {base_path}")
    except Exception:
        # Rodando como script normal
        base_path = os.path.abspath(".")
        print(f"📁 Rodando como script, base_path: {base_path}")
    
    full_path = os.path.join(base_path, relative_path)
    print(f"🔍 Caminho completo: {full_path}")
    print(f"✅ Existe: {os.path.exists(full_path)}")
    
    return full_path

def get_base_path():
    """
    Retorna o caminho base do programa.
    Funciona tanto em modo desenvolvimento (.py) quanto em executável (.exe)
    """
    if getattr(sys, 'frozen', False):
        # Rodando como executável
        return os.path.dirname(sys.executable)
    else:
        # Rodando como script
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def resource_path(relative_path):
    """
    Retorna o caminho absoluto para recursos (ícones, imagens).
    
    Args:
        relative_path: Caminho relativo ao diretório base
    
    Returns:
        str: Caminho absoluto
    """
    base_path = get_base_path()
    return os.path.join(base_path, relative_path)

def centralizar_janela(janela, largura, altura):
    """
    Centraliza uma janela na tela.
    
    Args:
        janela: Objeto Tk/Toplevel
        largura: Largura desejada
        altura: Altura desejada
    """
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f'{largura}x{altura}+{x}+{y}')