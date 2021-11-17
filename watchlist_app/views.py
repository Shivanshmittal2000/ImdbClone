from django.db.models import query
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse

from rest_framework import pagination, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle,ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from .paginations import WatchListPagination,WatchListLOPagination,WatchListCPagination
from .throttling import ReviewCreateThrottle,ReviewListThrottle
from .models import WatchList,StreamPlatform,Review
from .serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from . import permissions
from watchlist_app import serializers
# Create your views here.
# class based view


# using only GenericAPIView no need to write any function like put,get,post,delete only import them like ListCreateAPIView type of things
class ReviewList(generics.ListAPIView): 
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle] 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk) # so now it shows all reviews related to that movie

class ReviewUser(generics.ListAPIView):
    serializer_class=ReviewSerializer
    # def get_queryset(self):
    #     username=self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    def get_queryset(self):
        username=self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView): 
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    throttle_classes=[ReviewCreateThrottle]  # it restrict to a user that it creates no. of reviews acc. to rate defined in settings.py file on all the movies 
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        movie=WatchList.objects.get(pk=pk)
        user=self.request.user
        review_queryset=Review.objects.filter(watchlist=movie,review_user=user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        movie_review_rating=movie.number_rating
        movie_avg_rating=movie.avg_rating
        movie.number_rating +=1
        movie.avg_rating =(((movie_review_rating*movie_avg_rating) + serializer.validated_data['rating'])/(movie_review_rating +1))
        movie.save()
        serializer.save(watchlist=movie,review_user=user)  # As i need to put separately watchlist as other fields are getting from outside and movie i need to all her so use watchlist = movie


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView): # It remains same as changing url as it access the individual review
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]  # class based views need to use this another method of inserting throttling class if u are using function based view
    throttle_scope='review-detail'  # need to mention its value in settings.py in 'DEFAULT_THROTTLE_RATES'




# Using mixins 
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)




class WatchListAV(APIView):
    permission_classes=[permissions.IsAdminOrReadOnly]
    def get(self,request):
        movies=WatchList.objects.all()
        serializer=WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchList_temp(generics.ListAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializer
    # filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
    pagination_class=WatchListCPagination

    # search_fields=['=title','platform__name']  # = is used for exact match




class WatchDetailsAV(APIView):
    permission_classes=[permissions.IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk) # in this we can use pk=pk or id=pk can also be used
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=WatchListSerializer(movie)
        return Response(serializer.data)   # DRF browsable api format it prints in api-view by default it takes get and if need to use other mention that 
    
    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)

    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        content={'Delete Status':'Successful'}
        return Response(content,status=status.HTTP_200_OK)
        

# in viewset implement multiple view in one like for accessing individual and all the platforms we can use a single view 
class StreamPlatformVs(viewsets.ModelViewSet):  # we can use put patch, create and other methods also 
    permission_classes=[permissions.IsAdminOrReadOnly]
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer
    # in modelviewset all list , create, partial_update, destroy,put 

    # def list(self,request):
    #     queryset=StreamPlatform.objects.all()
    #     serializer=StreamPlatformSerializer(queryset,many=True)
    #     return Response(serializer.data)
    
    # def retrieve(self,request,pk=None):
    #     queryset=StreamPlatform.objects.all()
    #     watchlist=get_object_or_404(queryset,pk=pk)
    #     serializer=StreamPlatformSerializer(watchlist)
    #     return Response(serializer.data)

    


# class StreamPlatformAV(APIView):
#     permission_classes=[permissions.IsAdminOrReadOnly]
#     def get(self,request):
#         platform=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(platform,many=True,context={'request': request})
#         return Response(serializer.data)

#     def post(self,request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)




# class StreamDetailsAV(APIView):   
#     permission_classes=[permissions.IsAdminOrReadOnly]
#     def get(self,request,pk):
#         platform=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(platform ,context={'request': request}) # context is for only when HyperlinkedRealtedField is used         
#         return Response(serializer.data)

#     def put(self,request,pk):
#         platform=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def delete(self,request,pk):
#         platform=StreamPlatform.objects.get(pk=pk)
#         platform.delete()


# Here we are using function based view
# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method=='GET':
#         movies=Movie.objects.all()
#         serializer=MovieSerializer(movies,many=True)
#         # print(movies)
#         # print(movies.values())
#         # data={'list':list(movies.values())}  # this is the way without DRF it takes a lot of effort of programmer
#         # return JsonResponse(serializer.data,safe=False) return Json format with this
#         return Response(serializer.data)  # this is provide api_view so need to use DRF decorator when use Response it also return in Json format can be verified with "" there and in true t is in small case which is True in python dict in which T is in upper case
#     if request.method == "POST":
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == "GET":
#         try:
#             movie=Movie.objects.get(pk=pk) # in this we can use pk=pk or id=pk can also be used
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         serializer=MovieSerializer(movie)
#         return Response(serializer.data)   # DRF browsable api format it prints in api-view by default it takes get and if need to use other mention that 
#     if request.method == "PUT":
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)

#     if request.method == 'DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         content={'Delete Status':'Successful'}
#         return Response(content,status=status.HTTP_200_OK)
        