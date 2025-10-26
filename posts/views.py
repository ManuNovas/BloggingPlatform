from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from posts.models import Post
from posts.serializers import PostSerializer, SearchSerializer


def create_post(request):
    data = JSONParser().parse(request)
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data, status=201)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response


def update_post(request, post):
    data = JSONParser().parse(request)
    serializer = PostSerializer(post, data=data)
    if serializer.is_valid():
        serializer.save()
        response = JsonResponse(serializer.data)
    else:
        response = JsonResponse(serializer.errors, status=400)
    return response


def delete_post(post):
    post.delete()
    return HttpResponse(status=204)


def get_post(post):
    serializer = PostSerializer(post)
    return JsonResponse(serializer.data)


def get_posts(request):
    data = SearchSerializer(data=request.GET)
    if data.is_valid():
        term = data.validated_data.get('term')
        if term:
            posts = Post.objects.filter(
                Q(title__contains=term) | Q(content__contains=term) | Q(category__contains=term) | Q(
                    tags__contains=[term]))
        else:
            posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        response = JsonResponse(serializer.data, safe=False)
    else:
        response = JsonResponse(data.errors, status=400)
    return response

# Create your views here.
@csrf_exempt
def index(request):
    try:
        if request.method == 'POST':
            response = create_post(request)
        elif request.method == 'GET':
            response = get_posts(request)
        else:
            response = HttpResponse('Invalid HTTP Method', status=405)
    except Exception as e:
        print(e)
        response = HttpResponse('Internal Server Error', status=500)
    return response


@csrf_exempt
def pk(request, primary_key):
    try:
        post = Post.objects.get(pk=primary_key)
        if request.method == 'PUT':
            response = update_post(request, post)
        elif request.method == 'DELETE':
            response = delete_post(post)
        elif request.method == 'GET':
            response = get_post(post)
        else:
            response = HttpResponse('Invalid HTTP Method', status=405)
    except Exception as e:
        print(e)
        if e.__class__.__name__ == 'DoesNotExist':
            response = HttpResponse('Post Not Found', status=404)
        else:
            response = HttpResponse('Internal Server Error', status=500)
    return response
