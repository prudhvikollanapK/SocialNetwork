from django.db.models import Q
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, FriendRequest
from .serializers import UserSerializer, UserSearchSerializer, FriendRequestSerializer

import logging

logger = logging.getLogger(__name__)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        return User.objects.filter(
            Q(email__iexact=keyword) | Q(username__icontains=keyword)
        )


class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pending_requests_list(request):
    if request.method == 'GET':
        pending_requests = FriendRequest.objects.filter(to_user=request.user)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        to_user_id = request.data.get('to_user')
        if not to_user_id:
            return Response({'error': 'to_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'error': 'to_user not found'}, status=status.HTTP_404_NOT_FOUND)

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )
        if not created:
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def friend_request_view(request):
    to_user_id = request.data.get('to_user')
    if not to_user_id:
        return Response({'error': 'to_user is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        to_user = User.objects.get(id=to_user_id)
    except User.DoesNotExist:
        return Response({'error': 'to_user not found'}, status=status.HTTP_404_NOT_FOUND)

    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=to_user
    )
    if not created:
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, pk):
    logger.info(f"Accept friend request: {pk} for user: {request.user.id}")
    try:
        friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        logger.info(f"Friend request found: {friend_request}")
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)
        friend_request.delete()
        return Response({'status': 'Friend request accepted'}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        logger.error(f"Friend request not found: {pk} for user: {request.user.id}")
        return Response({'status': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, pk):
    logger.info(f"Reject friend request: {pk} for user: {request.user.id}")
    try:
        friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        logger.info(f"Friend request found: {friend_request}")
        friend_request.delete()
        return Response({'status': 'Friend request rejected'}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        logger.error(f"Friend request not found: {pk} for user: {request.user.id}")
        return Response({'status': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
