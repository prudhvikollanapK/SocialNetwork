from django.urls import path
from .views import *


urlpatterns = [
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', friend_request_view, name='friend-request'),
    path('accept-request/<int:pk>/', accept_friend_request, name='accept-request'),
    path('reject-request/<int:pk>/', reject_friend_request, name='reject-request'),
    path('friends/', FriendListView.as_view(), name='list-friends'),
    path('pending-requests/', pending_requests_list, name='pending-requests'),
]
