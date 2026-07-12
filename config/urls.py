from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("course/", include("core.urls"), name="course"),
    path("user/", include("users.urls"), name="user"),

    # JWT-эндпоинты
    path('token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
]
