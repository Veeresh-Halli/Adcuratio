from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^([a-zA-Z\s\'])+$',required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class BlogSerializer(serializers.Serializer):
    title = serializers.RegexField(regex=r'^([a-zA-Z0-9\s\'])+$',required=True)
    description = serializers.RegexField(regex=r'^([a-zA-Z0-9\s\'])+$',required=True)
    blog_image = serializers.ImageField()