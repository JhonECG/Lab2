import os
from P1 import SequentialFile, Record

def test_sequential_file():
    datafile = 'test_data.bin'
    auxfile = 'test_aux.bin'
    datacsv = 'data.csv'

    # Limpiar archivos antes de empezar
    with open(datafile, 'wb') as f:
        f.write(b'')
    with open(auxfile, 'wb') as f:
        f.write(b'')

    seq = SequentialFile(datafile, auxfile)

    # Test de importación desde CSV
    print("Probando importación desde CSV...")
    seq.import_from_csv(datacsv, sep=';')
    
    # Verificar que algunos registros se importaron correctamente
    print("Verificando registros importados...")
    found = seq.search(17648)  # Primer registro del ejemplo
    assert found is not None and found.active, 'Error: No se importó correctamente el registro 17648'    
    
    # Crear registros de prueba adicionales
    r1 = Record(1, 'Alice', 30, 'Peru', 'IT', 'Dev', 1000.0, '01/01/2020')
    r2 = Record(2, 'Bob', 25, 'Chile', 'HR', 'Manager', 2000.0, '02/02/2021')
    r3 = Record(3, 'Carol', 28, 'Mexico', 'Sales', 'Salesman', 1500.0, '03/03/2022')

    # Test de inserción
    print("Probando inserción de registros...")
    seq.insert(r1)
    seq.insert(r2)
    seq.insert(r3)
    
    print("Verificando registros insertados...")
    # Test de búsqueda
    found = seq.search(1)
    assert found is not None and found.active, 'Error: No encuentra r1 o no está activo'
    found = seq.search(2)
    assert found is not None and found.active, 'Error: No encuentra r2 o no está activo'
    found = seq.search(3)
    assert found is not None and found.active, 'Error: No encuentra r3 o no está activo'
    assert seq.search(99) is None, 'Error: Encuentra un registro inexistente'

    print("Probando eliminación...")
    # Test de eliminación lógica
    seq.remove(2)
    found = seq.search(2)
    assert found is not None and not found.active, 'Error: El registro 2 no fue marcado como inactivo'
    
    print("Verificando estado después de eliminación...")
    # Test que el registro eliminado sigue existiendo pero inactivo
    found = seq.search(2)
    assert found is not None, 'Error: El registro 2 no debería ser eliminado físicamente'
    assert not found.active, 'Error: El registro 2 debería estar marcado como inactivo'

    print("Probando búsqueda por rango...")
    # Test de búsqueda por rango (solo debe devolver registros activos)
    results = seq.range_search(1, 3)
    active_ids = [r.employee_id for r in results if r.active]

    print("Verificando resultados de búsqueda por rango...")
    assert 1 in active_ids, 'Error: range_search no encuentra r1 activo'
    assert 3 in active_ids, 'Error: range_search no encuentra r3 activo'
    assert 2 not in active_ids, 'Error: range_search no debería incluir r2 inactivo'
    
    print("=" * 50)
    print('Todos los tests pasaron correctamente.')
    print("=" * 50)

if __name__ == '__main__':
    test_sequential_file()
