from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Item
from .serializers import ItemSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

# ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

# Create your views here.
# @api_view(['GET', "POST"])
# def item_list_create(request):
#     if request.method == 'GET':
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update, Delete (GET, PUT, DELETE)
# @api_view(['GET', 'PUT', 'DELETE'])
# def item_detail(request, pk):
    
#     if request.method == 'GET':
#         try:
#             item = Item.objects.get(pk=pk)
#         except Item.DoesNotExist:
#             return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ItemSerializer(item)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         try:
#             item = Item.objects.get(pk=pk)
#         except Item.DoesNotExist:
#             return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ItemSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         item = Item.objects.get(pk=pk)
#         item.delete()
#         return Response({"Status":"Successfully Deteted"},status=status.HTTP_204_NO_CONTENT)

# ...................................................................................................
class ItemListCreate(APIView):
    
    def get_permissions(self):
            if self.request.method in ['POST', 'PUT', 'DELETE']:
                return [permissions.IsAuthenticated()]  # Require authentication for POST, PUT, DELETE
            return [permissions.AllowAny()]  # Allow any user for GET requests



    def get(self, request, pk=None):
        if pk:
            # Retrieve a single item by pk
            item = get_object_or_404(Item, pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        else:
            # Get the 'name' query parameter from the request
            name_query = request.query_params.get('name', None)
            
            # Retrieve a list of all items, or filter by name if provided
            if name_query:
                items = Item.objects.filter(name__icontains=name_query)  # Case-insensitive filtering by name
            else:
                items = Item.objects.all()


            # Set up pagination
            paginator = PageNumberPagination()
            paginator.page_size = 5  # Adjust page size as needed

            # Paginate the queryset
            paginated_items = paginator.paginate_queryset(items, request)

            # Serialize the paginated data
            serializer = ItemSerializer(paginated_items, many=True)

            # Return paginated response
            return paginator.get_paginated_response(serializer.data)
                                                    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response({"message": "Item deleted successfully."},status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    def post(self, request):
        # Get username and password from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # If authenticated, get or create a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            # Return an error if the credentials are invalid
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)