# src/ui/telas/tela_principal.py
"""
Tela principal do programa com área para arrastar arquivos.
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class TelaPrincipal:
    """Tela inicial com área de drop de arquivos"""
    
    def __init__(self, parent, cores, callback_arquivo_selecionado):
        """
        Inicializa a tela principal.
        
        Args:
            parent: Widget pai
            cores: Dicionário com as cores do tema
            callback_arquivo_selecionado: Função chamada quando um arquivo é selecionado
        """
        self.parent = parent
        self.cores = cores
        self.callback = callback_arquivo_selecionado
        self.frame = None
        self.arquivo_selecionado = None
        
    def mostrar(self):
        """Exibe a tela principal"""
        if self.frame:
            self.frame.destroy()
            
        self.frame = tk.Frame(self.parent, bg=self.cores['fundo'])
        self.frame.pack(fill='both', expand=True)
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        """Cria os widgets da tela principal"""
        
        # Título
        titulo = tk.Label(
            self.frame,
            text="K'PY AUTOMATE",
            bg=self.cores['fundo'],
            fg=self.cores['destaque'],
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=(50, 10))
        
        subtitulo = tk.Label(
            self.frame,
            text="Sistema de Identificação e Tratamento de Planilhas",
            bg=self.cores['fundo'],
            fg=self.cores['texto'],
            font=("Arial", 12)
        )
        subtitulo.pack(pady=(0, 30))
        
        # Área de drop
        self._criar_area_drop()
        
        # Ou
        ou_label = tk.Label(
            self.frame,
            text="ou",
            bg=self.cores['fundo'],
            fg=self.cores['texto_secundario'],
            font=("Arial", 10)
        )
        ou_label.pack(pady=10)
        
        # Botão para selecionar arquivo
        btn_selecionar = tk.Button(
            self.frame,
            text="📁 Selecionar Arquivo",
            command=self._selecionar_arquivo,
            bg=self.cores['botao_filtro'],
            fg=self.cores['texto'],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn_selecionar.pack()
        
        # Status
        self.status_label = tk.Label(
            self.frame,
            text="",
            bg=self.cores['fundo'],
            fg=self.cores['texto_secundario'],
            font=("Arial", 10)
        )
        self.status_label.pack(pady=20)
    
    def _criar_area_drop(self):
        """Cria a área onde o usuário pode arrastar arquivos"""
        
        # Frame da área de drop
        self.drop_frame = tk.Frame(
            self.frame,
            bg=self.cores['entrada'],
            width=500,
            height=200,
            highlightbackground=self.cores['destaque'],
            highlightthickness=2
        )
        self.drop_frame.pack(pady=20)
        self.drop_frame.pack_propagate(False)
        
        # Conteúdo da área de drop
        icon_label = tk.Label(
            self.drop_frame,
            text="📂",
            bg=self.cores['entrada'],
            fg=self.cores['texto'],
            font=("Arial", 48)
        )
        icon_label.pack(pady=(30, 10))
        
        text_label = tk.Label(
            self.drop_frame,
            text="Arraste seu arquivo Excel aqui",
            bg=self.cores['entrada'],
            fg=self.cores['texto'],
            font=("Arial", 12)
        )
        text_label.pack()
        
        # Bind de eventos para drag and drop
        self.drop_frame.bind('<Enter>', self._on_drag_enter)
        self.drop_frame.bind('<Leave>', self._on_drag_leave)
        self.drop_frame.bind('<Button-1>', self._selecionar_arquivo)
        
        # Também bind nos labels para facilitar
        icon_label.bind('<Button-1>', self._selecionar_arquivo)
        text_label.bind('<Button-1>', self._selecionar_arquivo)
    
    def _on_drag_enter(self, event):
        """Quando o mouse entra na área de drop"""
        self.drop_frame.configure(highlightbackground=self.cores['destaque'])
    
    def _on_drag_leave(self, event):
        """Quando o mouse sai da área de drop"""
        self.drop_frame.configure(highlightbackground=self.cores['destaque'])
    
    def _selecionar_arquivo(self, event=None):
        """Abre diálogo para selecionar arquivo"""
        arquivo = filedialog.askopenfilename(
            title="Selecione uma planilha",
            filetypes=[
                ("Arquivos Excel", "*.xlsx *.xls"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivo:
            self.arquivo_selecionado = arquivo
            nome_arquivo = os.path.basename(arquivo)
            self.status_label.config(
                text=f"✅ Arquivo selecionado: {nome_arquivo}",
                fg="#00ff00"
            )
            
            # Chama o callback com o arquivo selecionado
            if self.callback:
                self.callback(arquivo)