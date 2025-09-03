import time
import random
import os
from P1 import SequentialFile, Record as SeqRecord

class SequentialBenchmark:
    def __init__(self):
        self.data_sizes = [100, 500, 1000, 2000, 5000, 10000]

    def generate_test_data(self, size):
        """Genera datos de prueba aleatorios"""
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
            
            record = {
                'employee_id': emp_id,
                'employee_name': f'Employee_{i:05d}',
                'age': random.randint(22, 65),
                'country': random.choice(countries),
                'department': random.choice(departments),
                'position': random.choice(positions),
                'salary': round(random.uniform(30000, 150000), 2),
                'joining_date': f'2020-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
            }
            records.append(record)
        
        return records

    def clean_files(self, files):
        """Limpia archivos de prueba"""
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def measure_sequential_operations(self, data_size):
        """Mide el rendimiento de las operaciones en archivo secuencial"""
        print(f"\n--- Sequential File con {data_size} registros ---")
        
        data = self.generate_test_data(data_size)
        datafile = f'test_data_{data_size}.dat'
        auxfile = f'test_aux_{data_size}.dat'
        
        # Limpiar archivos existentes
        self.clean_files([datafile, auxfile])
        
        # Crear archivos vacíos antes de inicializar SequentialFile
        with open(datafile, 'wb') as f:
            pass
        with open(auxfile, 'wb') as f:
            pass
        
        seq_file = SequentialFile(datafile, auxfile)
        
        # Medir inserción - ejecutar 3 veces y promediar
        insert_times = []
        for trial in range(3):
            # Limpiar y recrear archivos para cada trial
            self.clean_files([datafile, auxfile])
            with open(datafile, 'wb') as f:
                pass
            with open(auxfile, 'wb') as f:
                pass
            seq_file = SequentialFile(datafile, auxfile)
            
            start_time = time.perf_counter()
            for record_data in data:
                record = SeqRecord(
                    record_data['employee_id'],
                    record_data['employee_name'],
                    record_data['age'],
                    record_data['country'],
                    record_data['department'],
                    record_data['position'],
                    record_data['salary'],
                    record_data['joining_date']
                )
                seq_file.insert(record)
            end_time = time.perf_counter()
            insert_times.append((end_time - start_time) * 1000)
        
        avg_insert_time = sum(insert_times) / len(insert_times)
        print(f"Insercion (promedio de 3 ejecuciones): {avg_insert_time:.2f} ms")
        
        # Medir búsqueda individual - 1 registro, 5 veces promedio
        search_sample = random.choice(data)
        search_times = []
        for trial in range(5):
            start_time = time.perf_counter()
            result = seq_file.search(search_sample['employee_id'])
            end_time = time.perf_counter()
            search_times.append((end_time - start_time) * 1000)
        
        avg_search_time = sum(search_times) / len(search_times)
        print(f"Busqueda individual (promedio de 5 ejecuciones): {avg_search_time:.4f} ms")
        
        # Medir búsqueda por rango - 3 veces promedio
        ids = [record['employee_id'] for record in data]
        ids.sort()
        range_size = max(50, len(ids) // 10)
        start_idx = random.randint(0, len(ids) - range_size) if len(ids) > range_size else 0
        end_idx = min(start_idx + range_size, len(ids) - 1)
        
        range_times = []
        for trial in range(3):
            start_time = time.perf_counter()
            range_results = seq_file.range_search(ids[start_idx], ids[end_idx])
            end_time = time.perf_counter()
            range_times.append((end_time - start_time) * 1000)
        
        avg_range_time = sum(range_times) / len(range_times)
        print(f"Busqueda por rango (promedio de 3 ejecuciones): {avg_range_time:.2f} ms")
        
        # Medir eliminación - 1 registro, 5 veces promedio
        delete_sample = random.choice(data)
        delete_times = []
        for trial in range(5):
            start_time = time.perf_counter()
            seq_file.remove(delete_sample['employee_id'])
            end_time = time.perf_counter()
            delete_times.append((end_time - start_time) * 1000)
        
        avg_delete_time = sum(delete_times) / len(delete_times)
        print(f"Eliminacion (promedio de 5 ejecuciones): {avg_delete_time:.4f} ms")
        
        # Limpiar archivos
        self.clean_files([datafile, auxfile])

    def run_benchmark(self):
        """Ejecuta todas las pruebas de rendimiento para Sequential File"""
        print("="*50)
        print("BENCHMARK SEQUENTIAL FILE")
        print("="*50)
        
        for data_size in self.data_sizes:
            print(f"\n{'='*50}")
            print(f"PROBANDO CON {data_size} REGISTROS")
            print(f"{'='*50}")
            
            self.measure_sequential_operations(data_size)

def main():
    """Función principal"""
    benchmark = SequentialBenchmark()
    benchmark.run_benchmark()
    print("\nBenchmark completado!")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
