from django.db import models

# Create your models here.
transactionState = (
    ('RENEW', 'RENEW'),
    ('LOST', 'LOST'),
    ('LATE_RETURN', 'LATE_RETURN'),
    ('DAMAGED_RETURN', 'DAMAGED_RETURN'),
    ('ISSUE', 'ISSUE'),
    ('RETURN', 'RETURN'),
    ('RESERVE', 'RESERVE')
)

class Book(models.Model):
    bookid = models.IntegerField(primary_key=True)
    title = models.TextField()
    isbn13 = models.BigIntegerField()
    isbn = models.CharField(max_length=1000)
    authors = models.TextField()
    publisher = models.TextField()
    available_copies = models.IntegerField()
    subject = models.TextField(0)

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    patron_id = models.IntegerField()
    state = models.CharField(max_length=14, choices=transactionState)
    due_date = models.DateField()

class Transaction_Audit(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    patron_id = models.IntegerField()
    state = models.CharField(max_length=14, choices=transactionState)
    particulars = models.TextField()
    charges = models.DateField()

class Patron(models.Model):
    patron_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    email = models.TextField()
    phone = models.BigIntegerField()
    address = models.TextField()
    deposit = models.DecimalField(decimal_places=2, max_digits=5)

class PatronAndBookDetails(Patron):
    book_id = models.IntegerField()
    state = models.CharField(max_length=14, choices=transactionState)
    due_date = models.DateField()
    title = models.TextField()
    isbn13 = models.BigIntegerField()


