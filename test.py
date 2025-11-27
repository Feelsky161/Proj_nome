import os
from datetime import datetime


def log_transactions(func):
    """Декоратор для логирования вызовов функции add_transaction."""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Лог: {func.__name__} вызвана с аргументами {args[1:]} и результатом {result}")
        return result

    return wrapper


class FinanceManager:
    def __init__(self):
        self.balance = 0.0
        self.transaction_history = []
        self.teacher_rating = None  # Новая переменная для оценки учителя
        self.filename = "transactions.txt"

    def load_data(self):
        """Загружает данные из файла при старте программы."""
        if not os.path.exists(self.filename):
            print("Файл данных не найден. Начинаем с пустого баланса.")
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    # Первая строка — баланс
                    self.balance = float(lines[0].strip().split(":")[1])

                    # Вторая строка — оценка учителя (если есть)
                    if len(lines) > 1 and lines[1].strip().startswith("rating:"):
                        self.teacher_rating = int(lines[1].strip().split(":")[1])
                        start_idx = 2
                    else:
                        start_idx = 1

                    # Остальные строки — транзакции
                    for line in lines[start_idx:]:
                        type, amount, category = line.strip().split(",")
                        self.transaction_history.append({
                            "type": type,
                            "amount": float(amount),
                            "category": category
                        })
            print("Данные успешно загружены из файла.")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}. Начинаем с пустого баланса.")

    def save_data(self):
        """Сохраняет данные в файл."""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(f"balance:{self.balance}\n")
                if self.teacher_rating is not None:
                    file.write(f"rating:{self.teacher_rating}\n")
                for transaction in self.transaction_history:
                    file.write(f"{transaction['type']},{transaction['amount']},{transaction['category']}\n")
            print("Данные успешно сохранены в файл.")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    @log_transactions
    def add_transaction(self, type, amount, category):
        """Добавляет новую транзакцию, обновляет баланс."""
        if type not in ["доход", "расход"]:
            print("Ошибка: тип операции должен быть «доход» или «расход».")
            return False

        if amount <= 0:
            print("Ошибка: сумма должна быть положительной.")
            return False

        if type == "расход" and amount > self.balance:
            print("Ошибка: недостаточно средств на балансе.")
            return False

        # Обновление баланса
        if type == "доход":
            self.balance += amount
        else:
            self.balance -= amount

        # Сохранение транзакции
        transaction = {
            "type": type,
            "amount": amount,
            "category": category
        }
        self.transaction_history.append(transaction)
        print(f"Транзакция добавлена: {transaction}")
        return True

    def set_teacher_rating(self, rating):
        """Устанавливает оценку учителя (1–12)."""
        if not isinstance(rating, int) or rating < 1 or rating > 12:
            print("Ошибка: оценка должна быть целым числом от 1 до 12.")
            return False
        self.teacher_rating = rating
        print(f"Оценка учителя установлена: {self.teacher_rating}")
        return True

    def get_teacher_rating(self):
        """Возвращает текущую оценку учителя."""
        return self.teacher_rating

    def get_transactions(self):
        """Возвращает список всех транзакций."""
        return self.transaction_history

    def get_balance(self):
        """Возвращает текущий баланс."""
        return self.balance

    def run(self):
        """Основной цикл взаимодействия с пользователем."""
        while True:
            print("\nМеню:")
            print("1. Добавить доход/расход")
            print("2. Показать баланс и транзакции")
            print("3. Установить оценку учителя (1–12)")
            print("4. Сохранить и выйти")
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                type = input("Введите тип (доход/расход): ").strip().lower()
                try:
                    amount = float(input("Введите сумму: "))
                except ValueError:
                    print("Ошибка: введите число!")
                    continue
                category = input("Введите категорию: ").strip()
                self.add_transaction(type, amount, category)

            elif choice == "2":
                print(f"\nТекущий баланс: {self.get_balance():.2f}")
                print("Список транзакций:")
                for transaction in self.get_transactions():
                    print(transaction)
                if self.get_teacher_rating() is not None:
                    print(f"Оценка учителя: {self.get_teacher_rating()}")

            elif choice == "3":
                try:
                    rating = int(input("Введите оценку учителя (1–12): "))
                    self.set_teacher_rating(rating)
                except ValueError:
                    print("Ошибка: введите целое число!")

            elif choice == "4":
                self.save_data()
                print("Программа завершена.")
                break

            else:
                print("Ошибка: введите 1, 2, 3 или 4.")


# Блок main
if __name__ == "__main__":
    manager = FinanceManager()
    manager.load_data()
    manager.run()
