import logging
import tkinter as tk
from controllers.login_controller import LoginController

# Configuração básica de logging
logging.basicConfig(
    filename='logs.txt',  # Nome do arquivo de log
    level=logging.INFO,    # Nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato da mensagem de log
)

# Log de inicialização do sistema
logging.info('O sistema foi iniciado.')

def main():
    root = tk.Tk()
    root.title("Acessos")
    
    # Definir o tamanho da janela
    root.geometry('400x300')

    # Título da tela
    tk.Label(root, text="Acessos", font=('Arial', 18)).pack(pady=20)

    # Instancia o controlador de login
    login_controller = LoginController(root)

    # Botões
    tk.Button(root, text="Usuários", command=login_controller.show_user_login_screen).pack(pady=10)
    tk.Button(root, text="Administrador", command=login_controller.show_admin_login_screen).pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
