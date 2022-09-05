from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField, Serializer
from .models import User, Follow



class UserRegisterSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'email', 
            'username', 
            'password', 
            'first_name', 
            'last_name', 
            'age'
            ]

    def create(self, validated_data):
        raw_password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if raw_password is not None:
            instance.set_password(raw_password)
        instance.save()
        return instance


class UserProfileSerializer(ModelSerializer):
    followers = SerializerMethodField()
    following = SerializerMethodField()


    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'bio',
            'profile_photo',
            'followers',
            'following'
        ]
    
    def get_followers(self, obj):
        query = Follow.objects.filter(to_user=obj).all()
        return len(query)
    
    def get_following(self, obj):
        query = Follow.objects.filter(from_user=obj).all()
        return len(query)




class FollowingSerializer(ModelSerializer):
    to_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'to_user',
        ]


class FollowersSerializer(ModelSerializer):
    from_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'from_user',
        ]