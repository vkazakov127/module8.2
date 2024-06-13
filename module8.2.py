# -*- coding: utf-8 -*-
import sys
import zipfile


class MyDataExcept(Exception):
    def __init__(self, message, extra_data):
        self.message = message
        self.extra_data = extra_data


class MyProcExcept(Exception):
    def __init__(self, message, extra_data):
        self.message = message
        self.extra_data = extra_data


def my_exception_generator(txt_param, message1, extra_data1):
    if txt_param == 'MyDataExcept':
        raise MyDataExcept(message1, extra_data1)
    elif txt_param == 'MyProcExcept':
        raise MyProcExcept(message1, extra_data1)


def my_collection_assign(collection, index, value):
    # Тут генерируется моё исключение MyDataExcept
    try:
        collection[index] = value
    except:
        # print(sys.exception().__class__)
        # Генерируется моё исключение
        my_exception_generator('MyDataExcept',
                               "Immutable collection",
                               {"collection": collection, "index": index, "value": value})


def my_unzip(filename):
    # Тут генерируется моё исключение MyProcExcept
    try:
        zfile = zipfile.ZipFile(filename, 'r')
    except FileNotFoundError:
        # Генерируется моё исключение MyProcExcept вместо системного
        my_exception_generator('MyProcExcept', f'Файл не найден: {filename}', None)
    else:
        print('No exception')
        print(f'ZIP-файл найден: {filename}')
        zipped_file_list = []
        for filename in zfile.namelist():
            try:
                # Возможны исключения, не мои (системные)
                zfile.extract(filename)
            except:
                print(f'ErrorClass: {sys.exception().__class__}, '
                      f'Description: {sys.exception()}')
            else:
                # Если успешно распаковано, то добавляем в список распакованных файлов из архива
                zipped_file_list.append(filename)
        print(f'Распаковано: {zipped_file_list}')
        zfile.close()
        return zipped_file_list  # Всё, что удалось распаковать


def using_my_data_exception():
    # Тут обрабатывается исключение MyDataExcept, переданное по стеку из функции "my_collection_assign()"
    print('-------- Use exception: MyDataExcept -----------')
    collect01 = ["кошка", "собака", "попугай"]
    collect02 = ("Apple", "Hyundai", "Smirnoff")
    print('-------- Modify collections --------------------')
    my_collects = [collect01, collect02]
    counter = 0
    for my_collect in my_collects:
        counter += 1
        print(f'{counter}. ----------- Collection -----------')
        print(f'Collection BEFORE = {my_collect}')
        try:
            my_collection_assign(my_collect, 0, "петух")
        except MyDataExcept as exc:  # Перехватываем исключение
            print('Exception "MyDataExcept" ')
            print(f'Ошибка       : {exc.message}')
            print(f'Дополнительно: {exc.extra_data}')
        else:
            print('No exception.')
        finally:
            print(f'Collection AFTER = {my_collect}')


def using_my_proc_exception():
    # Тут обрабатывается исключение MyProcExcept, переданное по стеку из функции "my_unzip()"
    print('-------- Use exception: MyProcExcept --------')
    # Кандидаты в депутаты
    zip_file_list = ['voyna-i-mir002.zip', 'voyna-i-mir001.zip']
    for zip1 in zip_file_list:
        try:
            unzipped_list = my_unzip(zip1)
        except MyProcExcept as e:
            print('Exception "MyProcExcept"')
            print(f'{e.message}')
        else:
            print('No exception.')
            # print(f'ZIP-файл найден: {zip1}')
            # print(f'Распаковано: {unzipped_list}')
        finally:
            print('-----------------')


# ------------- MyDataExcept ---------------------------
# Тут обрабатывается исключение MyDataExcept, переданное по стеку из функции "my_collection_assign()"
using_my_data_exception()

# ------------- MyProcExcept -----------------------
# Тут обрабатывается исключение MyProcExcept, переданное по стеку из функции "my_unzip()"
using_my_proc_exception()
