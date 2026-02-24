# src/ui/progress_bar.py
"""
Widget de barra de progresso personalizado para operações longas
"""
import customtkinter as ctk
import tkinter as tk
from threading import Thread
import time

class ProgressBar:
    """Barra de progresso flutuante para operações demoradas"""
    
    def __init__(self, parent, titulo="Processando...", mensagem="Aguarde enquanto processamos seus dados"):
        self.parent = parent
        self.titulo = titulo
        self.mensagem = mensagem
        self.progresso = 0
        self.esta_ativo = False
        self.janela = None
        
    def mostrar(self):
        """Exibe a janela de progresso"""
        self.esta_ativo = True
        
        # Criar janela
        self.janela = ctk.CTkToplevel(self.parent)
        self.janela.title(self.titulo)
        self.janela.geometry("400x200")
        self.janela.resizable(False, False)
        self.janela.transient(self.parent)
        self.janela.grab_set()  # Modal
        self.janela.focus_set()
        
        # Centralizar
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (200 // 2)
        self.janela.geometry(f'+{x}+{y}')
        
        # Frame principal
        frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Ícone (opcional)
        try:
            from src.utils.helpers import resource_path
            caminho_icon = resource_path("assets/icons/logo.ico")
            self.janela.iconbitmap(caminho_icon)
        except:
            pass
        
        # Título
        ctk.CTkLabel(
            frame,
            text=self.titulo,
            font=("Arial", 16, "bold"),
            text_color="#8b0000"
        ).pack(pady=(0, 10))
        
        # Mensagem
        self.label_mensagem = ctk.CTkLabel(
            frame,
            text=self.mensagem,
            font=("Arial", 11),
            text_color="#cccccc",
            wraplength=350
        )
        self.label_mensagem.pack(pady=(0, 15))
        
        # Barra de progresso do CustomTkinter
        self.progress_bar = ctk.CTkProgressBar(
            frame,
            width=350,
            height=15,
            corner_radius=5,
            fg_color="#3d3d3d",
            progress_color="#8b0000",
            mode="determinate"
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)  # 0%
        
        # Label de porcentagem
        self.label_porcentagem = ctk.CTkLabel(
            frame,
            text="0%",
            font=("Arial", 12, "bold"),
            text_color="#8b0000"
        )
        self.label_porcentagem.pack(pady=5)
        
        # Botão de cancelar (opcional)
        self.btn_cancelar = ctk.CTkButton(
            frame,
            text="Cancelar",
            command=self.cancelar,
            fg_color="#666666",
            hover_color="#888888",
            text_color="white",
            width=100,
            height=30
        )
        self.btn_cancelar.pack(pady=10)
        
        # Atualizar a janela
        self.janela.update()
        
    def atualizar(self, progresso, mensagem=None):
        """
        Atualiza o progresso da barra
        
        Args:
            progresso: Valor entre 0 e 100
            mensagem: Mensagem opcional para atualizar
        """
        if not self.esta_ativo or self.janela is None:
            return
        
        # Atualizar barra (CustomTkinter usa 0-1)
        self.progress_bar.set(progresso / 100)
        
        # Atualizar porcentagem
        self.label_porcentagem.configure(text=f"{progresso}%")
        
        # Atualizar mensagem se fornecida
        if mensagem:
            self.label_mensagem.configure(text=mensagem)
        
        # Forçar atualização da interface
        self.janela.update()
        
    def cancelar(self):
        """Cancela a operação em andamento"""
        self.esta_ativo = False
        self.fechar()
        
    def fechar(self):
        """Fecha a janela de progresso"""
        self.esta_ativo = False
        if self.janela:
            self.janela.grab_release()
            self.janela.destroy()
            self.janela = None


class ProgressBarContext:
    """Gerenciador de contexto para usar com 'with'"""
    
    def __init__(self, parent, titulo="Processando...", mensagem="Aguarde..."):
        self.progress = ProgressBar(parent, titulo, mensagem)
        
    def __enter__(self):
        self.progress.mostrar()
        return self.progress
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.fechar()


def executar_com_progresso(parent, funcao, titulo="Processando...", mensagem="Aguarde...", *args, **kwargs):
    """
    Executa uma função em thread separada com barra de progresso
    
    Args:
        parent: Widget pai
        funcao: Função a ser executada
        titulo: Título da janela
        mensagem: Mensagem inicial
        *args, **kwargs: Argumentos para a função
    """
    progress = ProgressBar(parent, titulo, mensagem)
    progress.mostrar()
    
    def worker():
        try:
            funcao(progress, *args, **kwargs)
        except Exception as e:
            from src.utils.logger import error
            error(f"Erro na execução com progresso: {e}")
        finally:
            progress.fechar()
    
    thread = Thread(target=worker)
    thread.daemon = True
    thread.start()
    
    return thread