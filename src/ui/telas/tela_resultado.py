# src/ui/telas/tela_resultado.py
"""
Tela de resultado para Curva ABC com CustomTkinter - ESTILO DEBUG
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import time
import pandas as pd

from src.utils.tooltip import criar_tooltip
from src.ui.widgets import BlocoResumo, BlocoPreview
from src.utils.config import LAYOUT

class TelaResultado:
    """Tela com resumo, preview e botões - Estilo Debug"""
    
    def __init__(self, parent, cores, identificador):
        self.parent = parent
        self.cores = cores
        self.identificador = identificador
        
        self.df_processed = None
        self.df_filtrado = None
        self.modelo_atual = None
        self.tempo_processamento = None
        self.file_path = None
        
        self.frame = None
        self.btn_filtro = None
        self.btn_export = None
        self.entry_path = None
        self.status_label = None
        self.resumo = None
        self.preview = None
        
    def mostrar(self):
        """Exibe a tela de resultado"""
        # Se já existe um frame, destruir apenas se for recriar
        if self.frame:
            self.frame.destroy()
            
        # Frame principal IGUAL AO DEBUG
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=self.cores['fundo'],
            corner_radius=0
        )
        self.frame.pack(fill='both', expand=True)
        
        self._criar_interface()
        
        # Se já tiver dados, mostra eles novamente
        if self.df_processed is not None:
            self._atualizar_resumo_preview(self.df_filtrado if self.df_filtrado is not None else self.df_processed)
            self.btn_filtro.configure(state="normal")
            self.btn_export.configure(state="normal")
            if self.file_path:
                self.entry_path.delete(0, "end")
                self.entry_path.insert(0, self.file_path)
            self.status_label.configure(text="✅ Dados carregados", text_color="#00ff00")
        
        # Forçar atualização
        self.parent.update_idletasks()
    
    def _criar_interface(self):
        """Cria a interface IGUAL AO DEBUG"""
        
        # Container principal com padding
        container = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # ===== HEADER =====
        header_frame = ctk.CTkFrame(
            container,
            fg_color="transparent",
            height=50
        )
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Título
        ctk.CTkLabel(
            header_frame,
            text="📊 CURVA ABC POR LOJA",
            font=("Arial", 20, "bold"),
            text_color=self.cores['texto'],
            fg_color="transparent"
        ).pack(anchor='w')
        
        # ===== FRAME DE ENTRADA =====
        self._criar_frame_entrada(container)
        
        # ===== CONTEÚDO PRINCIPAL =====
        content_frame = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        content_frame.pack(fill='both', expand=True, pady=10)
        
        # Resumo
        self.resumo = BlocoResumo(content_frame, self.cores)
        self.resumo.pack(fill='x', pady=(0, 10))
        
        # Preview
        self.preview = BlocoPreview(content_frame, self.cores)
        self.preview.pack(fill='both', expand=True)
        
        # ===== RODAPÉ COM BOTÃO =====
        footer_frame = ctk.CTkFrame(
            container,
            fg_color="transparent",
            height=70
        )
        footer_frame.pack(fill='x', pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        # Botão exportar
        self.btn_export = ctk.CTkButton(
            footer_frame,
            text="💾 EXPORTAR PARA EXCEL",
            command=self._export_file,
            fg_color=self.cores['botao_exportar'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            height=40,
            font=("Arial", 13, "bold"),
            corner_radius=6,
            border_width=0,
            state="disabled"
        )
        self.btn_export.pack(fill='x')
        criar_tooltip(self.btn_export, "Exportar dados para arquivo Excel")
    
    def _criar_frame_entrada(self, parent):
        """Cria o frame com campos de entrada"""
        frame_inputs = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        frame_inputs.pack(fill='x', pady=5)
        
        # Primeira linha: Arquivo e Entry
        row1 = ctk.CTkFrame(
            frame_inputs,
            fg_color="transparent"
        )
        row1.pack(fill='x', pady=2)
        
        # Label Arquivo
        ctk.CTkLabel(
            row1,
            text="Arquivo:",
            font=("Arial", 12),
            text_color=self.cores['texto'],
            fg_color="transparent",
            width=70
        ).pack(side="left", padx=(0, 5))
        
        # Entry
        self.entry_path = ctk.CTkEntry(
            row1,
            fg_color=self.cores['entrada'],
            text_color=self.cores['texto'],
            font=("Arial", 11),
            corner_radius=4,
            border_width=1,
            border_color=self.cores['destaque']
        )
        self.entry_path.pack(side="left", fill='x', expand=True)
        
        # Segunda linha: Botões
        row2 = ctk.CTkFrame(
            frame_inputs,
            fg_color="transparent"
        )
        row2.pack(fill='x', pady=5)
        
        # Frame para centralizar os botões
        botoes_center = ctk.CTkFrame(
            row2,
            fg_color="transparent"
        )
        botoes_center.pack(anchor='center')
        
        # Botão Procurar
        btn_browse = ctk.CTkButton(
            botoes_center,
            text="🔍 Procurar",
            command=self._browse_file,
            fg_color=self.cores['entrada'],
            hover_color=self.cores['destaque'],
            text_color=self.cores['texto'],
            width=100,
            height=32,
            font=("Arial", 11),
            corner_radius=4,
            border_width=0
        )
        btn_browse.pack(side="left", padx=3)
        criar_tooltip(btn_browse, "Selecionar arquivo Excel")
        
        # Botão Processar
        btn_ok = ctk.CTkButton(
            botoes_center,
            text="✅ Processar",
            command=self._process_file,
            fg_color=self.cores['destaque'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            width=100,
            height=32,
            font=("Arial", 11, "bold"),
            corner_radius=4,
            border_width=0
        )
        btn_ok.pack(side="left", padx=3)
        criar_tooltip(btn_ok, "Processar o arquivo selecionado")
        
        # Botão Filtrar
        self.btn_filtro = ctk.CTkButton(
            botoes_center,
            text="🔽 Filtrar",
            command=self._abrir_menu_filtro,
            fg_color=self.cores['botao_filtro'],
            hover_color="#5a7db8",
            text_color=self.cores['texto'],
            width=100,
            height=32,
            font=("Arial", 11),
            corner_radius=4,
            border_width=0,
            state="disabled"
        )
        self.btn_filtro.pack(side="left", padx=3)
        criar_tooltip(self.btn_filtro, "Filtrar lojas por grupo")
        
        # Botão Limpar
        btn_limpar = ctk.CTkButton(
            botoes_center,
            text="🗑️ Limpar",
            command=self._limpar_dados,
            fg_color=self.cores['botao_limpar'],
            hover_color="#888888",
            text_color=self.cores['texto'],
            width=100,
            height=32,
            font=("Arial", 11),
            corner_radius=4,
            border_width=0
        )
        btn_limpar.pack(side="left", padx=3)
        criar_tooltip(btn_limpar, "Limpar todos os dados")
        
        # Label de status
        self.status_label = ctk.CTkLabel(
            frame_inputs,
            text="⏳ Aguardando arquivo...",
            font=("Arial", 11),
            text_color=self.cores['texto_secundario'],
            fg_color="transparent"
        )
        self.status_label.pack(pady=5)
    
    def _browse_file(self):
        """Abre diálogo para selecionar arquivo"""
        p = filedialog.askopenfilename(
            title="Selecione a planilha",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls"), ("Todos", "*.*")]
        )
        if p:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, p)
            self.file_path = p
            self.status_label.configure(text="📁 Arquivo selecionado", text_color="#00ff00")
    
    def _process_file(self):
        """Processa o arquivo selecionado com identificação automática"""
        path = self.entry_path.get().strip()
        if not path:
            messagebox.showerror("Erro", "Selecione um arquivo!")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("Erro", f"Arquivo não encontrado:\n{path}")
            return
        
        try:
            self.status_label.configure(text="⏳ Identificando modelo...", text_color="#ffff00")
            self.parent.update()
            
            inicio = time.time()
            
            # Identificar o modelo automaticamente
            modelo, df = self.identificador.identificar(path)
            
            if modelo is None:
                messagebox.showerror(
                    "Erro",
                    "❌ Não foi possível identificar o modelo da planilha.\n\n"
                    "Verifique se o arquivo está no formato correto."
                )
                self.status_label.configure(text="❌ Modelo não identificado", text_color="#ff0000")
                return
            
            self.status_label.configure(text=f"✅ Modelo identificado: {modelo.nome}", text_color="#00ff00")
            self.parent.update()
            
            # Processar com o modelo identificado
            df_limpo = modelo.processar(df)
            
            fim = time.time()
            self.tempo_processamento = fim - inicio
            
            self.df_processed = df_limpo
            self.df_filtrado = None
            self.modelo_atual = modelo
            self.file_path = path
            
            # Atualizar resumo e preview
            self._atualizar_resumo_preview(df_limpo)
            
            # Habilita botões
            self.btn_filtro.configure(state="normal")
            self.btn_export.configure(state="normal")
            self.status_label.configure(text="✅ Processamento concluído!", text_color="#00ff00")
            
            messagebox.showinfo(
                "Sucesso",
                f"✅ Planilha processada em {self.tempo_processamento:.2f} segundos!\n"
                f"📊 Modelo: {modelo.nome}"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar:\n{str(e)}")
            self.resumo.limpar()
            self.preview.limpar()
            self.btn_export.configure(state="disabled")
            self.btn_filtro.configure(state="disabled")
            self.status_label.configure(text="❌ Erro no processamento", text_color="#ff0000")
    
    def _atualizar_resumo_preview(self, df_mostrar):
        """Atualiza o resumo e preview com os dados fornecidos"""
        
        # Usar o método get_resumo do modelo
        if self.modelo_atual and hasattr(self.modelo_atual, 'get_resumo'):
            resumo_texto = self.modelo_atual.get_resumo(df_mostrar)
            self.resumo.atualizar_conteudo(resumo_texto)
        else:
            self._atualizar_resumo_padrao(df_mostrar)
        
        # Usar o método get_preview do modelo
        if self.modelo_atual and hasattr(self.modelo_atual, 'get_preview'):
            preview_texto = self.modelo_atual.get_preview(df_mostrar, 20)
            self.preview.atualizar_conteudo(preview_texto)
        else:
            self._atualizar_preview_padrao(df_mostrar)
    
    def _atualizar_resumo_padrao(self, df_mostrar):
        """Resumo padrão caso o modelo não tenha o seu próprio"""
        resumo_lines = []
        
        num_produtos = df_mostrar['Código'].nunique() if 'Código' in df_mostrar.columns else 0
        num_lojas = df_mostrar['Loja_Nome'].nunique() if 'Loja_Nome' in df_mostrar.columns else 0
        qtd_total = df_mostrar['Qtd'].sum() if 'Qtd' in df_mostrar.columns else 0
        fat_total = df_mostrar['Total R$'].sum() if 'Total R$' in df_mostrar.columns else 0
        
        resumo_lines.append(f"📦 Total de produtos únicos: {self._formatar_br(num_produtos, 'inteiro')}")
        resumo_lines.append(f"🏪 Total de lojas: {self._formatar_br(num_lojas, 'inteiro')}")
        resumo_lines.append(f"📊 Quantidade total: {self._formatar_br(qtd_total, 'decimal_3')}")
        resumo_lines.append(f"💰 Faturamento total: {self._formatar_br(fat_total, 'moeda')}")
        
        if self.tempo_processamento:
            resumo_lines.append(f"⏱️ Tempo: {self.tempo_processamento:.2f} segundos")
        
        self.resumo.atualizar_conteudo("\n".join(resumo_lines))
    
    def _atualizar_preview_padrao(self, df_mostrar):
        """Preview padrão"""
        preview_lines = []
        preview_lines.append("=" * 120)
        preview_lines.append("PRIMEIRAS 20 LINHAS:")
        preview_lines.append("=" * 120)
        preview_lines.append("")
        
        # Pega as primeiras colunas que existem
        colunas = []
        for col in ['Código', 'Produto', 'Qtd', 'Total R$', 'Loja_Nome']:
            if col in df_mostrar.columns:
                colunas.append(col)
        
        if colunas:
            preview_df = df_mostrar[colunas].head(20).copy()
            preview_lines.append(preview_df.to_string(index=False))
        else:
            preview_lines.append("Nenhuma coluna reconhecida para preview")
        
        self.preview.atualizar_conteudo("\n".join(preview_lines))
    
    def _formatar_br(self, valor, tipo='moeda'):
        """Formata números no padrão brasileiro"""
        if pd.isna(valor) or valor == '':
            return ''
        
        try:
            valor_float = float(valor)
            
            if tipo == 'moeda':
                return f"R$ {valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            elif tipo == 'inteiro':
                return f"{int(valor_float)}"
            elif tipo == 'decimal_3':
                return f"{valor_float:,.3f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            elif tipo == 'decimal_2':
                return f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            else:
                return str(valor_float).replace('.', ',')
        except:
            return str(valor)
    
    def _limpar_dados(self):
        """Limpa todos os dados processados"""
        self.df_processed = None
        self.df_filtrado = None
        self.modelo_atual = None
        self.file_path = None
        self.entry_path.delete(0, "end")
        
        self.resumo.limpar()
        self.preview.limpar()
        
        self.btn_export.configure(state="disabled")
        self.btn_filtro.configure(state="disabled")
        self.status_label.configure(text="⏳ Aguardando arquivo...", text_color=self.cores['texto_secundario'])
        
        messagebox.showinfo("Limpo", "Dados limpos com sucesso!")
    
    def _abrir_menu_filtro(self):
        """Abre a janela de filtro"""
        if self.df_processed is None:
            return
        
        from src.ui.filtro import JanelaFiltro
        
        def callback_filtro(lojas_selecionadas):
            if lojas_selecionadas:
                self.df_filtrado = self.df_processed[
                    self.df_processed['Loja_Nome'].isin(lojas_selecionadas)
                ].copy()
                self._atualizar_resumo_preview(self.df_filtrado)
            else:
                self.df_filtrado = None
                self._atualizar_resumo_preview(self.df_processed)
            
            self.btn_export.configure(state="normal")
        
        lojas_disponiveis = self.df_processed['Loja_Nome'].dropna().unique()
        
        JanelaFiltro(
            self.parent,
            lojas_disponiveis,
            callback_filtro,
            self.cores
        )
    
    def _export_file(self):
        """Exporta os dados para Excel"""
        if self.df_processed is None:
            return
        
        df_exportar = self.df_filtrado if self.df_filtrado is not None else self.df_processed
        
        from datetime import datetime
        data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_padrao = f"Planilha_Tratada_{data_hora}.xlsx"
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            title="Salvar como",
            initialfile=nome_padrao
        )
        
        if save_path:
            try:
                df_exportar.to_excel(save_path, index=False)
                messagebox.showinfo("Sucesso", f"✅ Arquivo salvo em:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")
    
    def atualizar_cores(self, cores):
        """Atualiza as cores quando o tema muda"""
        self.cores = cores
        
        # Atualizar frame principal
        if hasattr(self, 'frame') and self.frame:
            self.frame.configure(fg_color=self.cores['fundo'])
        
        # Atualizar entry
        if hasattr(self, 'entry_path') and self.entry_path:
            self.entry_path.configure(
                fg_color=self.cores['entrada'],
                border_color=self.cores['destaque']
            )
        
        # Atualizar botões
        if hasattr(self, 'btn_filtro') and self.btn_filtro:
            self.btn_filtro.configure(
                fg_color=self.cores['botao_filtro'],
                text_color=self.cores['texto']
            )
        
        if hasattr(self, 'btn_export') and self.btn_export:
            self.btn_export.configure(
                fg_color=self.cores['botao_exportar'],
                text_color=self.cores['texto']
            )
        
        # Atualizar status label
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.configure(text_color=self.cores['texto_secundario'])
        
        # Atualizar widgets compostos
        if hasattr(self, 'resumo') and self.resumo:
            self.resumo.atualizar_cores(cores)
        
        if hasattr(self, 'preview') and self.preview:
            self.preview.atualizar_cores(cores)