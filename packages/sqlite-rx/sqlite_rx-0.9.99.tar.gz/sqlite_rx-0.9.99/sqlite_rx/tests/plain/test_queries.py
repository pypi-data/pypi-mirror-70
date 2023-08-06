
def test_table_creation(plain_client):
    result = plain_client.execute('CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)')
    expected_result = {"error": None, 'items': []}
    assert result == expected_result


def test_table_rows_insertion(plain_client):
    purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'XOM', 500, 53.00),
                 ]

    result = plain_client.execute('INSERT INTO stocks VALUES (?,?,?,?,?)', *purchases, execute_many=True)
    expected_result = {'error': None, 'items': [], 'row_count': 27}
    assert result == expected_result


def test_table_not_present(plain_client):
    result = plain_client.execute('SELECT * FROM IDOLS')
    assert type(result) == dict


def test_sql_script(plain_client):
    script = '''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
                CREATE TABLE accounts(id INTEGER PRIMARY KEY, description TEXT);

                INSERT INTO users(name, phone) VALUES ('John', '5557241'), 
                 ('Adam', '5547874'), ('Jack', '5484522');'''
    expected_result = {"error": None, 'items': []}
    result = plain_client.execute(script, execute_script=True)
    assert expected_result == result

