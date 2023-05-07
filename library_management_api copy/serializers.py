from rest_framework import serializers
from .models import Book, Transaction, Patron, Transaction_Audit, PatronAndBookDetails

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')

class TransactionDetialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['book_id', 'patron_id', 'state']

    # def create(self, validated_data):
    #     print(self)
    #     return super().create(validated_data)
        
class PatronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patron
        fields = ('__all__')

class PatronAndBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatronAndBookDetails
        fields = ('__all__')