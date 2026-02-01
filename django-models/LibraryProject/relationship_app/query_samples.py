books = Book.objects.filter(author__name="John Doe")

for book in books:
    print(book.title)


library_book = Library.objects.get(name=library_name)
books = library_book.books.all()
for book in books:
        print(book.title)

librarian = Librarian.objects.get(library__name=library_name).name
print(librarian)
