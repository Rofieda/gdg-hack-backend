from django.urls import path
from .views import CreateCompetitionView,ListEnterpriseCompetitionsView

urlpatterns = [

    path('competition/create/', CreateCompetitionView.as_view(), name='create-competition'),
    path('competitionList/<int:enterprise_id>/', ListEnterpriseCompetitionsView.as_view(), name='list-enterprise-competitions'),
    
]
