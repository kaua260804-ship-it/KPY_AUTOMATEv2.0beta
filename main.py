# main.py
"""
Ponto de entrada do programa K'PY AUTOMATE com Splash Screen.
"""
import sys
import os
import customtkinter as ctk
import time
import threading

# Importar a splash screen
from splash_screen import SplashScreen

# IMPORTAR TODOS OS MÓDULOS NECESSÁRIOS AQUI
try:
    from src.utils.config import ESCURO, CLARO, LAYOUT
    from src.utils.helpers import centralizar_janela
    from src.ui.menu import MenuLateral
    from src.ui.telas.tela_resultado import TelaResultado
    from src.ui.telas.tela_entradas import TelaEntradas
    from src.ui.telas.tela_criar_relatorio import TelaCriarRelatorio
    from src.core.identificador import IdentificadorModelos
    print("✅ Módulos importados com sucesso!")
except Exception as e:
    print(f"❌ Erro ao importar módulos: {e}")
    input("Pressione Enter para sair...")
    sys.exit(1)

# Configurar o tema e aparência do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

class Aplicacao:
    def __init__(self, root, splash=None):
        self.root = root
        self.splash = splash
        
        # Se tiver splash, atualizar status
        if self.splash:
            self.splash.atualizar_status("Configurando interface...", 60)
        
        self.root.title("K'PY AUTOMATE - BY.KAUA")
        
        # Configurar ícone da janela principal
        self._configurar_icone()
        
        # Configurar tamanho
        self.root.geometry(f"{LAYOUT['largura_janela']}x{LAYOUT['altura_janela']}")
        centralizar_janela(self.root, LAYOUT['largura_janela'], LAYOUT['altura_janela'])
        
        # Configurar grid para expandir
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.tema_escuro = True
        self._carregar_tema()
        
        if self.splash:
            self.splash.atualizar_status("Inicializando identificador...", 70)
        
        # Inicializa o identificador
        self.identificador = IdentificadorModelos()
        
        # Dicionário para guardar as telas
        self.telas = {}
        
        # Callbacks para cada relatório
        self.callbacks = {
            'curva_abc': self.abrir_curva_abc,
            'entradas_grupo': self.abrir_entradas,
            'criar_relatorio': self.abrir_criar_relatorio
        }
        
        if self.splash:
            self.splash.atualizar_status("Criando menu lateral...", 75)
        
        # ===== MENU LATERAL =====
        self.menu = MenuLateral(self.root, self.cores, self.callbacks, self.toggle_tema)
        
        # ===== ÁREA DE TRABALHO =====
        self.frame_work = ctk.CTkFrame(
            self.root,
            fg_color=self.cores['fundo'],
            corner_radius=0
        )
        self.frame_work.grid(row=0, column=1, sticky='nsew')
        
        if self.splash:
            self.splash.atualizar_status("Criando telas...", 80)
        
        # Criar as telas
        self._criar_telas()
        
        if self.splash:
            self.splash.atualizar_status("Finalizando...", 90)
        
        # Abre tela inicial
        self.abrir_curva_abc()
        
        if self.splash:
            self.splash.atualizar_status("Pronto!", 100)
            time.sleep(0.3)
            self.splash.fechar()
    
    def _configurar_icone(self):
        """Configura o ícone da janela principal"""
        try:
            caminho_icon = r"C:\Users\Compras Fribal\Documents\Programação\KPY_AUTOMATEv2.0\assets\icons\logo.ico"
            if os.path.exists(caminho_icon):
                self.root.iconbitmap(caminho_icon)
            else:
                print(f"⚠️ Ícone não encontrado: {caminho_icon}")
        except Exception as e:
            print(f"⚠️ Erro ao configurar ícone: {e}")
    
    def _criar_telas(self):
        """Cria todas as telas uma única vez"""
        print("🔄 Criando telas...")
        
        # Tela Curva ABC
        self.telas['curva_abc'] = TelaResultado(self.frame_work, self.cores, self.identificador)
        
        # Tela Entradas
        self.telas['entradas'] = TelaEntradas(self.frame_work, self.cores)
        
        # Tela Criar Relatório
        self.telas['criar_relatorio'] = TelaCriarRelatorio(self.frame_work, self.cores)
        
        print("✅ Telas criadas!")
    
    def _esconder_todas_telas(self):
        """Esconde todas as telas"""
        for tela in self.telas.values():
            if hasattr(tela, 'frame') and tela.frame:
                tela.frame.pack_forget()
    
    def _carregar_tema(self):
        """Carrega as cores do tema"""
        self.cores = ESCURO if self.tema_escuro else CLARO
    
    def toggle_tema(self):
        """Alterna entre tema claro e escuro"""
        self.tema_escuro = not self.tema_escuro
        self._carregar_tema()
        
        # Atualizar aparência do CustomTkinter
        if self.tema_escuro:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        
        self.root.configure(fg_color=self.cores['fundo'])
        self.menu.atualizar_cores(self.cores)
        self.frame_work.configure(fg_color=self.cores['fundo'])
        
        # Atualizar cores de todas as telas
        for nome, tela in self.telas.items():
            if hasattr(tela, 'atualizar_cores'):
                tela.atualizar_cores(self.cores)
        
        # Reexibir a tela atual
        tela_atual = None
        for nome, tela in self.telas.items():
            if hasattr(tela, 'frame') and tela.frame and tela.frame.winfo_ismapped():
                tela_atual = tela
                break
        
        if tela_atual and hasattr(tela_atual, 'frame'):
            tela_atual.frame.pack(fill='both', expand=True)
    
    def abrir_curva_abc(self):
        """Abre a tela de Curva ABC sem perder dados"""
        print("📊 Abrindo Curva ABC")
        self._esconder_todas_telas()
        tela = self.telas['curva_abc']
        
        if not hasattr(tela, 'frame') or not tela.frame:
            tela.mostrar()
        else:
            tela.frame.pack(fill='both', expand=True)
        
        self.frame_work.update_idletasks()
    
    def abrir_entradas(self):
        """Abre a tela de Entradas sem perder dados"""
        print("📦 Abrindo Entradas")
        self._esconder_todas_telas()
        tela = self.telas['entradas']
        
        if not hasattr(tela, 'frame') or not tela.frame:
            tela.mostrar()
        else:
            tela.frame.pack(fill='both', expand=True)
        
        self.frame_work.update_idletasks()
    
    def abrir_criar_relatorio(self):
        """Abre a tela de Criar Relatório"""
        print("📋 Abrindo Criar Relatório")
        self._esconder_todas_telas()
        tela = self.telas['criar_relatorio']
        
        if not hasattr(tela, 'frame') or not tela.frame:
            tela.mostrar()
        else:
            tela.frame.pack(fill='both', expand=True)
        
        self.frame_work.update_idletasks()

def main():
    print("🚀 Iniciando K'PY AUTOMATE com Splash Screen...")
    
    # Cria a splash screen
    splash = SplashScreen()
    splash.atualizar_status("Iniciando...", 10)
    
    # Pequena pausa para visualização
    time.sleep(0.5)
    
    splash.atualizar_status("Preparando ambiente...", 20)
    time.sleep(0.3)
    
    splash.atualizar_status("Carregando módulos...", 30)
    time.sleep(0.3)
    
    splash.atualizar_status("Configurando interface...", 40)
    time.sleep(0.3)
    
    # Fecha a splash antes de abrir a janela principal
    splash.fechar()
    
    # Agora abre a janela principal normalmente
    print("✅ Splash finalizada, abrindo programa principal...")
    root = ctk.CTk()
    app = Aplicacao(root)  # Não passa a splash
    root.mainloop()

if __name__ == "__main__":
    main()