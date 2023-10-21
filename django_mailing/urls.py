from django.urls import path, include

from django_mailing import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client/', views.client_list_view, name='client'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/login/', views.MailingLoginView.as_view(), name='login'),
    path('accounts/logout/', views.MailingLogoutView.as_view(), name='logout'),
    path('messages/', views.messages_view, name='messages'),
    path('tags/', views.tags_view, name='tags'),
    path('tags/delete/<int:tag_id>/', views.tag_delete, name='tag_delete'),
    path('timezone/', views.timezone_view, name='timezone'),
    path('timezone/delete/<int:timezone_id>/', views.timezone_delete, name='timezone_delete'),
    path('operator_cods/', views.operator_code, name='operator_cods'),
    path('operator_code/delete/<int:code_id>/', views.operator_code_delete, name='operator_code_delete'),
    path('edit_client/<int:pk>/', views.ClientUpdateView.as_view(), name='edit_client'),
    path('edit_mailing/<int:pk>/', views.MailingUpdateView.as_view(), name='edit_mailing'),
    path('delete_client/<int:client_id>/', views.delet_client, name='delete_client'),
    path('delete_mailing/<int:mailing_id>/', views.delete_mailing, name='delete_mailing'),
    path('mailing_list/', views.mailing_list_view, name='mailing_list'),
    path('login/github/', views.login_github, name='login_github'),
    path('login/github/callback/', views.login_github_callback, name='login_github_callback'),
]
