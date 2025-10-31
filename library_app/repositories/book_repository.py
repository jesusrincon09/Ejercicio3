from library_app.models.book import Book

class BookRepository:

    def get_all(self, filters=None):
        queryset = Book.objects.all().order_by('id')
        if filters:
            if 'title' in filters and filters['title']:
                queryset = queryset.filter(title__icontains=filters['title'])
            if 'author' in filters and filters['author']:
                queryset = queryset.filter(author__icontains=filters['author'])
            if 'isbn' in filters and filters['isbn']:
                queryset = queryset.filter(isbn__icontains=filters['isbn'])
            if 'library_id' in filters and filters['library_id']:
                queryset = queryset.filter(library_id=filters['library_id'])
            if 'published_year' in filters and filters['published_year']:
                queryset = queryset.filter(published_year__icontains=filters['published_year'])
        return queryset

    def get_by_id(self, book_id):
        return Book.objects.filter(id=book_id).first()

    def create(self, data):
        return Book.objects.create(**data)

    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
    
    def decrease_stock(self, book, cantidad=1):
        book.stock -= cantidad
        book.save()

    def increase_stock(self, book, cantidad=1):
        book.stock += cantidad
        book.save()
