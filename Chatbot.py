import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot de Vendas")
        self.root.geometry("400x625")

        self.cardapio = {
            "Xis Salada": 15.00,
            "Xis Frango": 14.00,
            "Xis Calabresa": 20.00,
            "Xis Camarão": 25.00,
            "Xis Strogonoff Supreme": 27.00,
            }
        self.pedido = {}

        self.create_widgets()

    def create_widgets(self):
        # Título
        self.title_label = tk.Label(self.root, text="Chat Bot", font=("Arial", 15))
        self.title_label.pack(pady=10)

        # Exibir cardápio
        self.cardapio_frame = tk.Frame(self.root)
        self.cardapio_frame.pack(pady=10)
        
        self.cardapio_label = tk.Label(self.cardapio_frame, text="Cardápio:", font=("Arial", 12))
        self.cardapio_label.grid(row=0, column=0, columnspan=2)

        row = 1
        for item, price in self.cardapio.items():
            item_label = tk.Label(self.cardapio_frame, text=f"{item} - R$ {price:.2f}")
            item_label.grid(row=row, column=0, sticky="w")
            order_button = tk.Button(self.cardapio_frame, text="Pedir", command=lambda item=item: self.adicionar_ao_pedido(item))
            order_button.grid(row=row, column=1)
            row += 1

        # Exibir pedido
        self.pedido_frame = tk.Frame(self.root)
        self.pedido_frame.pack(pady=10)

        self.pedido_label = tk.Label(self.pedido_frame, text="Seu Pedido:", font=("Helvetica", 12))
        self.pedido_label.grid(row=0, column=0, columnspan=2)

        self.pedido_text = tk.Text(self.pedido_frame, height=10, width=40, state=tk.DISABLED)
        self.pedido_text.grid(row=1, column=0, columnspan=2)

        # Forma de pagamento
        self.pagamento_frame = tk.Frame(self.root)
        self.pagamento_frame.pack(pady=10)

        self.pagamento_label = tk.Label(self.pagamento_frame, text="Forma de Pagamento:", font=("Helvetica", 12))
        self.pagamento_label.pack()

        self.cartao_var = tk.IntVar()
        self.dinheiro_var = tk.IntVar()
        self.pix_var = tk.IntVar()
        self.vale_var = tk.IntVar()

        self.cartao_check = tk.Checkbutton(self.pagamento_frame, text="Cartão", variable=self.cartao_var)
        self.cartao_check.pack(anchor="w")
        
        self.dinheiro_check = tk.Checkbutton(self.pagamento_frame, text="Dinheiro", variable=self.dinheiro_var)
        self.dinheiro_check.pack(anchor="w")
        
        self.pix_check = tk.Checkbutton(self.pagamento_frame, text="Pix", variable=self.pix_var)
        self.pix_check.pack(anchor="w")
        
        self.vale_check = tk.Checkbutton(self.pagamento_frame, text="Vale Alimentação", variable=self.vale_var)
        self.vale_check.pack(anchor="w")

        # Botão para finalizar pedido
        self.finalizar_button = tk.Button(self.root, text="Finalizar Pedido", command=self.finalizar_pedido)
        self.finalizar_button.pack(pady=10)

    def adicionar_ao_pedido(self, item):
        if item in self.pedido:
            self.pedido[item] += 1
        else:
            self.pedido[item] = 1
        self.atualizar_pedido_text()

    def atualizar_pedido_text(self):
        self.pedido_text.config(state=tk.NORMAL)
        self.pedido_text.delete(1.0, tk.END)
        total = 0
        for item, quantidade in self.pedido.items():
            price = self.cardapio[item] * quantidade
            self.pedido_text.insert(tk.END, f"{item} x{quantidade} - R$ {price:.2f}\n")
            total += price
        self.pedido_text.insert(tk.END, f"\nTotal: R$ {total:.2f}")
        self.pedido_text.config(state=tk.DISABLED)

    def finalizar_pedido(self):
        if not self.pedido:
            messagebox.showwarning("Pedido Vazio", "Seu pedido está vazio! Por favor, adicione itens ao pedido.")
            return
        
        formas_pagamento = []
        if self.cartao_var.get():
            formas_pagamento.append("Cartão")
        if self.dinheiro_var.get():
            formas_pagamento.append("Dinheiro")
        if self.pix_var.get():
            formas_pagamento.append("Pix")
        if self.vale_var.get():
            formas_pagamento.append("Vale Alimentação")

        if formas_pagamento:
            formas_pagamento_str = ', '.join(formas_pagamento)
            total = sum(self.cardapio[item] * quantidade for item, quantidade in self.pedido.items())
            resumo_pedido = (f"Seu pedido foi finalizado!\nTotal a pagar: R$ {total:.2f}\nForma de pagamento: {formas_pagamento_str}\n\n"
                             f"Detalhes do Pedido:\n")
            for item, quantidade in self.pedido.items():
                price = self.cardapio[item] * quantidade
                resumo_pedido += f"{item} x{quantidade} - R$ {price:.2f}\n"
            
            self.gravar_em_arquivo(resumo_pedido)
            
            messagebox.showinfo("Pedido Finalizado", resumo_pedido)
            self.pedido.clear()
            self.atualizar_pedido_text()
        else:
            messagebox.showwarning("Forma de Pagamento", "Você não selecionou uma forma de pagamento.")

    def gravar_em_arquivo(self, conteudo):
        with open("resumo_pedido.txt", "w") as arquivo:
            arquivo.write(conteudo)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
