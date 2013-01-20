-- Initialize the tables for the Invisible Libraries project

-- author names, ideally in the format provided
-- by the LC name authority file.
create table authors (
       id integer primary key,
       au_name text not NULL collate nocase
);

-- publisher names. This is, unfortunately, mostly a free-text
-- field since there's not a lot of control over how publisher
-- names are recorded.  We'll have to see how this works out
create table publishers (
       id integer primary key,
       pub_name text not NULL collate nocase
);

-- Names of academic departments, to keep track of
-- which departments we find a book in
create table departments (
       id integer primary key,
       dept_name text not NULL collate nocase
);

-- Different statuses that a book can be in in the Western catalogue:
-- 	     OWN: we own this exact book (based on ISBN)
--	     OWN_RELATED: we own a related copy (different ed, maybe)
create table statuses (
       id integer primary key,
       status text not null
);
insert into statuses (status) values ('OWN');
insert into statuses (status) values ('OWN RELATED');
insert into statuses (status) values ('UNOWNED');

-- basic citation information for each book we find
-- as well as a count of the number of copies, just in
-- case that's interesting.
create table books (
       id integer primary key,
       recorded_isbn text,
       callno text,
       author integer references authors(id),
       title text,
       publisher integer references publishers(id),
       numcopies integer,
       pubdate text, -- integer?
       oclc_id text,
       uwo_status integer references statuses(id),
       uwo_isbn text -- the isbn of the copy with own, if diff from recorded
);

create table book_callnos (
       book_id integer references books(id),
       callno text
);

create table book_depts (
       book_id integer references books(id),
       dept_id integer references departments(id)
);

create index authors_index on authors(au_name);
create index publisher_index on publishers(pub_name);
create index department_index on departments(dept_name);

create index books_isbn_index on books(recorded_isbn);
create index books_author_index on books(author);
create index books_title_index on books(title);
create index books_publisher_index on books(publisher);

create index book_depts_index on book_depts(book_id, dept_id);
create index book_callnos_index on book_callnos(book_id)
