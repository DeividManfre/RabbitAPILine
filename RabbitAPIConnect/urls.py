from django.contrib import admin
from django.urls import path
from lineapi_core.views import SendMessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
]
