import struct
import math
import bisect
import os
import pandas as pd

class Record:
    FORMAT = "i30si20s20s20sf10sb"
    FORMAT_SIZE = struct.calcsize(FORMAT)

    def __init__(self, employee_id, employee_name, age, country, 
                 department, position, salary, joining_date, active = True):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.age = age
        self.country = country
        self.department = department
        self.position = position
        self.salary = salary
        self.joining_date = joining_date
        self.active = active

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

    def __lt__(self, other):
        return self.employee_id < other.employee_id

class SequentialFile:
    def __init__(self, datafile, auxdata):
        self.datafile = datafile
        self.auxdata = auxdata
        self.data_sz = self._get_size(self.datafile)
        self.aux_sz = self._get_size(self.auxdata)
        if not os.path.exists(self.datafile):
            with open(self.datafile, 'wb') as f:
                f.write(b'')
        if not os.path.exists(self.auxdata):
            with open(self.auxdata, 'wb') as f:
                f.write(b'')

    def import_from_csv(self, file, sep = ','):
        data = pd.read_csv(file, sep=sep)
        data = data.sort_values(by='Employee_ID', ascending=True)
        for _, row in data.iterrows():
            record = Record(employee_id=row['Employee_ID'], employee_name=row['Employee_Name'],
                            age=row['Age'], country=row['Country'], department=row['Department'],
                            position=row['Position'], salary=row['Salary'],
                            joining_date=row['Joining_Date'])
            with open(self.datafile, 'ab') as f:
                f.write(record.pack())

    def _get_size(self, file):
        with open(file, 'rb') as f:
            f.seek(0, 2)
            return f.tell() // Record.FORMAT_SIZE

    def insert(self, record):
        if self.data_sz == 0:
            with open(self.datafile, 'ab') as f:
                f.write(record.pack())
            self.data_sz += 1
            return

        if self.data_sz > 0 and self.aux_sz <= math.log2(self.data_sz):
            with open(self.auxdata, 'ab') as f:
                f.write(record.pack())
            self.data_sz += 1
        else:
            with open(self.auxdata, 'ab') as f:
                f.write(record.pack())
            self.aux_sz += 1
            self.rebuild()

    def rebuild(self):
        aux_data = []
        with open(self.auxdata, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                if data.active:
                    aux_data.append(Record.unpack(data))

        data = []
        with open(self.datafile, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                aux_data.append(Record.unpack(data))

        for record in aux_data:
            bisect.insort(data, record)

        with open(self.datafile, 'wb') as f:
            for record in data:
                f.write(record.pack())

        self.aux_sz = 0
        self.data_sz += len(aux_data)

    def search(self, key):
        with open(self.datafile, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if record.employee_id == key:
                    return record
        
        with open(self.auxdata, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if record.employee_id == key:
                    return record
        return None

    def remove(self, key):
        with open(self.datafile, 'rb+') as f:
            while True:
                pos = f.tell()
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if record.employee_id == key and record.active:
                    record.active = False
                    f.seek(pos)
                    f.write(record.pack())
                    self.data_sz -= 1

        with open(self.auxdata, 'rb+') as f:
            while True:
                pos = f.tell()
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if record.employee_id == key and record.active:
                    record.active = False
                    f.seek(pos)
                    f.write(record.pack())
                    self.aux_sz -= 1
                    return
                record = Record.unpack(data)
                if record.employee_id == key:
                    record.active = False
                    self.aux_sz -= 1

    def range_search(self, init_key, end_key):
        results = []

        with open(self.datafile, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if init_key <= record.employee_id <= end_key and record.active:
                    results.append(record)

        with open(self.auxdata, 'rb') as f:
            while True:
                data = f.read(Record.FORMAT_SIZE)
                if not data:
                    break
                record = Record.unpack(data)
                if init_key <= record.employee_id <= end_key and record.active:
                    results.append(record)
        return results