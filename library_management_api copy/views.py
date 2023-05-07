from .models import Book, Transaction, Patron
from rest_framework import generics, viewsets, views, response, mixins, status
from .serializers import BookSerializer, TransactionDetialsSerializer, TransactionCreateSerializer, PatronSerializer, PatronAndBookSerializer
from .queries.books import getBooksByTitle, getBookById, getBookRecommendation
from .queries.patrons import getPatronById, getPatrons, getPatronLastTransaction
from .queries.transactions import getTransactions, createTransaction, getTransaction, returnTypesTransaction, issueOrRenewTransaction
from .schemas import bookSchema, patronSchema, transactionSchema, transactionPostSchema, patronPostSchema, transactionUpdateSchema
from django.core.exceptions import ValidationError

class BookList(generics.ListAPIView):
    serializer_class = BookSerializer
    schema = bookSchema

    def get_queryset(self):
        filters = dict((ele, self.request.GET.get(ele)) for ele in ['title', 'authors', 'bookid'] if self.request.GET.get(ele) is not None)
        return getBooksByTitle(filters)

class PatronList(generics.ListAPIView):
    serializer_class = PatronSerializer
    schema = patronSchema

    def get_queryset(self):
        filters = dict((ele, self.request.GET.get(ele)) for ele in ['name', 'email', 'phone', 'address', 'patron_id'] if self.request.GET.get(ele) is not None)
        return getPatrons(filters)

class PatronView(generics.ListAPIView):
    serializer_class = PatronAndBookSerializer
    schema = patronSchema

    def get_queryset(self):
        return getPatronById(self.kwargs.get('pk'))

class TransactionList(generics.ListAPIView):
    serializer_class = TransactionDetialsSerializer
    schema = transactionSchema

    def get_queryset(self):
        filters = dict((ele, self.request.GET.get(ele)) for ele in ['patron_id', 'book_id', 'transaction_id'] if self.request.GET.get(ele) is not None)
        return getTransactions(filters)

    # def get(self, request):
    #     filters = dict((ele, request.GET.get(ele)) for ele in ['patron_id', 'book_id', 'transaction_id'] if request.GET.get(ele) is not None)
    #     transactions = getTransactions(filters)
    #     transactions = TransactionDetialsSerializer(transactions, many=True).data if len(transactions)>=1 else {}
    #     return response.Response(transactions)    

class TransactionUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionDetialsSerializer
    schema = transactionUpdateSchema

    def get_object(self):
        return getTransaction(self.kwargs.get('pk'))
        
    def update(self, request, *args, **kwargs):
        transaction_id = self.kwargs.get('pk')
        data = {
            'particulars': request.data.get('particulars'),
            'state': request.data.get('state')
        }
        current_transaction = TransactionDetialsSerializer(getTransaction(transaction_id)).data
        transaction = { 'error': 'BAQ REQUEST' }
        if (data['state'] == current_transaction.get('state')): 
            return response.Response({ 'messages': 'Transaction is already in {0} state'.format(data['state']) }, status=status.HTTP_200_OK)
        if (current_transaction.get('state') == 'RESERVE' and data['state'] == 'ISSUE'):
            transaction = issueOrRenewTransaction(current_transaction, data) 
        if (current_transaction.get('state') == 'ISSUE' and data['state'] == 'RENEW'):
            transaction = issueOrRenewTransaction(current_transaction, data) 
        if (current_transaction.get('state') in ['ISSUE', 'RENEW'] and data['state'] in ['RETURN', 'LOST', 'LATE_RETURN', 'DAMAGED_RETURN']):
            transaction = returnTypesTransaction(current_transaction, data) 
        return response.Response(transaction)

class TransactionCreate(views.APIView):
    serializer_class = TransactionCreateSerializer
    schema = transactionPostSchema

    def get(self, request, format=None):
        if (request.data == {}):
            return response.Response(request.data)
        filters = dict((ele, self.request.GET.get(ele)) for ele in ['patron_id', 'book_id', 'transaction_id'] if self.request.GET.get(ele) is not None)
        return getTransactions(filters)

    def post(self, request, *args, **kwargs):
        data = {
            'book_id': request.data.get('book_id'),
            'patron_id': request.data.get('patron_id'),
            'state': request.data.get('state')
        }
        if (data['state'] not in ['ISSUE', 'RESERVE']):
            return response.Response({ 'error': 'BAQ REQUEST' }, status=status.HTTP_400_BAD_REQUEST)
        available_copies = BookSerializer(getBookById(data['book_id'])).data.get('available_copies')
        if (available_copies < 1):
            return response.Response({ 'messages': 'Copies not available' }, status=status.HTTP_201_CREATED)
        existing_transaction = TransactionDetialsSerializer(getTransactions({ 'book_id': data['book_id'], 'patron_id': data['patron_id'], 'state': ['ISSUE', 'RESERVE', 'RENEW'] }))
        if(existing_transaction != None):
            response.Response({}, status=status.HTTP_201_CREATED)
        transaction = createTransaction(data)
        return response.Response(TransactionDetialsSerializer(transaction).data, status=status.HTTP_201_CREATED)
        # transaction = TransactionDetialsSerializer(transaction)
        # print(transaction)
        # return response.Response(transaction, status=status.HTTP_201_CREATED)

    # def post(self, request):
        # print(request)
        # print(self.request)
        # data = {
        #     'book_id': request.data.get('book_id'),
        #     'patron_id': request.data.get('patron_id'),
        #     'due_data': request.data.get('due_data'),
        #     'state': request.data.get('state')
        # }
        # print(data)
        # transaction = createTransaction()
        # print(transaction)

class PatronCreate(generics.CreateAPIView):
    serializer_class = PatronSerializer
    schema = patronPostSchema

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class Recommendation(generics.ListAPIView):
    serializer_class = BookSerializer
    schema = bookSchema

    def get_queryset(self):
        last_transaction = TransactionDetialsSerializer(getPatronLastTransaction(self.kwargs.get('pk'))).data
        print(last_transaction)
        return getBookRecommendation(last_transaction['book_id'])

class BookCreate(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdate(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a Book record to be updated.
    queryset = Book.objects.all()
    serializer_class = BookSerializer    

class BookDelete(generics.RetrieveDestroyAPIView):
    # API endpoint that allows a customer record to be deleted.
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# class PatronDetail(generics.RetrieveAPIView):
#     queryset = Patron.objects.all()
#     serializer_class = PatronSerializer

#     def get_object(self):
#         patron_id = self.kwargs.get('pk')
#         return getPatronById(patron_id)

# class BookDetail(generics.RetrieveAPIView):
#     serializer_class = BookSerializer
#     schema = bookSchema

#     def get_object(self):
#         bookid = self.kwargs.get('pk')
#         return getBookById(bookid)