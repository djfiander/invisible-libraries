# Design notes for the Invisible Libraries analysis tools

## Loading data

    for each ISBN:
         if it's in the database:
             increment the counter on the existing record
         elif western owns this exact ISBN:
             add record to database
             mark status in database
         else:
             search openlibrary/oclc/whatever to find bib data
	     add record to database
             get related ISBNs from openlibrary/oclc/whatever
             for each related ISBN:
                 if Western owns it:
                     mark status in database
                     break
    # At this point the book is in the db, whether we own it
    # or not.
    record department(s) of owner in database

Books that don't have ISBNs are going to be more
challenging. There needs to be an interface that searches
openlibrary/oclc/whatever, gets the platform ID for the item,
then checks the database for that and goes through the rest of
the process that way, and this needs to be easy, so that anybody
can do it. There also needs to be a way to present the data entry
person with the results of a search of the western catalogue, so
that ownership can be manually confirmed.

Two faculty may have different editions of a work. We own one but
not the other. Factor out ISBNs and have a separate ISBN : work
mapping table?
