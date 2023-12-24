import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, \
    QInputDialog, QDialog, QTextEdit, QMessageBox


class ResultDialog(QDialog):
    def __init__(self, result_text):
        super().__init__()

        self.result_text = result_text
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Результаты расчетов')
        self.setGeometry(200, 200, 800, 600)

        self.result_text_edit = QTextEdit(self)
        self.result_text_edit.setPlainText(self.result_text)
        self.result_text_edit.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.result_text_edit)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ввод данных для супермаркетов')
        self.setGeometry(100, 100, 600, 400)

        self.label_basket = QLabel('Средняя потребительская корзина:')
        self.table_basket = QTableWidget(self)
        self.table_basket.setColumnCount(7)  # Убираем столбец "Количество"
        self.table_basket.setHorizontalHeaderLabels(['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж'])
        self.table_basket.setRowCount(12)

        # Заполняем таблицу средней покупательской способности данными по умолчанию
        self.fill_default_basket_data()

        self.label_intensity = QLabel('Интенсивность потока покупателей:')
        self.button_intensity = QPushButton('Настроить', self)
        self.button_intensity.clicked.connect(self.get_intensity)

        self.label_speed = QLabel('Скорость обслуживания на 1 кассе (чел/мин):')
        self.speed_input, _ = QInputDialog.getDouble(self, 'Скорость обслуживания', 'Введите скорость:', 60, 0, 999, 1)

        self.submit_button = QPushButton('Рассчитать', self)
        self.submit_button.clicked.connect(self.calculate_recommendations)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_basket)
        layout.addWidget(self.table_basket)
        layout.addWidget(self.label_intensity)
        layout.addWidget(self.button_intensity)
        layout.addWidget(self.label_speed)
        layout.addWidget(self.submit_button)

        self.intensity_morning = 0
        self.intensity_day = 0
        self.intensity_evening = 0

    def fill_default_basket_data(self):
        # Заполняем таблицу средней покупательской способности данными по умолчанию
        default_data = [
            [0.5, 0.3, 1, 1, 1, 0.2, 1],
            [0.5, 0.3, 1, 1, 1, 0.2, 1],
            [0.5, 0.3, 1, 1, 1, 0.2, 1],
            [1, 1, 1.9, 0.4, 1, 0.4, 0.3],
            [1, 1, 1.9, 0.4, 1, 0.4, 0.3],
            [1, 1, 1.9, 0.4, 1, 0.4, 0.3],
            [1, 1, 1.9, 0.4, 1, 0.4, 0.3],
            [0.7, 0.7, 2.5, 1.5, 1, 0.5, 0.8],
            [0.7, 0.7, 2.5, 1.5, 1, 0.5, 0.8],
            [0.7, 0.7, 2.5, 1.5, 1, 0.5, 0.8],
            [0.7, 0.7, 2.5, 1.5, 1, 0.5, 0.8],
            [0.7, 0.7, 2.5, 1.5, 1, 0.5, 0.8],
        ]

        for row, data_row in enumerate(default_data):
            for col, value in enumerate(data_row):
                item = QTableWidgetItem(str(value))
                self.table_basket.setItem(row, col, item)

    def get_intensity(self):
        # Получаем интенсивность потока покупателей от пользователя (замените на ваш способ ввода данных)
        # В данном примере используется простое диалоговое окно для ввода данных
        morning, ok1 = QInputDialog.getInt(self, 'Интенсивность утро', 'С 8:00 до 13:00:', 100, 0, 999, 10)
        day, ok2 = QInputDialog.getInt(self, 'Интенсивность день', 'С 13:00 до 17:00:', 150, 0, 999, 10)
        evening, ok3 = QInputDialog.getInt(self, 'Интенсивность вечер', 'С 17:00 до 21:00:', 450, 0, 999, 10)

        if ok1 and ok2 and ok3:
            self.intensity_morning = morning
            self.intensity_day = day
            self.intensity_evening = evening

    def calculate_recommendations(self):
        # Получаем данные о потребительской корзине
        basket_data = []
        for row in range(12):
            row_data = [self.table_basket.item(row, col).text() if self.table_basket.item(row, col) else '' for col in
                        range(7)]
            basket_data.append(row_data)

        # Проверяем, что все ячейки таблицы были заполнены
        if any('' in row for row in basket_data):
            self.show_warning('Ошибка', 'Заполните все ячейки в таблице.')
            return

        # Здесь вы можете обработать введенные данные и выполнить расчеты
        speed_per_cashier = self.speed_input
        stock_volume, optimal_stock_size = self.calculate_stock_recommendations(basket_data, speed_per_cashier)
        delivery_data = self.calculate_delivery_data(basket_data)
        cashiers_data = self.calculate_cashiers_recommendations(basket_data)

        # Вывод результатов
        result_text = f"Рекомендуемый объем складов и страховой запас: {stock_volume:.2f}, {optimal_stock_size:.2f}\n\n"
        result_text += "График и объем поставок каждого вида товаров по сети:\n"
        result_text += self.format_delivery_data(delivery_data)
        result_text += "\n\nРекомендуемое количество касс в каждом магазине:\n"
        result_text += self.format_cashiers_data(cashiers_data)

        # Открываем новое диалоговое окно для отображения результатов
        result_dialog = ResultDialog(result_text)
        result_dialog.exec_()

    def calculate_stock_recommendations(self, basket_data, speed_per_cashier):
        # Расчет рекомендуемого объема складов и страхового запаса
        total_demand = sum(float(cell) for row in basket_data for cell in row)
        stock_volume = total_demand * speed_per_cashier
        optimal_stock_size = total_demand * speed_per_cashier / 2  # Замените на свой расчет

        return stock_volume, optimal_stock_size

    def format_delivery_data(self, delivery_data):
        # Пример форматирования данных о поставках для вывода в виде таблицы
        formatted_data = "Дата\t\tВид товара\t\tМагазин\t\tОбъем\n"
        for product_data in delivery_data:
            product = product_data["product"]
            for delivery in product_data["deliveries"]:
                formatted_data += f"{delivery['date']}\t\t{product}\t\t\t{delivery['store']}\t\t\t{delivery['quantity']} ед.\n"
        return formatted_data

    def format_cashiers_data(self, cashiers_data):
        # Пример форматирования данных о кассирах для вывода в виде таблицы
        formatted_data = "Магазин\t\tКассиры\n"
        for data in cashiers_data:
            formatted_data += f"{data['store']}\t\t\t{data['cashiers']} касс\n"
        return formatted_data

    def calculate_delivery_data(self, basket_data):
        # Пример расчета графика и объема поставок каждого вида товаров по сети
        # Здесь вы можете использовать ваши формулы и логику расчетов
        delivery_data = []

        for store_number in range(1, 13):
            store_deliveries = []
            for row, product in enumerate(["А", "Б", "В", "Г", "Д", "Е", "Ж"]):
                delivery_row = {"product": product, "deliveries": []}
                for day in range(1, 31):  # Здесь используется произвольное количество дней, замените на свою логику
                    delivery_row["deliveries"].append(
                        {"date": f"{day:02d}.01.2023", "store": f"Магазин {store_number}", "quantity": 100})
                store_deliveries.append(delivery_row)

            delivery_data.extend(store_deliveries)

        return delivery_data

    def calculate_cashiers_recommendations(self, basket_data):
        # Пример расчета рекомендуемого количества касс в каждом магазине
        # Здесь вы можете использовать ваши формулы и логику расчетов
        cashiers_data = [{"store": f"Магазин {i}", "cashiers": i * 2} for i in range(1, 13)]

        return cashiers_data

    def show_warning(self, title, message):
        # Вспомогательная функция для отображения предупреждения
        QMessageBox.warning(self, title, message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
