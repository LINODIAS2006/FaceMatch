import tkinter as tk
from tkinter import messagebox
from models.database import Database

class AdminController:
    def __init__(self, root):
        self.root = root

    def show_admin_screen(self):
        self.root.geometry('400x300')
        tk.Label(self.root, text="Admin Dashboard").pack(pady=20)

        # Campos para o administrador cadastrar novos usuários
        tk.Label(self.root, text="Cadastrar novo usuário").pack(pady=10)
        tk.Label(self.root, text="Usuário").pack()
        self.new_username = tk.Entry(self.root)
        self.new_username.pack()

        tk.Label(self.root, text="Senha").pack()
        self.new_password = tk.Entry(self.root, show="*")
        self.new_password.pack()

        tk.Button(self.root, text="Cadastrar", command=self.register_new_user).pack(pady=10)

    def register_new_user(self):
        username = self.new_username.get()
        password = self.new_password.get()

        # Cadastra o novo usuário
        if username and password:
            Database.register_user(username, password)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome de usuário e a senha.")
