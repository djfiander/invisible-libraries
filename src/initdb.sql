-- Initialize the tables for the Invisible Libraries project

-- author names, ideally in the format provided
-- by the LC name authority file.
create table authors (
       id integer primary key autoincrement,
       au_name text not NULL collate nocase
);
create index authors_index on authors(au_name);

-- publisher names. This is, unfortunately, mostly a free-text
-- field since there's not a lot of control over how publisher
-- names are recorded.  We'll have to see how this works out
create table publishers (
       id integer primary key autoincrement,
       pub_name text not NULL collate nocase
);
create index publisher_index on publishers(pub_name);

-- basic citation information for each book we find
-- as well as a count of the number of copies, just in
-- case that's interesting.
create table books (
       id integer primary key autoincrement,
       work_id references works(id)
       recorded_isbn references isbns(id),
       callno text,
       author integer references authors(id),
       title text,
       publisher integer references publishers(id),
       numcopies integer,
       pubdate text, -- integer?
       oclc_id text,
       uwo_status integer references statuses(id),
       uwo_isbn references isbns(id) -- the isbn of the copy with own, if diff from recorded
);
create index books_isbn_index on books(recorded_isbn);
create index books_author_index on books(author);
create index books_title_index on books(title);
create index books_publisher_index on books(publisher);

create table works (
       id integer primary key autoincrement,
       master references books(id),
);

create table isbns (
       id integer primary key autoincrement,
       isbn text
);

-- All related ISBNs will be in the same class, which is
-- identified by the first ISBN in that class that we find
create table isbn_classes (
       master integer references(isbns(id)),
       isbn integer references(isbns(id))
);

create index isbn_class_index on isbn_classes(master);
create index isbn_isbn_index on isbn_classes(isbn);

-- Names of academic departments, to keep track of
-- which departments we find a book in
create table departments (
       id integer primary key autoincrement,
       dept_name text not NULL collate nocase
);
create index department_index on departments(dept_name);

-- Different statuses that a book can be in in the Western catalogue:
-- 	     OWN: we own this exact book (based on ISBN)
--	     OWN_RELATED: we own a related copy (different ed, maybe)
create table statuses (
       id integer primary key autoincrement,
       status text not null
);
insert into statuses (status) values ('OWN');
insert into statuses (status) values ('OWN RELATED');
insert into statuses (status) values ('UNOWNED');

create table book_callnos (
       book_id integer references books(id),
       callno text
);
create index book_callnos_index on book_callnos(book_id);

create table book_depts (
       book_id integer references books(id),
       dept_id integer references departments(id)
);
create index book_depts_index on book_depts(book_id, dept_id);
