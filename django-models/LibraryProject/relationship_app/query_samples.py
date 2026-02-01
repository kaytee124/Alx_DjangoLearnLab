author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)

for book in books:
    print(book.title)


library = Library.objects.get(name=library_name)
books = library.books.all()
for book in books:
    print(book.title)

librarian = Librarian.objects.get(library__name=library_name).name
print(librarian)
