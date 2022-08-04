"""defines url patterns for WebLog"""
from django.urls import path
from . import views

app_name = 'WebLog'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),

    #Page for Topics
    path('topics/', views.topics, name='topics'),

    # Page for Specific Topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # Page for adding new Topic
    path('new_topic/', views.new_topic, name='new_topic'),

    # Page for adding new Entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # Page for edditing an entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),





]