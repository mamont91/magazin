from aiogram.dispatcher.filters.state import StatesGroup, State


class Purchase(StatesGroup):
    EnterQuantity = State()
    Approval = State()
    Payment = State()
    Name_delivery = State()
    Phone_delivery = State()
    Adress_delivery = State()


class NewItem(StatesGroup):
    Name = State()
    Photo = State()
    Price = State()
    Confirm = State()


class Mailing(StatesGroup):
    Text = State()
    Language = State()

class Test(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()

class Test2(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    # Q4 = State()    # ДОдаю состояния.
    # Q5 = State()    # ДОдаю состояния.

class Test1(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()    # ДОдаю состояния.
    Q5 = State()    # ДОдаю состояния.