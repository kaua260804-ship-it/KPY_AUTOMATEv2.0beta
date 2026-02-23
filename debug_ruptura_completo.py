# debug_layout_final.py
"""
Debug com a solução final - botões em frame separado mas visualmente alinhados.
"""
import sys
import os
import customtkinter as ctk

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("="*80)
print("🔍 DEBUG - SOLUÇÃO FINAL")
print("="*80)

# Cores de teste
cores_teste = {
    'fundo': '#2d2d2d',
    'entrada': '#3d3d3d',
    'texto': '#ffffff',
    'texto_secundario': '#cccccc',
    'destaque': '#8b0000',
    'botao_filtro': '#4a6da8',
    'botao_exportar': '#8b0000',
    'botao_limpar': '#666666',
    'scrollbar': '#4d4d4d',
    'scrollbar_trough': '#333333',
}

# Criar janela
root = ctk.CTk()
root.geometry("1400x800")
root.title("DEBUG - SOLUÇÃO FINAL")

class TelaCriarRelatorioFinal:
    """Tela com botões independentes mas visualmente na mesma posição"""
    
    def __init__(self, parent, cores):
        self.parent = parent
        self.cores = cores
        self.frame = ctk.CTkFrame(parent, fg_color=cores['fundo'], corner_radius=0)
        self.frame.pack(fill='both', expand=True)
        self._criar_interface()
    
    def _criar_interface(self):
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # ===== TÍTULO =====
        titulo_frame = ctk.CTkFrame(container, fg_color="transparent", height=50)
        titulo_frame.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(
            titulo_frame,
            text="📋 CRIAR RELATÓRIO PERSONALIZADO (FINAL)",
            font=("Arial", 20, "bold"),
            text_color=self.cores['texto']
        ).pack(anchor='w')
        
        # ===== CABEÇALHO =====
        cabecalho = ctk.CTkFrame(container, fg_color="transparent", height=25)
        cabecalho.pack(fill='x', pady=(0, 5))
        
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
        
        # ===== 4 LINHAS DE ARQUIVO (só Procurar e Definir) =====
        for i in range(4):
            linha = ctk.CTkFrame(container, fg_color="transparent", height=32)
            linha.pack(fill='x', pady=1)
            linha.pack_propagate(False)
            
            # Entry do arquivo
            ctk.CTkEntry(
                linha, fg_color=self.cores['entrada'], text_color=self.cores['texto'],
                font=("Arial", 11), corner_radius=4, border_width=1,
                border_color=self.cores['destaque'], width=500, height=28
            ).pack(side='left', padx=(0, 10))
            
            # Status
            ctk.CTkLabel(
                linha, text="⭕", font=("Arial", 12),
                text_color=self.cores['texto_secundario'], width=150, height=28
            ).pack(side='left', padx=(0, 10))
            
            # Frame para botões da linha (Procurar e Definir)
            frame_botoes_linha = ctk.CTkFrame(linha, fg_color="transparent")
            frame_botoes_linha.pack(side='left')
            
            ctk.CTkButton(
                frame_botoes_linha, text="📁 Procurar", command=lambda: None,
                fg_color=self.cores['entrada'], hover_color=self.cores['destaque'],
                text_color=self.cores['texto'], width=80, height=28, corner_radius=4
            ).pack(side='left', padx=2)
            
            ctk.CTkButton(
                frame_botoes_linha, text="✅ Definir", command=lambda: None,
                fg_color=self.cores['botao_filtro'], hover_color="#5a7db8",
                text_color=self.cores['texto'], width=70, height=28,
                corner_radius=4
            ).pack(side='left', padx=2)
        
        # ===== LINHA DOS BOTÕES DE CONTROLE (INDEPENDENTE) =====
        linha_controle = ctk.CTkFrame(container, fg_color="transparent", height=32)
        linha_controle.pack(fill='x', pady=2)
        linha_controle.pack_propagate(False)
        
        # Espaço vazio para alinhar visualmente com as colunas anteriores
        ctk.CTkLabel(
            linha_controle,
            text="",
            width=660  # 500(Arquivo) + 150(Status) + 10(padding)
        ).pack(side='left')
        
        # Frame para os botões de controle (grid 2x3)
        frame_controle = ctk.CTkFrame(linha_controle, fg_color="transparent")
        frame_controle.pack(side='left')
        
        grid_frame = ctk.CTkFrame(frame_controle, fg_color="transparent")
        grid_frame.pack()
        
        # Configurar grid 2 colunas
        grid_frame.grid_columnconfigure(0, weight=1, pad=2)
        grid_frame.grid_columnconfigure(1, weight=1, pad=2)
        
        # Criar botões em grid 2x3
        botoes = [
            ("📂 CARREGAR", self.cores['destaque']),
            ("📊 RELATÓRIO", "#4a6da8"),
            ("⚙️ PROCESSAR", self.cores['destaque']),
            ("🔽 FILTRAR", self.cores['botao_filtro']),
            ("💾 EXPORTAR", self.cores['botao_exportar']),
            ("🗑️ LIMPAR", self.cores['botao_limpar'])
        ]
        
        posicoes = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]
        
        for (texto, cor), (row, col) in zip(botoes, posicoes):
            btn = ctk.CTkButton(
                grid_frame, text=texto, command=lambda: None,
                fg_color=cor, 
                hover_color="#a52a2a" if "CARREGAR" in texto or "PROCESSAR" in texto else
                           "#5a7db8" if "RELATÓRIO" in texto or "FILTRAR" in texto else
                           "#8b0000" if "EXPORTAR" in texto else "#888888",
                text_color=self.cores['texto'], width=90, height=28,
                corner_radius=4, font=("Arial", 10, "bold")
            )
            btn.grid(row=row, column=col, padx=2, pady=1)
        
        # ===== STATUS =====
        self.status_label = ctk.CTkLabel(
            container,
            text="⏳ Aguardando arquivos...",
            font=("Arial", 11),
            text_color=self.cores['texto_secundario']
        )
        self.status_label.pack(pady=5)
        
        self.relatorio_label = ctk.CTkLabel(
            container,
            text="Nenhum relatório selecionado",
            font=("Arial", 11, "italic"),
            text_color=self.cores['texto_secundario']
        )
        self.relatorio_label.pack(pady=2)
        
        # ===== RESUMO =====
        resumo_frame = ctk.CTkFrame(container, fg_color="transparent")
        resumo_frame.pack(fill='x', pady=10)
        
        ctk.CTkLabel(
            resumo_frame,
            text="📊 RESUMO",
            font=("Arial", 12, "bold"),
            text_color=self.cores['texto']
        ).pack(anchor='w')
        
        # ===== PREVIEW =====
        preview_frame = ctk.CTkFrame(container, fg_color="transparent")
        preview_frame.pack(fill='both', expand=True)
        
        ctk.CTkLabel(
            preview_frame,
            text="📋 PRÉ-VISUALIZAÇÃO (20 primeiras linhas)",
            font=("Arial", 12, "bold"),
            text_color=self.cores['texto']
        ).pack(anchor='w')

# Criar a tela
print("\n📋 CRIANDO TELA COM SOLUÇÃO FINAL...")
tela = TelaCriarRelatorioFinal(root, cores_teste)

print("\n" + "="*80)
print("✅ SOLUÇÃO FINAL APLICADA!")
print("="*80)
print("\n📌 CARACTERÍSTICAS:")
print("1. Botões em frame separado (não dentro da primeira linha)")
print("2. Visualmente alinhados com a coluna 'Ação' usando espaçador")
print("3. Aparecem para todas as linhas")
print("4. Grid 2x3 mantido")
print("5. Layout original preservado")
print("\n👉 Verifique a janela - os botões agora estão visíveis!")

root.mainloop()