
from django.contrib import admin
from django.urls import path
from board.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/',index)
]
