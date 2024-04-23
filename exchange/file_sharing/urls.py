from django.urls import path, include
from .views import *

urlpatterns = [
    path('', RecordHome.as_view(), name='home'),
    # path('', index, name='home'),
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    #path('post/<slug:post_slug>', show_post, name='post'),
    path('discipline/<slug:discipline_slug>', RecordDiscipline.as_view(), name='discipline'),
    #path('discipline/<int:discipline_id>', show_discipline, name='discipline'),
]
