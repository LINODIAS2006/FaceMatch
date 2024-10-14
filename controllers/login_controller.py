import tkinter as tk
from tkinter import messagebox, filedialog
import os
import tensorflow as tf
from models.database import Database
from models.image_processor import ImageProcessor  # Supondo que você tenha uma classe para processar imagens

# Desabilitar o uso da GPU no TensorFlow (se necessário)
tf.config.set_visible_devices([], 'GPU')

class LoginController:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.photos = []  # Lista para armazenar as fotos adicionadas

    def show_main_screen(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Alterar a cor de fundo da janela
        self.root.configure(bg='lightgreen')
        
        # Definir o título
        self.root.title("Acessos")
        self.root.geometry('400x300')

        # Título da tela
        tk.Label(self.root, text="Acessos", font=('Arial', 18),bg='lightgreen', fg='blue').pack(pady=20)

        # Botões de login
        tk.Button(self.root, text="Usuários", command=self.show_user_login_screen, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Administrador", command=self.show_admin_login_screen, bg='blue', fg='white').pack(pady=10)

    ### Usuário

    def show_user_login_screen(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Alterar a cor de fundo da janela
        self.root.configure(bg='lightyellow')

        # Definir o título
        self.root.title("Login dos Usuários")
        self.root.geometry('400x300')

        # Título da tela
        tk.Label(self.root, text="Login dos Usuários", font=('Arial', 18),bg='lightyellow', fg='blue').pack(pady=20)

        # Campo para nome do usuário
        tk.Label(self.root, text="Usuário",bg='lightyellow', fg='blue').pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        # Campo para senha
        tk.Label(self.root, text="Senha",bg='lightyellow',fg='blue').pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)

        # Botão Acessar
        tk.Button(self.root, text="Acessar", command=self.user_login, bg='blue', fg='white').pack(pady=10)

        # Botão Retornar
        tk.Button(self.root, text="Retornar", command=self.show_main_screen, bg='red', fg='white').place(x=320, y=10)

    def user_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if Database.authenticate_user(username, password):
            self.username = username
            messagebox.showinfo("Login", f"Bem-vindo, {username}!")
            self.show_user_dashboard()
        else:
            messagebox.showerror("Erro", "Usuário não cadastrado ou senha incorreta!")

    def show_user_dashboard(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Alterar a cor de fundo da janela
        self.root.configure(bg='lightyellow')

        # Definir o título da tela
        self.root.title(f"Usuário: {self.username}")
        self.root.geometry('400x300')

        # Exibir o nome do usuário
        tk.Label(self.root, text=f"Usuário: {self.username}", font=('Arial', 18),bg='lightyellow', fg='blue').pack(pady=20)

        # Botões
        tk.Button(self.root, text="Adicionar Fotos", command=self.add_photos, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Gerar Relatório", command=self.generate_report, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Remover Todas as Fotos", command=self.remove_all_photos, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Retornar", command=self.show_main_screen, bg='red', fg='white').place(x=320, y=10)

    def add_photos(self):
        folder_path = filedialog.askdirectory()

        if folder_path:
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
            added_photos = []

            # Percorre todos os arquivos na pasta e verifica se são imagens
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path) and filename.lower().endswith(image_extensions):
                    self.photos.append(full_path)
                    added_photos.append(full_path)

            if added_photos:
                messagebox.showinfo("Sucesso", f"{len(added_photos)} foto(s) adicionada(s) com sucesso!")
            else:
                messagebox.showwarning("Atenção", "Nenhuma imagem foi encontrada na pasta selecionada.")
        else:
            messagebox.showwarning("Atenção", "Nenhuma pasta foi selecionada.")

    def remove_all_photos(self):
        if self.photos:
            self.photos.clear()
            messagebox.showinfo("Sucesso", "Todas as fotos foram removidas!")
        else:
            messagebox.showinfo("Fotos", "Nenhuma foto foi adicionada.")

    def generate_report(self):
        if not self.photos:
            messagebox.showerror("Erro", "Nenhuma foto foi adicionada.")
            return

        report = []

        # Processa cada foto usando a rede neural
        for idx, photo in enumerate(self.photos, start=1):
            try:
                result = ImageProcessor.process_image(photo)  # Chama a rede neural para processar a imagem
                report.append(f"Imagem {idx}: {result}")
            except Exception as e:
                # Captura o erro e o exibe no relatório
                report.append(f"Erro ao processar Imagem {idx}: {str(e)}")

        self.show_report_screen(report)

    def show_report_screen(self, report):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Relatório de Processamento")
        self.root.geometry('400x300')

        tk.Label(self.root, text="Resultados da Rede Neural", font=('Arial', 18),bg='lightyellow', fg='blue').pack(pady=20)

        for result in report:
            tk.Label(self.root, text=result).pack(pady=5)

        tk.Button(self.root, text="Retornar", command=self.show_user_dashboard, bg='red', fg='white').pack(pady=20)

    ### Administrador

    def show_admin_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Alterar a cor de fundo da janela
        self.root.configure(bg='lightyellow')

        self.root.title("Login do Administrador")
        self.root.geometry('400x300')

        tk.Label(self.root, text="Login do Administrador", font=('Arial', 18),bg='lightyellow', fg='blue').pack(pady=20)

        tk.Label(self.root, text="Usuário",bg='lightyellow', fg='blue').pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Senha",bg='lightyellow', fg='blue').pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(self.root, text="Acessar", command=self.admin_login, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Retornar", command=self.show_main_screen, bg='red', fg='white').place(x=320, y=10)

    def admin_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if Database.authenticate_admin(username, password):
            self.username = username
            messagebox.showinfo("Login", "Bem-vindo, Admin!")
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas!")

    def show_admin_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Alterar a cor de fundo da janela
        self.root.configure(bg='lightyellow')

        self.root.title(f"Administrador: {self.username}")
        self.root.geometry('400x300')

        tk.Label(self.root, text=f"Administrador: {self.username}", font=('Arial', 18),bg='lightyellow', fg='blue').pack(pady=20)

        tk.Button(self.root, text="Cadastrar Usuário", command=self.show_user_registration_screen, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Integrar Sistema", command=self.integrate_system, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Mostrar Logs", command=self.show_logs, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Retornar", command=self.show_admin_login_screen, bg='red', fg='white').place(x=320, y=10)

    def show_user_registration_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Alterar a cor de fundo da janela
        self.root.configure(bg='lightyellow')

        self.root.title("Cadastrar Usuário")
        self.root.geometry('400x300')

        tk.Label(self.root, text="Cadastrar Usuário", font=('Arial', 18),bg='lightyellow', fg='blue').pack(pady=20)

        tk.Label(self.root, text="Nome do Usuário",bg='lightyellow', fg='blue').pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack()

        tk.Label(self.root, text="Senha",bg='lightyellow', fg='blue').pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=10)

        tk.Button(self.root, text="Cadastrar", command=self.register_new_user, bg='blue', fg='white').pack(pady=10)
        tk.Button(self.root, text="Retornar", command=self.show_admin_dashboard, bg='red', fg='white').place(x=320, y=10)

    def register_new_user(self):
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()

        if username and password:
            Database.register_user(username, password)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Preencha o nome e a senha!")

    def integrate_system(self):
        messagebox.showinfo("Integração", "Não foi integrado a nenhum sistema.")

    def show_logs(self):
        try:
            with open('logs.txt', 'r') as f:
                logs = f.read()
        except FileNotFoundError:
            logs = "Nenhum log encontrado."

        logs_window = tk.Toplevel(self.root)
        logs_window.title("Logs do Programa")
        logs_window.geometry("500x400")

        scrollbar = tk.Scrollbar(logs_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(logs_window, text="Logs do Programa", font=('Arial', 16),bg='lightyellow', fg='blue').pack(pady=10)

        log_text = tk.Text(logs_window, wrap='word', yscrollcommand=scrollbar.set)
        log_text.insert(tk.END, logs)
        log_text.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar.config(command=log_text.yview)

        tk.Button(logs_window, text="Retornar", command=logs_window.destroy, bg='red', fg='white').place(x=420, y=10)
