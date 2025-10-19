from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from posts.serializers import PostSerializer


def create_post(request):
    data = JSONParser().parse(request)
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data, status=201)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response

# Create your views here.
@csrf_exempt
def posts(request):
    try:
        if request.method == 'POST':
            response = create_post(request)
        else:
            response = HttpResponse('Invalid HTTP Method', status=405)
    except Exception as e:
        response = HttpResponse('Internal Server Error', status=500)
        print(e)
    return response

