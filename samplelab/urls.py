
from django import conf
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from cutomer.views import Index,CreateNote,ViewNote,Profile
from rest_framework_simplejwt.views import TokenVerifyView,TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('signup', SignUp.as_view(),name="signup"),
    path('', Index.as_view(),name="index"),
    # path('login', Login.as_view()),
    # path('profile', Profile.as_view()),
    # path('verify-signup', VerifySignup.as_view(),name="verify_signup"),
    # path('forgotpassword', ForgotPassword.as_view(),name="forgotpassword"),
    # path('verify-forgotpassword', ConfirmForgotPassword.as_view(),name="confirm_forgotpassword"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("create-note",CreateNote.as_view()),
    path("v/<str:random_string>",ViewNote.as_view())

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
