from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import User, FriendRequest, Friend
from .serializers import UserRegistrationSerializer, UserLoginSerializer, FriendRequestSerializer, FriendSerializer, UserSearchSerializer, UserSerializer

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

# User Login View
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Search View
class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSearchSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        if '@' in search:
            return self.queryset.filter(email__iexact=search)
        return self.queryset.filter(first_name__icontains=search) | self.queryset.filter(last_name__icontains=search)

# Friend Request View
class FriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

# Accept and Reject friend Request View
class FriendRequestAcceptRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, action):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
            if action == 'accept':
                friend_request.status = 'accepted'
                Friend.objects.create(user=request.user, friend=friend_request.from_user)
                Friend.objects.create(user=friend_request.from_user, friend=request.user)
                
            elif action == 'reject':
                friend_request.status = 'rejected'
            friend_request.save()
            return Response({'status': friend_request.status})
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

# 6. Friends List View
class FriendsListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)

# 7. Pending Friend Requests View
class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='sent')
