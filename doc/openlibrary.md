# Open Library API notes

Because the documentation at the Open Library [developers'
site](http://openlibrary.org/developers/api) is poor, at best

## Find a book given its ISBN

This returns all the metadata about the book:

    wget -q -O - 'http://openlibrary.org/query.json?type=/type/edition&isbn_10=1551923963&*='

    [
	{
		"number_of_pages": 223,
		"covers": [771854, 771853],
		"latest_revision": 7, 
		"genres": ["Juvenile fiction."],
		"source_records": ["marc:marc_western_washington_univ/wwu_bibs.mrc_revrev.mrc:974232968:1475"],
		"title": "Harry Potter and the philosopher's stone",
		"languages": [{"key": "/languages/eng"}], 
		"subjects": [
			    "Potter, Harry (Fictitious character)", 
			    "Witches -- Juvenile fiction", 
			    "Wizards -- Juvenile fiction", 
			    "Hogwarts School of Witchcraft and Wizardry (Imaginary place) -- Juvenile fiction", 
			    "Schools -- Juvenile fiction", 
			    "England -- Juvenile fiction"
			    ], 
		"publish_country": "bcc", 
		"by_statement": "J.K. Rowling.", 
		"oclc_numbers": ["44795766"], 
		"type": {"key": "/type/edition"}, 
		"revision": 7,
		"publishers": ["Raincoast Books"], 
		"description": {
			       "type": "/type/text", 
			       "value": "Rescued from the outrageous neglect of
			       his aunt and uncle, a young boy
			       with a great destiny proves his
			       worth while attending Hogwarts
			       School for Wizards and Witches."}, 
		"last_modified": {
				 "type": "/type/datetime", 
				 "value": "2010-08-18T01:14:33.955567"}, 
		"key": "/books/OL13639000M",
		"authors": [{"key": "/authors/OL23919A"}], 
		"publish_places": ["Vancouver"], 
		"oclc_number": ["44795766"], 
		"pagination": "223p. ;", 
		"created": {
			   "type": "/type/datetime", 
			   "value": "2008-08-29T20:16:56.461491"},
		"notes": {"type": "/type/text",
			 "value": "Published in the United States
			 as \"Harry Potter and the Sorcerer's
			 Stone.\"\n\n\"Gift, January
			 2008\"\n\nSmarties Gold Award winner."}, 
		"identifiers": {
			       "goodreads": ["858352", "742576"], 
			       "librarything": ["5403381"]}, 
			       "isbn_13": ["9781551923963", "9781551923987"], 
			       "isbn_10": ["1551923963", "155192398X"], 
		"publish_date": "2000", 
		"works": [{"key":"/works/OL82592W"}]
	}
    ] 

(alternatively, use the "isbn_13" parameter). This will give us
other ISBNs for this same edition (cloth vs paper, etc), as well
as the Open Library "work" id. Use the work identifier to get
other related ISBNs (other editions, translations, etc):

    wget -q -O - 'http://openlibrary.org/query.json?type=/type/edition&works=/works/OL82592W&isbn_10=&isbn_13='

    [{"isbn_13": null, "isbn_10": null, "key": "/books/OL25421228M"},
     {"isbn_13": null, "isbn_10": ["9645757029"], "key": "/books/OL23019679M"},
     {"isbn_13": ["9785353003083"], "isbn_10": ["535300308X"], "key": "/books/OL19680813M"}, 
     {"isbn_13": ["9782070541270"], "isbn_10": ["2070541274"], "key": "/books/OL19679484M"}, 
     {"isbn_13": null, "isbn_10": ["9979865555"], "key": "/books/OL23018371M"}, 
     {"isbn_13": null, "isbn_10": ["9744723629"], "key": "/books/OL23050677M"}, 
     {"isbn_13": null, "isbn_10": ["8983920688", "8983920696", "898392067X"], "key": "/books/OL23038810M"}, 
     {"isbn_13": null, "isbn_10": ["9757501956"], "key": "/books/OL19220977M"},
     {"isbn_13": null, "isbn_10": ["9654487659"], "key": "/books/OL23049290M"}, 
     {"isbn_13": null, "isbn_10": ["7020033431"], "key": "/books/OL23017268M"}, 
     {"isbn_13": null, "isbn_10": ["0798140232"], "key": "/books/OL23032819M"}, 
     {"isbn_13": null, "isbn_10": ["158234826X", "0747568979"], "key": "/books/OL23059913M"}, 
     {"isbn_13": null, "isbn_10": null, "key": "/books/OL23096517M"}, 
     {"isbn_13": null, "isbn_10": ["5845107415"], "key": "/books/OL23021231M"}, 
     {"isbn_13": null, "isbn_10": ["8186775609"], "key": "/books/OL23032880M"}, 
     {"isbn_13": null, "isbn_10": null, "key": "/books/OL23024206M"}, 
     {"isbn_13": null, "isbn_10": ["9573317249"], "key": "/books/OL23035226M"}, 
     {"isbn_13": null, "isbn_10": ["8478885544"], "key": "/books/OL22858290M"}, 
     {"isbn_13": null, "isbn_10": ["9638386894"], "key": "/books/OL23038915M"}, 
     {"isbn_13": null, "isbn_10": ["8700398365"], "key": "/books/OL23029279M"}]

Some of the editions will have no ISBNs at all, because they
predate ISBNs, but they'll still have OL book IDs, recorded in
the JSON as "key"
