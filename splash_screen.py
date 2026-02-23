# splash_screen.py
"""
Tela de carregamento (splash screen) para o K'PY AUTOMATE
"""
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import os
import time

class SplashScreen:
    """Tela de carregamento que aparece enquanto o programa inicializa"""
    
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.overrideredirect(True)  # Remove bordas da janela
        
        # Configurar tamanho e posição
        largura = 500
        altura = 300
        self._centralizar(largura, altura)
        
        # Cor de fundo
        self.janela.configure(bg='#2d2d2d')
        
        # Frame principal
        self.frame = tk.Frame(
            self.janela,
            bg='#2d2d2d',
            highlightbackground='#8b0000',
            highlightthickness=2
        )
        self.frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Carregar e redimensionar logo
        self._carregar_logo()
        
        # Título
        Label(
            self.frame,
            text="K'PY AUTOMATE",
            font=("Arial", 24, "bold"),
            bg='#2d2d2d',
            fg='#8b0000'
        ).pack(pady=(20, 5))
        
        # Subtítulo
        Label(
            self.frame,
            text="BY.KAUA",
            font=("Arial", 12),
            bg='#2d2d2d',
            fg='#cccccc'
        ).pack()
        
        # Espaço
        tk.Frame(self.frame, height=30, bg='#2d2d2d').pack()
        
        # Texto de carregamento
        self.label_status = Label(
            self.frame,
            text="Inicializando...",
            font=("Arial", 10),
            bg='#2d2d2d',
            fg='#ffffff'
        )
        self.label_status.pack(pady=10)
        
        # Barra de progresso
        self.progress_frame = tk.Frame(
            self.frame,
            width=300,
            height=10,
            bg='#3d3d3d'
        )
        self.progress_frame.pack(pady=5)
        self.progress_frame.pack_propagate(False)
        
        self.progress_bar = tk.Frame(
            self.progress_frame,
            width=0,
            height=10,
            bg='#8b0000'
        )
        self.progress_bar.place(x=0, y=0)
        
        # Porcentagem
        self.label_porcentagem = Label(
            self.frame,
            text="0%",
            font=("Arial", 9),
            bg='#2d2d2d',
            fg='#8b0000'
        )
        self.label_porcentagem.pack()
        
        # Versão
        Label(
            self.frame,
            text="Versão 2.0",
            font=("Arial", 8),
            bg='#2d2d2d',
            fg='#666666'
        ).pack(side='bottom', pady=10)
        
        self.janela.update()
    
    def _centralizar(self, largura, altura):
        """Centraliza a janela na tela"""
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
    
    def _carregar_logo(self):
        """Tenta carregar o logo do arquivo .ico"""
        try:
            from PIL import Image, ImageTk
            
            # Caminho do ícone
            caminho_icon = r"C:\Users\Compras Fribal\Documents\Programação\KPY_AUTOMATEv2.0\assets\icons\logo.ico"
            
            if os.path.exists(caminho_icon):
                # Carregar como PhotoImage para tkinter
                self.janela.iconbitmap(caminho_icon)
                
                # Tentar carregar para exibir na splash
                img = Image.open(caminho_icon)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                self.logo = ImageTk.PhotoImage(img)
                
                Label(
                    self.frame,
                    image=self.logo,
                    bg='#2d2d2d'
                ).pack(pady=10)
            else:
                # Mostrar texto alternativo
                Label(
                    self.frame,
                    text="K'PY",
                    font=("Arial", 40, "bold"),
                    bg='#2d2d2d',
                    fg='#8b0000'
                ).pack(pady=10)
        except Exception as e:
            print(f"⚠️ Erro ao carregar logo: {e}")
            # Fallback para texto
            Label(
                self.frame,
                text="K'PY",
                font=("Arial", 40, "bold"),
                bg='#2d2d2d',
                fg='#8b0000'
            ).pack(pady=10)
    
    def atualizar_status(self, mensagem, porcentagem):
        """Atualiza o status e a barra de progresso"""
        self.label_status.config(text=mensagem)
        self.label_porcentagem.config(text=f"{porcentagem}%")
        
        # Atualizar barra de progresso
        self.progress_bar.config(width=int(300 * (porcentagem / 100)))
        
        self.janela.update()
        time.sleep(0.1)
    
    def fechar(self):
        """Fecha a splash screen"""
        self.janela.destroy()
    
    def manter_aberta(self):
        """Mantém a splash screen aberta até ser fechada"""
        self.janela.mainloop()


# Se executar este arquivo diretamente, testa a splash screen
if __name__ == "__main__":
    splash = SplashScreen()
    splash.atualizar_status("Teste de carregamento...", 50)
    import time
    time.sleep(2)
    splash.fechar()