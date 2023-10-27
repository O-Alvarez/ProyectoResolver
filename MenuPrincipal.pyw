import pulp
from tkinter import *
import tkinter as tk

#Variacion de colores
#navy=azul marino
#white=blanco
#grey90=gris
#blue=azul

#jason modo color blanco
Modo_normal = {
    "bg": "white",
    "fg": "navy",
    "font": ("Helvetica", 12),
    "input_bg": "grey90",
}

Modo_oscuro = {
    "bg": "navy",
    "fg": "white",
    "font": ("Helvetica", 12),
    "input_bg": "white",
}

Color = Modo_normal
def cambiar_color():
    if Color == Modo_normal:
        Color = Modo_oscuro
    else:
        Color = Modo_normal

#funcion para resolver el problema
def solve_problem():
    global x, problem
    # Obtener los valores ingresados por el usuario
    cost_matrix = [[int(cost_matrix_entries[i][j].get()) for j in range(3)] for i in range(2)]
    demands = [int(demands_entries[j].get()) for j in range(3)]
    capacities = [int(capacities_entries[i].get()) for i in range(2)]

    # Crear un problema de minimización
    problem = pulp.LpProblem("Medication_Distribution", pulp.LpMinimize)

    # Variables de decisión
    x = [[pulp.LpVariable(f'x_{i}_{j}', lowBound=0, cat=pulp.LpInteger) for j in range(3)] for i in range(2)]

    # Función objetivo
    problem += pulp.lpSum(x[i][j] * cost_matrix[i][j] for i in range(2) for j in range(3)), "Costo_Total"

    # Restricciones de demanda
    for j in range(3):
        problem += pulp.lpSum(x[i][j] for i in range(2)) >= demands[j], f"Demanda_Farmacia_{j + 1}"

    # Restricciones de capacidad de almacén
    for i in range(2):
        problem += pulp.lpSum(x[i][j] for j in range(3)) <= capacities[i], f"Capacidad_Almacen_{i + 1}"

    # Resolver el problema
    problem.solve()

    # Actualizar la interfaz gráfica con los resultados
    if pulp.LpStatus[problem.status] == 'Optimal':
        for i in range(2):
            for j in range(3):
                x_entries[i][j].config(text=f"Almacén {i + 1} a Farmacia {j + 1}: {int(x[i][j].varValue)}")
        costo_label.config(text=f" Q.{pulp.value(problem.objective)}")
    else:
        for i in range(2):
            for j in range(3):
                x_entries[i][j].config(text="No es posible enviar")
        costo_label.config(text="El problema no tiene solución óptima")


# Crear la ventana principal
raiz = Tk()
raiz.title("MENU PRINCIPAL")
raiz.iconbitmap("img/Logo.ico")
# Configuración de la ventana raiz
raiz.geometry("1350x830")
raiz.config(bg="white")
raiz.update_idletasks()
width = raiz.winfo_width()
height = raiz.winfo_height()
x = (raiz.winfo_screenwidth() // 2) - (width // 2)
y = (raiz.winfo_screenheight() // 2) - (height // 2)
raiz.geometry("{}x{}+{}+{}".format(width, height, x, y))
# Creación de los frames para la ventana
# Frame para el título y el logo
frameLogo = Frame(bg="white")
frameLogo.pack(side="top", fill="x")
imgLogo = PhotoImage(file="img/LogoEmpresa.png")
imgLogo = imgLogo.subsample(3, 3)
labelLogo = Label(frameLogo, image=imgLogo)
labelLogo.configure(bg="white")
labelLogo.pack(side="left", padx=10, pady=10)
labelTitulo = Label(
    frameLogo,
    text="Distribuidora Chapín S.A.",
    font=("Helvetica", 40,"bold"),
    fg="navy",
    bg="white"
)
labelTitulo.pack(side="top", fill="x", pady=(70,0))

labelSubtitulo = Label(
    frameLogo,
    text="Minimización de costos de transporte",
    font=("Helvetica", 18,"bold"),
    fg="navy",
    bg="white",
)
labelSubtitulo.pack()
frameFormulario = Frame(bg="white")
frameFormulario.pack(fill="both", expand="True", padx=10, pady=10)

# Frame izquierdo del formulario

# Etiqueta para obtener información


# Etiquetas y campos de entrada para costos

#frame centro del formulario

# Crear etiquetas y campos de entrada para demands

# Frame derecho del formulario

    #Etiquetas e inputos para la entrada de Capacidades de almacenes

# boton para resolver el problema



# Etiqueta para mostrar el costo total

# Etiqueta para mostrar el costo mínimo


raiz.mainloop()  # Mantener la ventana en bucle

