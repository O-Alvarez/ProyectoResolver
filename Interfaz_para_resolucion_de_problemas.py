import pulp
import tkinter as tk

# Función para resolver el problema
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
                x_entries[i][j].config(text=f"Almacén {i + 1} -> Farmacia {j + 1}: {int(x[i][j].varValue)}")
        costo_label.config(text=f"Costo total mínimo: Q.{pulp.value(problem.objective)}")
    else:
        for i in range(2):
            for j in range(3):
                x_entries[i][j].config(text="No es posible enviar")
        costo_label.config(text="El problema no tiene solución óptima")

# Crear una ventana
window = tk.Tk()
window.title("Medication Distribution")

# Crear etiquetas y campos de entrada para cost_matrix
cost_matrix_labels = [[None] * 3 for _ in range(2)]
cost_matrix_entries = [[None] * 3 for _ in range(2)]
for i in range(2):
    for j in range(3):
        cost_matrix_labels[i][j] = tk.Label(window, text=f"Costo Almacén {i + 1} -> Farmacia {j + 1}:")
        cost_matrix_entries[i][j] = tk.Entry(window)
        cost_matrix_labels[i][j].grid(row=i, column=j, padx=10, pady=5)
        cost_matrix_entries[i][j].grid(row=i, column=j + 3, padx=10, pady=5)

# Crear etiquetas y campos de entrada para demands
demands_labels = [tk.Label(window, text=f"Demanda Farmacia {j + 1}:") for j in range(3)]
demands_entries = [tk.Entry(window) for _ in range(3)]
for j in range(3):
    demands_labels[j].grid(row=2, column=j, padx=10, pady=5)
    demands_entries[j].grid(row=2, column=j + 3, padx=10, pady=5)

# Crear etiquetas y campos de entrada para capacities
capacities_labels = [tk.Label(window, text=f"Capacidad Almacén {i + 1}:") for i in range(2)]
capacities_entries = [tk.Entry(window) for _ in range(2)]
for i in range(2):
    capacities_labels[i].grid(row=i, column=6, padx=10, pady=5)
    capacities_entries[i].grid(row=i, column=7, padx=10, pady=5)

# Botón para resolver el problema
solve_button = tk.Button(window, text="Resolver", command=solve_problem)
solve_button.grid(row=3, column=0, columnspan=8, padx=10, pady=10)

# Etiquetas para mostrar los resultados
x_entries = [[None] * 3 for _ in range(2)]
for i in range(2):
    for j in range(3):
        x_entries[i][j] = tk.Label(window, text="")
        x_entries[i][j].grid(row=i + 4, column=j, padx=10, pady=5)

# Etiqueta para mostrar el costo mínimo
costo_label = tk.Label(window, text="")
costo_label.grid(row=6, column=0, columnspan=8, padx=10, pady=5)

# Iniciar la aplicación
window.mainloop()
