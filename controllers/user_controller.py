import tkinter as tk
from tkinter import filedialog, messagebox
from models.database import Database
from models.image_processor import ImageProcessor

class UserController:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.photos = []  # Lista para armazenar as fotos carregadas

    def show_user_dashboard(self):
        # Limpa a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Define o título da tela
        self.root.title(f"Usuário: {self.username}")
        self.root.geometry('400x300')

        # Exibe o nome do usuário no topo
        tk.Label(self.root, text=f"Usuário: {self.username}", font=('Arial', 18)).pack(pady=20)

        # Botão para adicionar fotos
        tk.Button(self.root, text="Adicionar Fotos", command=self.add_photos).pack(pady=10)

        # Botão para gerar relatório
        tk.Button(self.root, text="Gerar Relatório", command=self.generate_report).pack(pady=10)

        # Botão para remover todas as fotos
        tk.Button(self.root, text="Remover Todas as Fotos", command=self.remove_all_photos).pack(pady=10)

        # Botão para retornar à tela de login
        tk.Button(self.root, text="Retornar", command=self.return_to_login).place(x=320, y=10)

    def add_photos(self):
        # Abre o diálogo para selecionar uma pasta com as fotos
        folder_path = filedialog.askdirectory()

        if folder_path:
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
            added_photos = []

            for filename in os.listdir(folder_path):
                if filename.lower().endswith(image_extensions):
                    full_path = os.path.join(folder_path, filename)
                    self.photos.append(full_path)  # Adiciona a foto à lista de fotos
                    added_photos.append(full_path)

            if added_photos:
                messagebox.showinfo("Sucesso", f"{len(added_photos)} foto(s) adicionada(s) com sucesso!")
            else:
                messagebox.showwarning("Atenção", "Nenhuma imagem encontrada na pasta selecionada.")

    def remove_all_photos(self):
        if not self.photos:
            messagebox.showinfo("Remover Fotos", "Nenhuma foto foi adicionada.")
        else:
            self.photos.clear()
            messagebox.showinfo("Remover Fotos", "Todas as fotos foram removidas com sucesso!")

        self.show_user_dashboard()  # Atualiza a tela

    def generate_report(self):
        if not self.photos:
            messagebox.showerror("Erro", "Nenhuma foto foi adicionada.")
        else:
            report = []
            for photo in self.photos:
                result = ImageProcessor.process_image(photo)  # Processa a imagem com a rede neural
                report.append(result)

            self.show_report_screen(report)  # Exibe os resultados do processamento

    def show_report_screen(self, report):
        # Limpa a janela existente
        for widget in self.root.winfo_children():
            widget.destroy()

        # Exibe o relatório
        self.root.title("Relatório de Processamento")
        self.root.geometry('400x300')

        tk.Label(self.root, text="Resultados da Rede Neural", font=('Arial', 18)).pack(pady=20)

        for idx, result in enumerate(report, start=1):
            tk.Label(self.root, text=f"Imagem {idx}: {result}").pack(pady=5)

        # Botão para retornar ao dashboard do usuário
        tk.Button(self.root, text="Retornar", command=self.show_user_dashboard).pack(pady=20)

    def return_to_login(self):
        from controllers.login_controller import LoginController
        login_controller = LoginController(self.root)
        login_controller.show_main_screen()
