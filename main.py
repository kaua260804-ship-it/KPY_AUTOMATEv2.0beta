# main.py
"""
Ponto de entrada do programa K'PY AUTOMATE.
Versão 2.2.0 - Com ajuste de fonte e temas personalizados
"""
import sys
import os
import customtkinter as ctk

# Configurar o tema e aparência do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("="*50)
print("🚀 K'PY AUTOMATE - BY.KAUA")
print("="*50)

try:
    from src.utils.config import ESCURO, CLARO, LAYOUT, get_tema_personalizado, listar_temas_disponiveis
    from src.utils.helpers import centralizar_janela
    from src.ui.menu import MenuLateral
    from src.ui.telas.tela_resultado import TelaResultado
    from src.ui.telas.tela_entradas import TelaEntradas
    from src.ui.telas.tela_criar_relatorio import TelaCriarRelatorio
    from src.core.identificador import IdentificadorModelos
    from src.utils.config_manager import config
    print("✅ Módulos importados com sucesso!")
except Exception as e:
    print(f"❌ Erro: {e}")
    input("Pressione Enter...")
    sys.exit(1)

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("K'PY AUTOMATE - BY.KAUA")
        
        # Carregar configurações salvas
        self.tema_atual = config.get('tema', 'escuro')
        self.cor_destaque = config.get('cor_destaque', '#8b0000')
        self.fonte_atual = config.get('tamanho_fonte', 12)
        
        # Configurar tamanho da janela
        self.root.geometry(f"{LAYOUT['largura_janela']}x{LAYOUT['altura_janela']}")
        centralizar_janela(self.root, LAYOUT['largura_janela'], LAYOUT['altura_janela'])
        
        # Configurar grid para expandir
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Definir tema inicial
        self.tema_escuro = (self.tema_atual == 'escuro')
        self._carregar_tema()
        
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
        
        # ===== MENU LATERAL =====
        self.menu = MenuLateral(self.root, self.cores, self.callbacks, self.toggle_tema, app=self)
        
        # ===== ÁREA DE TRABALHO =====
        self.frame_work = ctk.CTkFrame(
            self.root,
            fg_color=self.cores['fundo'],
            corner_radius=0
        )
        self.frame_work.grid(row=0, column=1, sticky='nsew')
        
        # Criar as telas
        self._criar_telas()
        
        # Abre tela inicial
        self.abrir_curva_abc()
        
        print("✅ Aplicação iniciada com sucesso!")
        print(f"📐 Tamanho da janela: {LAYOUT['largura_janela']}x{LAYOUT['altura_janela']}")
        print(f"🔤 Fonte: {self.fonte_atual}pt")
    
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
    
    def _carregar_tema(self):
        """Carrega as cores do tema baseado nas configurações"""
        if self.tema_escuro:
            self.cores = ESCURO.copy()
        else:
            self.cores = CLARO.copy()
        
        # Aplicar cor personalizada se existir
        tema_personalizado = config.get('tema_personalizado')
        if tema_personalizado:
            self.cores = get_tema_personalizado(
                tema_personalizado, 
                'escuro' if self.tema_escuro else 'claro'
            )
    
    def toggle_tema(self):
        """Alterna entre tema claro e escuro"""
        self.tema_escuro = not self.tema_escuro
        config.set('tema', 'escuro' if self.tema_escuro else 'claro')
        self._carregar_tema()
        
        # Atualizar aparência do CustomTkinter
        if self.tema_escuro:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        
        # Atualizar cores da interface
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
        
        print(f"🎨 Tema alterado para: {'Escuro' if self.tema_escuro else 'Claro'}")
    
    def aplicar_tema_personalizado(self, nome_tema):
        """Aplica um tema personalizado"""
        config.set('tema_personalizado', nome_tema)
        self._carregar_tema()
        
        # Atualizar menu com novas cores
        self.menu.aplicar_tema_personalizado(nome_tema, self.cores)
        
        # Atualizar todas as telas
        for nome, tela in self.telas.items():
            if hasattr(tela, 'atualizar_cores'):
                tela.atualizar_cores(self.cores)
        
        print(f"🎨 Tema personalizado aplicado: {nome_tema}")
    
    def abrir_seletor_temas(self):
        """Abre a tela de seleção de temas"""
        try:
            from src.ui.telas.tela_temas import TelaTemas
            
            def callback_tema(nome_tema):
                self.aplicar_tema_personalizado(nome_tema)
            
            TelaTemas(self.root, self.cores, callback_tema)
        except Exception as e:
            print(f"❌ Erro ao abrir seletor de temas: {e}")
            import traceback
            traceback.print_exc()
    
    def atualizar_fonte_global(self, tamanho):
        """Atualiza o tamanho da fonte em todas as telas"""
        for nome, tela in self.telas.items():
            if hasattr(tela, 'atualizar_fonte'):
                tela.atualizar_fonte(tamanho)
    
    def _esconder_todas_telas(self):
        """Esconde todas as telas"""
        for tela in self.telas.values():
            if hasattr(tela, 'frame') and tela.frame:
                tela.frame.pack_forget()
    
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
    root = ctk.CTk()
    app = Aplicacao(root)
    root.mainloop()

if __name__ == "__main__":
    main()