import coreapi
import coreschema
from rest_framework import schemas

bookSchema = schemas.AutoSchema(manual_fields=[
    coreapi.Field(
        name='title',
        location='query',
        description='Book name.'
    ),
    coreapi.Field(
        name='authors',
        location='query',
        description='Author name.'
    ),
    coreapi.Field(
        name='bookid',
        location='query',
        description='Author name.'
    )
])

patronSchema = schemas.AutoSchema(manual_fields=[
    coreapi.Field(
        name='patron_id',
        location='query',
        description='Patron ID.',
    ),
    coreapi.Field(
        name='name',
        location='query',
        description='Patron name.'
    ),
    coreapi.Field(
        name='phone',
        location='query',
        description='Patron phone.'
    ),
    coreapi.Field(
        name='email',
        location='query',
        description='Patron email.'
    ),
    coreapi.Field(
        name='address',
        location='query',
        description='Patron address.'
    )
])

patronPostSchema = schemas.AutoSchema(manual_fields=[
    coreapi.Field(
        name='name',
        location='body',
        description='Patron name.',
        required=True
    ),
    coreapi.Field(
        name='phone',
        location='body',
        description='Patron phone.',
        required=True
    ),
    coreapi.Field(
        name='email',
        location='body',
        required=True,
        description='Patron email.'
    ),
    coreapi.Field(
        name='address',
        location='body',
        required=True,
        description='Patron address.'
    ),
    coreapi.Field(
        name='deposit',
        location='body',
        required=True,
        description='Patron Deposit.'
    )
])

transactionSchema = schemas.AutoSchema(manual_fields=[
    coreapi.Field(
        name='patron_id',
        location='query',
        description='Patron ID.'
    ),
    coreapi.Field(
        name='book_id',
        location='query',
        description='Book ID.'
    ),
    coreapi.Field(
        name='transaction_id',
        location='query',
        description='Transaction ID.'
    ),
])

transactionPostSchema = schemas.AutoSchema(manual_fields=[
    coreapi.Field(
        name='patron_id',
        location='body',
        required=True,
        description='Patron ID.',
    ),
    coreapi.Field(
        name='book_id',
        location='body',
        required=True,
        description='Book ID.'
    ),
    coreapi.Field(
        name='state',
        location='body',
        required=True,
        schema=coreschema.Enum(enum=('RESERVE','ISSUE')),
        description='Transaction State.'
    )
])

transactionUpdateSchema = schemas.AutoSchema(manual_fields=[
    coreapi.Field(
        name='particulars',
        location='body',
        required=True,
        description='Patron ID.',
    ),
    coreapi.Field(
        name='state',
        location='body',
        required=True,
        schema=coreschema.Enum(enum=('LOST','RENEW','RETURN','LATE_RETURN','DAMAGED_RETURN')),
        description='Transaction State.'
    )
])
