# src/utils/screen_config.py
"""
Configurações de tela para diferentes resoluções
"""
import tkinter as tk

class ScreenManager:
    """Gerenciador de configurações de tela"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializa as configurações de tela"""
        # Criar janela temporária
        root = tk.Tk()
        root.withdraw()
        
        self.largura_tela = root.winfo_screenwidth()
        self.altura_tela = root.winfo_screenheight()
        
        root.destroy()
        
        # Classificar o tipo de tela
        if self.largura_tela <= 1366:
            self.tipo_tela = "pequena"
        elif self.largura_tela <= 1920:
            self.tipo_tela = "media"
        else:
            self.tipo_tela = "grande"
    
    def get_tamanho_janela(self, porcentagem=0.8):
        """Retorna tamanho da janela baseado na porcentagem da tela"""
        largura = int(self.largura_tela * porcentagem)
        altura = int(self.altura_tela * porcentagem)
        
        # Limites
        largura = max(1000, min(largura, 1600))
        altura = max(600, min(altura, 900))
        
        return largura, altura
    
    def get_fonte_tamanho(self, base=12):
        """Ajusta tamanho da fonte baseado na tela"""
        if self.tipo_tela == "pequena":
            return base
        elif self.tipo_tela == "media":
            return base + 1
        else:
            return base + 2
    
    def get_info_tela(self):
        """Retorna informações da tela"""
        return {
            'largura': self.largura_tela,
            'altura': self.altura_tela,
            'tipo': self.tipo_tela,
            'proporcao': f"{self.largura_tela}x{self.altura_tela}"
        }

# Singleton
screen = ScreenManager()