from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination,CursorPagination
class WatchListPagination(PageNumberPagination):
    page_size=5
    page_query_param='p'
    page_size_query_param='size'  # for size acc. to user's specifications
    max_page_size=4  # restrict user to max page size 
    last_page_strings='end'

class WatchListLOPagination(LimitOffsetPagination):
    default_limit=5
    max_limit=10
    limit_query_param='limit'
    offset_query_param='start'


class WatchListCPagination(CursorPagination):
    page_size=5
    ordering='created'
    
    