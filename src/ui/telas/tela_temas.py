# src/ui/telas/tela_temas.py
"""
Tela de seleção de temas personalizados
Versão ampliada - com tamanho maior e melhor visibilidade
"""
import customtkinter as ctk
from src.utils.config import TEMAS_PERSONALIZADOS, get_tema_personalizado
from src.utils.config_manager import config

class TelaTemas:
    """Tela para escolher temas personalizados"""
    
    def __init__(self, parent, cores, callback_aplicar_tema):
        self.parent = parent
        self.cores = cores
        self.callback = callback_aplicar_tema
        self.tema_atual = config.get('tema_personalizado', 'Vermelho')
        
        self.janela = None
        self._criar_janela()
    
    def _criar_janela(self):
        """Cria a janela de seleção de temas - TAMANHO AMPLIADO"""
        self.janela = ctk.CTkToplevel(self.parent)
        self.janela.title("🎨 Seletor de Temas")
        self.janela.geometry("900x650")  # AUMENTADO: 900x650
        self.janela.transient(self.parent)
        self.janela.grab_set()
        self.janela.focus_set()
        self.janela.configure(fg_color=self.cores['fundo'])
        
        # Centralizar
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (650 // 2)
        self.janela.geometry(f'+{x}+{y}')
        
        # Impedir redimensionamento para manter proporção
        self.janela.resizable(False, False)
        
        # ===== TÍTULO =====
        titulo = ctk.CTkLabel(
            self.janela,
            text="🎨 Escolha um Tema Personalizado",
            font=("Arial", 22, "bold"),
            text_color=self.cores['texto']
        )
        titulo.pack(pady=(25, 5))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self.janela,
            text="Selecione a cor que mais combina com você",
            font=("Arial", 13),
            text_color=self.cores['texto_secundario']
        )
        subtitulo.pack(pady=(0, 20))
        
        # ===== FRAME PRINCIPAL COM SCROLL (caso necessário) =====
        main_frame = ctk.CTkScrollableFrame(
            self.janela,
            fg_color="transparent",
            width=850,
            height=450
        )
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Criar grid 2x4 para os 8 temas
        temas = list(TEMAS_PERSONALIZADOS.items())
        
        for i, (nome_tema, info) in enumerate(temas):
            row = i // 4
            col = i % 4
            
            # Frame para cada tema (card)
            tema_frame = ctk.CTkFrame(
                main_frame,
                fg_color=self.cores['entrada'],
                border_width=3,
                border_color=self.cores['destaque'] if nome_tema == self.tema_atual else self.cores['entrada'],
                corner_radius=12,
                width=180,
                height=200
            )
            tema_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            tema_frame.grid_propagate(False)  # Mantém tamanho fixo
            
            # Preview da cor (grande)
            cor_preview = ctk.CTkFrame(
                tema_frame,
                fg_color=info['destaque'],
                height=100,
                width=140,
                corner_radius=8
            )
            cor_preview.pack(pady=(15, 8), padx=15)
            cor_preview.pack_propagate(False)
            
            # Nome do tema
            ctk.CTkLabel(
                tema_frame,
                text=info['nome'],
                font=("Arial", 14, "bold"),
                text_color=self.cores['texto']
            ).pack()
            
            # Código da cor
            ctk.CTkLabel(
                tema_frame,
                text=info['destaque'].upper(),
                font=("Arial", 11),
                text_color=self.cores['texto_secundario']
            ).pack(pady=(2, 8))
            
            # Botão selecionar (bem visível)
            btn_selecionar = ctk.CTkButton(
                tema_frame,
                text="✓ SELECIONAR",
                command=lambda t=nome_tema: self._selecionar_tema(t),
                fg_color=info['destaque'],
                hover_color=info['secundario'],
                text_color="white",
                height=35,
                width=130,
                font=("Arial", 12, "bold")
            )
            btn_selecionar.pack(pady=(5, 10))
        
        # Configurar grid para expandir proporcionalmente
        for i in range(2):  # 2 linhas
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 colunas
            main_frame.grid_columnconfigure(i, weight=1)
        
        # ===== BOTÃO FECHAR =====
        btn_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        btn_fechar = ctk.CTkButton(
            btn_frame,
            text="✖ Fechar",
            command=self.janela.destroy,
            fg_color=self.cores['botao_limpar'],
            hover_color="#888888",
            text_color="white",
            width=150,
            height=40,
            font=("Arial", 13, "bold")
        )
        btn_fechar.pack()
    
    def _selecionar_tema(self, nome_tema):
        """Seleciona um tema"""
        self.tema_atual = nome_tema
        self.callback(nome_tema)
        self.janela.destroy()