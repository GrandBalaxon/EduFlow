from django.urls import path

from users.apps import UsersConfig
from users.views import UserRetrieveApiView, UserUpdateApiView, UserCreateApiView, PaymentsListApiView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateApiView.as_view(), name='create'),
    path('<int:pk>/', UserRetrieveApiView.as_view(), name='details'),
    path('<int:pk>/update/', UserUpdateApiView.as_view(), name='update'),

    path('payments/', PaymentsListApiView.as_view(), name='payments'),
]