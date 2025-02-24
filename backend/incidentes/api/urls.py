from django.urls import path

from . import view

urlpatterns = [
    path("list/", view.IncidenteListView.as_view(), name="incidente-list"),
]
