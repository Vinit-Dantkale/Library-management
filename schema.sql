/* BOOK */
CREATE TABLE public.library_management_api_book (
	bookid int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	title text NOT NULL,
	authors text NULL,
	average_rating float4 NULL,
	isbn varchar(255) NULL,
	isbn13 int8 NOT NULL,
	language_code varchar(255) NULL,
	num_pages int4 NULL,
	ratings_count int4 NULL,
	available_copies int4 NULL,
	publication_date varchar(255) NULL,
	publisher text NULL,
	subject _text NULL,
	CONSTRAINT library_management_api_books_pkey PRIMARY KEY (bookid)
)
PARTITION BY RANGE (bookid);

CREATE TABLE library_management_api_book_0_to_3000 (LIKE library_management_api_book INCLUDING INDEXES);
CREATE TABLE library_management_api_book_3000_to_6000 (LIKE library_management_api_book INCLUDING INDEXES);
CREATE TABLE library_management_api_book_6000_to_9000 (LIKE library_management_api_book INCLUDING INDEXES);
CREATE TABLE library_management_api_book_9000_to_12000 (LIKE library_management_api_book INCLUDING INDEXES);

ALTER TABLE library_management_api_book ATTACH PARTITION library_management_api_book_0_to_3000 FOR VALUES FROM (0) TO (3000);
ALTER TABLE library_management_api_book ATTACH PARTITION library_management_api_book_3000_to_6000 FOR VALUES FROM (3000) TO (6000);
ALTER TABLE library_management_api_book ATTACH PARTITION library_management_api_book_6000_to_9000 FOR VALUES FROM (6000) TO (9000);
ALTER TABLE library_management_api_book ATTACH PARTITION library_management_api_book_9000_to_12000 FOR VALUES FROM (9000) TO (12000);

/* PATRON */
CREATE TABLE public.library_management_api_patron (
	patron_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar(255) NOT NULL,
	email varchar(255) NULL,
	phone int8 NULL,
	address text NULL,
	deposit float4 NOT NULL,
	CONSTRAINT library_management_api_patron_pkey PRIMARY KEY (patron_id)
);

CREATE INDEX library_management_api_patron_patron_id_index ON library_management_api_patron USING btree(patron_id);
CREATE INDEX library_management_api_patron_name_index ON library_management_api_patron USING btree(name);

/* TRANSACTIONS */
CREATE TYPE transaction_states AS ENUM('RESERVE','ISSUE','LOST','LATE_RETURN','DAMAGED_RETURN','RENEW', 'RETURN');

CREATE TABLE public.library_management_api_transaction (
	transaction_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	book_id int4 NOT NULL,
	patron_id int4 NOT NULL,
	state transaction_states NOT NULL,
	due_date varchar(255) NULL,
	CONSTRAINT library_management_api_transaction_pkey PRIMARY KEY (transaction_id)
);

CREATE INDEX library_management_api_transaction_transaction_id_index ON library_management_api_transaction USING btree(transaction_id);

ALTER TABLE public.library_management_api_transaction ADD CONSTRAINT transaction_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.library_management_api_book(bookid) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE public.library_management_api_transaction ADD CONSTRAINT transaction_patron_id_fkey FOREIGN KEY (patron_id) REFERENCES public.library_management_api_patron(patron_id) ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE public.library_management_api_transaction_audit (
	transaction_id int4 NULL,
	book_id int4 NOT NULL,
	patron_id int4 NOT NULL,
	"Timestamp" varchar(50) NULL,
	state transaction_states NOT NULL,
	particulars varchar(256) NULL,
	charges float4 NULL,
	performed_by int4 NULL
);

CREATE OR REPLACE FUNCTION push_transaction_to_audit()
RETURNS TRIGGER 
AS
$BODY$
BEGIN
	INSERT INTO library_management_api_transaction_audit(transaction_id, "Timestamp", book_id, patron_id, state, particulars, charges, performed_by)
	VALUES(NEW.transaction_id, now(), NEW.book_id, NEW.patron_id, NEW.state, NULL, NULL, NULL);
	RETURN NEW;
END;
$BODY$
LANGUAGE PLPGSQL;

CREATE TRIGGER push_transaction_to_audit_trigger 
AFTER INSERT OR UPDATE ON library_management_api_transaction FOR EACH ROW EXECUTE PROCEDURE push_transaction_to_audit();
