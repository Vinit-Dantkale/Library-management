from datetime import datetime, timedelta
from django.db import connection
from ..models import Transaction, Book
from ..serializers import BookSerializer
from .books import getBookById

translations = {
    "transaction_id": "transaction_id",
    "book_id": "book_id",
    "patron_id": "patron_id",
    "state": "state",
    "due_date": "due_date"
}

def fetchAll(cursor):
    column_names = [desc[0] for desc in cursor.description]
    return [dict(zip(column_names, row)) for row in cursor.fetchall()]

def calculateCharges(due_date, state):
    chargesMap = {
        'LATE_RETURN': 15,
        'DAMAGED_RETURN': 150,
        'LOST': 300,
        'RETURN': 0
    }
    days = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S.%f")
    days = days.days
    return chargesMap[state] * (days) if(state == 'LATE_RETURN') else chargesMap[state]

def getTransactions(filters, exact = False):
    if ('transaction_id' in filters):
        return [p for p in Transaction.objects.raw('SELECT * FROM library_management_api_transaction WHERE transaction_id = %s', [filters['transaction_id']])]
    query = "SELECT * FROM library_management_api_transaction "
    params = []
    for i, (key, val) in enumerate(filters.items()):
        query = query + ("WHERE " if i == 0 else "AND ") + key + " = %s "
        params.append(val)
    
    query = query + "LIMIT 10"
    print(query, params)
    return Transaction.objects.raw(query, params, translations)

def getTransaction(transaction_id):
    return [p for p in Transaction.objects.raw('SELECT * FROM library_management_api_transaction WHERE transaction_id = %s', [transaction_id])][0]

def getTransactionsForPatron(filters):
    return Transaction.objects.raw(
        'SELECT * FROM library_management_api_transaction NATURAL JOIN library_management_api_patron WHERE patron_id = %s AND book_id = %s AND state IN (%s)',
        [filters['patron_id'], filters['book_id'], filters['state'].join(',')])

def createTransaction(data): 
    due_after = '30 minutes' if(data['state'] == 'RESERVE') else '7 days'
    with connection.cursor() as cursor:
        cursor.execute("BEGIN")
        cursor.execute('UPDATE library_management_api_book SET available_copies = available_copies - 1  WHERE bookid = %s', [data['book_id']])
        cursor.execute(
            'INSERT INTO library_management_api_transaction (book_id, patron_id, state, due_date) VALUES (%s, %s, %s, now()::timestamp + %s::interval) RETURNING *',
            [data['book_id'], data['patron_id'], data['state'], due_after])
        row = fetchAll(cursor)
        cursor.execute("COMMIT")
        cursor.close()
        return row[0]
    
def issueOrRenewTransaction(current_transaction, data):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN")
        cursor.execute('UPDATE library_management_api_transaction SET state = %s, due_date = (now()::timestamp + %s::interval) WHERE transaction_id = %s RETURNING *', [data['state'], '7 days', current_transaction['transaction_id']])
        row = fetchAll(cursor)
        cursor.execute("COMMIT")
        cursor.close()
        return row[0]
    
def returnTypesTransaction(current_transaction, data):
    charges = calculateCharges(current_transaction['due_date'], data['state'])
    print(charges)
    with connection.cursor() as cursor:
        cursor.execute("BEGIN")
        if (data['state'] == 'RETURN'):
            cursor.execute('UPDATE library_management_api_book SET available_copies = available_copies + 1  WHERE bookid = %s', [current_transaction['book_id']])
        if (data['state'] in ['LOST','LATE_RETURN','DAMAGED_RETURN']):
            cursor.execute('UPDATE library_management_api_patron SET deposit = deposit - %s WHERE patron_id = %s', [charges, current_transaction['patron_id']])
        cursor.execute(
            'INSERT INTO library_management_api_transaction_audit(transaction_id, "Timestamp", book_id, patron_id, state, particulars, charges) VALUES (%s, now()::timestamp, %s, %s, %s, %s, %s) RETURNING *',
            [current_transaction['transaction_id'], current_transaction['book_id'], current_transaction['patron_id'], data['state'], data['particulars'], charges])
        row = fetchAll(cursor)
        cursor.execute('DELETE FROM library_management_api_transaction WHERE transaction_id = %s', [current_transaction['transaction_id']])
        print(row)
        cursor.execute("COMMIT")
        cursor.close()
        return row[0]
