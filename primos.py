import tkinter as tk
from tkinter import messagebox
import os

def eh_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    return True

class JogoPrimos:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Números Primos")
        self.root.geometry("600x400")
        self.root.configure(bg="black")
        
        self.acertos = 0
        self.erros = 0
        self.ultimo_numero = 0
        self.recorde = 0
        self.recorde_jogador = ""
        self.nome_jogador = ""
        self.ultimo_primo_acertado = "Nenhum"  # Inicializa sem referência
        
        # Carregar recorde do arquivo
        self.carregar_recorde()

        # Tela inicial para inserir nome do jogador
        self.label_nome = tk.Label(root, text="Digite seu nome:", font=("Arial", 14), fg="white", bg="black")
        self.label_nome.place(relx=0.5, rely=0.3, anchor="center")
        
        self.entry_nome = tk.Entry(root, font=("Arial", 14), fg="green", bg="black", justify="center", highlightthickness=1, highlightbackground="green", insertbackground="green")
        self.entry_nome.place(relx=0.5, rely=0.4, anchor="center")
        
        self.button_iniciar = tk.Button(root, text="Iniciar Jogo", bg="green", fg="white", font=("Arial", 12, "bold"), command=self.iniciar_jogo)
        self.button_iniciar.place(relx=0.5, rely=0.5, anchor="center")
    
    def carregar_recorde(self):
        if os.path.exists("recorde.txt"):
            with open("recorde.txt", "r") as file:
                data = file.read().split(",")
                self.recorde = int(data[0])
                self.recorde_jogador = data[1]
        else:
            self.recorde = 0
            self.recorde_jogador = "Nenhum"

    def salvar_recorde(self):
        with open("recorde.txt", "w") as file:
            file.write(f"{self.recorde},{self.recorde_jogador}")
    
    def iniciar_jogo(self):
        self.nome_jogador = self.entry_nome.get().strip()
        if not self.nome_jogador:
            messagebox.showerror("Erro", "Por favor, insira um nome válido!")
            return
        
        # Limpar tela inicial
        self.label_nome.destroy()
        self.entry_nome.destroy()
        self.button_iniciar.destroy()
        
        # Interface do jogo
        self.label_acertos = tk.Label(root, text=f"Acertos: {self.acertos}", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.label_acertos.place(x=10, y=10)
        
        self.label_erros = tk.Label(root, text=f"Erros: {self.erros}", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.label_erros.place(x=500, y=10)
        
        self.label_pergunta = tk.Label(root, text="Qual número você quer verificar?", font=("Arial", 14), fg="white", bg="black")
        self.label_pergunta.place(relx=0.5, rely=0.3, anchor="center")
        
        self.frame_central = tk.Frame(root, width=300, height=200, bg="black")
        self.frame_central.place(relx=0.5, rely=0.5, anchor="center")
        
        self.entry_numero = tk.Entry(self.frame_central, font=("Arial", 14), fg="green", bg="black", justify="center", highlightthickness=1, highlightbackground="green", insertbackground="green")
        self.entry_numero.pack(pady=10)
        self.entry_numero.bind("<Return>", self.verificar_numero)
        
        self.button_sair = tk.Button(self.frame_central, text="Sair", bg="red", fg="white", font=("Arial", 12, "bold"), command=self.sair_jogo)
        self.button_sair.pack(pady=20)
        
        # Exibir recorde
        self.label_recorde = tk.Label(root, text=f"Recorde: {self.recorde} - {self.recorde_jogador}", font=("Arial", 10), fg="white", bg="black")
        self.label_recorde.place(x=10, y=370)
        
        # Exibir nome do jogador atual
        self.label_jogador = tk.Label(root, text=f"Jogador: {self.nome_jogador}", font=("Arial", 10), fg="white", bg="black")
        self.label_jogador.place(x=500, y=370)
        
        # Exibir último número primo acertado
        self.label_ultimo_primo = tk.Label(root, text=f"Último primo: {self.ultimo_primo_acertado}", font=("Arial", 12, "bold"), fg="white", bg="black")
        self.label_ultimo_primo.place(relx=0.5, rely=0.9, anchor="center")
    
    def verificar_numero(self, event=None):
        entrada = self.entry_numero.get()
        try:
            numero = int(entrada)
            if numero <= self.ultimo_numero:
                messagebox.showerror("Erro", "O número deve ser maior que o último inserido!")
                self.entry_numero.delete(0, tk.END)
                return
            
            self.ultimo_numero = numero
            
            if eh_primo(numero):
                self.ultimo_primo_acertado = numero  # Atualiza o último primo acertado
                self.label_ultimo_primo.config(text=f"Último primo: {self.ultimo_primo_acertado}")
                
                messagebox.showinfo("Resultado", "Correto! Este número é primo.")
                self.acertos += 1
                self.label_acertos.config(text=f"Acertos: {self.acertos}")
                
                # Atualizar recorde se necessário
                if self.acertos > self.recorde:
                    self.recorde = self.acertos
                    self.recorde_jogador = self.nome_jogador
                    self.label_recorde.config(text=f"Recorde: {self.recorde} - {self.recorde_jogador}")
                    self.salvar_recorde()
            else:
                messagebox.showinfo("Resultado", "Errado! Este número não é primo.")
                self.erros += 1
                self.label_erros.config(text=f"Erros: {self.erros}")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")
        
        self.entry_numero.delete(0, tk.END)
    
    def sair_jogo(self):
        self.root.destroy()

# Criar a interface
root = tk.Tk()
jogo = JogoPrimos(root)
root.mainloop()
