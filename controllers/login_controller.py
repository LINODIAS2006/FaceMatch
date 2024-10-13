import tkinter as tk
from tkinter import messagebox, filedialog
import logging
import os
from models.database import Database
from models.image_processor import ImageProcessor

class LoginController:
    def __init__(self, root):
        self.root = root
        self.username = None  # Armazena o nome de usuário para usar nas próximas telas
        self.photos = []  # Lista para armazenar as fotos adicionadas

    ### Usuário

    def show_user_login_screen(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Definir o título
        self.root.title("Login dos Usuários")
        self.root.geometry('400x300')

        # Título da tela
        tk.Label(self.root, text="Login dos Usuários", font=('Arial', 18)).pack(pady=20)

        # Campo para nome do usuário
        tk.Label(self.root, text="Usuário").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        # Campo para senha
        tk.Label(self.root, text="Senha").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)

        # Botão Acessar
        tk.Button(self.root, text="Acessar", command=self.user_login).pack(pady=10)

        # Botão Retornar
        tk.Button(self.root, text="Retornar", command=self.show_main_screen).place(x=320, y=10)

    def user_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if Database.authenticate_user(username, password):
            self.username = username  # Armazena o nome do usuário
            logging.info(f'Usuário {username} fez login com sucesso.')
            messagebox.showinfo("Login", f"Bem-vindo, {username}!")
            self.show_user_dashboard()  # Redireciona para o painel do usuário
        else:
            logging.warning(f'Tentativa de login falhou para o usuário: {username}.')
            messagebox.showerror("Erro", "Credenciais inválidas")

    def show_user_dashboard(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Definir o título da tela
        self.root.title(f"Usuário: {self.username}")
        self.root.geometry('400x300')

        # Exibir o nome do usuário na parte de cima
        tk.Label(self.root, text=f"Usuário: {self.username}", font=('Arial', 18)).pack(pady=20)

        # Botão para adicionar fotos
        tk.Button(self.root, text="Adicionar Fotos", command=self.add_photos).pack(pady=10)

        # Botão para gerar relatório
        tk.Button(self.root, text="Gerar Relatório", command=self.generate_report).pack(pady=10)

        # Botão para remover todas as fotos
        tk.Button(self.root, text="Remover Todas as Fotos", command=self.remove_all_photos).pack(pady=10)

        # Botão para retornar
        tk.Button(self.root, text="Retornar", command=self.show_user_login_screen).place(x=320, y=10)

    def add_photos(self):
        # Abre o diálogo para o usuário selecionar uma pasta
        folder_path = filedialog.askdirectory()

        if folder_path:
            # Verificar se a pasta contém imagens
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
            added_photos = []

            for filename in os.listdir(folder_path):
                if filename.lower().endswith(image_extensions):  # Verifica se o arquivo é uma imagem
                    full_path = os.path.join(folder_path, filename)
                    self.photos.append(full_path)  # Adiciona a foto à lista de fotos
                    added_photos.append(full_path)

            if added_photos:
                logging.info(f'Fotos adicionadas por {self.username}: {added_photos}')
                messagebox.showinfo("Sucesso", f"{len(added_photos)} foto(s) adicionada(s) com sucesso!")
            else:
                messagebox.showwarning("Atenção", "Nenhuma imagem foi encontrada na pasta selecionada.")

    def remove_all_photos(self):
        # Verifica se há fotos adicionadas
        if not self.photos:
            messagebox.showinfo("Remover Fotos", "Nenhuma foto foi adicionada.")
        else:
            # Limpa todas as fotos da lista
            self.photos.clear()
            logging.info(f'Todas as fotos foram removidas por {self.username}.')
            messagebox.showinfo("Remover Fotos", "Todas as fotos foram removidas com sucesso!")

        # Volta para o dashboard do usuário
        self.show_user_dashboard()

    def generate_report(self):
        # Verifica se há fotos adicionadas
        if not self.photos:
            logging.warning(f'{self.username} tentou gerar um relatório sem adicionar fotos.')
            messagebox.showerror("Erro", "Nenhuma foto foi adicionada.")
        else:
            # Processar as fotos na rede neural
            report = []
            for photo in self.photos:
                result = ImageProcessor.process_image(photo)  # Processa a imagem com a rede neural
                report.append(result)

            logging.info(f'Relatório gerado por {self.username}.')
            self.show_report_screen(report)  # Exibe os resultados

    def show_report_screen(self, report):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título da tela de relatório
        self.root.title("Relatório de Processamento")
        self.root.geometry('400x300')

        # Exibir o resultado do processamento
        tk.Label(self.root, text="Resultados da Rede Neural", font=('Arial', 18)).pack(pady=20)

        # Exibir cada resultado
        for idx, result in enumerate(report, start=1):
            tk.Label(self.root, text=f"Imagem {idx}: {result}").pack(pady=5)

        # Botão para retornar ao dashboard do usuário
        tk.Button(self.root, text="Retornar", command=self.show_user_dashboard).pack(pady=20)

    ### Administrador

    def show_admin_login_screen(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Definir o título
        self.root.title("Login do Administrador")
        self.root.geometry('400x300')

        # Título da tela
        tk.Label(self.root, text="Login do Administrador", font=('Arial', 18)).pack(pady=20)

        # Campo para nome do administrador
        tk.Label(self.root, text="Usuário").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        # Campo para senha do administrador
        tk.Label(self.root, text="Senha").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack(pady=10)

        # Botão Acessar
        tk.Button(self.root, text="Acessar", command=self.admin_login).pack(pady=10)

        # Botão Retornar
        tk.Button(self.root, text="Retornar", command=self.show_main_screen).place(x=320, y=10)

    def admin_login(self):
        username = self.username.get()
        password = self.password.get()

        if Database.authenticate_admin(username, password):
            self.username = username  # Armazena o nome do administrador
            logging.info(f'Administrador {username} fez login com sucesso.')
            messagebox.showinfo("Login", "Bem-vindo, Admin!")
            self.show_admin_dashboard()  # Redireciona para o dashboard do administrador
        else:
            logging.warning(f'Tentativa de login falhou para o administrador: {username}.')
            messagebox.showerror("Erro", "Credenciais inválidas")

    def show_admin_dashboard(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Definir o título da tela
        self.root.title(f"Administrador: {self.username}")
        self.root.geometry('400x300')

        # Exibir o nome do administrador na parte de cima
        tk.Label(self.root, text=f"Administrador: {self.username}", font=('Arial', 18)).pack(pady=20)

        # Botão para cadastrar usuário
        tk.Button(self.root, text="Cadastrar Usuário", command=self.show_user_registration_screen).pack(pady=10)

        # Botão para integrar sistema
        tk.Button(self.root, text="Integrar Sistema", command=self.integrate_system).pack(pady=10)

        # Botão para mostrar logs
        tk.Button(self.root, text="Mostrar Logs", command=self.show_logs).pack(pady=10)

        # Botão para retornar
        tk.Button(self.root, text="Retornar", command=self.show_admin_login_screen).place(x=320, y=10)

    def integrate_system(self):
        # Exibe uma mensagem indicando que o sistema não foi integrado
        logging.info('Administrador tentou integrar sistema. Nenhuma integração disponível.')
        messagebox.showinfo("Integração", "Não foi integrado a nenhum sistema.")

    def show_logs(self):
        # Abre uma nova janela com os logs do programa
        logs = self.get_logs()  # Supondo que os logs estão disponíveis
        self.show_logs_screen(logs)

    def get_logs(self):
        # Método para obter os logs do arquivo logs.txt
        try:
            with open("logs.txt", "r") as file:
                logs = file.read()
        except FileNotFoundError:
            logs = "Nenhum log disponível."
        return logs

    def show_logs_screen(self, logs):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título da tela de logs
        self.root.title("Logs do Programa")
        self.root.geometry('400x300')

        # Exibir os logs
        tk.Label(self.root, text="Logs do Programa", font=('Arial', 18)).pack(pady=20)
        tk.Label(self.root, text=logs, justify="left", wraplength=380).pack(pady=10)

        # Botão para retornar ao dashboard do administrador
        tk.Button(self.root, text="Retornar", command=self.show_admin_dashboard).pack(pady=20)

    ### Cadastro de Usuários

    def show_user_registration_screen(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Definir o título da tela
        self.root.title("Cadastrar Usuário")
        self.root.geometry('400x300')

        # Título da tela
        tk.Label(self.root, text="Cadastrar Usuário", font=('Arial', 18)).pack(pady=20)

        # Campo para nome do usuário
        tk.Label(self.root, text="Nome do Usuário").pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack()

        # Campo para senha do usuário
        tk.Label(self.root, text="Senha").pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=10)

        # Botão para cadastrar usuário
        tk.Button(self.root, text="Cadastrar", command=self.register_new_user).pack(pady=10)

        # Botão para retornar
        tk.Button(self.root, text="Retornar", command=self.show_admin_dashboard).place(x=320, y=10)

    def register_new_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if username and password:
            Database.register_user(username, password)
            logging.info(f'Novo usuário cadastrado: {username}.')
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            logging.warning('Tentativa de cadastro de usuário falhou. Nome ou senha ausentes.')
            messagebox.showerror("Erro", "Por favor, preencha o nome e a senha.")

    ### Tela Principal

    def show_main_screen(self):
        # Limpar a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Redefinir a tela principal
        self.root.title("Acessos")
        self.root.geometry('400x300')

        tk.Label(self.root, text="Acessos", font=('Arial', 18)).pack(pady=20)

        # Botões da tela principal
        tk.Button(self.root, text="Usuários", command=self.show_user_login_screen).pack(pady=10)
        tk.Button(self.root, text="Administrador", command=self.show_admin_login_screen).pack(pady=10)
