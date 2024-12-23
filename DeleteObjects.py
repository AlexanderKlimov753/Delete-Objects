import ctypes

import maptype
import mapapi
import mapgdi
import mapsyst
import maperr
import seekapi
import rscapi
import sitapi
import maprscex

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def delete_objects(hmap: maptype.HMAP, hobj: maptype.HOBJ) -> int:

    if hmap == 0:
        return 0

    root = tk.Tk()
    root.title("Удаление объектов")

    # создание меток для диапазона объектов
    first_label = tk.Label(text="первый номер объекта: ")
    second_label = tk.Label(text="второй номер объекта: ")
    first_label.grid(row=0, column=0, sticky="w")
    second_label.grid(row=1, column=0, sticky="w")

    first_value = tk.IntVar()
    second_value = tk.IntVar()
    
    first_value.set(" ")
    second_value.set(" ")

    first_entry = tk.Entry(width=10, textvariable=first_value)
    second_entry = tk.Entry(width=10, textvariable=second_value)
    first_entry.grid(row=0, column=1, padx=5, pady=5)
    second_entry.grid(row=1, column=1, padx=5, pady=5)

    def run():
        # Создание диапазона объектов
        start_obj_num = first_value.get()
        end_obj_num = second_value.get()

        # подсчет количества удаленных объектов
        deleted_objects = 0

        # итерация по дипазону объектов
        for obj_num in range(start_obj_num, end_obj_num + 1):
            # создание нового объекта для каждой итерации 
            hobj = mapapi.mapCreateObject(hmap)
            if hobj == 0:
                messagebox.showerror("Ошибка", "Не удалось создать объект")
                continue

            # поиск объекта с текущим номером
            flag = maptype.WO_FIRST
            while seekapi.mapTotalSeekObject(hmap, hobj, flag) != 0:
                if mapapi.mapObjectNumber(hobj) == obj_num:
                    # удаление объекта
                    hsite = sitapi.mapGetObjectSiteIdent(hmap, hobj)
                    ret = sitapi.mapDeleteSiteObjectByNumber(hmap, hsite, obj_num)
                    if ret != 0:
                        deleted_objects += 1
                    break
                flag = maptype.WO_NEXT

            # освобождение объектов
            mapapi.mapFreeObject(hobj)

        # показ результата и количества удаленных объектов
        messagebox.showinfo("Результат", f"Удалено {deleted_objects} объектов")
        root.destroy()

    def close():
        root.destroy()

    # кнопки "Выполнить" и "Отменить"
    run_button = tk.Button(text="Выполнить", command=run)
    run_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")
    close_button = tk.Button(text="Отменить", command=close)
    close_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")

    # центирование окна и установка значения не изменять размер
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()

    return 0