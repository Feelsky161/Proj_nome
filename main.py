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
                    # Остальные строки — транзакции
                    for line in lines[1:]:
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
            print("3. Сохранить и выйти")
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

            elif choice == "3":
                self.save_data()
                print("Программа завершена.")
                break

            else:
                print("Ошибка: введите 1, 2 или 3.")

# Блок main
if __name__ == "__main__":
    manager = FinanceManager()
    manager.load_data()
    manager.run()
