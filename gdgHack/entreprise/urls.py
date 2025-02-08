from django.urls import path
from .views import CreateCompetitionView,ListEnterpriseCompetitionsView , CreateInternshipView , StudentInternshipListView

urlpatterns = [

    path('competition/create/', CreateCompetitionView.as_view(), name='create-competition'),
    path('competitionList/<int:enterprise_id>/', ListEnterpriseCompetitionsView.as_view(), name='list-enterprise-competitions'),
    path('internships/create/', CreateInternshipView.as_view(), name='create-internship'),
    path('internshipsList/<int:enterprise_id>/', StudentInternshipListView.as_view(), name='student-internships'),
    
]
