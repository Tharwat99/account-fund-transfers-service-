from rest_framework.pagination import PageNumberPagination

class ListAccountsPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'  
    max_page_size = 100  # Optional maximum page size