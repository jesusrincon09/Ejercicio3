from library_app.models.library import Library

class LibraryService:
    def __init__(self, repository):
        self.repository = repository

    def list_libraries(self, filters=None):
        return self.repository.get_all(filters)

    def get_library_by_id(self, library_id):
        library = self.repository.get_by_id(library_id)
        if not library:
            raise Exception("La biblioteca no existe.") 
        return library

    def create_library(self, data):
        existing = self.repository.get_all({'name': data.get('name')})
        if existing.exists():
            raise Exception("Ya existe una biblioteca con este nombre.")
        return self.repository.create(data)

    def update_library(self, instance, data):
        if 'name' in data:
            existing = self.repository.get_all({'name': data['name']}).exclude(id=instance.id)
            if existing.exists():
                raise Exception("Ya existe una biblioteca con este nombre.")
        return self.repository.update(instance, data)

    def delete_library(self, instance):
        if not instance:
            raise Exception("La biblioteca no existe.")

        if instance.books.exists():
            raise Exception("No se puede eliminar la biblioteca porque tiene libros asociados.")
        
        if instance.members.exists():
            raise Exception("No se puede eliminar la biblioteca porque tiene miembros asociados.")

        self.repository.delete(instance)

