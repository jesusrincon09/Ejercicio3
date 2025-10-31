from library_app.models import Library

class LibraryRepository:

    def get_all(self, filters=None):
        queryset = Library.objects.all().order_by('id')
        if filters:
            if 'name' in filters and filters['name']:
                queryset = queryset.filter(name__icontains=filters['name'])
            if 'address' in filters and filters['address']:
                queryset = queryset.filter(address__icontains=filters['address'])
            if 'phone' in filters and filters['phone']:
                queryset = queryset.filter(phone__icontains=filters['phone'])
            if 'email' in filters and filters['email']:
                queryset = queryset.filter(email__icontains=filters['email'])
        return queryset

    def get_by_id(self, library_id):
        return Library.objects.filter(id=library_id).first()

    def create(self, data):
        return Library.objects.create(**data)

    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
