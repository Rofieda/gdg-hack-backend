from django.urls import path
from .views import CreateUserView 
from .views import RegisterUserView , LoginView , TokenRefreshView , LogoutAPIView

 

urlpatterns = [
    path('users/', CreateUserView.as_view()),  # pour la creation (user)
    #path('users/<int:pk>/', UserView.as_view()),  # pour put et delete (user)
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'), # first documenttion 
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    

]