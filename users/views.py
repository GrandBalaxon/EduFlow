import stripe
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Course, Lesson
from users.models import User, Payment, Subscription
from users.permissions import IsProfileOwner
from users.serializers import UserPublicSerializer, UserPrivateSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session


@extend_schema(
    tags=["Пользователи"],
    summary='Получение данных о пользователе',
    description='Авторизованный пользователь может посмотреть профиль любого пользователя. '
                'Для своего профиля возвращается полная информация (email, телефон, город, аватар, платежи), '
                'для чужого — только общая (email, телефон, город, аватар).'
)
class UserRetrieveApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        obj = self.get_object()
        if obj == self.request.user:
            return UserPrivateSerializer
        return UserPublicSerializer

@extend_schema(tags=["Пользователи"], summary="Регистрация / Создание пользователя")
class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPrivateSerializer
    permission_classes = [AllowAny]

@extend_schema(tags=["Пользователи"], summary="Обновление данных пользователя")
class UserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPrivateSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

@extend_schema(
    tags=["Пользователи"],
    summary="Удаление аккаунта пользователя",
    description="Только владелец (не модератор) может удалить собственный аккаунт."
)
class UserDestroyApiView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserPrivateSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]


@extend_schema(tags=["Платежи"], summary="Список платежей пользователя")
class PaymentsListApiView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['method', 'course', 'lesson']
    ordering_fields = ['date']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@extend_schema(tags=["Платежи"], summary="Создание платежа за курс или урок")
class PaymentCreateApiView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except stripe.error.StripeError as e:
            return Response(
                {'error': f'Ошибка Stripe: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )

    def perform_create(self, serializer):
        course_pk = self.kwargs.get('course_pk')
        lesson_pk = self.kwargs.get('pk')

        # Определяем, за что платёж
        if lesson_pk:
            lesson = get_object_or_404(Lesson, pk=lesson_pk, course_id=course_pk)
            payment = serializer.save(
                user=self.request.user,
                method='stripe',
                course=lesson.course,
                lesson=lesson,
                amount=lesson.price
            )
            product = create_stripe_product(lesson)
        else:
            course = get_object_or_404(Course, pk=course_pk)
            payment = serializer.save(
                user=self.request.user,
                method='stripe',
                course=course,
                amount=course.price
            )
            product = create_stripe_product(course)

        payment_amount = payment.amount
        price = create_stripe_price(product, payment_amount)
        session = create_stripe_checkout_session(price.id)

        payment.stripe_session_id = session.id
        payment.stripe_payment_url = session.url
        payment.save()


@extend_schema(
    tags=["Платежи"],
    summary="Проверка статуса платежа",
    description="Проверяет статус сессии Stripe и обновляет is_paid в локальной записи."
)
class PaymentStatusApiView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()

        if not payment.stripe_session_id:
            return Response(
                {'error': 'У этого платежа нет сессии Stripe'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
            payment.is_paid = session.payment_status == 'paid'
            payment.save(update_fields=['is_paid'])
        except stripe.error.StripeError as e:
            return Response(
                {'error': f'Ошибка Stripe: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response(self.get_serializer(payment).data)


@extend_schema(
    tags=["Подписки"],
    summary="Управление подпиской на курс",
    description="Переключает подписку: если нет — создаёт, если есть — отключает, если отключена — возобновляет.",
    request=None,  # тело запроса не требуется
    responses={200: {"description": "Статус подписки изменён"}},
)
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
