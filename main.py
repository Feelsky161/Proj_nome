import os
from datetime import datetime
import colorama
from colorama import Fore, Style

# Инициализация colorama (нужно для Windows)
colorama.init()

def log_transactions(func):
    """Декоратор для логирования вызовов функции add_transaction."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{Fore.LIGHTBLUE_EX}Лог: {func.__name__} вызвана с аргументами {args[1:]} и результатом {result}{Style.RESET_ALL}")
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
            print(f"{Fore.LIGHTBLUE_EX}Файл данных не найден. Начинаем с пустого баланса.{Style.RESET_ALL}")
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
            print(f"{Fore.GREEN}Данные успешно загружены из файла.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка при загрузке данных: {e}. Начинаем с пустого баланса.{Style.RESET_ALL}")

    def save_data(self):
        """Сохраняет данные в файл."""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(f"balance:{self.balance}\n")
                if self.teacher_rating is not None:
                    file.write(f"rating:{self.teacher_rating}\n")
                for transaction in self.transaction_history:
                    file.write(f"{transaction['type']},{transaction['amount']},{transaction['category']}\n")
            print(f"{Fore.GREEN}Данные успешно сохранены в файл.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка при сохранении данных: {e}{Style.RESET_ALL}")

    @log_transactions
    def add_transaction(self, type, amount, category):
        """Добавляет новую транзакцию, обновляет баланс."""
        if type not in ["доход", "расход"]:
            print(f"{Fore.RED}Ошибка: тип операции должен быть «доход» или «расход».{Style.RESET_ALL}")
            return False

        if amount <= 0:
            print(f"{Fore.RED}Ошибка: сумма должна быть положительной.{Style.RESET_ALL}")
            return False

        if type == "расход" and amount > self.balance:
            print(f"{Fore.RED}Ошибка: недостаточно средств на балансе.{Style.RESET_ALL}")
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
        print(f"{Fore.GREEN}Транзакция добавлена: {transaction}{Style.RESET_ALL}")
        return True

    def set_teacher_rating(self, rating):
        """Устанавливает оценку учителя (1–12)."""
        if not isinstance(rating, int) or rating < 1 or rating > 12:
            print(f"{Fore.RED}Ошибка: оценка должна быть целым числом от 1 до 12.{Style.RESET_ALL}")
            return False
        self.teacher_rating = rating
        print(f"{Fore.GREEN}Оценка учителя установлена: {self.teacher_rating}{Style.RESET_ALL}")
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
            print(f"\n{Fore.BLUE}Меню:{Style.RESET_ALL}")
            print(f"{Fore.BLUE}1. Добавить доход/расход{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}2. Показать баланс и транзакции{Style.RESET_ALL}")
            print(f"{Fore.RED}3. Установить оценку учителя (1–12){Style.RESET_ALL}")
            print(f"{Fore.GREEN}4. Сохранить и выйти{Style.RESET_ALL}")
            choice = input(f"{Fore.MAGENTA}Выберите действие: {Style.RESET_ALL}").strip()

            if choice == "1":
                type = input(f"{Fore.MAGENTA}Введите тип (доход/расход): {Style.RESET_ALL}").strip().lower()
                try:
                    amount = float(input(f"{Fore.MAGENTA}Введите сумму: {Style.RESET_ALL}"))
                except ValueError:
                    print(f"{Fore.RED}Ошибка: введите число!{Style.RESET_ALL}")
                    continue
                category = input(f"{Fore.MAGENTA}Введите категорию: {Style.RESET_ALL}").strip()
                self.add_transaction(type, amount, category)

            elif choice == "2":
                print(f"\n{Fore.YELLOW}Текущий баланс: {self.get_balance():.2f}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Список транзакций:{Style.RESET_ALL}")
                for transaction in self.get_transactions():
                    print(f"  {transaction}")
                if self.get_teacher_rating() is not None:
                    print(f"{Fore.YELLOW}Оценка учителя: {self.get_teacher_rating()}{Style.RESET_ALL}")

            elif choice == "3":
                try:
                    rating = int(input(f"{Fore.MAGENTA}Введите оценку учителя (1–12): {Style.RESET_ALL}"))
                    self.set_teacher_rating(rating)
                except ValueError:
                    print(f"{Fore.RED}Ошибка: введите целое число!{Style.RESET_ALL}")

            elif choice == "4":
                self.save_data()
                print(f"{Fore.GREEN}Программа завершена.{Style.RESET_ALL}")
                break

            else:
                print(f"{Fore.RED}Ошибка: неверный выбор. Введите 1, 2, 3 или 4.{Style.RESET_ALL}")

# Блок main
if __name__ == "__main__":
    manager = FinanceManager()
    manager.load_data()
    manager.run()