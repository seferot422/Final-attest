from datetime import datetime, date
from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error

class Animal:
    def __init__(self, name, birth_date, commands):
        self._name = name
        self._birth_date = self._validate_date(birth_date)
        self._commands = commands

    def _validate_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("������������ ������ ����. ����������� YYYY-MM-DD")

    def get_age(self):
        today = date.today()
        age = today.year - self._birth_date.year - ((today.month, today.day) < (self._birth_date.month, self._birth_date.day))
        return age

    def add_command(self, new_command):
        self._commands.append(new_command)

    def get_commands(self):
        return ", ".join(self._commands)

    def __str__(self):
        return f"{self.__class__.__name__}: {self._name}, �������: {self.get_age()} ���, �������: {self.get_commands()}"

# �������� ��������
class Dog(Animal):
    def __init__(self, name, birth_date, commands):
        super().__init__(name, birth_date, commands)

class Cat(Animal):
    def __init__(self, name, birth_date, commands):
        super().__init__(name, birth_date, commands)

class Hamster(Animal):
    def __init__(self, name, birth_date, commands):
        super().__init__(name, birth_date, commands)

# ������� ��������
class Horse(Animal):
    def __init__(self, name, birth_date, commands):
        super().__init__(name, birth_date, commands)

class Camel(Animal):
    def __init__(self, name, birth_date, commands):
        super().__init__(name, birth_date, commands)

class Donkey(Animal):
    def __init__(self, name, birth_date, commands):
        super().__init__(name, birth_date, commands)

class AnimalRegistry:
    def __init__(self):
        self._animals = []
        self._counter = Counter()

    def add_animal(self, animal_type, name, birth_date, commands):
        animal_classes = {
            'dog': Dog,
            'cat': Cat,
            'hamster': Hamster,
            'horse': Horse,
            'camel': Camel,
            'donkey': Donkey
        }

        if animal_type not in animal_classes:
            raise ValueError("����������� ��� ���������")

        commands_list = [cmd.strip() for cmd in commands.split(',')]
        new_animal = animal_classes[animal_type](name, birth_date, commands_list)
        self._animals.append(new_animal)
        self._counter.add()
        return new_animal

    def list_animals(self):
        return self._animals

    def find_animal(self, name):
        for animal in self._animals:
            if animal._name.lower() == name.lower():
                return animal
        return None

    def teach_animal(self, name, new_command):
        animal = self.find_animal(name)
        if animal:
            animal.add_command(new_command)
            return True
        return False

    def get_young_animals(self, min_age=1, max_age=3):
        return [animal for animal in self._animals if min_age <= animal.get_age() <= max_age]

class Counter:
    def __init__(self):
        self._count = 0
        self._is_open = False

    def add(self):
        if not self._is_open:
            raise RuntimeError("������� �� ������. ����������� with statement.")
        self._count += 1

    def __enter__(self):
        self._is_open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._is_open = False
        if exc_type is not None:
            print(f"��������� ������: {exc_val}")
        return True

    def get_count(self):
        return self._count

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.connection_config)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection.is_connected():
            self.connection.commit()
            self.connection.close()

def main_menu():
    registry = AnimalRegistry()
    
    while True:
        print("\n������ �������� ���������")
        print("1. ������� ����� ��������")
        print("2. ������ ���� ��������")
        print("3. ������� �������� ����� �������")
        print("4. ������ ������ ���������")
        print("5. ������ ������� �������� (1-3 ����)")
        print("6. �����")
        
        choice = input("�������� ��������: ")
        
        if choice == '1':
            try:
                with registry._counter:
                    print("\n��������� ���� ��������:")
                    print("dog, cat, hamster, horse, camel, donkey")
                    animal_type = input("������� ��� ���������: ").lower()
                    name = input("��� ���������: ")
                    birth_date = input("���� �������� (����-��-��): ")
                    commands = input("������� (����� �������): ")
                    
                    animal = registry.add_animal(animal_type, name, birth_date, commands)
                    print(f"\n��������� ����� ��������: {animal}")
                    print(f"����� ��������: {registry._counter.get_count()}")
            except Exception as e:
                print(f"������: {e}")
        
        elif choice == '2':
            print("\n������ ���� ��������:")
            for animal in registry.list_animals():
                print(animal)
        
        elif choice == '3':
            name = input("��� ��������� ��� ��������: ")
            command = input("����� �������: ")
            if registry.teach_animal(name, command):
                print(f"�������� {name} ������ �����: {command}")
            else:
                print("�������� �� �������")
        
        elif choice == '4':
            name = input("��� ���������: ")
            animal = registry.find_animal(name)
            if animal:
                print(f"������� ��������� {name}: {animal.get_commands()}")
            else:
                print("�������� �� �������")
        
        elif choice == '5':
            print("\n������� �������� (1-3 ����):")
            for animal in registry.get_young_animals():
                print(animal)
        
        elif choice == '6':
            print("����� �� ���������")
            break
        
        else:
            print("�������� �����, ���������� �����")

if __name__ == "__main__":
    main_menu()