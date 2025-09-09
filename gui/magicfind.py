import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

url_base = "http://localhost:3000/"
url_bugigangas = f"{url_base}bugigangas"  # Alterado
url_login = f"{url_base}login"

usuario_id = None
token = None

def login():
    global usuario_id, token
    email = simpledialog.askstring("Login", "E-mail:")
    senha = simpledialog.askstring("Login", "Senha:", show="*")

    if email and senha:
        response = requests.post(url_login, json={"email": email, "senha": senha})
        if response.status_code == 200:
            data = response.json()
            usuario_id = data["id"]
            token = data["token"]
            messagebox.showinfo("Login", f"Bem-vindo, {data['nome']}!")
        else:
            messagebox.showerror("Erro", "Não foi possível realizar o login.")

def listar_bugigangas():  
    response = requests.get(url_bugigangas)
    if response.status_code == 200:
        bugigangas = response.json()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "ID   Nome                  Descrição           Classe\n")
        result_text.insert(tk.END, "-----------------------------------------------------\n")
        for bugiganga in bugigangas:
            result_text.insert(tk.END, f"{bugiganga['id']:<5}{bugiganga['nome']:<20}{bugiganga['descricao']:<20}{bugiganga.get('Classe', 'N/A')}\n")
    else:
        messagebox.showerror("Erro", "Não foi possível obter as bugigangas.")

def adicionar_bugiganga(): 
    if not token:
        messagebox.showerror("Erro", "É necessário fazer login antes de adicionar uma bugiganga.")
        return

    nome = simpledialog.askstring("Adicionar Bugiganga", "Nome:")
    descricao = simpledialog.askstring("Adicionar Bugiganga", "Descrição:")
    classe = simpledialog.askstring("Adicionar Bugiganga", "Classe:")

    if nome and descricao and classe:
        response = requests.post(
            url_bugigangas,
            json={"nome": nome, "descricao": descricao, "Classe": classe},
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 201:
            bugiganga = response.json()
            messagebox.showinfo("Sucesso", f"Bugiganga criada com sucesso! ID: {bugiganga['id']}")
        else:
            messagebox.showerror("Erro", "Não foi possível criar a bugiganga.")

def atualizar_bugiganga():  
    if not token:
        messagebox.showerror("Erro", "É necessário fazer login antes de atualizar uma bugiganga.")
        return

    listar_bugigangas()
    id_bugiganga = simpledialog.askinteger("Atualizar Bugiganga", "Digite o ID da bugiganga a ser atualizada:")
    nome = simpledialog.askstring("Atualizar Bugiganga", "Novo nome (ou deixe vazio):")
    descricao = simpledialog.askstring("Atualizar Bugiganga", "Nova descrição (ou deixe vazio):")
    classe = simpledialog.askstring("Atualizar Bugiganga", "Nova classe (ou deixe vazio):")

    dados = {"nome": nome, "descricao": descricao, "Classe": classe}
    dados = {chave: valor for chave, valor in dados.items() if valor}

    response = requests.patch(
        f"{url_bugigangas}/{id_bugiganga}",
        json=dados,
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        messagebox.showinfo("Sucesso", "Bugiganga atualizada com sucesso!")
    else:
        messagebox.showerror("Erro", "Não foi possível atualizar a bugiganga.")

def excluir_bugiganga():  
    if not token:
        messagebox.showerror("Erro", "É necessário fazer login antes de excluir uma bugiganga.")
        return

    listar_bugigangas()
    id_bugiganga = simpledialog.askinteger("Excluir Bugiganga", "Digite o ID da bugiganga a ser excluída:")

    response = requests.delete(
        f"{url_bugigangas}/{id_bugiganga}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        messagebox.showinfo("Sucesso", "Bugiganga excluída com sucesso!")
    else:
        messagebox.showerror("Erro", "Não foi possível excluir a bugiganga.")

def grafico_bugigangas_por_classe(): 
    response = requests.get(url_bugigangas)
    if response.status_code == 200:
        bugigangas = response.json()
        classes = [bugiganga.get("Classe", "Sem classe") for bugiganga in bugigangas]
        classes_unicas = list(set(classes))
        quantidades = [classes.count(classe) for classe in classes_unicas]

        fig = plt.figure(figsize=(8, 5))
        plt.bar(classes_unicas, quantidades, color="orange")
        plt.title("Quantidade de Bugigangas por Classe", color="white")
        plt.xlabel("Classe", color="white")
        plt.ylabel("Quantidade", color="white")
        plt.gca().set_facecolor("#2d2d2d")
        plt.gcf().set_facecolor("#2d2d2d")
        plt.xticks(color="white")
        plt.yticks(color="white")

        plot_window = tk.Toplevel(root)
        plot_window.title("Gráfico de Bugigangas por Classe")
        plot_window.configure(bg="#2d2d2d")
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Erro", "Não foi possível gerar o gráfico.")

def grafico_bugigangas_por_usuario():  
    response = requests.get(url_bugigangas)
    if response.status_code == 200:
        bugigangas = response.json()
        usuarios = [bugiganga["usuario"]["nome"] for bugiganga in bugigangas]
        usuarios_unicos = list(set(usuarios))
        quantidades = [usuarios.count(usuario) for usuario in usuarios_unicos]

        fig = plt.figure(figsize=(8, 5))
        plt.pie(quantidades, labels=usuarios_unicos, autopct="%1.1f%%", startangle=90, colors=["orange", "white", "gold"])
        plt.title("Distribuição de Bugigangas por Usuário", color="white")
        plt.gcf().set_facecolor("#2d2d2d")

        plot_window = tk.Toplevel(root)
        plot_window.title("Gráfico de Bugigangas por Usuário")
        plot_window.configure(bg="#2d2d2d")
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Erro", "Não foi possível gerar o gráfico.")

# GUI Setup
root = tk.Tk()
root.title("Gerenciamento de Bugigangas")
root.geometry("900x600")  # Resolução
root.configure(bg="#2d2d2d")

# Estilo config
style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background="#2d2d2d")
style.configure("TButton", background="#ff8c42", foreground="black", font=("Helvetica", 10), borderwidth=2)
style.map("TButton", background=[("active", "#ff6f00")])
style.configure("TLabel", background="#2d2d2d", foreground="orange", font=("Helvetica", 12))
style.configure("TEntry", fieldbackground="#3d3d3d", foreground="white", insertcolor="white")
style.configure("TText", background="#3d3d3d", foreground="white")

# Frame do botão
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Botões
ttk.Button(button_frame, text="Login", command=login).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Listar Bugigangas", command=listar_bugigangas).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Adicionar Bugiganga", command=adicionar_bugiganga).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(button_frame, text="Atualizar Bugiganga", command=atualizar_bugiganga).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(button_frame, text="Excluir Bugiganga", command=excluir_bugiganga).grid(row=0, column=4, padx=5, pady=5)
ttk.Button(button_frame, text="Gráfico por Classe", command=grafico_bugigangas_por_classe).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Gráfico por Usuário", command=grafico_bugigangas_por_usuario).grid(row=1, column=1, padx=5, pady=5)

# Area de texto que mostra os resultados
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20, bg="#3d3d3d", fg="white", insertbackground="white")
result_text.pack(pady=10)

# Iniciar a GUI
root.mainloop()