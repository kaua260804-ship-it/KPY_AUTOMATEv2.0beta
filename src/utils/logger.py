# src/utils/logger.py
"""
Logger DESATIVADO - Versão vazia para não quebrar os imports
"""
import logging

class Logger:
    def __init__(self):
        pass
    
    def get_logger(self):
        return logging.getLogger('dummy')
    
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass
    def critical(self, msg): pass
    def exception(self, msg): pass

# Singleton
log = Logger()

# Funções vazias
def debug(msg): pass
def info(msg): pass
def warning(msg): pass
def error(msg): pass
def critical(msg): pass
def exception(msg): pass