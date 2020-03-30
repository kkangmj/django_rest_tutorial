'''
# Tutorial 1
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer

@csrf_exempt
def snippet_list(request):
    # List all code snippets
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        # many=True : Telling drf that queryset contains multiple items
        serializer = SnippetSerializer(snippets, many=True)
        # safe=False : 첫 번째 argument가 dict가 아닌 경우 설정
        # serializer.data : [{"code": " foo = \"bar\"\n", "id": 1, "language": "python", ...}, {...}, {...}]
        return JsonResponse(serializer.data, safe=False)

    # Create new snippet
    if request.method == 'POST':
        data = JSONParser().parser(request)
        # .save() will create a new instance
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    # Get particular snippet object
    try:
        # Snippet.objects.get(pk=pk) : <Snippet: Snippet object(pk)>
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    # Retrieve snippet
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        # serializer.data : {'id': 1, 'title':'', ...}
        return JsonResponse(serializer.data)

    # Update snippet
    elif request.method == 'PUT':
        data = JSONParser().parser(request)
        # .update() will update snippet instance
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # Delete snippet
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

'''

# Tutorial 2
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Snippet
from .serializers import SnippetSerializer

# List all snippets or create new one
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update or delete a code snippet
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_vaild():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)