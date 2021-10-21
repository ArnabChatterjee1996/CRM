from django.urls import path

from .views import *

urlpatterns = [
    path('person/search/', search_person, name='Search Person with ID'),
    path('person/update/', update_person, name='Update Person with ID'),
    path('person/add/note/', add_note_for_person, name='Add note for a Person with ID'),


    path('v1/health', server_health),

]
