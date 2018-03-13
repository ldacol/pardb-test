from django.urls import path

from . import views

urlpatterns = [
	path('/results/', view.peeringlist, name='results'),
]
