from P2 import AVL  # si tu clase está guardada en avl_file.py

# 1. Crear el árbol AVL vinculado al archivo binario
avl = AVL("employees_avl.dat")

# 2. Importar datos desde el CSV
avl.import_from_csv("employee.csv")

# 3. Buscar un registro por ID
rec = avl.search_record(1002)
print("Busqueda por ID=1002:", rec.employee_name if rec else "No encontrado")

# 4. Eliminar un registro
avl.remove_record(1003)
print("Empleado con ID=1003 eliminado")

# 5. Búsqueda por rango
res = avl.range_search_records(1000, 1010)
print("\nEmpleados en rango [1000-1010]:")
print("\nID    |Nombre        ")
print("\n-------------------------")
for r in res:
    print(r.employee_id," | ", r.employee_name)
