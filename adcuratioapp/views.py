from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from adcuratioapp import serializers as app_serializers
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from adcuratioapp import models as app_models


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        register_serializer = app_serializers.RegisterSerializer(data=request.data)

        if not register_serializer.is_valid():
            return Response(status=400, data=register_serializer.errors)
        
        serialized_data = register_serializer.validated_data
        
        is_user_exists = User.objects.filter(Q(email = serialized_data.get('email')) | Q(username = serialized_data.get('username')))
        
        if is_user_exists:
            return Response(status=400, data="Username or Email already registered, try with other username or Email.")
        
        if not is_user_exists:
            user = User.objects.create_user(
                username = serialized_data.get('username'),
                email = serialized_data.get('email'),
                password = serialized_data.get('password'),
            )
            user.save()
            return Response(status=200, data='user created successfully.')

class LoginView(APIView):
    def post(self, request):
        login_serializer = app_serializers.LoginSerializer(data=request.data)

        if not login_serializer.is_valid():
            return Response(status=400, data=login_serializer.errors)
        
        serilaized_data = login_serializer.validated_data
        
        user_instance = User.objects.filter(email = serilaized_data.get('email')).last()

        if user_instance is not None:
            user = authenticate(
                username=user_instance.username,
                password=serilaized_data.get('password') 
            )
            if user is not None:
                login(request,user)
                if request.user.is_authenticated:
                    tokens = RefreshToken.for_user(request.user)

                    data = {
                        "refresh":str(tokens),
                        "access":str(tokens.access_token)
                    }

                    return Response(status=200, data=data)
        return Response(status=400, data="Email or Password is wrong.")
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
            logout(request)
            return Response(status=200, data="Logged out successfully.")


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = app_models.Blogs.objects.filter(author=request.user)
      
        blogs_array = []
        for blog in blogs:
            blogs_array.append(blog.get_details())
   
        return Response(status=200, data={"blogs":blogs_array})
    

class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, blog_id):
     
        blog = app_models.Blogs.objects.filter(blog_id=blog_id).last()
       
        if not blog:
            return Response(status=404, data="Blog Doesn't Exists")
        else:
            return Response(status=200, data=blog.get_details())
        
   
    def post(self, request):
        blog_serializer = app_serializers.BlogSerializer(data=request.data)

        if not blog_serializer.is_valid():
            return Response(status=400,data=blog_serializer.errors)
        
        serilaized_data = blog_serializer.validated_data

        blog = app_models.Blogs.objects.create(
            author = request.user,
            title = serilaized_data.get('title'),
            description = serilaized_data.get('description'),
            blog_image = serilaized_data.get('blog_image')
        )
        blog.save()

        return Response(status=201, data="Blog Created Successfully")
    
    def put(self, request, blog_id):
        blog = app_models.Blogs.objects.filter(blog_id=blog_id).last()
       
        if not blog:
            return Response(status=404, data="Blog Doesn't Exists")
        else:
            if blog.author != request.user:
                return Response(status=400, data="You don't have permission to update the blog.")
        
            blog_serializer = app_serializers.BlogSerializer(data=request.data)

            if not blog_serializer.is_valid():
                return Response(status=400,data=blog_serializer.errors)
            
            serilaized_data = blog_serializer.validated_data

            blog.title = serilaized_data.get('title')
            blog.description = serilaized_data.get('description')
            blog.blog_image = serilaized_data.get('blog_image')
            blog.save()

            return Response(status=200, data="Updatd the blog Successfully.")
        
    def delete(self, request, blog_id):
        blog = app_models.Blogs.objects.filter(blog_id=blog_id).last()
       
        if not blog:
            return Response(status=404, data="Blog Doesn't Exists")
        else:
            if blog.author != request.user:
                return Response(status=400, data="You don't have permission to delete the blog.")
        
            blog = app_models.Blogs.objects.filter(blog_id=blog_id).delete()

            return Response(status=200, data="Blog Successfully Deleted.")
    



