# src/ui/telas/tela_criar_relatorio.py
"""
Tela para criar relatórios personalizados a partir de múltiplos arquivos.
Versão 2.2.0 - Sem drag and drop
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import pandas as pd
from datetime import datetime

from src.utils.tooltip import criar_tooltip
from src.ui.widgets import BlocoResumo, BlocoPreview
from src.core.identificador import IdentificadorModelos
from src.relatorios.relatorios_disponiveis import GerenciadorRelatorios
from src.utils.helpers import resource_path
from src.utils.logger import info, error, warning, debug
from src.ui.progress_bar import ProgressBar, executar_com_progresso
from src.utils.config_manager import config

class TelaCriarRelatorio:
    """Tela para criar relatórios personalizados"""
    
    def __init__(self, parent, cores):
        self.parent = parent
        self.cores = cores
        self.identificador = IdentificadorModelos()
        
        # Configurações
        self.fonte_atual = config.get('tamanho_fonte', 12)
        
        info("\n" + "="*60)
        info("🔍 MODELOS DISPONÍVEIS NA TELA:")
        for m in self.identificador.modelos:
            info(f"  - {m.nome}")
        info("="*60 + "\n")
        
        self.gerenciador_relatorios = GerenciadorRelatorios()
        
        # Listas para armazenar os 4 arquivos
        self.arquivos = [None] * 4
        self.dfs_processados = [None] * 4
        self.modelos = [None] * 4
        self.tipos_identificados = [None] * 4
        self.arquivos_definidos = [False] * 4
        
        # DataFrames para os relatórios
        self.df_curva = None
        self.df_estoque = None
        self.df_media = None
        self.df_ruptura = None
        self.df_combinado = None
        self.df_filtrado = None
        
        # Relatório selecionado
        self.relatorio_selecionado = None
        self.relatorios_disponiveis = []
        
        # Atributos da interface
        self.frame = None
        self.entries = []
        self.botoes_procurar = []
        self.botoes_definir = []
        self.btn_carregar = None
        self.btn_exportar = None
        self.btn_limpar = None
        self.btn_relatorio = None
        self.btn_processar = None
        self.btn_filtrar = None
        self.resumo = None
        self.preview = None
        self.status_label = None
        self.relatorio_label = None
        self.status_arquivos = []
        self.container = None
        
    def mostrar(self):
        """Exibe a tela de criar relatório"""
        if self.frame:
            self.frame.destroy()
        
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=self.cores['fundo'],
            corner_radius=0
        )
        self.frame.pack(fill='both', expand=True)
        
        self._criar_interface()
        self.parent.update_idletasks()
    
    def _criar_interface(self):
        """Cria a interface completa"""
        self.container = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # ===== TÍTULO =====
        titulo_frame = ctk.CTkFrame(self.container, fg_color="transparent", height=50)
        titulo_frame.pack(fill='x', pady=(0, 10))
        titulo_frame.pack_propagate(False)
        
        self.titulo_label = ctk.CTkLabel(
            titulo_frame,
            text="📋 CRIAR RELATÓRIO PERSONALIZADO",
            font=("Arial", 20, "bold"),
            text_color=self.cores['texto']
        )
        self.titulo_label.pack(anchor='w')
        
        # ===== ÁREA DE ARQUIVOS =====
        arquivos_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        arquivos_frame.pack(fill='x', pady=5)
        
        # Cabeçalho
        cabecalho = ctk.CTkFrame(arquivos_frame, fg_color="transparent", height=25)
        cabecalho.pack(fill='x', pady=(0, 5))
        cabecalho.pack_propagate(False)
        
        ctk.CTkLabel(
            cabecalho,
            text="Arquivo",
            font=("Arial", 12, "bold"),
            text_color=self.cores['texto'],
            width=500
        ).pack(side='left', padx=(0, 10))
        
        ctk.CTkLabel(
            cabecalho,
            text="Status",
            font=("Arial", 12, "bold"),
            text_color=self.cores['texto'],
            width=150
        ).pack(side='left', padx=(0, 10))
        
        ctk.CTkLabel(
            cabecalho,
            text="Ação",
            font=("Arial", 12, "bold"),
            text_color=self.cores['texto'],
            width=500
        ).pack(side='left')
        
        # Lista de botões de controle por linha
        botoes_por_linha = [
            ("📂 CARREGAR", "btn_carregar", self.cores['destaque']),
            ("📊 RELATÓRIO", "btn_relatorio", "#4a6da8"),
            ("⚙️ PROCESSAR", "btn_processar", self.cores['destaque']),
            ("🔽 FILTRAR", "btn_filtrar", self.cores['botao_filtro']),
            ("💾 EXPORTAR", "btn_exportar", self.cores['botao_exportar']),
            ("🗑️ LIMPAR", "btn_limpar", self.cores['botao_limpar'])
        ]
        
        # 4 linhas de arquivo
        for i in range(4):
            linha = ctk.CTkFrame(arquivos_frame, fg_color="transparent", height=32)
            linha.pack(fill='x', pady=1)
            linha.pack_propagate(False)
            
            # Entry do arquivo
            entry = ctk.CTkEntry(
                linha, fg_color=self.cores['entrada'], text_color=self.cores['texto'],
                font=("Arial", 11), corner_radius=4, border_width=1,
                border_color=self.cores['destaque'], width=500, height=28
            )
            entry.pack(side='left', padx=(0, 10))
            self.entries.append(entry)
            
            # Status
            status_label = ctk.CTkLabel(
                linha, text="⭕", font=("Arial", 12),
                text_color=self.cores['texto_secundario'], width=150, height=28
            )
            status_label.pack(side='left', padx=(0, 10))
            self.status_arquivos.append(status_label)
            
            # Frame para botões da linha
            frame_botoes = ctk.CTkFrame(linha, fg_color="transparent")
            frame_botoes.pack(side='left')
            
            # Botão Procurar
            btn_procurar = ctk.CTkButton(
                frame_botoes, text="📁 Procurar", command=lambda i=i: self._procurar_arquivo(i),
                fg_color=self.cores['entrada'], hover_color=self.cores['destaque'],
                text_color=self.cores['texto'], width=80, height=28, corner_radius=4
            )
            btn_procurar.pack(side='left', padx=2)
            criar_tooltip(btn_procurar, f"Selecionar arquivo {i+1}")
            self.botoes_procurar.append(btn_procurar)
            
            # Botão Definir
            btn_definir = ctk.CTkButton(
                frame_botoes, text="✅ Definir", command=lambda i=i: self._toggle_definir_arquivo(i),
                fg_color=self.cores['botao_filtro'], hover_color="#5a7db8",
                text_color=self.cores['texto'], width=70, height=28,
                corner_radius=4, state="disabled"
            )
            btn_definir.pack(side='left', padx=2)
            criar_tooltip(btn_definir, "Definir/Redefinir arquivo")
            self.botoes_definir.append(btn_definir)
            
            # Separador
            ctk.CTkLabel(frame_botoes, text="|", text_color=self.cores['texto_secundario']).pack(side='left', padx=5)
            
            # Adicionar botões de controle nas primeiras 3 linhas (2 botões por linha)
            if i < 3:
                btn1_text, btn1_attr, btn1_cor = botoes_por_linha[i*2]
                btn2_text, btn2_attr, btn2_cor = botoes_por_linha[i*2 + 1]
                
                # Primeiro botão da linha
                btn1 = ctk.CTkButton(
                    frame_botoes, text=btn1_text, 
                    command=lambda attr=btn1_attr: self._executar_comando(attr),
                    fg_color=btn1_cor,
                    hover_color="#a52a2a" if "CARREGAR" in btn1_text or "PROCESSAR" in btn1_text else
                              "#5a7db8" if "RELATÓRIO" in btn1_text or "FILTRAR" in btn1_text else
                              "#8b0000" if "EXPORTAR" in btn1_text else "#888888",
                    text_color=self.cores['texto'], width=90, height=28,
                    corner_radius=4, state="disabled", font=("Arial", 10, "bold")
                )
                btn1.pack(side='left', padx=2)
                criar_tooltip(btn1, btn1_text)
                setattr(self, btn1_attr, btn1)
                
                # Segundo botão da linha
                btn2 = ctk.CTkButton(
                    frame_botoes, text=btn2_text,
                    command=lambda attr=btn2_attr: self._executar_comando(attr),
                    fg_color=btn2_cor,
                    hover_color="#a52a2a" if "CARREGAR" in btn2_text or "PROCESSAR" in btn2_text else
                              "#5a7db8" if "RELATÓRIO" in btn2_text or "FILTRAR" in btn2_text else
                              "#8b0000" if "EXPORTAR" in btn2_text else "#888888",
                    text_color=self.cores['texto'], width=90, height=28,
                    corner_radius=4, state="disabled", font=("Arial", 10, "bold")
                )
                btn2.pack(side='left', padx=2)
                criar_tooltip(btn2, btn2_text)
                setattr(self, btn2_attr, btn2)
        
        # ===== STATUS =====
        self.status_label = ctk.CTkLabel(
            self.container,
            text="⏳ Aguardando arquivos...",
            font=("Arial", 11),
            text_color=self.cores['texto_secundario']
        )
        self.status_label.pack(pady=5)
        
        self.relatorio_label = ctk.CTkLabel(
            self.container,
            text="Nenhum relatório selecionado",
            font=("Arial", 11, "italic"),
            text_color=self.cores['texto_secundario']
        )
        self.relatorio_label.pack(pady=2)
        
        # ===== CONTEÚDO (RESUMO + PREVIEW) =====
        self.content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content_frame.pack(fill='both', expand=True, pady=10)
        
        self.resumo = BlocoResumo(self.content_frame, self.cores)
        self.resumo.pack(fill='x', pady=(0, 10))
        
        self.preview = BlocoPreview(self.content_frame, self.cores)
        self.preview.pack(fill='both', expand=True)
    
    def atualizar_fonte(self, tamanho):
        """Atualiza o tamanho da fonte em todos os elementos"""
        self.fonte_atual = tamanho
        
        # Atualizar título
        if hasattr(self, 'titulo_label'):
            self.titulo_label.configure(font=("Arial", min(20, tamanho + 8), "bold"))
        
        # Atualizar entries
        for entry in self.entries:
            entry.configure(font=("Arial", tamanho - 1))
        
        # Atualizar status labels
        self.status_label.configure(font=("Arial", tamanho - 1))
        self.relatorio_label.configure(font=("Arial", tamanho - 1, "italic"))
        
        # Atualizar widgets compostos
        if hasattr(self, 'resumo'):
            self.resumo.atualizar_fonte(tamanho)
        if hasattr(self, 'preview'):
            self.preview.atualizar_fonte(tamanho)
    
    def _executar_comando(self, attr_name):
        """Executa o comando baseado no nome do atributo"""
        if attr_name == "btn_carregar":
            self._carregar_arquivos()
        elif attr_name == "btn_relatorio":
            self._escolher_relatorio()
        elif attr_name == "btn_processar":
            self._processar_relatorio()
        elif attr_name == "btn_filtrar":
            self._abrir_filtro()
        elif attr_name == "btn_exportar":
            self._exportar_excel()
        elif attr_name == "btn_limpar":
            self._limpar_tudo()
    
    def _procurar_arquivo(self, indice):
        """Abre diálogo para selecionar arquivo"""
        path = filedialog.askopenfilename(
            title=f"Selecione o arquivo {indice+1}",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls"), ("Todos", "*.*")]
        )
        
        if path:
            self.arquivos[indice] = path
            self.entries[indice].delete(0, "end")
            self.entries[indice].insert(0, path)
            
            self.arquivos_definidos[indice] = False
            self.botoes_definir[indice].configure(state="normal", text="✅ Definir", fg_color=self.cores['botao_filtro'])
            self.entries[indice].configure(border_color=self.cores['destaque'])
            
            self._identificar_arquivo(indice)
    
    def _identificar_arquivo(self, indice):
        """Identifica automaticamente o tipo do arquivo"""
        try:
            info(f"\n🔍 IDENTIFICANDO ARQUIVO {indice+1}: {self.arquivos[indice]}")
            
            modelo, df = self.identificador.identificar(self.arquivos[indice])
            
            if modelo is not None:
                self.tipos_identificados[indice] = modelo.nome
                self.status_arquivos[indice].configure(
                    text=f"🔍 {modelo.nome}", text_color="yellow"
                )
                info(f"✅ Status atualizado para: {modelo.nome}")
            else:
                self.tipos_identificados[indice] = "Não identificado"
                self.status_arquivos[indice].configure(
                    text="❓ Não identificado", text_color="orange"
                )
                warning("❌ Não identificado")
                
        except Exception as e:
            self.tipos_identificados[indice] = "Erro"
            self.status_arquivos[indice].configure(text="❌ Erro", text_color="red")
            error(f"❌ ERRO: {e}")
    
    def _toggle_definir_arquivo(self, indice):
        """Alterna entre definir e redefinir o arquivo"""
        if not self.arquivos_definidos[indice]:
            self.arquivos_definidos[indice] = True
            self.entries[indice].configure(border_color="green")
            
            tipo = self.tipos_identificados[indice] if self.tipos_identificados[indice] is not None else "Definido"
            self.status_arquivos[indice].configure(text=f"✅ {tipo}", text_color="green")
            self.botoes_definir[indice].configure(text="🔄 Redefinir", fg_color="#ffa500")
            
            # Adicionar aos recentes
            if self.arquivos[indice]:
                from src.utils.config_manager import config
                config.adicionar_arquivo_recente(self.arquivos[indice])
        else:
            self.arquivos_definidos[indice] = False
            self.entries[indice].configure(border_color=self.cores['destaque'])
            
            if self.tipos_identificados[indice] is not None:
                self.status_arquivos[indice].configure(text=f"🔍 {self.tipos_identificados[indice]}", text_color="yellow")
            else:
                self.status_arquivos[indice].configure(text="⭕", text_color=self.cores['texto_secundario'])
            
            self.botoes_definir[indice].configure(text="✅ Definir", fg_color=self.cores['botao_filtro'])
        
        self._verificar_pode_carregar()
    
    def _verificar_pode_carregar(self):
        """Verifica se há pelo menos um arquivo definido"""
        for i in range(4):
            if self.arquivos_definidos[i]:
                self.btn_carregar.configure(state="normal")
                return
        self.btn_carregar.configure(state="disabled")
    
    def _carregar_arquivos(self):
        """Carrega todos os arquivos definidos com barra de progresso"""
        arquivos_validos = []
        for i in range(4):
            if self.arquivos_definidos[i] and self.arquivos[i] is not None:
                arquivos_validos.append(i)
        
        if not arquivos_validos:
            messagebox.showwarning("Aviso", "Nenhum arquivo definido!")
            return
        
        # Usar a função auxiliar com barra de progresso
        executar_com_progresso(
            self.frame,
            self._carregar_arquivos_thread,
            "📂 Carregando Arquivos",
            "Preparando para carregar os arquivos...",
            arquivos_validos
        )
    
    def _carregar_arquivos_thread(self, progress, arquivos_validos):
        """Versão em thread do carregamento de arquivos"""
        try:
            progress.atualizar(10, "Lendo arquivos...")
            
            mensagens = []
            total_arquivos = len(arquivos_validos)
            
            # Resetar DataFrames
            self.df_curva = None
            self.df_estoque = None
            self.df_filtrado = None
            self.relatorio_selecionado = None
            
            for idx, i in enumerate(arquivos_validos):
                progresso_parcial = 10 + (idx * 80 // total_arquivos)
                progress.atualizar(progresso_parcial, f"Processando arquivo {i+1} de {total_arquivos}...")
                
                info(f"\n📄 Carregando arquivo {i+1}: {self.arquivos[i]}")
                
                modelo, df = self.identificador.identificar(self.arquivos[i])
                
                if modelo is None:
                    mensagens.append(f"❌ Arquivo {i+1}: Tipo não identificado")
                    continue
                
                info(f"   Modelo: {modelo.nome}")
                
                # Processar o DataFrame com o modelo
                df_limpo = modelo.processar(df)
                df_limpo = df_limpo.reset_index(drop=True)
                
                self.dfs_processados[i] = df_limpo
                self.modelos[i] = modelo
                
                # Separar por tipo
                if "Curva ABC" in modelo.nome:
                    self.df_curva = df_limpo
                    info("   ✅ Curva ABC armazenada")
                elif "Estoque" in modelo.nome:
                    self.df_estoque = df_limpo
                    info("   ✅ Estoque armazenado")
                
                mensagens.append(f"✅ Arquivo {i+1}: {modelo.nome} - {len(df_limpo)} linhas")
            
            progress.atualizar(90, "Carregando média de vendas...")
            
            # Carregar média de vendas
            caminho_media = resource_path("data/media_vendas.xlsx")
            if os.path.exists(caminho_media):
                self.df_media = pd.read_excel(caminho_media)
                info(f"📈 Média de vendas carregada: {len(self.df_media)} linhas")
            else:
                self.df_media = None
                warning("⚠️ Arquivo de média de vendas não encontrado")
            
            progress.atualizar(95, "Atualizando interface...")
            
            # Atualizar interface (isso precisa ser feito na thread principal)
            self.frame.after(0, lambda: self._atualizar_interface_apos_carregar(mensagens))
            
            progress.atualizar(100, "Concluído!")
            
        except Exception as e:
            error(f"❌ Erro no carregamento: {e}")
            self.frame.after(0, lambda: messagebox.showerror("Erro", f"Erro ao carregar: {e}"))
            raise
    
    def _atualizar_interface_apos_carregar(self, mensagens):
        """Atualiza a interface após o carregamento (na thread principal)"""
        resumo_text = "\n".join(mensagens)
        resumo_text += f"\n\n📊 Dados carregados:"
        if self.df_curva is not None:
            resumo_text += f"\n   • Curva ABC: {len(self.df_curva)} linhas"
        if self.df_estoque is not None:
            resumo_text += f"\n   • Estoque: {len(self.df_estoque)} linhas"
        if self.df_media is not None:
            resumo_text += f"\n   • Média de vendas: {len(self.df_media)} linhas"
        
        self.resumo.atualizar_conteudo(resumo_text)
        
        # Preview dos dados básicos
        preview_text = self._gerar_preview_dados()
        self.preview.atualizar_conteudo(preview_text)
        
        # Habilitar botão de relatório
        self.btn_relatorio.configure(state="normal")
        self.status_label.configure(text="✅ Dados carregados! Escolha um relatório.", text_color="#00ff00")
        
        messagebox.showinfo("Sucesso", f"{len(mensagens)} arquivo(s) carregado(s)!")
    
    def _gerar_preview_dados(self):
        """Gera preview dos dados carregados"""
        linhas = []
        linhas.append("=" * 100)
        linhas.append("📋 DADOS CARREGADOS - ESCOLHA UM RELATÓRIO")
        linhas.append("=" * 100)
        linhas.append("")
        
        if self.df_curva is not None:
            linhas.append(f"📊 CURVA ABC: {len(self.df_curva)} linhas")
            linhas.append(self.df_curva[['Código', 'Produto', 'Qtd', 'Loja_Nome']].head(3).to_string())
            linhas.append("")
        
        if self.df_estoque is not None:
            linhas.append(f"📦 ESTOQUE: {len(self.df_estoque)} linhas")
            linhas.append(self.df_estoque[['Codigo', 'Descricao', 'Estoque_Loja', 'Loja']].head(3).to_string())
            linhas.append("")
        
        return "\n".join(linhas)
    
    def _escolher_relatorio(self):
        """Abre menu para escolher relatório"""
        if self.df_curva is None and self.df_estoque is None:
            messagebox.showwarning("Aviso", "Carregue os arquivos primeiro!")
            return
        
        tipos = []
        if self.df_curva is not None:
            tipos.append("Curva ABC por Loja")
        if self.df_estoque is not None:
            tipos.append("Estoque")
        
        self.relatorios_disponiveis = self.gerenciador_relatorios.get_relatorios_disponiveis(tipos)
        
        popup = ctk.CTkToplevel(self.frame)
        popup.title("Escolher Relatório")
        popup.geometry("400x400")
        popup.transient(self.frame)
        popup.grab_set()
        popup.configure(fg_color=self.cores['fundo'])
        
        ctk.CTkLabel(
            popup, text="📊 RELATÓRIOS DISPONÍVEIS",
            font=("Arial", 16, "bold"), text_color=self.cores['texto']
        ).pack(pady=20)
        
        for relatorio in self.relatorios_disponiveis:
            btn = ctk.CTkButton(
                popup, text=relatorio.nome,
                command=lambda r=relatorio, p=popup: self._selecionar_relatorio(r, p),
                fg_color=self.cores['entrada'], hover_color=self.cores['destaque'],
                text_color=self.cores['texto'], height=40, width=300, corner_radius=6
            )
            btn.pack(pady=5)
    
    def _selecionar_relatorio(self, relatorio, popup):
        """Seleciona o relatório e habilita o botão Processar"""
        popup.destroy()
        self.relatorio_selecionado = relatorio
        self.relatorio_label.configure(text=f"📋 Relatório selecionado: {relatorio.nome}", text_color="green")
        self.btn_processar.configure(state="normal", fg_color=self.cores['destaque'], hover_color="#a52a2a")
        self.status_label.configure(text=f"✅ Relatório '{relatorio.nome}' selecionado. Clique em Processar.", text_color="#00ff00")
    
    def _processar_relatorio(self):
        """Processa o relatório selecionado com barra de progresso"""
        if self.relatorio_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um relatório primeiro!")
            return
        
        executar_com_progresso(
            self.frame,
            self._processar_relatorio_thread,
            f"📊 Gerando {self.relatorio_selecionado.nome}",
            "Preparando dados..."
        )
    
    def _processar_relatorio_thread(self, progress):
        """Versão em thread do processamento de relatório"""
        try:
            progress.atualizar(10, "Inicializando...")
            
            self.df_filtrado = None
            
            if "Ruptura" in self.relatorio_selecionado.nome:
                progress.atualizar(20, "Verificando dados necessários...")
                
                if self.df_curva is None or self.df_estoque is None:
                    self.frame.after(0, lambda: messagebox.showerror(
                        "Erro", "Precisa de Curva ABC e Estoque para gerar ruptura!"
                    ))
                    return
                
                progress.atualizar(30, "Carregando modelo de ruptura...")
                from src.models.modelo_ruptura import ModeloRuptura
                modelo_ruptura = ModeloRuptura()
                
                progress.atualizar(40, "Processando dados de estoque e vendas...")
                self.df_ruptura = modelo_ruptura.processar(
                    self.df_estoque,
                    self.df_curva,
                    self.df_media
                )
                
                progress.atualizar(80, "Gerando preview...")
                if self.df_ruptura is None:
                    raise ValueError("Falha ao gerar relatório de ruptura - retornou None")
                
                if hasattr(modelo_ruptura, 'get_preview'):
                    preview = modelo_ruptura.get_preview(self.df_ruptura, 20)
                else:
                    preview = self._gerar_preview_padrao(self.df_ruptura)
                
                self.df_combinado = self.df_ruptura
                
            else:
                progress.atualizar(30, "Combinando dados...")
                dfs_temp = []
                if self.df_curva is not None:
                    dfs_temp.append(self.df_curva)
                if self.df_estoque is not None:
                    dfs_temp.append(self.df_estoque)
                
                if dfs_temp:
                    self.df_combinado = pd.concat(dfs_temp, ignore_index=True)
                else:
                    self.df_combinado = pd.DataFrame()
                
                progress.atualizar(70, "Gerando relatório...")
                preview = self.relatorio_selecionado.gerar(self.df_combinado)
            
            progress.atualizar(90, "Atualizando interface...")
            
            # Atualizar interface na thread principal
            self.frame.after(0, lambda: self._atualizar_interface_apos_processar(preview))
            
            progress.atualizar(100, "Concluído!")
            
        except Exception as e:
            error(f"❌ Erro ao gerar relatório: {e}")
            self.frame.after(0, lambda: messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}"))
            self.frame.after(0, lambda: self.status_label.configure(text="❌ Erro ao gerar relatório", text_color="#ff0000"))
            raise
    
    def _atualizar_interface_apos_processar(self, preview):
        """Atualiza a interface após o processamento"""
        self.preview.atualizar_conteudo(preview)
        self.btn_exportar.configure(state="normal")
        self.btn_filtrar.configure(state="normal")
        self.status_label.configure(
            text=f"✅ {self.relatorio_selecionado.nome} gerado! Use o filtro se desejar.",
            text_color="#00ff00"
        )
    
    def _gerar_preview_padrao(self, df):
        """Gera preview padrão caso o modelo não tenha método próprio"""
        if df is None or len(df) == 0:
            return "Nenhum dado para preview"
        
        linhas = []
        linhas.append("=" * 100)
        linhas.append("📋 PRIMEIRAS 20 LINHAS")
        linhas.append("=" * 100)
        linhas.append("")
        
        preview_df = df.head(20).copy()
        linhas.append(preview_df.to_string(index=False))
        
        return "\n".join(linhas)
    
    def _abrir_filtro(self):
        """Abre a janela de filtro para o relatório atual"""
        if self.df_ruptura is None and self.df_combinado is None:
            messagebox.showwarning("Aviso", "Processe um relatório primeiro!")
            return
        
        df_atual = self.df_ruptura if self.df_ruptura is not None else self.df_combinado
        
        if df_atual is None or len(df_atual) == 0:
            messagebox.showwarning("Aviso", "Nenhum dado para filtrar!")
            return
        
        from src.ui.filtro_relatorio import JanelaFiltroRelatorio
        
        def callback_filtro(filtros):
            df_filtrado = df_atual.copy()
            
            for coluna, valores in filtros.items():
                if coluna in df_filtrado.columns and valores:
                    df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]
            
            df_filtrado = df_filtrado.reset_index(drop=True)
            
            if len(df_filtrado) > 0:
                self.df_filtrado = df_filtrado
                preview_text = self._gerar_preview_filtrado(df_filtrado)
                self.preview.atualizar_conteudo(preview_text)
                
                self.status_label.configure(
                    text=f"✅ Filtro aplicado: {len(df_filtrado)} de {len(df_atual)} linhas",
                    text_color="#00ff00"
                )
                
                messagebox.showinfo("Filtro", f"Filtro aplicado! {len(df_filtrado)} linhas restantes.")
            else:
                messagebox.showwarning("Filtro", "Nenhuma linha encontrada com esses filtros!")
        
        colunas_permitidas = [
            'CATEGORIA',
            'GRUPO',
            'Subgrupo',
            'COMPRADOR',
            'STATUS DO ESTOQUE',
            'RUPTURA',
            'LOJA'
        ]
        
        colunas_existentes = [col for col in colunas_permitidas if col in df_atual.columns]
        
        if not colunas_existentes:
            messagebox.showwarning("Aviso", "Nenhuma coluna disponível para filtro!")
            return
        
        JanelaFiltroRelatorio(
            self.frame,
            df_atual,
            colunas_existentes,
            callback_filtro,
            self.cores
        )
    
    def _gerar_preview_filtrado(self, df):
        """Gera preview dos dados filtrados"""
        if df is None or len(df) == 0:
            return "Nenhum dado para preview"
        
        linhas = []
        linhas.append("=" * 100)
        linhas.append("📋 DADOS FILTRADOS - PRIMEIRAS 20 LINHAS")
        linhas.append("=" * 100)
        linhas.append("")
        linhas.append(f"Total de linhas após filtro: {len(df)}")
        linhas.append("")
        
        preview_df = df.head(20).copy()
        linhas.append(preview_df.to_string(index=False))
        
        return "\n".join(linhas)
    
    def _exportar_excel(self):
        """Exporta o relatório atual para Excel"""
        if hasattr(self, 'df_filtrado') and self.df_filtrado is not None:
            df_exportar = self.df_filtrado
            nome_base = "Filtrado"
        elif self.df_ruptura is not None:
            df_exportar = self.df_ruptura
            nome_base = "Ruptura"
        elif self.df_combinado is not None:
            df_exportar = self.df_combinado
            nome_base = "Combinado"
        else:
            messagebox.showwarning("Aviso", "Nenhum relatório gerado para exportar!")
            return
        
        df_exportar = df_exportar.reset_index(drop=True)
        
        if hasattr(self, 'df_filtrado') and self.df_filtrado is not None:
            resposta = messagebox.askyesno(
                "Exportar",
                f"Exportar dados FILTRADOS ({len(self.df_filtrado)} linhas)?\n\n"
                "Clique em NÃO para exportar os dados COMPLETOS."
            )
            if not resposta:
                if self.df_ruptura is not None:
                    df_exportar = self.df_ruptura
                    nome_base = "Ruptura_Completa"
                elif self.df_combinado is not None:
                    df_exportar = self.df_combinado
                    nome_base = "Combinado_Completo"
        
        data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome = f"Relatorio_{nome_base}_{data_hora}.xlsx"
        
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("Todos os arquivos", "*.*")],
            initialfile=nome
        )
        
        if path:
            try:
                self.status_label.configure(
                    text=f"⏳ Exportando {len(df_exportar)} linhas...",
                    text_color="#ffff00"
                )
                self.parent.update()
                
                df_exportar.to_excel(path, index=False)
                
                messagebox.showinfo(
                    "Sucesso",
                    f"✅ Relatório exportado com sucesso!\n\n"
                    f"📁 Arquivo: {os.path.basename(path)}\n"
                    f"📊 Linhas: {len(df_exportar)}"
                )
                
                self.status_label.configure(
                    text=f"✅ Exportado: {os.path.basename(path)}",
                    text_color="#00ff00"
                )
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar:\n{str(e)}")
                self.status_label.configure(text="❌ Erro na exportação", text_color="#ff0000")
    
    def _limpar_tudo(self):
        """Limpa todos os arquivos e dados"""
        for i in range(4):
            self.arquivos[i] = None
            self.dfs_processados[i] = None
            self.modelos[i] = None
            self.tipos_identificados[i] = None
            self.arquivos_definidos[i] = False
            self.entries[i].delete(0, "end")
            self.entries[i].configure(border_color=self.cores['destaque'])
            self.status_arquivos[i].configure(text="⭕", text_color=self.cores['texto_secundario'])
            self.botoes_definir[i].configure(state="disabled", text="✅ Definir", fg_color=self.cores['botao_filtro'])
        
        self.df_curva = None
        self.df_estoque = None
        self.df_media = None
        self.df_ruptura = None
        self.df_combinado = None
        self.df_filtrado = None
        self.relatorio_selecionado = None
        self.relatorios_disponiveis = []
        
        self.resumo.limpar()
        self.preview.limpar()
        self.btn_exportar.configure(state="disabled")
        self.btn_relatorio.configure(state="disabled")
        self.btn_processar.configure(state="disabled", fg_color=self.cores['botao_limpar'])
        self.btn_filtrar.configure(state="disabled")
        self.btn_carregar.configure(state="disabled")
        self.relatorio_label.configure(text="Nenhum relatório selecionado")
        self.status_label.configure(text="⏳ Aguardando arquivos...", text_color=self.cores['texto_secundario'])
        messagebox.showinfo("Limpo", "Todos os dados foram limpos!")
    
    def atualizar_cores(self, cores):
        """Atualiza as cores quando o tema muda"""
        self.cores = cores
        
        if hasattr(self, 'frame') and self.frame:
            self.frame.configure(fg_color=self.cores['fundo'])
        
        for entry in self.entries:
            entry.configure(
                fg_color=self.cores['entrada'],
                border_color=self.cores['destaque']
            )
        
        for btn in self.botoes_procurar:
            btn.configure(
                fg_color=self.cores['entrada'],
                hover_color=self.cores['destaque']
            )
        
        if hasattr(self, 'btn_carregar'):
            self.btn_carregar.configure(fg_color=self.cores['destaque'])
        
        if hasattr(self, 'btn_exportar'):
            self.btn_exportar.configure(fg_color=self.cores['botao_exportar'])
        
        if hasattr(self, 'btn_processar'):
            if self.relatorio_selecionado is not None:
                self.btn_processar.configure(fg_color=self.cores['destaque'])
            else:
                self.btn_processar.configure(fg_color=self.cores['botao_limpar'])
        
        if hasattr(self, 'btn_filtrar'):
            self.btn_filtrar.configure(fg_color=self.cores['botao_filtro'])
        
        if hasattr(self, 'btn_limpar'):
            self.btn_limpar.configure(fg_color=self.cores['botao_limpar'])
        
        if hasattr(self, 'btn_relatorio'):
            self.btn_relatorio.configure(fg_color="#4a6da8")
        
        if hasattr(self, 'resumo'):
            self.resumo.atualizar_cores(cores)
        
        if hasattr(self, 'preview'):
            self.preview.atualizar_cores(cores)