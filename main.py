import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QSpinBox, QPushButton, QHBoxLayout
import random


class StoreInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Интерфейс магазина")
        self.resize(400, 500)  # Установка размеров окна

        # Переменные для хранения данных
        self.basket_table = None
        self.customer_intensity_morning_entry = None
        self.customer_intensity_day_entry = None
        self.customer_intensity_evening_entry = None
        self.service_speed_entry = None
        self.result_label = None

        # Создание элементов интерфейса
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Создание таблицы для корзины
        self.create_basket_table()
        layout.addWidget(self.basket_table)

        # Добавление полей ввода и кнопки
        input_layout = QVBoxLayout()

        # Утро
        morning_layout = QHBoxLayout()
        morning_label = QLabel("Кл./час утро")
        morning_label.setAlignment(Qt.AlignLeft)  # Выравнивание к левому краю
        morning_layout.addWidget(morning_label)
        self.customer_intensity_morning_entry = QSpinBox(self)
        self.customer_intensity_morning_entry.setRange(0, 999)
        self.customer_intensity_morning_entry.setValue(100)
        morning_layout.addWidget(self.customer_intensity_morning_entry)
        input_layout.addLayout(morning_layout)

        # День
        day_layout = QHBoxLayout()
        day_label = QLabel("Кл./час день")
        day_label.setAlignment(Qt.AlignLeft)  # Выравнивание к левому краю
        day_layout.addWidget(day_label)
        self.customer_intensity_day_entry = QSpinBox(self)
        self.customer_intensity_day_entry.setRange(0, 999)
        self.customer_intensity_day_entry.setValue(150)
        day_layout.addWidget(self.customer_intensity_day_entry)
        input_layout.addLayout(day_layout)

        # Вечер
        evening_layout = QHBoxLayout()
        evening_label = QLabel("Кл./час вечер")
        evening_label.setAlignment(Qt.AlignLeft)  # Выравнивание к левому краю
        evening_layout.addWidget(evening_label)
        self.customer_intensity_evening_entry = QSpinBox(self)
        self.customer_intensity_evening_entry.setRange(0, 999)
        self.customer_intensity_evening_entry.setValue(450)
        evening_layout.addWidget(self.customer_intensity_evening_entry)
        input_layout.addLayout(evening_layout)

        # Общая скорость обслуживания
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Скорость обслуживания клиентов")
        speed_label.setAlignment(Qt.AlignLeft)  # Выравнивание к левому краю
        speed_layout.addWidget(speed_label)
        self.service_speed_entry = QSpinBox(self)
        self.service_speed_entry.setRange(0, 999)
        self.service_speed_entry.setValue(60)
        speed_layout.addWidget(self.service_speed_entry)
        input_layout.addLayout(speed_layout)

        layout.addLayout(input_layout)

        calculate_button = QPushButton("Рассчитать", self)
        calculate_button.clicked.connect(self.calculate)
        layout.addWidget(calculate_button)

        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        central_widget.setLayout(layout)

    def create_basket_table(self):
        self.basket_table = QTableWidget(self)
        self.basket_table.setColumnCount(2)
        self.basket_table.setHorizontalHeaderLabels(["Товар", "Количество"])

        # Пример заполнения таблицы начальными данными
        initial_data = [("A", 0.5), ("B", 0.3), ("C", 1), ("D", 1), ("E", 0.2), ("F", 1), ("G", 1)]
        self.basket_table.setRowCount(len(initial_data))
        for row, data in enumerate(initial_data):
            self.basket_table.setItem(row, 0, QTableWidgetItem(data[0]))
            self.basket_table.setItem(row, 1, QTableWidgetItem(str(data[1])))

    def calculate(self):
        # Получение данных из полей ввода
        basket_data = [(self.basket_table.item(row, 0).text(), float(self.basket_table.item(row, 1).text()))
                       for row in range(self.basket_table.rowCount())]

        intensity_morning_data = self.customer_intensity_morning_entry.value()
        intensity_day_data = self.customer_intensity_day_entry.value()
        intensity_evening_data = self.customer_intensity_evening_entry.value()
        speed_data = self.service_speed_entry.value()

        # Пример обработки данных
        recommended_storage_volume = random.randint(1000, 2000)  # Замените на расчет по вашим формулам
        recommended_reserve = random.randint(100, 200)  # Замените на расчет по вашим формулам

        result_text = f"Рекомендуемый объем складов: {recommended_storage_volume} ед.\n"
        result_text += f"Страховой запас: {recommended_reserve} ед."

        self.result_label.setText(result_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StoreInterface()
    window.show()
    sys.exit(app.exec_())
