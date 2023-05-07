from django.urls import re_path, path
from rest_framework.documentation import include_docs_urls
from .views import Recommendation, BookList, PatronCreate, TransactionList, PatronList, PatronView, TransactionCreate, TransactionUpdate


urlpatterns = [
    path('transactions', TransactionList.as_view()),
    path('transaction', TransactionCreate.as_view()),
    path('transaction/<int:pk>', TransactionUpdate.as_view()),
    path('books', BookList.as_view(), name='List of books'),
    path('patrons', PatronList.as_view()),
    path('patrons/<int:pk>', PatronView.as_view()),
    path('patron', PatronCreate.as_view()),
    path('recommendation/<int:pk>', Recommendation.as_view()),
    path('', include_docs_urls(title='Library Management'))
]