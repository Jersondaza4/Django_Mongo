from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=200)
    published_date = serializers.DateField()
    genre = serializers.CharField(max_length=100)