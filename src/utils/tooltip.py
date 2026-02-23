# src/utils/tooltip.py
"""
Sistema de tooltips para os botões.
"""
import tkinter as tk

class ToolTip:
    """Classe para gerenciar tooltips nos widgets"""
    
    def __init__(self, widget, texto):
        """
        Inicializa um tooltip.
        
        Args:
            widget: Widget que receberá o tooltip
            texto: Texto a ser exibido
        """
        self.widget = widget
        self.texto = texto
        self.tooltip = None
        self._bind_events()
    
    def _bind_events(self):
        """Vincula os eventos de mouse ao widget"""
        self.widget.bind('<Enter>', self._show)
        self.widget.bind('<Leave>', self._hide)
    
    def _show(self, event):
        """Mostra o tooltip quando o mouse entra"""
        if self.tooltip:
            return
        
        # Posiciona o tooltip próximo ao mouse
        x = event.x_root + 15
        y = event.y_root + 10
        
        # Cria a janela do tooltip
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)  # Remove decorações da janela
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        # Label com o texto
        label = tk.Label(
            self.tooltip,
            text=self.texto,
            bg="#ffffcc",
            fg="#000000",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack()
    
    def _hide(self, event):
        """Esconde o tooltip quando o mouse sai"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def criar_tooltip(widget, texto):
    """
    Função de conveniência para criar tooltips.
    
    Args:
        widget: Widget que receberá o tooltip
        texto: Texto a ser exibido
    
    Returns:
        ToolTip: Objeto do tooltip criado
    """
    return ToolTip(widget, texto)