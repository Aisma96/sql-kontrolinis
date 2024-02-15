import sqlite3

conn = sqlite3.connect('kontrolinis_darbas.db')
c = conn.cursor()

# with conn:
#     c.execute("CREATE TABLE FINANCES("
#               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#               "type string CHECK (type = 'income' or type = 'expenses'), amount REAL, category string)")


def enter_income():

    amount_type = 'income'
    amount = float(input('Enter amount of money: '))
    category = input('Enter income category: ')
    with conn:
        c.execute('INSERT INTO FINANCES (type, amount, category) VALUES(?,?,?)', (amount_type, amount, category))
        print(c.fetchall())
        print('Data has been inserted into FINANCES table.')


def enter_expenses():
    amount_type = 'expenses'
    amount = float(input('Enter amount of money: '))
    category = input('Enter expenses category: ')
    with conn:
        c.execute('INSERT INTO FINANCES (type, amount, category) VALUES(?,?,?)', (amount_type, amount, category))
        print(c.fetchall())
        print('Data has been inserted into FINANCES table.')


def get_balance():
    with conn:
        c.execute("SELECT SUM(amount) FROM FINANCES WHERE type='income'")
        total_income = c.fetchone()
        total_in = total_income[0]

        c.execute("SELECT SUM(amount) FROM FINANCES WHERE type='expenses'")
        total_expenses = c.fetchone()
        total_ex = total_expenses[0]

        balance = total_in - total_ex
        print('Total income: ', total_in)
        print('Total expenses: ', total_ex)
        print('Balance:', balance)


def get_all_incomes():
    with conn:
        incomes = c.execute("SELECT * FROM FINANCES WHERE type = 'income' GROUP by amount")
        for item in incomes:
            print(item)


def get_all_expenses():
    with conn:
        expenses = c.execute("SELECT * FROM FINANCES WHERE type = 'expenses' GROUP by amount")
        for item in expenses:
            print(item)


def delete_income_expense():
    amount_type = input('Enter type income/expenses: ')
    amount = input('Enter amount of money: ')
    category = input('Enter expenses category: ')

    amount_type_pattern = amount_type + '%' if amount_type else '%'
    category_pattern = category + '%' if category else '%'

    del_tuple = (amount_type_pattern, amount, category_pattern)

    del_search_query = '''
    DELETE FROM FINANCES
    WHERE
    type LIKE ?
    AND
    amount = ?
    AND
    category LIKE ?
    '''
    with conn:
        c.execute(del_search_query, del_tuple)
        print(c.fetchall())
        print('Raw has been deleted.')


def update_income_expense():
    update_amount_type = input('Update type income/expenses: ')
    update_amount = input('Update amount of money: ')
    update_category = input('Update category: ')

    amount_type = input('Enter type income/expenses: ')
    amount = input('Enter amount of money: ')
    category = input('Enter category: ')

    amount_type_pattern = amount_type + '%' if amount_type else '%'
    category_pattern = category + '%' if category else '%'

    update_tuple = (update_amount_type, update_amount, update_category, amount_type_pattern, amount, category_pattern)
    with conn:
        c.execute('UPDATE FINANCES SET type=?, amount=?, category=? '
                  'WHERE type LIKE? AND amount=? AND category LIKE ?',
                  update_tuple)
        print(c.fetchall())
        print('Raw has been updated.')


while True:
    option = int(input('1. Enter income, 2 Enter expenses, 3. Get balance, 4. Get all incomes, '
                       '5. Get all expenses, 6. Delete income/expense, 7. Update income/expense, 8. Exit: '))
    if option == 1:
        enter_income()
    elif option == 2:
        enter_expenses()
    elif option == 3:
        get_balance()
    elif option == 4:
        get_all_incomes()
    elif option == 5:
        get_all_expenses()
    elif option == 6:
        delete_income_expense()
    elif option == 7:
        update_income_expense()
    elif option == 8:
        print('Exiting program.')
        break
    else:
        print('Option must be a number between 1 to 8.')




