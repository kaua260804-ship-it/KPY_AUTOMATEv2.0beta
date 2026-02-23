# src/ui/widgets.py
"""
Widgets personalizados para a interface.
"""
import tkinter as tk
import customtkinter as ctk

class BlocoResumo:
    """Widget para exibir o resumo dos dados"""
    
    def __init__(self, parent, cores):
        """
        Inicializa o bloco de resumo.
        
        Args:
            parent: Widget pai
            cores: Dicionário com as cores do tema
        """
        self.parent = parent
        self.cores = cores
        self._criar_widget()
    
    def _criar_widget(self):
        """Cria o widget de resumo"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.frame,
            text="📊 RESUMO",
            font=("Arial", 14, "bold"),
            text_color=self.cores['texto']
        )
        self.titulo.pack(anchor='w', pady=(0, 2))  # pady=(0,2) dá um espaçamento pequeno
        
        # Linha separadora (opcional, mas fica bonito)
        separador = ctk.CTkFrame(self.frame, fg_color=self.cores['texto_secundario'], height=1)
        separador.pack(fill='x', pady=(0, 5))
        
        # Frame para o texto com scroll
        self.text_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.text_frame.pack(fill='both', expand=True)
        
        # Textbox para o conteúdo
        self.textbox = ctk.CTkTextbox(
            self.text_frame,
            font=("Consolas", 11),
            text_color=self.cores['texto'],
            fg_color=self.cores['entrada'],
            corner_radius=4,
            border_width=0,
            wrap='word'
        )
        self.textbox.pack(side='left', fill='both', expand=True)
    
    def pack(self, **kwargs):
        """Empacota o frame"""
        self.frame.pack(**kwargs)
    
    def atualizar_cores(self, cores):
        """Atualiza as cores do widget"""
        self.cores = cores
        self.titulo.configure(text_color=self.cores['texto'])
        self.textbox.configure(
            text_color=self.cores['texto'],
            fg_color=self.cores['entrada']
        )
    
    def atualizar_conteudo(self, conteudo):
        """Atualiza o texto do resumo"""
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('1.0', conteudo)
    
    def limpar(self):
        """Limpa o conteúdo do resumo"""
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('1.0', "Nenhum dado processado. Selecione um arquivo e clique em Processar.")


class BlocoPreview:
    """Widget para exibir o preview dos dados"""
    
    def __init__(self, parent, cores):
        """
        Inicializa o bloco de preview.
        
        Args:
            parent: Widget pai
            cores: Dicionário com as cores do tema
        """
        self.parent = parent
        self.cores = cores
        self._criar_widget()
    
    def _criar_widget(self):
        """Cria o widget de preview"""
        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.frame,
            text="📋 PRÉ-VISUALIZAÇÃO (20 primeiras linhas)",
            font=("Arial", 14, "bold"),
            text_color=self.cores['texto']
        )
        self.titulo.pack(anchor='w', pady=(0, 2))  # pady=(0,2) dá um espaçamento pequeno
        
        # Linha separadora
        separador = ctk.CTkFrame(self.frame, fg_color=self.cores['texto_secundario'], height=1)
        separador.pack(fill='x', pady=(0, 5))
        
        # Frame para o texto com scroll
        self.text_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.text_frame.pack(fill='both', expand=True)
        
        # Textbox para o conteúdo
        self.textbox = ctk.CTkTextbox(
            self.text_frame,
            font=("Consolas", 10),
            text_color=self.cores['texto'],
            fg_color=self.cores['entrada'],
            corner_radius=4,
            border_width=0,
            wrap='none'  # Para não quebrar linhas
        )
        self.textbox.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.text_frame,
            orientation='vertical',
            command=self.textbox.yview,
            fg_color=self.cores['scrollbar'],
            button_color=self.cores['destaque']
        )
        self.scrollbar.pack(side='right', fill='y')
        self.textbox.configure(yscrollcommand=self.scrollbar.set)
    
    def pack(self, **kwargs):
        """Empacota o frame"""
        self.frame.pack(**kwargs)
    
    def atualizar_cores(self, cores):
        """Atualiza as cores do widget"""
        self.cores = cores
        self.titulo.configure(text_color=self.cores['texto'])
        self.textbox.configure(
            text_color=self.cores['texto'],
            fg_color=self.cores['entrada']
        )
        self.scrollbar.configure(
            fg_color=self.cores['scrollbar'],
            button_color=self.cores['destaque']
        )
    
    def atualizar_conteudo(self, conteudo):
        """Atualiza o texto do preview"""
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('1.0', conteudo)
    
    def limpar(self):
        """Limpa o conteúdo do preview"""
        self.textbox.delete('1.0', 'end')


class BarraStatus:
    """Widget para barra de status inferior"""
    
    def __init__(self, parent, cores):
        """
        Inicializa a barra de status.
        
        Args:
            parent: Widget pai
            cores: Dicionário com as cores do tema
        """
        self.parent = parent
        self.cores = cores
        self._criar_widget()
    
    def _criar_widget(self):
        """Cria a barra de status"""
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=self.cores['menu'],
            height=25,
            corner_radius=0
        )
        self.frame.pack_propagate(False)
        
        self.label = ctk.CTkLabel(
            self.frame,
            text="Pronto",
            font=("Arial", 11),
            text_color=self.cores['texto_secundario']
        )
        self.label.pack(side='left', padx=10)
    
    def place(self, **kwargs):
        """Posiciona a barra de status"""
        self.frame.place(**kwargs)
    
    def atualizar_cores(self, cores):
        """Atualiza as cores da barra"""
        self.cores = cores
        self.frame.configure(fg_color=self.cores['menu'])
        self.label.configure(text_color=self.cores['texto_secundario'])
    
    def atualizar(self, texto):
        """Atualiza o texto da barra"""
        self.label.configure(text=texto)