import struct
import math
import pandas as pd

class Record:
    FORMAT = "i30si20s20s20sf10sb"
    FORMAT_SIZE = struct.calcsize(FORMAT)

    def __init__(self, employee_id, employee_name, age, country, 
                 department, position, salary, joining_date):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.age = age
        self.country = country
        self.department = department
        self.position = position
        self.salary = salary
        self.joining_date = joining_date
        self.active = True 

    def pack(self):
        data = struct.pack(self.FORMAT, self.employee_id, self.employee_name.encode(), self.age,
                           self.country.encode(), self.department.encode(), self.position.encode(),
                           self.salary, self.joining_date.encode(), self.active)
        return data
    
    @staticmethod
    def unpack(data):
        employee_id, employee_name, age, country, department, position, salary, joining_date, active = struct.unpack(Record.FORMAT, data)
        return Record(employee_id, employee_name.decode(), age, country.decode(),
                      department.decode(), position.decode(), salary, joining_date.decode(), active)

class SequentialFile:
    def __init__(self, datafile, auxdata):
        self.datafile = datafile
        self.auxdata = auxdata
        self.data_sz = self._get_size(self.datafile)
        self.aux_sz = self._get_size(self.auxdata)

    def import_from_csv(self, file):
        data = pd.read_csv(file)
        for _, row in data.iterrows():
            record = Record(employee_id=row['employee_id'], employee_name=row['employee_name'],
                            age=row['age'], country=row['country'], department=row['department'],
                            position=row['position'], salary=row['salary'],
                            joining_date=row['joining_date'])
            self.insert(record)

    def _get_size(self, file):
        with open(file, 'rb') as f:
            f.seek(0, 2)
            return f.tell() // Record.FORMAT_SIZE

    def insert(self, record):
        if self.aux_sz <= math.log2(self.data_sz):
            with open(self.auxdata, 'ab') as f:
                f.write(record.pack())
            self.data_sz += 1
        else:
            aux_data = []
            with open(self.auxdata, 'rb') as f:
                while True:
                    data = f.read(Record.FORMAT_SIZE)
                    if not data:
                        break
                    aux_data.append(Record.unpack(data))
          
            with open(self.datafile, 'ab') as f:
                for record in aux_data:
                    f.write(record.pack())
            self.data_sz += len(aux_data)

            with open(self.auxdata, 'wb') as f:
                f.write(b'')

    def search(self, key):
        with open(self.datafile, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if record.employee_id == key:
                    return record
        return None

    def remover(self,key):
        with open(self.datafile, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if record.employee_id == key:
                    record.active = False

    def range_search(self, init_key, end_key):
        with open(self.datafile, 'rb') as f:
            results = []
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if init_key <= record.employee_id <= end_key:
                    results.append(record)
            return results
