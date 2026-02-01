books = Book.objects.filter(author__name="John Doe")

for book in books:
    print(book.title)


library_book = Library.objects.get(name="Central Library")
books = library_book.books.all()
for book in books:
    print(book.title)

librarian = Librarian.objects.get(library__name="Central Library").name
print(librarian)