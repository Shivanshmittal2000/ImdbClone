from django.contrib.auth.models import User
from django.http import response

from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app import serializers
from watchlist_app import models

# class StreamPlatfromTestCase(APITestCase):
#     def setUp(self):
#         self.user=User.objects.create_user(username="example",password='Password@123')
#         self.token=Token.objects.get(user__username=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
#         self.stream=models.StreamPlatform.objects.create(name='netflix',about='#1 Streaming platform', website ='https://netflix.com')
#     def test_streamplatform_create(self):
#         data={
#             'name' : 'netflix',
#             'about' : '#1 Streaming platform',
#             'website' : 'https://netflix.com'
#         }
#         response= self.client.post(reverse('streamplatform-list'),data)
#         self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

#     def test_streamplatform_list(self):
#         response=self.client.get(reverse('streamplatform-list'))
#         self.assertEqual(response.status_code,status.HTTP_200_OK)

#     def test_streamplatform_ind(self):
#         response=self.client.get(reverse('streamplatform-detail',args=(self.stream.id, )))
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    
# class WatchListTestCase(APITestCase):
#     def setUp(self):
#         self.user=User.objects.create_user(username='example',password='NewPassword')
#         self.token=Token.objects.get(user__username=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
#         self.stream=models.StreamPlatform.objects.create(name='netflix',about='#1 Streaming platform', website ='https://netflix.com')
#         self.watchlist=models.WatchList.objects.create( platform = self.stream ,title = 'Example Movie ',
#             storyline = ' This is example movie',
#             active = True)

#     def test_watchlist_create(self):
#         data={
#             'platform' : self.stream,
#             'title' :'Example Movie ',
#             'storyline' : ' This is example movie',
#             'active' : True
#         }
#         response=self.client.post(reverse('watch_list'),data)
#         self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
#     def test_watchlist_list(self)        :
#         response=self.client.get(reverse('watch_list',))
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
        
#     def test_watchlist_ind(self):
#         response= self.client.get(reverse('watchlist_details', args=(self.watchlist.id, )))
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
        
class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='example',password='NewPassword')
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream=models.StreamPlatform.objects.create(name='netflix',about='#1 Streaming platform', website ='https://netflix.com')
        self.watchlist=models.WatchList.objects.create( platform = self.stream ,title = 'Example Movie ',
            storyline = ' This is example movie',
            active = True)
        self.watchlist2=models.WatchList.objects.create( platform = self.stream ,title = 'Example Movie 2 ',
            storyline = ' This is example movie',
            active = True)  # Created a second movie
        self.review=models.Review.objects.create(review_user = self.user,
                rating=5,
                description='Nice Movie',
                watchlist =self.watchlist2,
                active=True)   # Created a review for watchlist2
    def test_Review_create(self):   # Created a review for watchlist
        data={
                'review_user' : self.user,
                'rating':5,
                'description':'Nice Movie',
                'watchlist' :self.watchlist,
                'active':True
            }
        # self.client.force_authenticate(user=None)  # this line make logout user so that it does not allow to login and give 401 unauthirized error
        response=self.client.post(reverse('review_create', args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    def test_review_update(self):
        data={
                'review_user' : self.user,
                'rating':4,
                'description':'Nice movie but more comedy -updated',
                'watchlist' :self.watchlist2,
                'active':True
            }
        response=self.client.put(reverse('review_details',args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_movielist(self):
        response=self.client.get(reverse('review_list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_individual(self):
        response=self.client.get(reverse('review_details',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_user(self):
        response=self.client.get('/watch/reviews/?username'+self.user.username)   # if you want to use direct url instead of writing with reverse
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        