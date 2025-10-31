# library_app/urls.py
from rest_framework import routers
from .views.library_viewset import LibraryViewSet
from .views.book_viewset import BookViewSet
from library_app.views.member_viewset import MemberViewSet
from rest_framework.routers import SimpleRouter
from library_app.views.loan_viewset import LoanViewSet

router = SimpleRouter()
router.register(r'libraries', LibraryViewSet, basename='library')
router.register(r'books', BookViewSet, basename='book')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = router.urls
