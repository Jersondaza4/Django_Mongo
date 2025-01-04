from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from bson import ObjectId
from .serializers import BookSerializer
from rest_framework import viewsets
from .models import Book

# Connecting to MongoDB database
db = settings.MONGO_DB


class BookViewSet(viewsets.ModelViewSet):
    # Ensure that only authenticated users can access
    permission_classes = [IsAuthenticated]

    serializer_class = BookSerializer

    def get_queryset(self):
        # Get all books from
        books = list(db.books.find())
        for book in books:
            book["_id"] = str(book["_id"])
        return books

    def retrieve(self, request, pk=None):
        # get book by ID
        try:
            book = db.books.find_one({"_id": ObjectId(pk)})
            if not book:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
            book["_id"] = str(book["_id"]) 
            return Response(book, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        # Create new book
        serializer = BookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            validated_data = serializer.validated_data
            result = db.books.insert_one(validated_data)
            return Response({"_id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        # Update a book
        if not pk:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = db.books.find_one({"_id": ObjectId(pk)})
            if not book:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

            validated_data = serializer.validated_data
            db.books.update_one({"_id": ObjectId(pk)}, {"$set": validated_data})
            return Response({"message": "Book updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        # delete a book
        if not pk:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = db.books.find_one({"_id": ObjectId(pk)})
            if not book:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

            db.books.delete_one({"_id": ObjectId(pk)})
            return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BookAggregationAPIView(APIView):
    #Pipeline to get average price
    permission_classes = [IsAuthenticated]
    def get(self, request, year):
        pipeline = [
            {"$match": {"published_date": {"$regex": f"^{year}"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
        ]
        result = list(db.books.aggregate(pipeline))
        if result:
            return Response({"year": year, "average_price": result[0]["average_price"]}, status=200)
        return Response({"error": "No books found for the specified year."}, status=404)