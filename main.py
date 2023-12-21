import tkinter as tk
from tkinter import ttk
import random

class SupermarketSimulation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Supermarket Simulation")

        # Переменные для хранения данных о потребительской корзине
        self.basket_data = {
            'магазины 1-3': {'А': 0.5, 'Б': 0.3, 'В': 1, 'Г': 1, 'Д': 1, 'Е': 0.2, 'Ж': 1},
            'магазины 4-7': {'А': 1, 'Б': 1, 'В': 1.9, 'Г': 0.4, 'Д': 1, 'Е': 0.4, 'Ж': 0.3},
            'магазины 8-12': {'А': 0.7, 'Б': 0.7, 'В': 2.5, 'Г': 1.5, 'Д': 1, 'Е': 0.5, 'Ж': 0.8}
        }

        # Переменные для хранения данных о товарах
        self.goods_data = {
            'А': {'срок_хранения': 3, 'объем_перевозки': 1000},
            'Б': {'срок_хранения': 3, 'объем_перевозки': 800},
            'В': {'срок_хранения': 21, 'объем_перевозки': 1200},
            'Г': {'срок_хранения': 90, 'объем_перевозки': 1200},
            'Д': {'срок_хранения': 3, 'объем_перевозки': 1200},
            'Е': {'срок_хранения': 365, 'объем_перевозки': 1000},
            'Ж': {'срок_хранения': 365, 'объем_перевозки': 1000},
        }

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Количество магазинов:").grid(row=0, column=0)
        self.num_stores_entry = ttk.Entry(self.root)
        self.num_stores_entry.grid(row=0, column=1)

        # Добавление элементов для ввода данных о потребительской корзине
        ttk.Label(self.root, text="Потребительская корзина:").grid(row=1, column=0, columnspan=2)

        self.basket_frame = ttk.Frame(self.root)
        self.basket_frame.grid(row=2, column=0, columnspan=2)

        for i, store_range in enumerate(self.basket_data.keys()):
            ttk.Label(self.basket_frame, text=store_range).grid(row=i, column=0)
            for j, product in enumerate(self.basket_data[store_range].keys()):
                ttk.Label(self.basket_frame, text=product).grid(row=i, column=j + 1)
                entry_var = tk.DoubleVar()
                entry_var.set(self.basket_data[store_range][product])
                ttk.Entry(self.basket_frame, textvariable=entry_var, width=5).grid(row=i, column=j + 2)

        ttk.Button(self.root, text="Запустить моделирование", command=self.run_simulation).grid(row=3, column=0, columnspan=2)

        # Добавление элементов для вывода результатов
        self.result_text = tk.Text(self.root, height=20, width=80)
        self.result_text.grid(row=4, column=0, columnspan=2)

    def run_simulation(self):
        num_stores = int(self.num_stores_entry.get())
        customers_per_store = [random.randint(80, 120) for _ in range(num_stores)]

        # Очистка текстового поля
        self.result_text.delete(1.0, tk.END)

        # Вывод результатов в текстовое поле
        self.result_text.insert(tk.END, "Число покупателей в каждом магазине:\n")
        for i, customers in enumerate(customers_per_store, start=1):
            self.result_text.insert(tk.END, f"Магазин {i}: {customers} человек\n")

        # Логика моделирования
        self.result_text.insert(tk.END, "\nМоделирование за 2 месяца:\n")
        for month in range(1, 3):
            self.result_text.insert(tk.END, f"\nМесяц {month}:\n")
            for day in range(1, 31):
                self.result_text.insert(tk.END, f"\nДень {day}:\n")
                for hour in range(8, 22):
                    self.result_text.insert(tk.END, f"\nЧас {hour}:\n")
                    for i in range(num_stores):
                        # Логика обслуживания покупателей
                        customers_served = random.randint(50, 70)
                        self.result_text.insert(tk.END, f"Магазин {i + 1}: Обслужено {customers_served} человек\n")

                        # Логика учета товаров
                        self.calculate_goods_inventory(i, customers_served)

        # Расчет рекомендуемого объема складов, страхового запаса и других параметров
        self.calculate_recommendations()

    def calculate_goods_inventory(self, store_index, customers_served):
        store_key = f"магазины {store_index + 1}"
        if store_key in self.basket_data:
            for product, quantity_per_customer in self.basket_data[store_key].items():
                # Логика учета товаров
                required_volume = customers_served * quantity_per_customer
                current_volume = random.randint(800, 1200)
                after_delivery = current_volume + required_volume
                recommended_inventory = after_delivery + max(0, (current_volume - after_delivery) * 0.2)

                # Вывод результатов в текстовое поле
                self.result_text.insert(tk.END,
                                        f"Магазин {store_index + 1}: Товар {product}, Рекомендуемый объем склада: {recommended_inventory}\n")
        else:
            print(f"Ошибка: Не найден ключ '{store_key}' в basket_data.")

    def calculate_recommendations(self):
        total_inventory = 0
        total_insurance_stock = 0

        for product in self.goods_data.keys():
            # Расчет общего объема товаров на всех складах
            total_inventory += sum([random.randint(800, 1200) for _ in range(int(self.num_stores_entry.get()))])

            # Расчет страхового запаса (может быть адаптировано)
            total_insurance_stock += sum([random.randint(50, 100) for _ in range(int(self.num_stores_entry.get()))])

        # Вывод результатов в текстовое поле
        self.result_text.insert(tk.END, f"\nОбщий объем товаров на складах: {total_inventory}\n")
        self.result_text.insert(tk.END, f"Общий страховой запас: {total_insurance_stock}\n")

if __name__ == "__main__":
    app = SupermarketSimulation()
    app.root.mainloop()
