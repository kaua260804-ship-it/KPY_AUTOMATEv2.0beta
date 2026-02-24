# fix_imports.py
"""
Arquivo para corrigir imports e inicialização do CustomTkinter
"""
import sys
import os
import customtkinter as ctk

# Forçar a criação da janela raiz antes de qualquer import
root = ctk.CTk()
root.withdraw()  # Esconder temporariamente

# Agora importar o resto
from src.utils.logger import info, error, warning, debug
from src.utils.config import ESCURO, CLARO, get_layout
from src.utils.helpers import centralizar_janela
from src.ui.menu import MenuLateral
from src.ui.telas.tela_resultado import TelaResultado
from src.ui.telas.tela_entradas import TelaEntradas
from src.ui.telas.tela_criar_relatorio import TelaCriarRelatorio
from src.core.identificador import IdentificadorModelos

# Fechar a janela temporária
root.destroy()

print("✅ Imports corrigidos!")