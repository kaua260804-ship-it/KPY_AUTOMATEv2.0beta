# src/ui/menu.py
"""
Módulo para o menu lateral do programa.
Versão 2.2.0 - Com ajuste de fonte e temas personalizados (sem modo compacto)
"""
import customtkinter as ctk
import os
from src.utils.tooltip import criar_tooltip
from src.utils.helpers import resource_path
from src.utils.config_manager import config

class MenuLateral:
    """Menu lateral com botões de navegação"""
    
    def __init__(self, parent, cores, callbacks, callback_tema, app=None):
        """
        Inicializa o menu lateral.
        
        Args:
            parent: Widget pai
            cores: Dicionário com as cores do tema atual
            callbacks: Dicionário com as funções para cada relatório
            callback_tema: Função para alternar tema
            app: Referência para a aplicação principal
        """
        self.parent = parent
        self.cores = cores
        self.callbacks = callbacks
        self.callback_tema = callback_tema
        self.app = app
        
        # Configurações de fonte
        self.fonte_atual = config.get('tamanho_fonte', 12)
        self.fonte_familia = "Arial"
        
        self._criar_menu()
        self._configurar_atalhos()
    
    def _criar_menu(self):
        """Cria a interface do menu lateral"""
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=self.cores['menu'],
            width=220,
            corner_radius=0
        )
        self.frame.grid(row=0, column=0, sticky='ns')
        self.frame.grid_propagate(False)
        
        # ===== LOGO =====
        logo_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        logo_frame.pack(pady=(20, 10))
        
        ctk.CTkLabel(
            logo_frame,
            text="K'PY",
            font=(self.fonte_familia, 24, "bold"),
            text_color=self.cores['destaque']
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="📋 MENU",
            font=(self.fonte_familia, 14, "bold"),
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
            font=(self.fonte_familia, self.fonte_atual, "bold"),
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
            font=(self.fonte_familia, self.fonte_atual, "bold"),
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
            font=(self.fonte_familia, self.fonte_atual, "bold"),
            corner_radius=6
        )
        self.btn_criar.pack(pady=5, padx=15, fill='x')
        criar_tooltip(self.btn_criar, "Criar relatórios personalizados com múltiplos arquivos")
        
        # ===== BOTÃO DE TEMA =====
        self.btn_tema = ctk.CTkButton(
            self.frame,
            text="🌓 Tema",
            command=self.callback_tema,
            fg_color=self.cores['entrada'],
            hover_color=self.cores['destaque'],
            text_color=self.cores['texto'],
            height=35,
            font=(self.fonte_familia, self.fonte_atual - 1),
            corner_radius=6
        )
        self.btn_tema.pack(pady=2, padx=15, fill='x')
        criar_tooltip(self.btn_tema, "Alternar entre tema claro e escuro")
        
        # NOVO: Botão Seletor de Temas
        self.btn_seletor_temas = ctk.CTkButton(
            self.frame,
            text="🎨 Temas",
            command=self.abrir_seletor_temas,
            fg_color=self.cores['entrada'],
            hover_color=self.cores['destaque'],
            text_color=self.cores['texto'],
            height=35,
            font=(self.fonte_familia, self.fonte_atual - 1),
            corner_radius=6
        )
        self.btn_seletor_temas.pack(pady=2, padx=15, fill='x')
        criar_tooltip(self.btn_seletor_temas, "Escolher tema personalizado")
        
        # Espaço
        ctk.CTkFrame(self.frame, fg_color="transparent", height=20).pack()
        
        # ===== STATUS DA FONTE =====
        fonte_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        fonte_frame.pack(side='bottom', pady=10)
        
        self.fonte_label = ctk.CTkLabel(
            fonte_frame,
            text=f"🔤 Fonte: {self.fonte_atual}pt (Ctrl+ / Ctrl-)",
            font=(self.fonte_familia, 9),
            text_color=self.cores['texto_secundario']
        )
        self.fonte_label.pack()
        
        # Versão no rodapé
        ctk.CTkLabel(
            fonte_frame,
            text="Versão 2.2.0",
            font=(self.fonte_familia, 9),
            text_color=self.cores['texto_secundario']
        ).pack()
    
    def _configurar_atalhos(self):
        """Configura os atalhos de teclado"""
        self.parent.bind('<Control-plus>', self.aumentar_fonte)
        self.parent.bind('<Control-minus>', self.diminuir_fonte)
        self.parent.bind('<Control-0>', self.resetar_fonte)
        print("✅ Atalhos configurados: Ctrl+ (aumentar fonte), Ctrl- (diminuir), Ctrl+0 (resetar)")
    
    def aumentar_fonte(self, event=None):
        """Aumenta o tamanho da fonte"""
        self.fonte_atual = min(self.fonte_atual + 1, 18)
        config.set('tamanho_fonte', self.fonte_atual)
        self._atualizar_fontes()
        self.fonte_label.configure(text=f"🔤 Fonte: {self.fonte_atual}pt (Ctrl+ / Ctrl-)")
        if self.app and hasattr(self.app, 'atualizar_fonte_global'):
            self.app.atualizar_fonte_global(self.fonte_atual)
        print(f"🔤 Fonte aumentada para {self.fonte_atual}pt")
    
    def diminuir_fonte(self, event=None):
        """Diminui o tamanho da fonte"""
        self.fonte_atual = max(self.fonte_atual - 1, 8)
        config.set('tamanho_fonte', self.fonte_atual)
        self._atualizar_fontes()
        self.fonte_label.configure(text=f"🔤 Fonte: {self.fonte_atual}pt (Ctrl+ / Ctrl-)")
        if self.app and hasattr(self.app, 'atualizar_fonte_global'):
            self.app.atualizar_fonte_global(self.fonte_atual)
        print(f"🔤 Fonte diminuída para {self.fonte_atual}pt")
    
    def resetar_fonte(self, event=None):
        """Reseta o tamanho da fonte para o padrão (12)"""
        self.fonte_atual = 12
        config.set('tamanho_fonte', 12)
        self._atualizar_fontes()
        self.fonte_label.configure(text=f"🔤 Fonte: {self.fonte_atual}pt (Ctrl+ / Ctrl-)")
        if self.app and hasattr(self.app, 'atualizar_fonte_global'):
            self.app.atualizar_fonte_global(12)
        print("🔤 Fonte resetada para 12pt")
    
    def _atualizar_fontes(self):
        """Atualiza o tamanho da fonte em todos os botões do menu"""
        self.btn_curva.configure(font=(self.fonte_familia, self.fonte_atual, "bold"))
        self.btn_entradas.configure(font=(self.fonte_familia, self.fonte_atual, "bold"))
        self.btn_criar.configure(font=(self.fonte_familia, self.fonte_atual, "bold"))
        self.btn_tema.configure(font=(self.fonte_familia, self.fonte_atual - 1))
        self.btn_seletor_temas.configure(font=(self.fonte_familia, self.fonte_atual - 1))
    
    def abrir_seletor_temas(self):
        """Abre a janela de seleção de temas"""
        if self.app and hasattr(self.app, 'abrir_seletor_temas'):
            self.app.abrir_seletor_temas()
    
    def aplicar_tema_personalizado(self, nome_tema, cores_tema):
        """Aplica um tema personalizado (cores diferentes)"""
        if 'destaque' in cores_tema:
            self.cores['destaque'] = cores_tema['destaque']
            self.cores['botao_exportar'] = cores_tema.get('destaque', self.cores['destaque'])
            self.cores['botao_filtro'] = cores_tema.get('secundario', '#4a6da8')
            
            # Atualizar botões com nova cor
            self.btn_curva.configure(fg_color=self.cores['destaque'])
            self.btn_entradas.configure(fg_color=self.cores['destaque'])
            self.btn_criar.configure(fg_color=self.cores['destaque'])
            
            print(f"🎨 Tema personalizado aplicado: {nome_tema}")
    
    def atualizar_cores(self, cores):
        """Atualiza as cores do menu quando o tema muda"""
        self.cores = cores
        self.frame.configure(fg_color=self.cores['menu'])
        
        # Atualizar botões principais
        self.btn_curva.configure(fg_color=self.cores['destaque'], text_color=self.cores['texto'])
        self.btn_entradas.configure(fg_color=self.cores['destaque'], text_color=self.cores['texto'])
        self.btn_criar.configure(fg_color=self.cores['destaque'], text_color=self.cores['texto'])
        
        # Atualizar botões de configuração
        self.btn_tema.configure(fg_color=self.cores['entrada'], text_color=self.cores['texto'])
        self.btn_seletor_temas.configure(fg_color=self.cores['entrada'], text_color=self.cores['texto'])
        
        # Atualizar labels
        self.fonte_label.configure(text_color=self.cores['texto_secundario'])