from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Course
from users.models import User, Payment, Subscription
from users.permissions import IsProfileOwner
from users.serializers import UserPublicSerializer, UserPrivateSerializer, PaymentSerializer


class UserRetrieveApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        obj = self.get_object()
        if obj == self.request.user:
            return UserPrivateSerializer
        return UserPublicSerializer


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPrivateSerializer
    permission_classes = [AllowAny]


class UserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPrivateSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]


class UserDestroyApiView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserPrivateSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]


class PaymentsListApiView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['method', 'course', 'lesson']
    ordering_fields = ['date']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SubscriptionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_pk = kwargs.get('course_pk')
        course_item = get_object_or_404(Course, pk=course_pk)

        subs_item, created = Subscription.objects.get_or_create(
            user=user,
            course=course_item,
            defaults={'is_active': True}
        )

        if not created:
            subs_item.is_active = not subs_item.is_active
            subs_item.save()
            message = 'Подписка возобновлена' if subs_item.is_active else 'Подписка отключена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message, "is_active": subs_item.is_active})
