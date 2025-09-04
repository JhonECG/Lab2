import time
import random
import os
from P2 import AVL, Record

class AVL_Times:
    def __init__(self):
        self.data_sizes = [100, 500, 1000, 2000, 5000, 10000]

    def generate_test_data(self, size):
        # Generar datos de prueba aleatorios
        countries = ['USA', 'UK', 'Germany', 'France', 'Spain', 'Italy', 'Canada', 'Australia']
        departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
        positions = ['Manager', 'Developer', 'Analyst', 'Coordinator', 'Director', 'Assistant']
        
        records = []
        used_ids = set()
        
        for i in range(size):
            # Generar ID único
            emp_id = random.randint(1000, 999999)
            while emp_id in used_ids:
                emp_id = random.randint(1000, 999999)
            used_ids.add(emp_id)

            record = Record(
                emp_id,
                f'Employee_{i:05d}',
                random.randint(22, 65),
                random.choice(countries),
                random.choice(departments),
                random.choice(positions),
                round(random.uniform(30000, 150000), 2),
                f'2020-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
            )
            records.append(record)

        return records

    def clean_files(self, files):
        # Limpiar archivos de prueba
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def measure_avl_operations(self, data_size):
        # Medir el rendimiento de las operaciones en archivo secuencial
        print(f"\n--- Sequential File con {data_size} registros ---")
        
        data = self.generate_test_data(data_size)
        avl = AVL('avl_test_data.dat')


        
        # Limpiar archivos existentes
        self.clean_files([avl.datafile])

        insert_times = []
        for trial in range(3):
            avl = AVL("test_avl.dat")  # Reiniciar el árbol
            start_time = time.perf_counter()
            for record in data:
                avl.insert_record(record)
            end_time = time.perf_counter()
            insert_times.append((end_time - start_time) * 1000)

        avg_insert_time = sum(insert_times) / len(insert_times)
        print(f"Inserción (promedio de 3 ejecuciones): {avg_insert_time:.2f} ms")

        # Medir la búsqueda individual
        search_sample = random.choice(data)
        search_times = []
        for trial in range(5):
            start_time = time.perf_counter()
            result = avl.search_record(search_sample.employee_id)
            end_time = time.perf_counter()
            search_times.append((end_time - start_time) * 1000)

        avg_search_time = sum(search_times) / len(search_times)
        print(f"Búsqueda individual (promedio de 5 ejecuciones): {avg_search_time:.4f} ms")

        # Medir la búsqueda por rango
        ids = [record.employee_id for record in data]
        ids.sort()
        range_size = max(50, len(ids) // 10)
        start_idx = random.randint(0, len(ids) - range_size) if len(ids) > range_size else 0
        end_idx = min(start_idx + range_size, len(ids) - 1)

        range_times = []
        for trial in range(3):
            start_time = time.perf_counter()
            range_results = avl.range_search_records(ids[start_idx], ids[end_idx])
            end_time = time.perf_counter()
            range_times.append((end_time - start_time) * 1000)

        avg_range_time = sum(range_times) / len(range_times)
        print(f"Búsqueda por rango (promedio de 3 ejecuciones): {avg_range_time:.2f} ms")

        # Medir la eliminación
        delete_sample = random.choice(data)
        delete_times = []
        for trial in range(5):
            start_time = time.perf_counter()
            avl.remove_record(delete_sample.employee_id)
            end_time = time.perf_counter()
            delete_times.append((end_time - start_time) * 1000)

        avg_delete_time = sum(delete_times) / len(delete_times)
        print(f"Eliminación (promedio de 5 ejecuciones): {avg_delete_time:.4f} ms")


    def run_benchmark(self):
            # Ejecutar todas las pruebas de rendimiento para Sequential File
            print("="*50)
            print("AVL FILE")
            print("="*50)

            for data_size in self.data_sizes:
                print(f"\n{'='*50}")
                print(f"PROBANDO CON {data_size} REGISTROS")
                print(f"{'='*50}")

                self.measure_avl_operations(data_size)

def main():
    benchmark = AVL_Times()
    benchmark.run_benchmark()
    print("\nPruebas de tiempo completadas!")

if __name__ == "__main__":
    main()
