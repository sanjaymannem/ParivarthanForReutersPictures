from django.urls import path
from .views import any_view
urlpatterns = [
		path('<str:value>', any_view),
		path('', any_view),
]
#style="background-image: url('{% static 'translateit/devote1.jfif'%}'); background-position: center; background-repeat: no-repeat;"