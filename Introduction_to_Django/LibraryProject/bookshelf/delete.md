Book.objects.filter(title="Nineteen Eighty-Four").delete()
Books.objects.get(title= "Nineteen Eighty-Four")

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
