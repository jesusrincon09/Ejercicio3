from rest_framework.exceptions import NotFound

class MemberService:

    def __init__(self, repository):
        self.repository = repository

    def list_members(self, filters=None):
        return self.repository.get_all(filters)

    def get_member_by_id(self, member_id):
        member = self.repository.get_by_id(member_id)
        if not member:
            raise NotFound("El miembro no existe.")
        return member

    def create_member(self, data):
        existing = self.repository.get_all({'email': data.get('email')})
        if existing.exists():
            raise Exception("Ya existe un miembro con este correo electrónico.")
        self.repository.create(data)
        return {"code": 201, "msg": "Miembro creado correctamente."}

    def update_member(self, instance, data):
        if 'email' in data:
            existing = self.repository.get_all({'email': data['email']}).exclude(id=instance.id)
            if existing.exists():
                raise Exception("Ya existe un miembro con este correo electrónico.")
        self.repository.update(instance, data)
        return {"code": 200, "msg": "Miembro actualizado correctamente."}

    def delete_member(self, instance):
        if not instance:
            raise Exception("El miembro no existe.")
        
        if instance.loans.exists():
            raise Exception("No se puede eliminar el miembro porque tiene préstamos asociados.")

        self.repository.delete(instance)
        return {"code": 204, "msg": "Miembro eliminado correctamente."}

