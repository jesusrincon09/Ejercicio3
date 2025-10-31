from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from library_app.models.book import Book
from library_app.repositories.library_repository import LibraryRepository
from library_app.repositories.book_repository import BookRepository

class BookService:
    def __init__(self, repository):
        self.repository = repository

    def list_books(self, filters=None):
        return self.repository.get_all(filters)

    def get_book_by_id(self, book_id):
        book = self.repository.get_by_id(book_id)
        if not book:
            raise Exception("El libro no existe.")
        return book

    def create_book(self, data):
        existing = self.repository.get_all({'isbn': data.get('isbn')})
        if existing.exists():
            raise Exception("Ya existe un libro con este ISBN.")

        year = data.get('published_year')
        if year and year > datetime.now().year:
            raise ValueError("El año de publicación no puede ser mayor al actual.")
        
        return self.repository.create(data)

    def update_book(self, instance, data):
        if 'isbn' in data:
            existing = self.repository.get_all({'isbn': data['isbn']}).exclude(id=instance.id)
            if existing.exists():
                raise Exception("Ya existe un libro con este ISBN.")
        return self.repository.update(instance, data)

    def delete_book(self, instance):
        if not instance:
            raise Exception("El libro no existe.")
        
        if instance.loans.exists():
            raise Exception("No se puede eliminar el libro porque tiene préstamos asociados.")
        
        self.repository.delete(instance)
        return {"code": 204, "msg": "Libro eliminado correctamente."}

