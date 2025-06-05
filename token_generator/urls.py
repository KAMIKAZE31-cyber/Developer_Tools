from django.urls import path
from . import views

urlpatterns = [
    path('', views.TokenListView.as_view(), name='token-list'),
    path('generate/', views.GenerateTokenView.as_view(), name='generate-token'),
    path('delete/<int:token_id>/', views.DeleteTokenView.as_view(), name='delete-token'),
] 