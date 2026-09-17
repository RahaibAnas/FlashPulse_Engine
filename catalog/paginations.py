from rest_framework import pagination

class PagePagination(pagination.PageNumberPagination):
    max_page_size = 10
    page_size = 5
