from ..models import Patron, Transaction
from django.db.models.expressions import RawSQL
from django.db import connection

translations = {
    "patron_id": "patron_id",
    "email": "email",
    "name": "name",
    "phone": "phone",
    "address": "address" 
}

def getPatronById1(patron_id):
    # print(Patron.objects.filter())
    # return Patron.objects.filter()
    # print(Patron.objects.raw('SELECT * FROM library_management_api_patron WHERE patron_id = %i', [id], translations))
    # return Patron.objects.raw('SELECT * FROM library_management_api_patron WHERE id = %d', [patron_id])
    Patron.objects.all()

def getPatronById(patron_id):
    return Patron.objects.raw("select * from library_management_api_book join library_management_api_transaction on book_id = bookid where patron_id = %s", [patron_id])
    # return Patron.objects.raw("SELECT * FROM library_management_api_patron NATURAL JOIN library_management_api_transaction WHERE patron_id = %s", [patron_id])
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM library_management_api_patron WHERE id = %s", [patron_id],)
    #     row = cursor.fetchone()
    # print(row)
    # return row

def getPatronLastTransaction(patron_id):
    return [p for p in Transaction.objects.raw('SELECT * FROM library_management_api_transaction WHERE patron_id = %s ORDER BY due_date DESC LIMIT 1', [patron_id])][0]

def getPatrons(filters, exact = False):
    if ('patron_id' in filters):
        return [p for p in Patron.objects.raw('SELECT * FROM library_management_api_patron WHERE patron_id = %s', [filters['patron_id']])]
    query = "SELECT * FROM library_management_api_patron "
    params = []
    for i, (key, val) in enumerate(filters.items()):
        query = query + ("WHERE " if i == 0 else "AND ") + key + (" = %s " if key == 'phone' else " LIKE %s ")
        params.append(val if key == 'phone' else '%{val}%'.format(val=val))
    
    query = query + "LIMIT 100"
    print(query, params)
    return Patron.objects.raw(query, params, translations)

# def getPatrons():
#     return Patron.objects.raw('SELECT name, email, id, address, phone FROM library_management_api_patron')