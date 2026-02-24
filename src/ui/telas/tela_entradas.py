# src/ui/telas/tela_entradas.py
"""
Tela específica para processar Entradas por Grupo.
Versão 2.1.0 - Com barra de progresso
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time
import pandas as pd
import customtkinter as ctk

from src.utils.tooltip import criar_tooltip
from src.ui.widgets import BlocoResumo, BlocoPreview
from src.utils.config import LAYOUT
from src.models.modelo_entradas import ModeloEntradas
from src.utils.logger import info, error, warning, debug
from src.ui.progress_bar import ProgressBar, executar_com_progresso

class TelaEntradas:
    """Tela específica para Entradas por Grupo"""
    
    def __init__(self, parent, cores):
        self.parent = parent
        self.cores = cores
        self.modelo = ModeloEntradas()
        
        self.df_processed = None
        self.file_path = None
        self.tempo_processamento = None
        
        # Atributos que serão criados no mostrar()
        self.frame = None
        self.entry_path = None
        self.status_label = None
        self.resumo = None
        self.preview = None
        self.btn_export = None
        
    def mostrar(self):
        """Exibe a tela"""
        # Se já existe um frame, destruir apenas se for recriar
        if self.frame:
            self.frame.destroy()
        
        # Frame principal que preenche tudo
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=self.cores['fundo'],
            corner_radius=0
        )
        self.frame.pack(fill='both', expand=True)
        
        self._criar_interface()
        
        # Se já tiver dados, mostra eles novamente
        if self.df_processed is not None:
            self._atualizar_resumo_preview()
            self.btn_export.configure(state="normal")
            if self.file_path:
                self.entry_path.delete(0, "end")
                self.entry_path.insert(0, self.file_path)
            self.status_label.configure(text="✅ Dados carregados", text_color="#00ff00")
        
        # Forçar atualização
        self.parent.update()
        self.parent.update_idletasks()
    
    def _criar_interface(self):
        """Cria a interface"""
        
        # Container principal com padding
        container = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # ===== TÍTULO =====
        titulo_frame = ctk.CTkFrame(
            container,
            fg_color="transparent",
            height=50
        )
        titulo_frame.pack(fill='x', pady=(0, 10))
        titulo_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            titulo_frame,
            text="📦 ENTRADAS POR GRUPO",
            font=("Arial", 20, "bold"),
            text_color=self.cores['texto'],
            fg_color="transparent"
        ).pack(anchor='w')
        
        # ===== FRAME DE ENTRADA =====
        self._criar_frame_entrada(container)
        
        # ===== CONTEÚDO =====
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
        
        # ===== RODAPÉ =====
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
        """Cria o frame de entrada"""
        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        frame.pack(fill='x', pady=5)
        
        # Primeira linha
        row1 = ctk.CTkFrame(frame, fg_color="transparent")
        row1.pack(fill='x', pady=2)
        
        ctk.CTkLabel(
            row1,
            text="Arquivo:",
            font=("Arial", 12),
            text_color=self.cores['texto'],
            width=70
        ).pack(side='left', padx=(0, 5))
        
        self.entry_path = ctk.CTkEntry(
            row1,
            fg_color=self.cores['entrada'],
            text_color=self.cores['texto'],
            font=("Arial", 11),
            corner_radius=4,
            border_width=1,
            border_color=self.cores['destaque']
        )
        self.entry_path.pack(side='left', fill='x', expand=True)
        
        # Segunda linha - botões
        row2 = ctk.CTkFrame(frame, fg_color="transparent")
        row2.pack(fill='x', pady=5)
        
        botoes = ctk.CTkFrame(row2, fg_color="transparent")
        botoes.pack(anchor='center')
        
        # Botão Procurar
        btn_browse = ctk.CTkButton(
            botoes,
            text="🔍 Procurar",
            command=self._browse_file,
            fg_color=self.cores['entrada'],
            hover_color=self.cores['destaque'],
            text_color=self.cores['texto'],
            width=100,
            height=32,
            corner_radius=4
        )
        btn_browse.pack(side='left', padx=3)
        criar_tooltip(btn_browse, "Selecionar arquivo Excel")
        
        # Botão Processar
        btn_ok = ctk.CTkButton(
            botoes,
            text="✅ Processar",
            command=self._process_file,
            fg_color=self.cores['destaque'],
            hover_color="#a52a2a",
            text_color=self.cores['texto'],
            width=100,
            height=32,
            corner_radius=4
        )
        btn_ok.pack(side='left', padx=3)
        criar_tooltip(btn_ok, "Processar o arquivo selecionado")
        
        # Botão Limpar
        btn_limpar = ctk.CTkButton(
            botoes,
            text="🗑️ Limpar",
            command=self._limpar_dados,
            fg_color=self.cores['botao_limpar'],
            hover_color="#888888",
            text_color=self.cores['texto'],
            width=100,
            height=32,
            corner_radius=4
        )
        btn_limpar.pack(side='left', padx=3)
        criar_tooltip(btn_limpar, "Limpar todos os dados")
        
        # Label de status
        self.status_label = ctk.CTkLabel(
            frame,
            text="⏳ Aguardando arquivo...",
            font=("Arial", 11),
            text_color=self.cores['texto_secundario']
        )
        self.status_label.pack(pady=5)
        
        return frame
    
    def _browse_file(self):
        """Abre diálogo para selecionar arquivo"""
        p = filedialog.askopenfilename(
            title="Selecione a planilha",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        if p:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, p)
            self.file_path = p
            self.status_label.configure(text="📁 Arquivo selecionado", text_color="#00ff00")
    
    def _process_file(self):
        """Processa o arquivo com barra de progresso"""
        path = self.entry_path.get().strip()
        if not path:
            messagebox.showerror("Erro", "Selecione um arquivo!")
            return
        
        executar_com_progresso(
            self.frame,
            self._process_file_thread,
            "📦 Processando Entradas",
            "Lendo e processando arquivo...",
            path
        )
    
    def _process_file_thread(self, progress, path):
        """Versão em thread do processamento"""
        try:
            progress.atualizar(10, "Verificando arquivo...")
            
            if not os.path.exists(path):
                self.frame.after(0, lambda: messagebox.showerror("Erro", f"Arquivo não encontrado:\n{path}"))
                return
            
            progress.atualizar(20, "Lendo arquivo Excel...")
            
            inicio = time.time()
            
            # Ler o arquivo
            df = pd.read_excel(path)
            progress.atualizar(40, f"Arquivo lido: {len(df)} linhas")
            
            # Processar com o modelo
            progress.atualizar(60, "Processando dados...")
            df_limpo = self.modelo.processar(df)
            
            fim = time.time()
            self.tempo_processamento = fim - inicio
            
            progress.atualizar(80, "Atualizando dados...")
            
            self.df_processed = df_limpo
            self.file_path = path
            
            progress.atualizar(90, "Atualizando interface...")
            
            # Atualizar interface na thread principal
            self.frame.after(0, lambda: self._atualizar_interface_apos_processar())
            
            progress.atualizar(100, "Concluído!")
            
        except Exception as e:
            error(f"❌ Erro no processamento: {e}")
            self.frame.after(0, lambda: messagebox.showerror("Erro", f"Erro ao processar:\n{str(e)}"))
            self.frame.after(0, lambda: self.status_label.configure(text="❌ Erro", text_color="#ff0000"))
            raise
    
    def _atualizar_interface_apos_processar(self):
        """Atualiza a interface após o processamento"""
        self._atualizar_resumo_preview()
        self.btn_export.configure(state="normal")
        self.status_label.configure(text="✅ Processamento concluído!", text_color="#00ff00")
        
        messagebox.showinfo("Sucesso", f"✅ Processado em {self.tempo_processamento:.2f} segundos!\n"
                                      f"📊 Total de linhas: {len(self.df_processed)}")
    
    def _atualizar_resumo_preview(self):
        """Atualiza o resumo e preview com os dados processados"""
        if self.df_processed is None:
            return
        
        if self.resumo and hasattr(self.modelo, 'get_resumo'):
            self.resumo.atualizar_conteudo(self.modelo.get_resumo(self.df_processed))
        
        if self.preview and hasattr(self.modelo, 'get_preview'):
            self.preview.atualizar_conteudo(self.modelo.get_preview(self.df_processed, 20))
    
    def _limpar_dados(self):
        """Limpa os dados"""
        self.df_processed = None
        self.file_path = None
        self.entry_path.delete(0, "end")
        
        if self.resumo:
            self.resumo.limpar()
        if self.preview:
            self.preview.limpar()
        
        self.btn_export.configure(state="disabled")
        self.status_label.configure(text="⏳ Aguardando arquivo...", text_color=self.cores['texto_secundario'])
        
        messagebox.showinfo("Limpo", "Dados limpos com sucesso!")
    
    def _export_file(self):
        """Exporta para Excel"""
        if self.df_processed is None:
            return
        
        from datetime import datetime
        data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome = f"Entradas_Tratadas_{data_hora}.xlsx"
        
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=nome
        )
        if path:
            try:
                self.df_processed.to_excel(path, index=False)
                messagebox.showinfo("Sucesso", f"✅ Arquivo salvo em:\n{path}")
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