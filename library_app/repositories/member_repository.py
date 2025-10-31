from library_app.models.member import Member

class MemberRepository:

    def get_all(self, filters=None):
        queryset = Member.objects.all().order_by('id')
        if filters:
            if 'name' in filters and filters['name']:
                queryset = queryset.filter(name__icontains=filters['name'])
            if 'last_name' in filters and filters['last_name']:
                queryset = queryset.filter(last_name__icontains=filters['last_name'])
            if 'email' in filters and filters['email']:
                queryset = queryset.filter(email__icontains=filters['email'])
            if 'library' in filters and filters['library']:
                queryset = queryset.filter(library_id=filters['library'])
            if 'max_loans' in filters and filters['max_loans'] is not None:
                queryset = queryset.filter(max_loans=filters['max_loans'])
        return queryset

    def get_by_id(self, member_id):
        return Member.objects.filter(id=member_id).first()

    def create(self, data):
        return Member.objects.create(**data)

    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
