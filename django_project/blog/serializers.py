from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
    #title = serializers.CharField(max_length=100)
    #content = serializers.CharField()
    #date_posted = serializers.DateTimeField()
    #author = serializers.RelatedField(source='author',queryset=User.objects.all())
    #class Meta:
    #    model = User
    #    fields = ['username']


    #def create(self, validated_data):
     #   return Post.objects.create(validated_data)

    #def update(self, instance, validated_data):
     #   instance.title = validated_data.get('title',instance.title)
     #   instance.content = validated_data.get('content', instance.content)
     #   instance.date_posted = validated_data.get('date_posted', instance.date_posted)
     #   instance.author = validated_data.get('author', instance.author)
     #   return instance