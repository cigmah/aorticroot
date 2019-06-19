from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Post
from posts.serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        
        serialized = PostSerializer(data={"user_id": user.id, **data})
        
        if serialized.is_valid():
            created = serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
