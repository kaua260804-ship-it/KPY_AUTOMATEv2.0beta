# src/ui/menu.py
"""
Módulo para o menu lateral do programa.
"""
import customtkinter as ctk
import os
from src.utils.tooltip import criar_tooltip
from src.utils.helpers import resource_path

class MenuLateral:
    """Menu lateral com botões de navegação"""
    
    def __init__(self, parent, cores, callbacks, callback_tema):
        """
        Inicializa o menu lateral.
        
        Args:
            parent: Widget pai
            cores: Dicionário com as cores do tema atual
            callbacks: Dicionário com as funções para cada relatório
            callback_tema: Função para alternar tema
        """
        self.parent = parent
        self.cores = cores
        self.callbacks = callbacks
        self.callback_tema = callback_tema
        
        self._criar_menu()
    
    def _criar_menu(self):
        """Cria a interface do menu lateral"""
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=self.cores['menu'],
            width=220,
            corner_radius=0
        )
        self.frame.grid(row=0, column=0, sticky='ns')  # sticky='ns' só expande na vertical
        self.frame.grid_propagate(False)  # Mantém largura fixa
        
        # Logo ou título
        ctk.CTkLabel(
            self.frame,
            text="K'PY",
            font=("Arial", 24, "bold"),
            text_color=self.cores['destaque']
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            self.frame,
            text="📋 MENU",
            font=("Arial", 14, "bold"),
            text_color=self.cores['texto']
        ).pack(pady=(0, 10))
        
        # Linha decorativa
        linha = ctk.CTkFrame(
            self.frame,
            fg_color=self.cores['destaque'],
            height=2
        )
        linha.pack(fill='x', padx=20, pady=5)
        
        # Espaço
        ctk.CTkFrame(self.frame, fg_color="transparent", height=10).pack()
        
        # ===== BOTÕES DOS RELATÓRIOS =====
        
        # Botão Curva ABC
        self.btn_curva = ctk.CTkButton(
            self.frame,
            text="📊 CURVA ABC",
            command=self.callbacks['curva_abc'],
            fg_color=self.cores['destaque'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            height=40,
            font=("Arial", 12, "bold"),
            corner_radius=6
        )
        self.btn_curva.pack(pady=5, padx=15, fill='x')
        criar_tooltip(self.btn_curva, "Processar relatório Curva ABC por Loja")
        
        # Botão Entradas por Grupo
        self.btn_entradas = ctk.CTkButton(
            self.frame,
            text="📦 ENTRADAS GRUPO",
            command=self.callbacks['entradas_grupo'],
            fg_color=self.cores['destaque'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            height=40,
            font=("Arial", 12, "bold"),
            corner_radius=6
        )
        self.btn_entradas.pack(pady=5, padx=15, fill='x')
        criar_tooltip(self.btn_entradas, "Processar relatório Entradas por Grupo")
        
        # Botão Criar Relatório
        self.btn_criar = ctk.CTkButton(
            self.frame,
            text="📋 CRIAR RELATÓRIO",
            command=self.callbacks['criar_relatorio'],
            fg_color=self.cores['destaque'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            height=40,
            font=("Arial", 12, "bold"),
            corner_radius=6
        )
        self.btn_criar.pack(pady=5, padx=15, fill='x')
        criar_tooltip(self.btn_criar, "Criar relatórios personalizados com múltiplos arquivos")
        
        # Espaço
        ctk.CTkFrame(self.frame, fg_color="transparent", height=20).pack()
        
        # ===== BOTÃO DE TEMA =====
        self.btn_tema = ctk.CTkButton(
            self.frame,
            text="🌓 Tema",
            command=self.callback_tema,
            fg_color=self.cores['entrada'],
            hover_color=self.cores['destaque'],
            text_color=self.cores['texto'],
            height=35,
            font=("Arial", 11),
            corner_radius=6
        )
        self.btn_tema.pack(pady=5, padx=15, fill='x')
        criar_tooltip(self.btn_tema, "Alternar entre tema claro e escuro")
        
        # Versão no rodapé
        ctk.CTkLabel(
            self.frame,
            text="Versão 2.0",
            font=("Arial", 9),
            text_color=self.cores['texto_secundario']
        ).pack(side='bottom', pady=10)
    
    def atualizar_cores(self, cores):
        """Atualiza as cores do menu quando o tema muda"""
        self.cores = cores
        self.frame.configure(fg_color=self.cores['menu'])
        
        # Atualizar botões
        self.btn_curva.configure(
            fg_color=self.cores['destaque'],
            text_color=self.cores['texto']
        )
        self.btn_entradas.configure(
            fg_color=self.cores['destaque'],
            text_color=self.cores['texto']
        )
        self.btn_criar.configure(
            fg_color=self.cores['destaque'],
            text_color=self.cores['texto']
        )
        self.btn_tema.configure(
            fg_color=self.cores['entrada'],
            text_color=self.cores['texto']
        )