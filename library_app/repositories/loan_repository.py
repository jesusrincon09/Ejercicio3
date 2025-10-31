from library_app.models.loan import Loan

class LoanRepository:

    def get_all(self, filters=None):
        queryset = Loan.objects.select_related('book', 'member').order_by('-loan_date')
        if filters:
            if 'member' in filters and filters['member']:
                queryset = queryset.filter(member_id=filters['member'])
            if 'book' in filters and filters['book']:
                queryset = queryset.filter(book_id=filters['book'])
            if 'returned' in filters and filters['returned'] is not None:
                queryset = queryset.filter(returned=filters['returned'])
        return queryset

    def get_by_id(self, loan_id):
        return Loan.objects.filter(id=loan_id).first()

    def create(self, data):
        return Loan.objects.create(**data)

    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()

