from django.urls import path

from users.apps import UsersConfig
from users.views import UserRetrieveApiView, UserUpdateApiView, UserCreateApiView, PaymentsListApiView, \
    UserDestroyApiView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateApiView.as_view(), name='create'),
    path('<int:pk>/', UserRetrieveApiView.as_view(), name='details'),
    path('<int:pk>/update/', UserUpdateApiView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDestroyApiView.as_view(), name='delete'),

    path('payments/', PaymentsListApiView.as_view(), name='payments'),
]