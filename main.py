import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, \
    QInputDialog, QDialog, QTextEdit, QMessageBox, QFormLayout


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


class IntensityInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Настройка интенсивности потока покупателей')
        self.setGeometry(200, 200, 400, 200)

        self.intensity_morning = 0
        self.error_morning = 0
        self.intensity_day = 0
        self.error_day = 0
        self.intensity_evening = 0
        self.error_evening = 0

        form_layout = QFormLayout(self)

        self.setup_intensity_input(form_layout, 'Утро (8:00 - 13:00):', 'morning')
        self.setup_intensity_input(form_layout, 'День (13:00 - 17:00):', 'day')
        self.setup_intensity_input(form_layout, 'Вечер (17:00 - 21:00):', 'evening')

        submit_button = QPushButton('Применить', self)
        submit_button.clicked.connect(self.accept)

        form_layout.addRow(submit_button)

    def setup_intensity_input(self, layout, label_text, prefix):
        intensity, ok1 = QInputDialog.getInt(self, label_text, 'Интенсивность (чел/час):', 100, 0, 999, 10)
        error, ok2 = QInputDialog.getInt(self, label_text, 'Погрешность (чел/час):', 20, 0, 999, 10)

        if ok1 and ok2:
            setattr(self, f'intensity_{prefix}', intensity)
            setattr(self, f'error_{prefix}', error)

            layout.addRow(f'{label_text}', QLabel(f'{intensity}±{error} чел/час)'))


class SpeedInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Настройка скорости обслуживания на 1 кассе')
        self.setGeometry(200, 200, 400, 200)

        self.speed_value = 60
        self.error_value = 5

        form_layout = QFormLayout(self)

        self.setup_speed_input(form_layout, 'Скорость обслуживания (чел/час):')
        self.setup_speed_input(form_layout, 'Погрешность (чел/час):')

        submit_button = QPushButton('Применить', self)
        submit_button.clicked.connect(self.accept)

        form_layout.addRow(submit_button)

    def setup_speed_input(self, layout, label_text):
        value, ok = QInputDialog.getInt(self, label_text, 'Значение:', 60, 0, 999, 10)
        if ok:
            setattr(self, f'{label_text.lower().replace(" ", "_")}_value', value)
            if 'Погрешность' in label_text:
                setattr(self, 'error_value', value)

            layout.addRow(f'{label_text}', QLabel(f'{value} чел/час)'))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ввод данных для супермаркетов')
        self.setGeometry(100, 100, 770, 620)

        self.label_basket = QLabel('Средняя потребительская корзина:')
        self.table_basket = QTableWidget(self)
        self.table_basket.setColumnCount(7)
        self.table_basket.setHorizontalHeaderLabels(['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж'])
        self.table_basket.setRowCount(12)

        # Заполняем таблицу средней покупательской способности данными по умолчанию
        self.fill_default_basket_data()

        self.label_intensity = QLabel('Интенсивность потока покупателей:')
        self.button_intensity = QPushButton('Настроить', self)
        self.button_intensity.clicked.connect(self.get_intensity)

        self.label_speed = QLabel('Скорость обслуживания на 1 кассе (чел/час):')
        self.button_speed = QPushButton('Настроить', self)
        self.button_speed.clicked.connect(self.get_speed)

        self.submit_button = QPushButton('Рассчитать', self)
        self.submit_button.clicked.connect(self.calculate_recommendations)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_basket)
        layout.addWidget(self.table_basket)
        layout.addWidget(self.label_intensity)
        layout.addWidget(self.button_intensity)
        layout.addWidget(self.label_speed)
        layout.addWidget(self.button_speed)
        layout.addWidget(self.submit_button)

        self.intensity_morning = 0
        self.error_morning = 0
        self.intensity_day = 0
        self.error_day = 0
        self.intensity_evening = 0
        self.error_evening = 0

    def fill_default_basket_data(self):
        # Заполняем таблицу средней покупательской способности данными по умолчанию
        default_data = [
            [0.5, 0.2, 1.5, 1.9, 1.4, 4.2, 1],
            [1.3, 0.9, 1.2, 3.2, 1.2, 1.2, 2],
            [4, 0.3, 1, 1, 2.1, 3.2, 1],
            [1, 1, 1.9, 0.4, 3.2, 0.4, 0.3],
            [2.1, 1.1, 3.3, 4.2, 1, 1.4, 2.3],
            [2.2, 2.2, 2.2, 2.1, 3.1, 0.4, 1.3],
            [0.4, 3.3, 1.1, 1.4, 2.5, 0.2, 0.3],
            [0.4, 0.7, 2.5, 1.3, 1.7, 1.5, 0.8],
            [0.9, 0.5, 1.5, 2.5, 1.5, 0.6, 0.2],
            [1.7, 1.7, 3.1, 0.5, 2, 0.2, 2],
            [2.7, 1.3, 1, 2.2, 3, 0.7, 1.5],
            [1.3, 2.3, 2, 2.8, 0.5, 0.9, 0.2],
        ]

        for row, data_row in enumerate(default_data):
            for col, value in enumerate(data_row):
                item = QTableWidgetItem(str(value))
                self.table_basket.setItem(row, col, item)

    def get_intensity(self):
        # Получаем интенсивность потока покупателей от пользователя
        # В данном примере используется простое диалоговое окно для ввода данных
        intensity_dialog = IntensityInputDialog()
        result = intensity_dialog.exec_()

        if result == QDialog.Accepted:
            self.intensity_morning = intensity_dialog.intensity_morning
            self.error_morning = intensity_dialog.error_morning
            self.intensity_day = intensity_dialog.intensity_day
            self.error_day = intensity_dialog.error_day
            self.intensity_evening = intensity_dialog.intensity_evening
            self.error_evening = intensity_dialog.error_evening

    def get_speed(self):
        # Получаем скорость обслуживания на одной кассе от пользователя
        speed_dialog = SpeedInputDialog()
        result = speed_dialog.exec_()

        if result == QDialog.Accepted:
            self.speed_value = speed_dialog.speed_value
            self.error_value = speed_dialog.error_value

    def calculate_recommendations(self):
        # Получаем данные о потребительской корзине
        basket_data = []
        for row in range(12):
            row_data = [self.table_basket.item(row, col).text() if self.table_basket.item(row, col) else '' for col in
                        range(7)]
            basket_data.append(row_data)

        # Получаем данные об интенсивности потока покупателей и скорости обслуживания
        intensity_data = {
            'morning': {'intensity': self.intensity_morning, 'error': self.error_morning},
            'day': {'intensity': self.intensity_day, 'error': self.error_day},
            'evening': {'intensity': self.intensity_evening, 'error': self.error_evening}
        }
        speed_data = {'speed_value': self.speed_value, 'error_value': self.error_value}

        # Проверяем, что все ячейки таблицы были заполнены
        if any('' in row for row in basket_data):
            self.show_warning('Ошибка', 'Заполните все ячейки в таблице.')
            return

        # Здесь передаем данные из интерфейса в функции расчетов
        stock_volume, optimal_stock_size = self.calculate_stock_recommendations(basket_data, intensity_data, speed_data)
        delivery_data = self.calculate_delivery_data(basket_data, intensity_data, speed_data)
        cashiers_data = self.calculate_cashiers_recommendations(basket_data, intensity_data, speed_data)

        # Вывод результатов
        result_text = f"Рекомендуемый объем складов и страховой запас: {stock_volume:.2f}, {optimal_stock_size:.2f}\n\n"
        result_text += "График и объем поставок каждого вида товаров по сети в течение двух месяцев:\n"
        result_text += self.format_delivery_data(delivery_data)
        result_text += "\n\nРекомендуемое количество касс в каждом магазине:\n"
        result_text += self.format_cashiers_data(cashiers_data)

        # Открываем новое диалоговое окно для отображения результатов
        result_dialog = ResultDialog(result_text)
        result_dialog.exec_()

    def calculate_stock_recommendations(self, basket_data, intensity_data, speed_data):
        total_demand = sum(float(cell) for row in basket_data for cell in row)

        total_intensity = (
                intensity_data['morning']['intensity'] * 5 +
                intensity_data['day']['intensity'] * 4 +
                intensity_data['evening']['intensity'] * 4
        )

        total_error_intensity = (
                intensity_data['morning']['error'] * 5 +
                intensity_data['day']['error'] * 4 +
                intensity_data['evening']['error'] * 4
        )

        total_error_speed = speed_data['error_value'] / 100  # Convert error to decimal

        adjusted_intensity = total_intensity + total_error_intensity

        stock_volume = total_demand * adjusted_intensity * (1 + total_error_speed)
        optimal_stock_size = total_demand * adjusted_intensity / 2

        return stock_volume, optimal_stock_size

    def format_delivery_data(self, delivery_data):
        formatted_data = "Вид товара \t Магазин \t\t Объем\n"

        for store_data in delivery_data:
            store_number = store_data["store_number"]
            for product_data in store_data["deliveries"]:
                product = product_data["product"]
                quantity_per_day = product_data["quantity_per_day"]
                formatted_data += f"{product} \t Магазин {store_number} \t\t {quantity_per_day:.2f}\n"

        # Convert the formatted data to a table
        table_data = [line.split('/') for line in formatted_data.strip().split('\n')]
        max_lengths = [max(len(cell.strip()) for cell in row) for row in zip(*table_data)]
        formatted_table = '\n'.join(
            '|'.join(cell.strip().ljust(length) for cell, length in zip(row, max_lengths)) for row in table_data)

        return formatted_table

    def format_cashiers_data(self, cashiers_data):
        # форматирование данных о кассирах для вывода в виде таблицы
        formatted_data = "Магазин\t\tКассиры\n"
        for data in cashiers_data:
            formatted_data += f"{data['store']}\t\t\t{data['cashiers']} касс\n"
        return formatted_data

    def calculate_delivery_data(self, basket_data, intensity_data, speed_data):
        # расчет графика и объема поставок каждого вида товаров по сети
        delivery_data = []

        for store_number, row_data in enumerate(basket_data, 1):
            store_deliveries = []
            for product, quantity_per_customer in zip(["А", "Б", "В", "Г", "Д", "Е", "Ж"], row_data):
                quantity_per_hour = float(quantity_per_customer) * (intensity_data['morning']['intensity'] +
                                                                    intensity_data['day']['intensity'] +
                                                                    intensity_data['evening']['intensity'])

                # Учитываем погрешность интенсивности
                quantity_per_hour += float(quantity_per_customer) * (intensity_data['morning']['error'] +
                                                                     intensity_data['day']['error'] +
                                                                     intensity_data['evening']['error'])

                # Учитываем время работы магазина в часах
                hours_per_day = 5 + 4 + 4  # утро - 5 часов, день - 4 часа, вечер - 4 часа
                quantity_per_day = quantity_per_hour * hours_per_day

                # Учитываем скорость обслуживания на одной кассе и ее погрешность
                quantity_per_day /= speed_data['speed_value']
                quantity_per_day += quantity_per_day * (
                        speed_data['error_value'] / 100)  # Переводим погрешность в десятичный формат

                store_deliveries.append({"product": product, "quantity_per_day": quantity_per_day})

            delivery_data.append({"store_number": store_number, "deliveries": store_deliveries})

        return delivery_data

    def calculate_cashiers_recommendations(self, basket_data, intensity_data, speed_data):
        cashiers_data = []

        for i, row_data in enumerate(basket_data, 1):
            total_quantity_per_hour = 0

            for quantity_per_customer, intensity_values in zip(row_data, intensity_data.values()):
                total_quantity_per_hour += float(quantity_per_customer) * intensity_values['intensity']
                total_quantity_per_hour += float(quantity_per_customer) * intensity_values['error']

            recommended_cashiers = total_quantity_per_hour / speed_data['speed_value']

            cashiers_data.append({"store": f"Магазин {i}", "cashiers": round(recommended_cashiers)})

        return cashiers_data

    def show_warning(self, title, message):
        # Вспомогательная функция для отображения предупреждения
        QMessageBox.warning(self, title, message)


# запуск основной программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())