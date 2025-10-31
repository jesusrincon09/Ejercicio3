from rest_framework.exceptions import NotFound, ValidationError
from datetime import datetime
from django.utils import timezone

class LoanService:
    def __init__(self, repository, book_repository, member_repository):
        self.repository = repository
        self.book_repository = book_repository
        self.member_repository = member_repository

    def list_loans(self, filters=None):
        return self.repository.get_all(filters)

    def get_loan_by_id(self, loan_id):
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            raise NotFound("El préstamo no existe.")
        return loan

    def create_loan(self, data):
        book = data.get("book")       
        member = data.get("member")   
        if book.stock <= 0:
            raise Exception("No hay ejemplares disponibles para este libro.")

        if member.loans.filter(book=book, returned=False).exists():
            raise Exception("El miembro ya tiene este libro prestado.")
        
        member_active_loans = member.loans.filter(returned=False).count()
        if member_active_loans >= member.max_loans:
            raise Exception("El miembro ha alcanzado el límite máximo de préstamos activos.")

        self.repository.create(data)
        self.book_repository.decrease_stock(book, 1)

        return {
            "code": 201,
            "msg": "Préstamo registrado correctamente.",
        }


    def return_book(self, loan):
        if loan.returned:
            raise Exception("Este préstamo ya fue devuelto.")

        loan.returned = True
        loan.return_date = timezone.now()
        book = loan.book
        book.stock += 1
        self.book_repository.update(book, {"stock": book.stock})

        self.repository.update(loan, {
            "returned": True,
            "return_date": loan.return_date
        })

        return {"code": 200, "msg": "Libro devuelto correctamente."}

