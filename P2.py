import struct
import math
import pandas as pd

class Record:
    FORMAT = "i30si20s20s20sf10sb"
    FORMAT_SIZE = struct.calcsize(FORMAT)

    def __init__(self, employee_id, employee_name, age, country,
                 department, position, salary, joining_date, active=True):
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
        return Record(employee_id, employee_name.decode().strip('\x00'), age, country.decode().strip('\x00'),
                      department.decode().strip('\x00'), position.decode().strip('\x00'), salary, joining_date.decode().strip('\x00'), active)

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self, datafile, auxdata):
        self.auxdata = auxdata
        self.datafile = datafile
        self.root = None
        self.load_tree()

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

    def insert(self, node, val):
        if node is None:
            return Node(val)
        if node.val == val:
            return node
        if val < node.val:
            node.left = self.insert(node.left, val)
        else:
            node.right = self.insert(node.right, val)

            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            return  node

    def search(self, node, val):
        if node is None:
            return False
        if node.val == val:
            return True
        if val < node.val:
            return self.search(node.left, val)
        return self.search(node.right, val)