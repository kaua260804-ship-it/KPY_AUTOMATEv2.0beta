# src/ui/filtro.py
"""
Módulo para a janela de filtro de lojas.
"""
import tkinter as tk
from src.utils.tooltip import criar_tooltip
from src.utils.config import MACROS

class JanelaFiltro:
    """Janela para filtrar lojas com macros"""
    
    def __init__(self, parent, lojas_disponiveis, callback_aplicar, cores):
        """
        Inicializa a janela de filtro.
        
        Args:
            parent: Widget pai
            lojas_disponiveis: Lista de lojas disponíveis
            callback_aplicar: Função a ser chamada ao aplicar o filtro
            cores: Dicionário com as cores do tema atual
        """
        self.parent = parent
        self.lojas = sorted(lojas_disponiveis)
        self.callback = callback_aplicar
        self.cores = cores
        
        # Variáveis de estado
        self.var_lojas = []
        self.macro_emporio_ativo = False
        self.macro_mercearia_ativo = False
        self.macro_outros_ativo = False
        
        self._criar_janela()
    
    def _criar_janela(self):
        """Cria a interface da janela de filtro"""
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Filtrar Lojas")
        self.janela.geometry("400x600")
        self.janela.configure(bg=self.cores['fundo'])
        
        # Título
        tk.Label(
            self.janela,
            text="Selecione as lojas para filtrar:",
            bg=self.cores['fundo'],
            fg=self.cores['texto'],
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Frame para macros
        self._criar_macros()
        
        # Frame com scroll para as checkboxes
        self._criar_lista_lojas()
        
        # Botões
        self._criar_botoes()
    
    def _criar_macros(self):
        """Cria os botões de macro"""
        frame_macros = tk.Frame(self.janela, bg=self.cores['fundo'])
        frame_macros.pack(fill='x', padx=10, pady=5)
        
        # Botão EMPÓRIO
        self.btn_emporio = tk.Button(
            frame_macros,
            text="🏪 EMPÓRIO",
            command=self._toggle_macro_emporio,
            bg=self.cores['macro_emporio'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            font=("Arial", 9, "bold"),
            width=12
        )
        self.btn_emporio.pack(side=tk.LEFT, padx=2)
        criar_tooltip(self.btn_emporio, "Selecionar lojas do grupo EMPÓRIO")
        
        # Botão MERCEARIA
        self.btn_mercearia = tk.Button(
            frame_macros,
            text="🥩 MERCEARIA",
            command=self._toggle_macro_mercearia,
            bg=self.cores['macro_mercearia'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            font=("Arial", 9, "bold"),
            width=12
        )
        self.btn_mercearia.pack(side=tk.LEFT, padx=2)
        criar_tooltip(self.btn_mercearia, "Selecionar lojas do grupo MERCEARIA")
        
        # Botão OUTROS
        self.btn_outros = tk.Button(
            frame_macros,
            text="🔮 OUTROS",
            command=self._toggle_macro_outros,
            bg=self.cores['macro_outros'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            font=("Arial", 9, "bold"),
            width=12
        )
        self.btn_outros.pack(side=tk.LEFT, padx=2)
        criar_tooltip(self.btn_outros, "Selecionar lojas não categorizadas")
    
    def _criar_lista_lojas(self):
        """Cria a lista com checkboxes para as lojas"""
        frame_check = tk.Frame(self.janela, bg=self.cores['entrada'])
        frame_check.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas com scrollbar
        canvas = tk.Canvas(frame_check, bg=self.cores['entrada'], highlightthickness=0)
        scrollbar = tk.Scrollbar(
            frame_check,
            orient="vertical",
            command=canvas.yview,
            bg=self.cores['scrollbar'],
            troughcolor=self.cores['scrollbar_trough']
        )
        
        scrollable_frame = tk.Frame(canvas, bg=self.cores['entrada'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Lista de checkboxes
        for loja in self.lojas:
            var = tk.BooleanVar(value=True)
            self.var_lojas.append(var)
            
            chk = tk.Checkbutton(
                scrollable_frame,
                text=loja,
                variable=var,
                bg=self.cores['entrada'],
                fg=self.cores['texto'],
                selectcolor=self.cores['menu'],
                activebackground=self.cores['entrada'],
                activeforeground=self.cores['texto']
            )
            chk.pack(anchor='w', padx=10, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _criar_botoes(self):
        """Cria os botões de ação"""
        frame_botoes = tk.Frame(self.janela, bg=self.cores['fundo'])
        frame_botoes.pack(fill='x', padx=10, pady=10)
        
        # Botão Selecionar Todos
        btn_todos = tk.Button(
            frame_botoes,
            text="✅ Selecionar Todos",
            command=self._selecionar_todos,
            bg=self.cores['botao_filtro'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            bd=0
        )
        btn_todos.pack(side=tk.LEFT, padx=5)
        criar_tooltip(btn_todos, "Selecionar todas as lojas")
        
        # Botão Limpar Seleção
        btn_limpar = tk.Button(
            frame_botoes,
            text="🗑️ Limpar Seleção",
            command=self._limpar_selecao,
            bg=self.cores['botao_limpar'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            bd=0
        )
        btn_limpar.pack(side=tk.LEFT, padx=5)
        criar_tooltip(btn_limpar, "Desmarcar todas as lojas")
        
        # Botão OK
        btn_ok = tk.Button(
            frame_botoes,
            text="✅ OK",
            command=self._aplicar,
            bg=self.cores['destaque'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            font=("Arial", 10, "bold"),
            bd=0
        )
        btn_ok.pack(side=tk.RIGHT, padx=5)
        criar_tooltip(btn_ok, "Aplicar filtro selecionado")
    
    def _toggle_macro_emporio(self):
        """Ativa/desativa o macro de EMPÓRIO"""
        self.macro_emporio_ativo = not self.macro_emporio_ativo
        
        for i, loja in enumerate(self.lojas):
            if loja in MACROS['emporio']:
                self.var_lojas[i].set(self.macro_emporio_ativo)
        
        # Atualiza cor do botão
        if self.macro_emporio_ativo:
            self.btn_emporio.config(bg=self.cores['destaque'])
        else:
            self.btn_emporio.config(bg=self.cores['macro_emporio'])
    
    def _toggle_macro_mercearia(self):
        """Ativa/desativa o macro de MERCEARIA"""
        self.macro_mercearia_ativo = not self.macro_mercearia_ativo
        
        for i, loja in enumerate(self.lojas):
            if loja in MACROS['mercearia']:
                self.var_lojas[i].set(self.macro_mercearia_ativo)
        
        # Atualiza cor do botão
        if self.macro_mercearia_ativo:
            self.btn_mercearia.config(bg=self.cores['destaque'])
        else:
            self.btn_mercearia.config(bg=self.cores['macro_mercearia'])
    
    def _toggle_macro_outros(self):
        """Ativa/desativa o macro de OUTROS"""
        self.macro_outros_ativo = not self.macro_outros_ativo
        
        # Outros = todas as lojas fora dos macros
        lojas_macro = set(MACROS['emporio'] + MACROS['mercearia'])
        
        for i, loja in enumerate(self.lojas):
            if loja not in lojas_macro:
                self.var_lojas[i].set(self.macro_outros_ativo)
        
        # Atualiza cor do botão
        if self.macro_outros_ativo:
            self.btn_outros.config(bg=self.cores['destaque'])
        else:
            self.btn_outros.config(bg=self.cores['macro_outros'])
    
    def _selecionar_todos(self):
        """Seleciona todas as lojas"""
        for var in self.var_lojas:
            var.set(True)
        
        # Reseta estados dos macros
        self.macro_emporio_ativo = False
        self.macro_mercearia_ativo = False
        self.macro_outros_ativo = False
        
        self.btn_emporio.config(bg=self.cores['macro_emporio'])
        self.btn_mercearia.config(bg=self.cores['macro_mercearia'])
        self.btn_outros.config(bg=self.cores['macro_outros'])
    
    def _limpar_selecao(self):
        """Desmarca todas as lojas"""
        for var in self.var_lojas:
            var.set(False)
        
        # Reseta estados dos macros
        self.macro_emporio_ativo = False
        self.macro_mercearia_ativo = False
        self.macro_outros_ativo = False
        
        self.btn_emporio.config(bg=self.cores['macro_emporio'])
        self.btn_mercearia.config(bg=self.cores['macro_mercearia'])
        self.btn_outros.config(bg=self.cores['macro_outros'])
    
    def _aplicar(self):
        """Aplica o filtro e fecha a janela"""
        lojas_selecionadas = [
            self.lojas[i] for i in range(len(self.lojas))
            if self.var_lojas[i].get()
        ]
        self.callback(lojas_selecionadas)
        self.janela.destroy()