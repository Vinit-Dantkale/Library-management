from django.db import connection
from ..models import Book

translations = {
    "bookid": "bookid",
    "title": "title",
    "authors": "authors",
    "publication_date": "publication_date",
    "publishers": "publishers" 
}

def getBooksByTitle(filters, exact = False):
    if ('bookid' in filters):
        return [p for p in Book.objects.raw('SELECT * FROM library_management_api_book WHERE bookid = %s', [filters['bookid']])]
    query = "SELECT * FROM library_management_api_book "
    params = []
    for i, (key, val) in enumerate(filters.items()):
        query = query + ("WHERE " if i == 0 else "AND ") + "LOWER(" + key + ") LIKE LOWER(%s) "
        params.append('%{val}%'.format(val=val))
    
    query = query + "LIMIT 1000"
    return Book.objects.raw(query, params, translations)

def getBookById(bookid):
    return [p for p in Book.objects.raw('SELECT * FROM library_management_api_book WHERE bookid = %s', [bookid])][0]
    # c = Book.objects.raw("SELECT * FROM library_management_api_book WHERE bookid = %d", [bookid], translations)
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM library_management_api_book WHERE bookid = 41865", [bookid])
    #     # row = cursor.fetchone()
    #     print(dictfetchone(cursor))

    # return Book.objects.raw("SELECT * FROM library_management_api_book WHERE bookid = %d", [bookid], translations)

def getBookRecommendation(book_id):
    query = "SELECT * FROM library_management_api_book WHERE subject && (SELECT subject FROM library_management_api_book WHERE bookid = %s)"
    return Book.objects.raw(query, [book_id], translations)