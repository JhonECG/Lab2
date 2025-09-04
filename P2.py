import struct
import pandas as pd

class Record:
    FORMAT = "i30si20s20s20sf10s"
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
        return struct.pack(self.FORMAT,
                           self.employee_id,
                           self.employee_name.encode().ljust(30, b'\x00'),
                           self.age,
                           self.country.encode().ljust(20, b'\x00'),
                           self.department.encode().ljust(20, b'\x00'),
                           self.position.encode().ljust(20, b'\x00'),
                           self.salary,
                           self.joining_date.encode().ljust(10, b'\x00'))

    @staticmethod
    def unpack(data):
        fields = struct.unpack(Record.FORMAT, data)
        return Record(fields[0],
                      fields[1].decode().strip('\x00'),
                      fields[2],
                      fields[3].decode().strip('\x00'),
                      fields[4].decode().strip('\x00'),
                      fields[5].decode().strip('\x00'),
                      fields[6],
                      fields[7].decode().strip('\x00'),
                      True)

class Node:
    def __init__(self, record):
        self.record = record
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self, datafile):
        self.root = None
        self.datafile = datafile

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, node, record):
        if not node:
            return Node(record)
        if record.employee_id < node.record.employee_id:
            node.left = self.insert(node.left, record)
        elif record.employee_id > node.record.employee_id:
            node.right = self.insert(node.right, record)
        else:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and record.employee_id < node.left.record.employee_id:
            return self.rotate_right(node)
        if balance < -1 and record.employee_id > node.right.record.employee_id:
            return self.rotate_left(node)
        if balance > 1 and record.employee_id > node.left.record.employee_id:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and record.employee_id < node.right.record.employee_id:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert_record(self, record):
        self.root = self.insert(self.root, record)
        with open(self.datafile, "ab") as f:
            f.write(record.pack())

    # === búsqueda ===
    def search(self, node, key):
        if not node:
            return None
        if key == node.record.employee_id:
            return node.record
        if key < node.record.employee_id:
            return self.search(node.left, key)
        return self.search(node.right, key)

    def search_record(self, key):
        return self.search(self.root, key)

    def get_min(self, node):
        while node.left:
            node = node.left
        return node

    def remove(self, node, key):
        if not node:
            return node
        if key < node.record.employee_id:
            node.left = self.remove(node.left, key)
        elif key > node.record.employee_id:
            node.right = self.remove(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self.get_min(node.right)
            node.record = temp.record
            node.right = self.remove(node.right, temp.record.employee_id)

        if not node:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def remove_record(self, key):
        self.root = self.remove(self.root, key)

    def range_search(self, node, start, end, result):
        if not node:
            return
        if start < node.record.employee_id:
            self.range_search(node.left, start, end, result)
        if start <= node.record.employee_id <= end:
            result.append(node.record)
        if end > node.record.employee_id:
            self.range_search(node.right, start, end, result)

    def range_search_records(self, start, end):
        result = []
        self.range_search(self.root, start, end, result)
        return result

    def import_from_csv(self, file):
        data = pd.read_csv(file, sep=";")
        for _, row in data.iterrows():
            record = Record(int(row['Employee_ID']),
                            row['Employee_Name'],
                            int(row['Age']),
                            row['Country'],
                            row['Department'],
                            row['Position'],
                            float(row['Salary']),
                            row['Joining_Date'])
            self.insert_record(record)


    
