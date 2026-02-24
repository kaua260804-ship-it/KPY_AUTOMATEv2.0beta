# src/utils/config_manager.py
"""
Gerenciador de configurações do usuário
Salva preferências como tema, fonte, modo compacto
"""
import json
import os
from src.utils.helpers import get_resource_path

class ConfigManager:
    """Gerencia as configurações do usuário"""
    
    _instance = None
    _config = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._carregar_config()
        return cls._instance
    
    def _get_config_path(self):
        """Retorna o caminho do arquivo de configuração"""
        try:
            # Salvar na pasta do usuário (não na pasta do programa)
            from pathlib import Path
            home = Path.home()
            config_dir = home / ".kpy_automate"
            
            if not config_dir.exists():
                config_dir.mkdir(parents=True)
            
            return config_dir / "config.json"
        except:
            # Fallback para pasta local
            return "config.json"
    
    def _carregar_config(self):
        """Carrega as configurações do arquivo"""
        self.config_file = self._get_config_path()
        
        # Configurações padrão
        self._config = {
            'tema': 'escuro',
            'cor_destaque': '#8b0000',
            'tamanho_fonte': 12,
            'modo_compacto': False,
            'ultimos_arquivos': [],
            'favoritos': []
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    salvo = json.load(f)
                    self._config.update(salvo)
                print(f"✅ Configurações carregadas de {self.config_file}")
        except Exception as e:
            print(f"⚠️ Erro ao carregar configurações: {e}")
    
    def salvar(self):
        """Salva as configurações no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            return False
    
    def get(self, chave, default=None):
        """Retorna uma configuração"""
        return self._config.get(chave, default)
    
    def set(self, chave, valor):
        """Define uma configuração e salva"""
        self._config[chave] = valor
        self.salvar()
    
    def adicionar_arquivo_recente(self, caminho):
        """Adiciona arquivo à lista de recentes"""
        recentes = self._config.get('ultimos_arquivos', [])
        
        # Remover se já existir
        if caminho in recentes:
            recentes.remove(caminho)
        
        # Adicionar no início
        recentes.insert(0, caminho)
        
        # Manter apenas 10
        self._config['ultimos_arquivos'] = recentes[:10]
        self.salvar()

# Singleton
config = ConfigManager()