# list_adapter.py
from ctypes import *
import os
from list import DoublyLinkedList  # импортируем исправленный класс из list.py


class ListBackend:
    """Базовый интерфейс для бэкендов"""
    def create(self): pass
    def insert(self, index, value): pass
    def delete(self, index): pass
    def get_count(self): pass
    def get_element(self, index): pass
    def free(self): pass


class CPPBackend(ListBackend):
    """Бэкенд для C++ библиотеки через ctypes"""
    def __init__(self, lib_path):
        self.lib = cdll.LoadLibrary(lib_path)
        self._setup_ctypes()
        self.handle = None

    def _setup_ctypes(self):
        self.lib.py_create_list.restype = c_void_p
        self.lib.py_insert_list.argtypes = [c_void_p, c_int, c_char_p]
        self.lib.py_delete_item.argtypes = [c_void_p, c_int]
        self.lib.py_get_count.argtypes = [c_void_p]
        self.lib.py_get_count.restype = c_int
        self.lib.py_get_element.argtypes = [c_void_p, c_int]
        self.lib.py_get_element.restype = c_char_p
        self.lib.py_free_list.argtypes = [c_void_p]

    def create(self):
        self.handle = self.lib.py_create_list()
        return self.handle

    def insert(self, index, value):
        self.lib.py_insert_list(self.handle, index, value.encode('utf-8'))

    def delete(self, index):
        self.lib.py_delete_item(self.handle, index)

    def get_count(self):
        return self.lib.py_get_count(self.handle)

    def get_element(self, index):
        c_str = self.lib.py_get_element(self.handle, index)
        return c_str.decode('utf-8') if c_str else None

    def free(self):
        if self.handle:
            self.lib.py_free_list(self.handle)
            self.handle = None


class PythonBackend(ListBackend):
    """Бэкенд для чистой Python-реализации"""
    def __init__(self):
        self.list_obj = None

    def create(self):
        self.list_obj = DoublyLinkedList()
        return self.list_obj

    def insert(self, index, value):
        self.list_obj.insert(index, value)

    def delete(self, index):
        self.list_obj.delete(index)

    def get_count(self):
        return self.list_obj.get_count()

    def get_element(self, index):
        return self.list_obj.get_element(index)

    def free(self):
        self.list_obj = None  # Python сам управляет памятью