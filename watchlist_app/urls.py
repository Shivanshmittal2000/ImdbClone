# from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views


router=DefaultRouter()
router.register('stream',views.StreamPlatformVs,basename='streamplatform') #  no need to add as_view() here 

urlpatterns = [
    # in this using class based view
    path('list/',views.WatchListAV.as_view(),name='watch_list'),
    path('list2/',views.WatchList_temp.as_view(),name='watchlist-temp'),
    path('<int:pk>/',views.WatchDetailsAV.as_view(), name='watchlist_details'),

    path('',include(router.urls)),
    # path('stream/',views.StreamPlatformAV.as_view(), name='streamplatform_list'),
    # path('stream/<int:pk>/',views.StreamDetailsAV.as_view(), name='streamplatform_details'),

    path('<int:pk>/reviews/',views.ReviewList.as_view(), name='review_list'),
    path('<int:pk>/review-create/',views.ReviewCreate.as_view(), name='review_create'),
    path('review/<int:pk>/',views.ReviewDetail.as_view(), name='review_details'),

    # path('reviews/<str:username>/',views.ReviewUser.as_view(),name='user-review-details'), # It is used when filter thorugh url
    path('reviews/',views.ReviewUser.as_view(),name='user-review-details') # It is use when filter through serach paramneter ? this type


    # path('review/',views.ReviewList.as_view(), name='review_list'),
    # path('review/<int:pk>/',views.ReviewDetail.as_view(), name='review_details')


    # these path are for function based view
    # path('list/',views.movie_list,name='movie_list'),
    # path('<int:pk>/',views.movie_details, name='movie_details')
]
