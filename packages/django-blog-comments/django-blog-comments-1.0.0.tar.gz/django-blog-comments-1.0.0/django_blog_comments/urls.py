from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('',views.post_comment,name='post_comments')
]
