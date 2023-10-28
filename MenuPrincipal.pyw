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
frameIzquierdo = Frame(frameFormulario, bg="blue", width=600, height=500)
frameIzquierdo.pack(side="left", fill="both", expand="True")
# Etiqueta para obtener información
labelTituloDatos = Label(frameIzquierdo, text="Costos de Distribución", font=("Helvetica", 18,"bold"), fg="white", bg="blue")
labelTituloDatos.pack(side="top", pady=(10,0))

# Etiquetas y campos de entrada para costos
cost_matrix_labels = [[None] * 3 for _ in range(2)]
cost_matrix_entries = [[None] * 3 for _ in range(2)]
for i in range(2):
    for j in range(3):
        cost_matrix_labels[i][j] = Label(frameIzquierdo, text=f"Costo Almacén {i + 1} a Farmacia {j + 1}:", font=("Helvetica", 12, "bold"), fg="white", bg="blue")
        cost_matrix_entries[i][j] = Entry(frameIzquierdo, justify="center", font=("Helvetica", 14), fg="navy", bg="grey90")
        cost_matrix_labels[i][j].pack(padx=10, pady=5)
        cost_matrix_entries[i][j].pack(padx=10, pady=5)
#frame centro del formulario
frameCentro = Frame(frameFormulario, bg="white", width=400, height=500)
frameCentro.pack(side="left", fill="both", expand="True")
labelTituloDatos = Label(frameCentro, text="Demanda de Farmacias", font=("Helvetica", 18,"bold"), fg="navy", bg="white")
labelTituloDatos.pack(side="top", pady=(10,0))
# Crear etiquetas y campos de entrada para demands
demands_labels = [tk.Label(frameCentro, text=f"Demanda Farmacia {j + 1}:", font=("Helvetica", 12, "bold"), fg="navy", bg="white") for j in range(3)]
demands_entries = [tk.Entry(frameCentro, justify="center",font=("Helvetica", 14), fg="navy", bg="grey90" ) for _ in range(3)]
for j in range(3):
    demands_labels[j].pack( padx=10, pady=5)
    demands_entries[j].pack( padx=10, pady=5)
# Frame derecho del formulario
frameDerecho = Frame(frameFormulario, bg="navy", width=400, height=500)
frameDerecho.pack(side="right", fill="both", expand="True")
labelTitulo= Label(frameCentro, text="Capacidad de Almacenes", font=("Helvetica", 18,"bold"), fg="navy", bg="white")
labelTitulo.pack(side="top", pady=(10,0))
    #Etiquetas e inputos para la entrada de Capacidades de almacenes
capacities_labels = [tk.Label(frameCentro, text=f"Capacidad Almacén {i + 1}:",font=("Helvetica", 12, "bold"), fg="navy", bg="white") for i in range(2)]
capacities_entries = [tk.Entry(frameCentro, justify="center", font=("Helvetica", 14),bg="grey90") for _ in range(2)]
for i in range(2):
    capacities_labels[i].pack( padx=10, pady=5)
    capacities_entries[i].pack( padx=10, pady=5)
# boton para resolver el problema
solve_button = tk.Button(
    frameCentro,
    text="Resolver",
    font=("Helvetica", 18, "bold"),
    fg="white",
    bg="navy",
    borderwidth=2,  # Ancho del borde
    relief="sunken",  # Estilo del borde (raised, sunken, flat, etc.)
    padx=20,  # Espacio horizontal dentro del botón
    pady=10,  # Espacio vertical dentro del botón,
    command=solve_problem
)
solve_button.pack(padx=10, pady=10)



# Etiqueta para mostrar el costo total
x_entries = [[None] * 3 for _ in range(2)]
labelResultado= Label(frameDerecho, text="Cantidad de unidades a enviar", font=("Helvetica", 18,"bold"), fg="white", bg="navy")
labelResultado.pack(padx=10, pady=10)
for i in range(2):
    for j in range(3):
        x_entries[i][j] = tk.Label(frameDerecho, text="" ,font=("Helvetica", 12, "bold"), fg="white", bg="navy")
        x_entries[i][j].pack(padx=10, pady=5)

# Etiqueta para mostrar el costo mínimo
labelcostomimino= Label(frameDerecho, text="Costo mínimo:", font=("Helvetica", 18,"bold"), fg="white", bg="navy")
labelcostomimino.pack(padx=10, pady=(30,0))
costo_label = tk.Label(frameDerecho, text="", font=("Helvetica", 16, "bold"), fg="white", bg="navy")
costo_label.pack(padx=10, pady=5)


raiz.mainloop()  # Mantener la ventana en bucle

