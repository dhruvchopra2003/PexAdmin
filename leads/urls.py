from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:leadId>", views.leadView, name="leadView"),
    path("<str:leadId>/lead", views.finalLead, name="finalLead"),
    path("<str:leadId>/download", views.download_lead, name="downloadLead"),
]
