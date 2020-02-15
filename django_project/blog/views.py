from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status , generics ,views ,mixins
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import HttpResponse
# Create your views here.
#posts =[
#    {
#        'author':'shivash.g',
#        'title':'Post 1',
#        'date':'20 Jan 2020',
#        'content': 'First Django Blog Project/Post1'
#    },
#    {
#        'author':'shivash.g',
#        'title':'Post 2',
#        'date':'20 Jan 2020',
#        'content': 'First Django Blog Project/Post2'
#    },
#]

def home(request):
    #return HttpResponse('<h1>Home Page</h1>')
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostAPIView(APIView):
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailsView(APIView):
    def get_object(self,id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist :
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        post = self.get_object(id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    @csrf_exempt
    def put(self,request,id):
        post = self.get_object(id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    @csrf_exempt
    def delete(self,request,id):
        post = self.get_object(id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@csrf_exempt
def post_list_update(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data , status=201)
        return JsonResponse(serializer.errors , status=400)


@csrf_exempt
def specific_post(request,pk):
    try:
        post = Post.objects.get(pk=pk)

    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(post , data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data , status=201)
        return JsonResponse(serializer.errors , status=400)

def about(request):
    #return HttpResponse('<h1>Blog Page</h1>')
    return render(request, 'blog/about.html',{'title' : "About" })



class GenericAPIView(generics.GenericAPIView , mixins.ListModelMixin , mixins.CreateModelMixin , mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request ,id = None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    @csrf_exempt
    def post(self,request):
        return self.create(request)
    @csrf_exempt
    def put(self,request,id = None):
        return self.update(request)

    @csrf_exempt
    def delete(self,request,id=None):
        return self.destroy(request,id)





