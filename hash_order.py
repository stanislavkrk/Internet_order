'''
До наявної програми із створення інтернет замовлення, в якій було реалізовано пошук замовлення,
додаємо можливість створення відповідних хеш-таблиць до основних полів даних:
номер замовлення, прізвище, ім'я, товар, кількість замовленого товару.
Бачимо, що пошук став набагато більш логічним:
тепер він виводить безпосередньо необхідне нам значення, а не всі елементи, де він знайшов це значення в тому числі.
Видалення замовлення працює на базі того ж самого класу, через інтерфейс абстрактного класу.
Обрав для реалізації функціоналу саме цю програму, а не бібліотеку, тому що в цьому коді набагато більш прозора логіка
і він значно зручніший для додавання функціоналу.

'''

from abc import ABC, abstractmethod

class AbstrDict(ABC):
    '''
    Абстрактний клас, інтерфейс для решти класів
    '''
    @abstractmethod
    def client_list(self) -> list:
        pass

class InputData(AbstrDict):
    '''
    В цьому класі відбувається введення користувачем даних для подальшої обробки програмою.
    Дані повертаються списком
    '''
    def client_list(self) -> list:
        cl_list = [
            input("Введіть ваше ім'я: "),
            input("Введіть ваше прізвище: "),
            input("ведіть обраний товар: "),
            input("Введіть кількість одиниці товару: "),
            input("Введіть дату вашого замовлення в форматі ДД.ММ: ")
        ]

        print("Отримані дані:", cl_list)
        return cl_list

class Client(AbstrDict):

    count = 0
    client_lists = []

    # Хеш-таблиці для кожного параметра
    name_hash = {}
    lastname_hash = {}
    item_hash = {}
    quantity_hash = {}
    date_hash = {}
    number_hash = {}

    def client_list(self) -> list:
        return Client.client_lists

    def __init__(self, list_data=AbstrDict.client_list) -> None:
        self.name = list_data[0]
        self.lastname = list_data[1]
        self.item = list_data[2]
        self.quantity = list_data[3]
        self.date = list_data[4]

        Client.count += 1
        self.number = Client.count

        # Оновлюємо хеш-таблиці
        self._add_to_hashes()

        Client.client_lists.append(self)

    def _add_to_hashes(self):
        # Додаємо поточний клієнт до всіх хеш-таблиць
        Client.name_hash.setdefault(self.name.lower(), []).append(self)
        Client.lastname_hash.setdefault(self.lastname.lower(), []).append(self)
        Client.item_hash.setdefault(self.item.lower(), []).append(self)
        Client.quantity_hash.setdefault(self.quantity, []).append(self)
        Client.date_hash.setdefault(self.date, []).append(self)
        Client.number_hash[self.number] = self  # Додаємо номер клієнта

    @classmethod
    def print_count(cls):
        print('\nНа даний момент клієнтів у базі:', cls.count)

    def __str__(self):
        return (f"Клієнт #{self.number}: {self.name} {self.lastname}, "
                f"\nТовар: {self.item}, \nКількість: {self.quantity}, \nДата: {self.date}")


class ClientDel(AbstrDict):
    '''
    В цьому класі ми відпрацьовуємо процедуру видалення замовлення, після того, як прийняли через інтерфейс
    список знайдених методом SearchClient замовлень.
    *** також, додали функціонал, який видаляє всі дані з усіх хеш-таблиць після видалення конкретного замовлення.
    '''

    def client_list(self) -> list:
        return Client.client_lists

    @classmethod
    def delete_client(cls, list_data=AbstrDict.client_list):
        confirm = input("Ви впевнені, що хочете видалити ці замовлення? (Yes/No): ")
        if confirm.lower() == 'yes':
            for client in list_data:
                # Видаляємо клієнта зі списку
                if client in Client.client_lists:
                    Client.client_lists.remove(client)
                    Client.count -= 1

                # Видаляємо клієнта з усіх хеш-таблиць
                if client.name.lower() in Client.name_hash:
                    Client.name_hash[client.name.lower()].remove(client)
                    if not Client.name_hash[client.name.lower()]:
                        del Client.name_hash[client.name.lower()]

                if client.lastname.lower() in Client.lastname_hash:
                    Client.lastname_hash[client.lastname.lower()].remove(client)
                    if not Client.lastname_hash[client.lastname.lower()]:
                        del Client.lastname_hash[client.lastname.lower()]

                if client.item.lower() in Client.item_hash:
                    Client.item_hash[client.item.lower()].remove(client)
                    if not Client.item_hash[client.item.lower()]:
                        del Client.item_hash[client.item.lower()]

                if client.quantity in Client.quantity_hash:
                    Client.quantity_hash[client.quantity].remove(client)
                    if not Client.quantity_hash[client.quantity]:
                        del Client.quantity_hash[client.quantity]

                if client.date in Client.date_hash:
                    Client.date_hash[client.date].remove(client)
                    if not Client.date_hash[client.date]:
                        del Client.date_hash[client.date]

                if client.number in Client.number_hash:
                    del Client.number_hash[client.number]

            print("Замовлення були успішно видалені.")
        else:
            print("Видалення скасовано.")

        print('Загальна кількість клієнтів у базі:', Client.count)

class SearchClient(AbstrDict):
    '''
    Додаємо клас пошуку, який створює хеш-таблиці для можливості пошуку по параметрам таким як:
    номер замовлення, ім'я, прізвище клієнта, назва товару,
    '''
    results_of_search = []
    keywords = []

    def client_list(self) -> list:
        return SearchClient.results_of_search

    def __init__(self):
        keywords_search = input("Введіть дані для пошуку: ")
        SearchClient.keywords = keywords_search.split('/')

    def search(self, list_data=AbstrDict.client_list) -> list:
        # Спочатку очищаємо результати
        SearchClient.results_of_search = []

        for keyword in SearchClient.keywords:
            keyword = keyword.strip().lower()

            # Використовуємо хеш-таблиці для пошуку
            if keyword.isdigit():  # Пошук за номером
                number = int(keyword)
                if number in Client.number_hash:
                    SearchClient.results_of_search.append(Client.number_hash[number])
            if keyword in Client.name_hash:
                SearchClient.results_of_search.extend(Client.name_hash[keyword])
            if keyword in Client.lastname_hash:
                SearchClient.results_of_search.extend(Client.lastname_hash[keyword])
            if keyword in Client.item_hash:
                SearchClient.results_of_search.extend(Client.item_hash[keyword])
            if keyword in Client.quantity_hash:
                SearchClient.results_of_search.extend(Client.quantity_hash[keyword])
            if keyword in Client.date_hash:
                SearchClient.results_of_search.extend(Client.date_hash[keyword])

        # Видаляємо дублікати (якщо кілька параметрів співпали з одним замовленням)
        SearchClient.results_of_search = list(set(SearchClient.results_of_search))

        return SearchClient.results_of_search

    def print_results(self):
        if not SearchClient.results_of_search:
            print("Клієнтів не знайдено.")
        else:
            print("\nЗнайдені клієнти: ")
            for found_client in SearchClient.results_of_search:
                print(found_client)

# ----------------------------------------------Функції-----------------------------------------------------------------

def choose_function() -> None:
    '''
    Функція, яка є інтерфейсом головного меню.

    :return: None
    '''

    print('\n1 - Створити нове інтернет замовлення'
          '\n2 - Видалити замовлення'
          '\n3 - Знайти необхідне замовлення')
    print('\nВведіть відповідну цифру'
          '\n(або напишіть No, щоб покинути програму)')
    inbuilt_commands = ("1", "2", "3", "No", "no")
    user_inputs = []
    while (keyboard_input := input()) not in inbuilt_commands:
        user_inputs.append(keyboard_input)

    match keyboard_input:
        case "1":
            add_client()
            print('\nБажаєте працювати з іншою функцією?')
            choose_function()

        case "2":
            add_del()
            print('\nБажаєте працювати з іншою функцією?')
            choose_function()

        case "3":
            searching_client()
            print('\nБажаєте працювати з іншою функцією?')
            choose_function()
        case "No", "no":
            exit(0)

def add_client() -> None:
    '''
    Функція, яка огортає роботу функціоналу створення замовлень.

    :return: None
    '''
    input_now = InputData()
    client_data = input_now.client_list()
    client_create = Client(client_data)
    client_create.print_count()
    print('Ваше замовлення: ', Client.client_lists[Client.count-1])
    print('Бажаєте створити нове замовлення? Yes/No')
    inbuilt_commands = ("Yes", "No", "yes", "no")
    user_inputs = []
    while (keyboard_input := input()) not in inbuilt_commands:
        user_inputs.append(keyboard_input)

    match keyboard_input:
        case "Yes" | "yes":
            add_client()

        case "No" | "no":
            print('\nДобре, ідемо далі.')

def searching_client() -> None:
    '''
    Функція, яка огортає роботу функціоналу пошуку замовлень.

    :return: None
    '''

    search_obj = SearchClient()
    data_list = search_obj.search(Client.client_lists)
    search_obj.print_results()
    SearchClient.results_of_search = []
    print('Бажаєте повторити пошук? Yes/No')
    inbuilt_commands = ("Yes", "No", "yes", "no")
    user_inputs = []
    while (keyboard_input := input()) not in inbuilt_commands:
        user_inputs.append(keyboard_input)

    match keyboard_input:
        case "Yes" | "yes":
            searching_client()

        case "No" | "no":
            print('\nДобре, ідемо далі.')

def add_del() -> None:
    '''
    Функція, яка огортає роботу функціоналу видалення замовлень.

    :return: None
    '''
    print('В цьому розділі ви можете знайти необхідне вам замовлення та видалити із системи.'
          '\nВи можете шукати замовлення за такими параметрами:\n'
          "\nПорядковий номер/Ім'я клієнта/Товар/Кількість товару/Дата замовлення ДД.ММ\n"
          '\nВведіть всю відому вам інформацію через знак / і ми зробимо пошук.'
          '\nВи не маєте знати всі параметри, введіть тільки ті що знаєте в довільному порядку.')
    search_del = SearchClient()
    del_list = search_del.search(Client.client_lists)
    search_del.print_results()
    if search_del.results_of_search:
        ClientDel.delete_client(del_list)
        SearchClient.results_of_search = []
    else:
        confirm = input("Повторити запит? (Yes/No): ")
        if confirm.lower() == 'yes':
            add_del()
        else:
            print("Йдемо далі")


if __name__ == "__main__":
    choose_function()









