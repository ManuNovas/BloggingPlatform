from rest_framework.fields import IntegerField, CharField, ListField, DateTimeField
from rest_framework.serializers import Serializer

from posts.models import Post


class PostSerializer(Serializer):
    id = IntegerField(read_only=True)
    title = CharField(max_length=64, required=True)
    content = CharField(required=True)
    category = CharField(max_length=32, required=True)
    tags = ListField(child=CharField(max_length=32), required=True)
    createdAt = DateTimeField(read_only=True)
    updatedAt = DateTimeField(read_only=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, post, validated_data):
        post.title = validated_data.get('title', post.title)
        post.content = validated_data.get('content', post.content)
        post.category = validated_data.get('category', post.category)
        post.tags = validated_data.get('tags', post.tags)
        post.save()
        return post

    def get(self, post):
        return post


class SearchSerializer(Serializer):
    term = CharField(min_length=3, max_length=64, required=False)
