# src/ui/filtro_relatorio.py
"""
Janela de filtro personalizada para relatórios.
"""
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from src.utils.tooltip import criar_tooltip

class JanelaFiltroRelatorio:
    """Janela para filtrar relatórios por colunas"""
    
    def __init__(self, parent, df, colunas_permitidas, callback_aplicar_filtro, cores):
        """
        Inicializa a janela de filtro.
        
        Args:
            parent: Widget pai
            df: DataFrame com os dados
            colunas_permitidas: Lista de colunas que podem ser filtradas
            callback_aplicar_filtro: Função chamada ao aplicar o filtro
            cores: Dicionário com as cores do tema
        """
        self.parent = parent
        self.df_original = df.copy()  # Guardar original
        self.df = df.copy()  # DataFrame atual (será filtrado dinamicamente)
        self.colunas_permitidas = colunas_permitidas
        self.callback = callback_aplicar_filtro
        self.cores = cores
        
        # Filtrar apenas as colunas que existem no DataFrame
        self.colunas = [col for col in colunas_permitidas if col in df.columns]
        
        # Dicionário para armazenar os filtros ativos
        self.filtros_ativos = {}
        
        self._criar_janela()
    
    def _criar_janela(self):
        """Cria a interface da janela de filtro"""
        self.janela = ctk.CTkToplevel(self.parent)
        self.janela.title("🔍 Filtrar Relatório")
        self.janela.geometry("500x600")
        self.janela.transient(self.parent)
        self.janela.grab_set()
        self.janela.configure(fg_color=self.cores['fundo'])
        
        # === TÍTULO ===
        titulo_frame = ctk.CTkFrame(self.janela, fg_color="transparent", height=40)
        titulo_frame.pack(fill='x', padx=20, pady=(15, 5))
        
        ctk.CTkLabel(
            titulo_frame,
            text="🔍 FILTRAR RELATÓRIO",
            font=("Arial", 18, "bold"),
            text_color=self.cores['texto']
        ).pack(anchor='w')
        
        ctk.CTkLabel(
            titulo_frame,
            text="Clique em uma coluna para selecionar valores",
            font=("Arial", 11, "italic"),
            text_color=self.cores['texto_secundario']
        ).pack(anchor='w', pady=(2, 0))
        
        # === BOTÃO APLICAR FILTRO ===
        btn_aplicar = ctk.CTkButton(
            self.janela,
            text="✅ APLICAR FILTROS",
            command=self._aplicar_todos_filtros,
            fg_color=self.cores['destaque'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            height=40,
            font=("Arial", 13, "bold")
        )
        btn_aplicar.pack(fill='x', padx=20, pady=10)
        criar_tooltip(btn_aplicar, "Aplicar todos os filtros selecionados")
        
        # === LISTA DE COLUNAS COM SCROLL ===
        colunas_container = ctk.CTkFrame(self.janela, fg_color="transparent")
        colunas_container.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Canvas para scroll
        self.canvas = ctk.CTkCanvas(
            colunas_container,
            bg=self.cores['fundo'],
            highlightthickness=0
        )
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(
            colunas_container,
            orientation="vertical",
            command=self.canvas.yview,
            fg_color=self.cores['scrollbar'],
            button_color=self.cores['destaque']
        )
        
        # Frame que vai conter as colunas
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        
        def _configure_scrollable_frame(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.scrollable_frame.bind("<Configure>", _configure_scrollable_frame)
        
        # Criar a janela do canvas
        canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configurar o canvas para redimensionar
        def _configure_canvas(event):
            self.canvas.itemconfig(canvas_window, width=event.width)
        
        self.canvas.bind("<Configure>", _configure_canvas)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind da rodinha
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Criar itens das colunas
        self._atualizar_lista_colunas()
        
        # === BOTÕES INFERIORES ===
        frame_botoes = ctk.CTkFrame(self.janela, fg_color="transparent", height=50)
        frame_botoes.pack(fill='x', padx=20, pady=10)
        
        btn_limpar = ctk.CTkButton(
            frame_botoes,
            text="🗑️ LIMPAR FILTROS",
            command=self._limpar_filtros,
            fg_color=self.cores['botao_limpar'],
            hover_color="#888888",
            text_color=self.cores['texto'],
            height=35,
            width=150
        )
        btn_limpar.pack(side='left', padx=5)
        criar_tooltip(btn_limpar, "Limpar todos os filtros")
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="✖️ CANCELAR",
            command=self.janela.destroy,
            fg_color=self.cores['entrada'],
            hover_color=self.cores['destaque'],
            text_color=self.cores['texto'],
            height=35,
            width=150
        )
        btn_cancelar.pack(side='right', padx=5)
        criar_tooltip(btn_cancelar, "Fechar sem aplicar")
    
    def _atualizar_lista_colunas(self):
        """Atualiza a lista de colunas na interface"""
        # Limpar frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Recriar itens
        for coluna in self.colunas:
            self._criar_item_coluna(self.scrollable_frame, coluna)
    
    def _criar_item_coluna(self, parent, coluna):
        """Cria um item de coluna clicável"""
        frame_coluna = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=40,
            cursor="hand2"
        )
        frame_coluna.pack(fill='x', pady=2, padx=5)
        frame_coluna.pack_propagate(False)
        
        # Nome da coluna
        label_coluna = ctk.CTkLabel(
            frame_coluna,
            text=f"📊 {coluna}",
            font=("Arial", 13, "bold"),
            text_color=self.cores['texto'],
            anchor='w'
        )
        label_coluna.pack(side='left', padx=10)
        
        # Label do filtro ativo
        label_filtro = ctk.CTkLabel(
            frame_coluna,
            text="",
            font=("Arial", 11, "italic"),
            text_color="green"
        )
        label_filtro.pack(side='left', padx=10, fill='x', expand=True)
        
        # Se já tem filtro ativo, mostrar
        if coluna in self.filtros_ativos:
            valores = self.filtros_ativos[coluna]
            if len(valores) == 1:
                label_filtro.configure(text=f"✅ {str(valores[0])[:30]}")
            elif len(valores) > 1:
                label_filtro.configure(text=f"✅ {len(valores)} valores")
        
        # Bind de clique
        frame_coluna.bind("<Button-1>", lambda e, c=coluna, l=label_filtro: self._mostrar_opcoes_filtro(c, l))
        label_coluna.bind("<Button-1>", lambda e, c=coluna, l=label_filtro: self._mostrar_opcoes_filtro(c, l))
    
    def _mostrar_opcoes_filtro(self, coluna, label_filtro):
        """Mostra as opções de filtro para a coluna (respeitando filtros já aplicados)"""
        # Aplicar filtros atuais no DataFrame para mostrar opções dinâmicas
        df_filtrado = self.df_original.copy()
        for c, valores in self.filtros_ativos.items():
            if c != coluna and valores:  # Ignorar a coluna atual
                df_filtrado = df_filtrado[df_filtrado[c].isin(valores)]
        
        # Criar popup
        popup = ctk.CTkToplevel(self.janela)
        popup.title(f"Filtrar por {coluna}")
        popup.geometry("400x500")
        popup.transient(self.janela)
        popup.grab_set()
        popup.configure(fg_color=self.cores['menu'])
        
        # Título
        ctk.CTkLabel(
            popup,
            text=f"🔍 {coluna}",
            font=("Arial", 16, "bold"),
            text_color=self.cores['texto']
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            popup,
            text=f"Total de registros disponíveis: {len(df_filtrado)}",
            font=("Arial", 11),
            text_color=self.cores['texto_secundario']
        ).pack(pady=(0, 10))
        
        # Frame com scroll
        container = ctk.CTkFrame(popup, fg_color="transparent")
        container.pack(fill='both', expand=True, padx=15, pady=5)
        
        canvas = ctk.CTkCanvas(
            container,
            bg=self.cores['menu'],
            highlightthickness=0
        )
        scrollbar = ctk.CTkScrollbar(
            container,
            orientation="vertical",
            command=canvas.yview,
            fg_color=self.cores['scrollbar']
        )
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        
        def _configure_scrollable(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", _configure_scrollable)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind da rodinha
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Checkboxes para os valores
        check_vars = {}
        valores_selecionados = self.filtros_ativos.get(coluna, [])
        
        # Valores únicos do DataFrame filtrado
        try:
            valores_unicos = df_filtrado[coluna].dropna().unique()
            
            # Ordenar
            try:
                valores_unicos = sorted(valores_unicos)
            except:
                valores_unicos = sorted(valores_unicos, key=str)
            
            for valor in valores_unicos:
                if pd.notna(valor):
                    texto_valor = str(valor)
                    var = ctk.BooleanVar(value=texto_valor in valores_selecionados)
                    check_vars[texto_valor] = var
                    
                    check = ctk.CTkCheckBox(
                        scrollable_frame,
                        text=texto_valor[:50] + "..." if len(texto_valor) > 50 else texto_valor,
                        variable=var,
                        fg_color=self.cores['destaque'],
                        text_color=self.cores['texto']
                    )
                    check.pack(anchor='w', pady=2, padx=10)
                    
        except Exception as e:
            print(f"Erro ao carregar valores: {e}")
            ctk.CTkLabel(
                scrollable_frame,
                text="Erro ao carregar valores",
                text_color="red"
            ).pack(pady=10)
        
        # Botões
        frame_botoes = ctk.CTkFrame(popup, fg_color="transparent", height=60)
        frame_botoes.pack(fill='x', padx=15, pady=15)
        
        btn_ok = ctk.CTkButton(
            frame_botoes,
            text="✅ OK",
            command=lambda: self._confirmar_filtro_coluna(coluna, check_vars, popup, label_filtro),
            fg_color=self.cores['destaque'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            height=35,
            width=100
        )
        btn_ok.pack(side='left', padx=5)
        
        btn_limpar = ctk.CTkButton(
            frame_botoes,
            text="🗑️ Limpar",
            command=lambda: self._limpar_filtro_coluna(coluna, popup, label_filtro),
            fg_color=self.cores['botao_limpar'],
            hover_color="#888888",
            text_color=self.cores['texto'],
            height=35,
            width=100
        )
        btn_limpar.pack(side='left', padx=5)
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="✖️ Cancelar",
            command=popup.destroy,
            fg_color=self.cores['entrada'],
            hover_color=self.cores['destaque'],
            text_color=self.cores['texto'],
            height=35,
            width=100
        )
        btn_cancelar.pack(side='right', padx=5)
    
    def _confirmar_filtro_coluna(self, coluna, check_vars, popup, label_filtro):
        """Confirma os valores selecionados para a coluna"""
        valores_selecionados = [
            valor for valor, var in check_vars.items() 
            if var.get()
        ]
        
        if valores_selecionados:
            self.filtros_ativos[coluna] = valores_selecionados
            if len(valores_selecionados) == 1:
                label_filtro.configure(text=f"✅ {valores_selecionados[0][:30]}")
            else:
                label_filtro.configure(text=f"✅ {len(valores_selecionados)} valores")
        else:
            if coluna in self.filtros_ativos:
                del self.filtros_ativos[coluna]
            label_filtro.configure(text="")
        
        popup.destroy()
    
    def _limpar_filtro_coluna(self, coluna, popup, label_filtro):
        """Limpa o filtro da coluna atual"""
        if coluna in self.filtros_ativos:
            del self.filtros_ativos[coluna]
        label_filtro.configure(text="")
        popup.destroy()
    
    def _aplicar_todos_filtros(self):
        """Aplica todos os filtros selecionados"""
        self.callback(self.filtros_ativos)
        self.janela.destroy()
    
    def _limpar_filtros(self):
        """Limpa todos os filtros"""
        self.filtros_ativos = {}
        self.df = self.df_original.copy()  # Restaurar DataFrame original
        self.janela.destroy()
        self._criar_janela()
        messagebox.showinfo("Filtros", "Todos os filtros foram limpos!")