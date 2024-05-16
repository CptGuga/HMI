import tkinter as tk
from PIL import ImageTk, Image
import datetime

def switch(num):
    if num == 0: return 1
    else: return 0

def change_color():
    if standby_var.get() != "":
        current_color = standby_lbl.cget("bg")
        next_color = "#F0F0F0" if current_color == "red" else "red"
        standby_lbl.config(bg=next_color)
        root.after(1000, change_color)
    else:
        standby_lbl.config(bg="#F0F0F0")


def refresh_time():
    global start_time
    global prod_num
    global delta
    global delta_bank
    global start_stop
    global modo
    x = datetime.datetime.now()
    date_var.set(x.strftime("%x"))
    time_var.set(x.strftime("%X"))
    
    if (start_stop == 1 and modo == 0):
        
        #refreshing delta
        delta = (x-start_time).total_seconds()
        
        #refreshing tax
        if delta+delta_bank != 0:
            tax_num_var.set(f'{(prod_num/(delta+delta_bank))*3600:.2f}')        
      
    root.after(1000,refresh_time)
    return

def trata_string(string):
    global prod_num
    global cars_num 
    global xyz_num
    global delta
    global delta_bank
    global start_stop
    global modo
    global start_time
    key = int(string[1])
    match string[0]:
        case 'm':
            modo_var.set(modo_strings[key])
            modo = key
            if key == 1: delta_bank += delta
            else: start_time = datetime.datetime.now()
        case 't':
            trans_var.set(trans_strings[key])
        case 's':
            semaforo_lbl.config(image=semaforo_img[key])
            start_stop = key
            if key == 0: delta_bank += delta
            else: 
                start_time = datetime.datetime.now()
                standby_var.set("")
        case 'e':
            estacao_state[key] = switch(estacao_state[key])
            estacao_lbl[key].config(image=estacao_img[estacao_state[key]])
        case 'p':
            prod_num+=1
            prod_num_var.set(str(prod_num))
            if delta + delta_bank != 0:
                tax_num_var.set(f'{(prod_num/(delta+delta_bank))*3600:.2f}')
        case 'c':
            if key == 0:
                cars_num -= 1
            else:
                cars_num += 1
            cars_num_var.set(str(cars_num))
        case 'd':
            xyz_num[key] += 1
            xyz_num_var[key].set(str(xyz_num[key]))
        case 'r':
            standby_var.set("STAND BY")
            change_color()
            prod_num = 0
            prod_num_var.set("0")
            cars_num = 0
            cars_num_var.set("0")
            delta_bank = 0
            tax_num_var.set(f'{0:.2f}')
            for i in range (3):
                xyz_num[i] = 0
                xyz_num_var[i].set("0")
                
                
            
        
    return

def get_input():
    code = input("informação: ")
    trata_string(code)
    root.after(1000*5,get_input)
    return

root = tk.Tk()
#root.geometry("1280x720")
root.resizable(0,0)
root.title("Linha de Montagem")


'''
-----------------------------------------------------------------------------
Janela de Dados
-----------------------------------------------------------------------------
'''

data_frm = tk.Frame(master=root, width=200, bg="khaki3", relief="raised", borderwidth=2)
data_frm.pack(side="left",fill="both")
data_frm.pack_propagate(False)

for i in range(9):
    data_frm.rowconfigure(i,weight=1)

# Contadores
prod_num = 0
cars_num = 0
xyz_num = [0,0,0]
delta = 0
delta_bank = 0

# 
start_stop = 0
modo = 0
trans = 0

# StringVars
prod_num_var = tk.StringVar(value="0")
cars_num_var = tk.StringVar(value="0")
tax_num_var = tk.StringVar(value="0")
xyz_num_var = []
for i in range(3):
    xyz_num_var.append(tk.StringVar(value="0"))

#Título dos Dados
data_title_frm = tk.Frame(master=data_frm,borderwidth=2, relief="raised", bg="khaki3", height=50, width = 20)
data_title_frm.grid(row=0,column=0,columnspan=2, sticky="nesw")
data_title_frm.grid_propagate(False)

data_title_lbl = tk.Label(master=data_title_frm, text="Laboratório de PIC - DEMI", bg="khaki3",font=("arial",15))
data_title_lbl.pack(fill="both", expand=True)


# Título Produção
title_prod_lbl = tk.Label(master=data_frm,text="Produção",bg="khaki3",font=("arial",10))
title_prod_lbl.grid(row=2,column=0,columnspan=2, sticky="we")

#Título Distribuição
title_dist_lbl = tk.Label(master=data_frm,text="Distribuição",bg="khaki3",font=("arial",10))
title_dist_lbl.grid(row=5,column=0,columnspan=2,sticky="we")

# Componentes Produzidos
prod_lbl = tk.Label(master=data_frm, text="Comp. Produzidos:", bg="khaki3",font=("arial",15),anchor="w")           
prod_lbl.grid(row=3,column=0,sticky="w")

prod_num_lbl = tk.Label(master=data_frm, textvariable=prod_num_var, bg="khaki3",font=("arial",15),width=6,anchor='e')
prod_num_lbl.grid(row=3,column=1)

# Carros em Trânsito
cars_lbl = tk.Label(master=data_frm, text="Componentes em Trânsito:", bg="khaki3",font=("arial",15),anchor="w")
cars_lbl.grid(row=1,column=0,sticky="w")

cars_num_lbl = tk.Label(master=data_frm, textvariable=cars_num_var, bg="khaki3",font=("arial",15),width=6,anchor='e')
cars_num_lbl.grid(row=1,column=1)

#Taxa de Produção
tax_lbl = tk.Label(master=data_frm, text="Taxa de Produção(UND/h):", bg="khaki3",font=("arial",15),anchor="w")
tax_lbl.grid(row=4,column=0,sticky="w")

tax_num_lbl = tk.Label(master=data_frm, textvariable=tax_num_var, bg="khaki3",font=("arial",15),width=6,anchor='e')
tax_num_lbl.grid(row=4,column=1)

#X Distribuídos
xdist_lbl = tk.Label(master=data_frm, text="Comp. Distribuídos E1:", bg="khaki3",font=("arial",15),anchor="w")
xdist_lbl.grid(row=6,column=0,sticky="w")

xdist_num_lbl = tk.Label(master=data_frm, textvariable=xyz_num_var[0], bg="khaki3",font=("arial",15),width=6,anchor='e')
xdist_num_lbl.grid(row=6,column=1)

#Y Distribuídos
ydist_lbl = tk.Label(master=data_frm, text="Comp. Distribuídos E2:", bg="khaki3",font=("arial",15),anchor="w")
ydist_lbl.grid(row=7,column=0,sticky="w")

ydist_num_lbl = tk.Label(master=data_frm, textvariable=xyz_num_var[1], bg="khaki3",font=("arial",15),width=6,anchor='e')
ydist_num_lbl.grid(row=7,column=1)

#Z Distribuídos
zdist_lbl = tk.Label(master=data_frm, text="Comp. Distribuídos E3:", bg="khaki3",font=("arial",15),anchor="w")
zdist_lbl.grid(row=8,column=0,sticky="w")

zdist_num_lbl = tk.Label(master=data_frm, textvariable=xyz_num_var[2], bg="khaki3",font=("arial",15),width=6,anchor='e')
zdist_num_lbl.grid(row=8,column=1)


'''
-----------------------------------------------------------------------------
Janela da Linha
-----------------------------------------------------------------------------
'''

linha_frm = tk.Frame(master = root, width=768, height=432)
linha_frm.pack(side="left")

linha_img = ImageTk.PhotoImage(Image.open("linha.png"))
linha_lbl = tk.Label(master = linha_frm, image=linha_img)
linha_lbl.pack(expand=True, fill="both")


# luzes das estações
estacao_img = [ImageTk.PhotoImage(Image.open("Unlit.png")), ImageTk.PhotoImage(Image.open("Lit.png"))]
estacao_lbl = []

for i in range(4):
    estacao_lbl.append(tk.Label(master=linha_frm, image=estacao_img[0]))
    
estacao_lbl[0].place(x=78, y=93)
estacao_lbl[1].place(x=370, y=20)
estacao_lbl[2].place(x=635, y=93)
estacao_lbl[3].place(x=370, y=330)

estacao_state = [0]*4                 # Detentor dos estados das estações

#semáforo de start/stop
semaforo_img = [ImageTk.PhotoImage(Image.open("Red.png")), ImageTk.PhotoImage(Image.open("Green.png"))]
semaforo_lbl = tk.Label(master = linha_frm , text = "On/Off", image = semaforo_img[0], compound = "bottom")
semaforo_lbl.place(anchor="center", relx=0.5, rely=0.44)

# sinal de standby
standby_var = tk.StringVar(value="STAND BY")
standby_lbl = tk.Label(master = linha_frm, textvariable=standby_var, font=("impact",40), fg="#F0F0F0")
standby_lbl.place(x=20, y=350)


'''
-----------------------------------------------------------------------------
Rodapé
-----------------------------------------------------------------------------
'''

rodape_frm = tk.Frame(master=linha_frm,height=50, bg="khaki3", relief="raised", borderwidth=2)
rodape_frm.pack(fill="both")

rodape_frm.columnconfigure(0,weight=3)
rodape_frm.columnconfigure(1,weight=3)


modo_strings = ["Modo: Produção", "Modo: Distribuição"]
modo_var = tk.StringVar(value=modo_strings[0])
modo_lbl = tk.Label(master=rodape_frm, textvariable=modo_var,font=("arial",15), bg="khaki3",width=20,anchor='w',relief="groove", borderwidth=2)
modo_lbl.grid(row=0,column=0,sticky="nesw")


trans_strings = ["Em transição: Não","Em transição: Sim"]
trans_var = tk.StringVar(value=trans_strings[0])
trans_lbl = tk.Label(master=rodape_frm, textvariable=trans_var, font=("arial",15),bg="khaki3",width=20,anchor='w',relief="groove",borderwidth=2)
trans_lbl.grid(row=0,column=1,sticky="nesw")


date_frm = tk.Frame(master=rodape_frm,bg="khaki3",relief="groove", borderwidth=2)
date_frm.grid(row=0,column=2,sticky="e")

date_var = tk.StringVar()
date_lbl = tk.Label(master=date_frm, textvariable=date_var, bg="khaki3")

time_var = tk.StringVar()
time_lbl = tk.Label(master=date_frm, textvariable=time_var, bg="khaki3")

time_lbl.pack()
date_lbl.pack()

'''
-----------------------------------------------------------------------------
Inicializar a Janela
-----------------------------------------------------------------------------
'''

root.after(0,refresh_time)
root.after(0,get_input)
root.after(0,change_color)
root.mainloop()