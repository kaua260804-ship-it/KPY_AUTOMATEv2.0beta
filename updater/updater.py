# updater/updater.py
"""
Sistema de atualização automática do K'PY AUTOMATE
"""
import os
import sys
import json
import tempfile
import subprocess
import requests
from tkinter import messagebox, Tk
import tkinter as tk
from tkinter import ttk
import threading

class Updater:
    def __init__(self, app_path=None):
        if app_path is None:
            if getattr(sys, 'frozen', False):
                self.app_path = os.path.dirname(sys.executable)
            else:
                self.app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.app_path = app_path
            
        self.version_file = os.path.join(self.app_path, 'version.json')
        self.update_url = "https://raw.githubusercontent.com/kaua260804-ship-it/KPY_AUTOMATEv2.0beta/main/version.json"
        self.temp_dir = tempfile.mkdtemp()
        
    def get_current_version(self):
        """Lê a versão atual do programa"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data.get('latest_version', '0.0.0')
            return '2.0.0'  # Versão padrão
        except:
            return '2.0.0'
    
    def check_for_updates(self):
        """Verifica se há atualizações disponíveis"""
        try:
            response = requests.get(self.update_url, timeout=5)
            if response.status_code == 200:
                server_data = response.json()
                current = self.get_current_version()
                
                # Comparar versões
                if server_data['latest_version'] > current:
                    return {
                        'has_update': True,
                        'version': server_data['latest_version'],
                        'url': server_data['download_url'],
                        'required': server_data.get('required', False),
                        'notes': server_data.get('release_notes', '')
                    }
            return {'has_update': False}
        except Exception as e:
            print(f"Erro ao verificar atualizações: {e}")
            return {'has_update': False}
    
    def download_update(self, url, progress_callback=None):
        """Baixa a atualização"""
        try:
            local_filename = os.path.join(self.temp_dir, 'KPY_AUTOMATE_update.exe')
            
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size:
                            progress = int((downloaded / total_size) * 100)
                            progress_callback(progress)
            
            return local_filename
        except Exception as e:
            print(f"Erro ao baixar atualização: {e}")
            return None
    
    def install_update(self, update_file):
        """Instala a atualização"""
        try:
            # Criar script de atualização
            script = f'''@echo off
timeout /t 2 /nobreak > nul
taskkill /f /im KPY_AUTOMATE.exe 2>nul
timeout /t 2 /nobreak > nul
copy /y "{update_file}" "{self.app_path}\\KPY_AUTOMATE.exe"
start "" "{self.app_path}\\KPY_AUTOMATE.exe"
del "{update_file}"
del "%~f0"
'''
            batch_file = os.path.join(self.temp_dir, 'update.bat')
            with open(batch_file, 'w') as f:
                f.write(script)
            
            # Executar script e sair
            subprocess.Popen(['cmd', '/c', batch_file], shell=True)
            sys.exit(0)
        except Exception as e:
            print(f"Erro ao instalar atualização: {e}")
            return False


class UpdateDialog:
    """Janela de progresso da atualização"""
    
    def __init__(self, parent, updater, update_info):
        self.parent = parent
        self.updater = updater
        self.update_info = update_info
        
        self.janela = tk.Toplevel(parent)
        self.janela.title("Atualização Disponível")
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)
        self.janela.transient(parent)
        self.janela.grab_set()
        
        # Centralizar
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (300 // 2)
        self.janela.geometry(f'+{x}+{y}')
        
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria a interface da janela"""
        try:
            self.janela.iconbitmap(os.path.join(self.updater.app_path, 'assets', 'icons', 'logo.ico'))
        except:
            pass
        
        # Título
        tk.Label(
            self.janela,
            text="📦 Atualização Disponível",
            font=("Arial", 16, "bold"),
            fg="#8b0000"
        ).pack(pady=(20, 10))
        
        # Versão
        tk.Label(
            self.janela,
            text=f"Nova versão: {self.update_info['version']}",
            font=("Arial", 12)
        ).pack(pady=5)
        
        # Notas da versão
        if self.update_info.get('notes'):
            tk.Label(
                self.janela,
                text=f"Novidades: {self.update_info['notes']}",
                font=("Arial", 10),
                wraplength=350
            ).pack(pady=5)
        
        # Frame de progresso (inicialmente escondido)
        self.progress_frame = tk.Frame(self.janela)
        
        tk.Label(
            self.progress_frame,
            text="Baixando atualização...",
            font=("Arial", 10)
        ).pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="0%",
            font=("Arial", 9)
        )
        self.progress_label.pack()
        
        # Frame de botões
        button_frame = tk.Frame(self.janela)
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Atualizar Agora",
            command=self.iniciar_download,
            bg="#8b0000",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5,
            cursor="hand2"
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Depois",
            command=self.janela.destroy,
            bg="#666666",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=5,
            cursor="hand2"
        ).pack(side='left', padx=5)
    
    def update_progress(self, value):
        """Atualiza a barra de progresso"""
        self.progress_bar['value'] = value
        self.progress_label.config(text=f"{value}%")
        self.janela.update()
    
    def iniciar_download(self):
        """Inicia o download em thread separada"""
        # Esconder botões e mostrar progresso
        for widget in self.janela.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.progress_frame:
                widget.pack_forget()
        
        self.progress_frame.pack(pady=20)
        self.janela.update()
        
        def download_thread():
            update_file = self.updater.download_update(
                self.update_info['url'],
                self.update_progress
            )
            
            if update_file:
                self.janela.after(0, lambda: self.instalando(update_file))
            else:
                self.janela.after(0, lambda: self.erro_download())
        
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
    
    def instalando(self, update_file):
        """Mostra mensagem de instalação"""
        self.progress_label.config(text="Instalando...")
        self.janela.update()
        
        # Fechar janela e instalar
        self.janela.destroy()
        self.updater.install_update(update_file)
    
    def erro_download(self):
        """Mostra erro no download"""
        messagebox.showerror(
            "Erro",
            "Falha ao baixar a atualização.\nVerifique sua conexão com a internet."
        )
        self.janela.destroy()


def check_updates(parent=None):
    """Função principal para verificar atualizações"""
    updater = Updater()
    update_info = updater.check_for_updates()
    
    if update_info['has_update']:
        if parent:
            UpdateDialog(parent, updater, update_info)
        else:
            # Criar janela temporária
            root = tk.Tk()
            root.withdraw()
            UpdateDialog(root, updater, update_info)
            root.mainloop()
    else:
        if parent:
            messagebox.showinfo(
                "Atualizações",
                "Você já está usando a versão mais recente!"
            )
    
    return update_info


if __name__ == "__main__":
    # Teste
    check_updates()