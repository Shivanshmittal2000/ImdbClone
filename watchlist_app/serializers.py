from rest_framework import serializers
from .models import Review, WatchList,StreamPlatform

# function for validators also write in class but without self and before calling place and write same as it is no change
# ModelSerializer

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model=Review
        exclude=['watchlist']
        # fields="__all__"
        
class WatchListSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name')
    # this is method to make a custom field
    # len_name=serializers.SerializerMethodField() #  len_name is name of custom variable now need to implement method of this using get_ prefix and also need to add in class meta fields or it sets to __all__
    class Meta:
        model=WatchList
        fields="__all__"
        # fields=['id','name','description','active','len_name']  # also need to set here or sets fileds to __all__
        # exclude=['name']




class StreamPlatformSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='streamplatform_details') # when HyperlinkedModelSerializer is used
    # here below watchlist is realted_name Watchlist model where field is platform and then name of serializer
    watchlist=WatchListSerializer(many=True,read_only=True)  # it gives all info of that watchlist id 
    # watchlist=serializers.StringRelatedField(many=True) # it return the __str__ of that model Watchlist as watchlist is related_name of in watchlist model
    # watchlist=serializers.PrimaryKeyRelatedField(many=True,read_only=True) # It only gives the primary key field
    # watchlist=serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlist_details'
    # ) # in this view_name is name of url of that field
    class Meta:
        model=StreamPlatform
        fields='__all__'

    # field level validation
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError('Name length is too short')
    #     return value

    # # object level validation
    # def validate(self,data):
    #     # print(data.get('name'),data.get('description'))
    #     if data.get('name')== data.get('description'):
    #         raise serializers.ValidationError('name and desc can not be same')
    #     return data

    # def get_len_name(self,object):
    #     length=len(object.name)
    #     return length


# normal serializer
# def check_name(value):
#     if len(value) <2:
#         raise serializers.ValidationError('Name length is too short so not valid')
#     return value
# class MovieSerializer(serializers.Serializer):

#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(max_length=100,validators=[check_name])
#     description=serializers.CharField(max_length=1000)
#     active=serializers.BooleanField(default=False)
#     def check_name(self,value):
#         if len(value) <2:
#             raise serializers.ValidationError('Name length is too short so not valid')
#         return value
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self,instance,validate_data):
#         instance.name=validate_data.get('name',instance.name)
#         instance.description=validate_data.get('description',instance.description)
#         instance.active=validate_data.get('active',instance.active)
#         instance.save()
#         return instance

# # field level validation
#     def validate_name(self,value):
#         if len(value)<2:
#             raise serializers.ValidationError('Name length is too short')
#         return value
# # object level validation
#     def validate(self,data):
#         # print(data.get('name'),data.get('description'))
#         if data.get('name')== data.get('description'):
#             raise serializers.ValidationError('name and desc can not be same')
#         return data