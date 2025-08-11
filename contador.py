#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contador Sequencial - Programa com interface gráfica
Contador de números de 0-999 com sincronização via banco de dados
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import threading
import time
import os
from pathlib import Path

class ContadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador Sequencial")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Configurar o banco de dados
        self.db_path = Path.home() / "contador.db"
        self.setup_database()
        
        # Variável para controlar a atualização
        self.updating = False
        self.last_value = 0
        
        # Configurar a interface
        self.setup_ui()
        
        # Configurar atalhos de teclado
        self.setup_keyboard_shortcuts()
        
        # Iniciar thread de sincronização
        self.start_sync_thread()
        
        # Carregar valor inicial
        self.load_current_value()
        
    def setup_database(self):
        """Configura o banco de dados SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contador (
                    id INTEGER PRIMARY KEY,
                    valor INTEGER NOT NULL DEFAULT 0,
                    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Inserir valor inicial se não existir
            cursor.execute('SELECT COUNT(*) FROM contador')
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO contador (id, valor) VALUES (1, 0)')
            
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao configurar banco de dados: {e}")
    
    def setup_ui(self):
        """Configura a interface gráfica"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Contador Sequencial", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Display do contador
        self.counter_var = tk.StringVar(value="0")
        self.counter_entry = ttk.Entry(main_frame, textvariable=self.counter_var,
                                      font=("Arial", 24, "bold"), 
                                      justify="center", width=10)
        self.counter_entry.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        self.counter_entry.bind('<Return>', self.on_entry_change)
        self.counter_entry.bind('<FocusOut>', self.on_entry_change)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        # Botão -1
        self.btn_minus = ttk.Button(button_frame, text="-1", 
                                   command=self.decrement, width=8)
        self.btn_minus.grid(row=0, column=0, padx=(0, 10))
        
        # Botão Zerar
        self.btn_zero = ttk.Button(button_frame, text="Zerar", 
                                  command=self.reset, width=8)
        self.btn_zero.grid(row=0, column=1, padx=(0, 10))
        
        # Botão +1
        self.btn_plus = ttk.Button(button_frame, text="+1", 
                                  command=self.increment, width=8)
        self.btn_plus.grid(row=0, column=2)
        
        # Status
        self.status_var = tk.StringVar(value="Conectado")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                font=("Arial", 10))
        status_label.grid(row=3, column=0, columnspan=3)
        
        # Instruções
        instructions = ttk.Label(main_frame, 
                               text="Atalhos: ↑/↓ para incrementar/decrementar, Backspace para zerar",
                               font=("Arial", 9), foreground="gray")
        instructions.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
    def setup_keyboard_shortcuts(self):
        """Configura os atalhos de teclado"""
        self.root.bind('<Up>', lambda e: self.increment())
        self.root.bind('<Down>', lambda e: self.decrement())
        self.root.bind('<BackSpace>', lambda e: self.reset())
        self.root.bind('<Key>', self.on_key_press)
        
    def on_key_press(self, event):
        """Manipula teclas pressionadas"""
        # Permitir edição direta no campo de entrada
        if event.widget == self.counter_entry:
            return
            
    def increment(self):
        """Incrementa o contador"""
        current = self.get_current_value()
        if current < 999:
            self.update_value(current + 1)
    
    def decrement(self):
        """Decrementa o contador"""
        current = self.get_current_value()
        if current > 0:
            self.update_value(current - 1)
    
    def reset(self):
        """Zera o contador"""
        self.update_value(0)
    
    def get_current_value(self):
        """Obtém o valor atual do contador"""
        try:
            return int(self.counter_var.get())
        except ValueError:
            return 0
    
    def update_value(self, new_value):
        """Atualiza o valor no banco de dados e na interface"""
        if 0 <= new_value <= 999:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE contador 
                    SET valor = ?, ultima_atualizacao = CURRENT_TIMESTAMP 
                    WHERE id = 1
                ''', (new_value,))
                conn.commit()
                conn.close()
                
                self.counter_var.set(str(new_value))
                self.status_var.set("Atualizado")
            except Exception as e:
                self.status_var.set(f"Erro: {e}")
    
    def on_entry_change(self, event=None):
        """Manipula mudanças no campo de entrada"""
        try:
            value = int(self.counter_var.get())
            if 0 <= value <= 999:
                self.update_value(value)
            else:
                # Restaurar valor anterior se fora do range
                self.counter_var.set(str(self.last_value))
                messagebox.showwarning("Aviso", "O valor deve estar entre 0 e 999")
        except ValueError:
            # Restaurar valor anterior se não for número
            self.counter_var.set(str(self.last_value))
            messagebox.showwarning("Aviso", "Digite apenas números")
    
    def load_current_value(self):
        """Carrega o valor atual do banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT valor FROM contador WHERE id = 1')
            result = cursor.fetchone()
            conn.close()
            
            if result:
                value = result[0]
                self.counter_var.set(str(value))
                self.last_value = value
        except Exception as e:
            self.status_var.set(f"Erro ao carregar: {e}")
    
    def sync_with_database(self):
        """Sincroniza com o banco de dados a cada segundo"""
        while True:
            try:
                if not self.updating:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT valor FROM contador WHERE id = 1')
                    result = cursor.fetchone()
                    conn.close()
                    
                    if result:
                        db_value = result[0]
                        current_value = self.get_current_value()
                        
                        if db_value != current_value:
                            self.root.after(0, lambda: self.counter_var.set(str(db_value)))
                            self.last_value = db_value
                            self.root.after(0, lambda: self.status_var.set("Sincronizado"))
                
                time.sleep(1)
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Erro de sincronização: {e}"))
                time.sleep(5)  # Esperar mais tempo em caso de erro
    
    def start_sync_thread(self):
        """Inicia a thread de sincronização"""
        sync_thread = threading.Thread(target=self.sync_with_database, daemon=True)
        sync_thread.start()

def main():
    """Função principal"""
    root = tk.Tk()
    app = ContadorApp(root)
    
    # Configurar fechamento da aplicação
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_closing()

if __name__ == "__main__":
    main()

