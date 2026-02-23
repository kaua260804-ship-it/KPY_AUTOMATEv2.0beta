# src/utils/icones.py
"""
Gerenciador de ícones para o programa.
"""
import os
from src.utils.helpers import resource_path

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except:
    PIL_AVAILABLE = False

class GerenciadorIcones:
    """Classe para gerenciar os ícones do programa"""
    
    def __init__(self):
        self.icones = {}
        self.carregar_icones()
    
    def carregar_icones(self):
        """Carrega todos os ícones das pastas"""
        if not PIL_AVAILABLE:
            return
        
        # Lista de ícones para carregar
        icones = {
            'caixa': 'icone_caixa.png',
            'loja': 'icone_loja.png',
            'dinheiro': 'icone_dinheiro.png',
            'grafico': 'icone_grafico.png',
            'filtro': 'icone_filtro.png',
            'limpar': 'icone_limpar.png',
            'salvar': 'icone_salvar.png',
            'ok': 'icone_ok.png',
            'tema': 'icone_tema.png',
            'procurar': 'icone_procurar.png',
            'processar': 'icone_processar.png',
        }
        
        for nome, arquivo in icones.items():
            caminho = resource_path(f"assets/icons/ui/{arquivo}")
            if os.path.exists(caminho):
                try:
                    img = Image.open(caminho)
                    img = img.resize((20, 20), Image.Resampling.LANCZOS)
                    self.icones[nome] = ImageTk.PhotoImage(img)
                except:
                    self.icones[nome] = None
            else:
                self.icones[nome] = None
    
    def get_icone(self, nome):
        """Retorna um ícone carregado"""
        return self.icones.get(nome)