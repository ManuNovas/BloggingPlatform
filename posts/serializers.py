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