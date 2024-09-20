from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserSearchView, FriendRequestView, FriendRequestAcceptRejectView, FriendsListView, PendingFriendRequestsView

urlpatterns = [
    path('reg/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/<int:pk>/<str:action>/', FriendRequestAcceptRejectView.as_view(), name='handle-friend-request'),
    path('friends_list/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]
