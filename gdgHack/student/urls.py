# urls.py

from django.urls import path
from .views import StudentProfileCreateView , StudentProfileRetrieveView , CreateTeamProjectView , AddMemberToTeamView ,CreateTaskExchangeView , AddRatingView , AddRatingView , StudentRatingsListView
from .views import SearchJobByTypeView , SearchJobByLocationView , SearchJobBySalaryView , SearchJobByStartDateView , CreateJobOfferView , CreateEnterpriseProfileView , CreateTeamProjectView2 , RegisterStudentView  , RegisterEnterpriseView 
from . import views 

urlpatterns = [
    path('studentprofile/', StudentProfileCreateView.as_view(), name='student-profile-create'), #creat             # check
    path('studentprofile/<int:id>/', StudentProfileRetrieveView.as_view(), name='student-profile-detail'),         #chck
    path('create-teamproject/', CreateTeamProjectView.as_view(),  name='create-teamproject'),
    path('add-member-teamproject/', AddMemberToTeamView.as_view(),  name='create-teamproject'),



    path('virtual_experiences/', views.VirtualExperienceListCreateView.as_view(), name='virtual_experience_list_create'),                  # check
    path('virtual_experiences/<int:student_id>/', views.StudentVirtualExperienceListView.as_view(), name='student_virtual_experiences'),   #check


    path('task_exchanges/create/', CreateTaskExchangeView.as_view(), name='create_task_exchange'),
    path('task_exchanges/<int:student_id>/', views.StudentTaskExchangeListView.as_view(), name='student_task_exchanges'),


    path('ratings/add/', AddRatingView.as_view(), name='add_rating'),  # Add a rating
    #path('ratings/', AddRatingView.as_view(), name='get_student_ratings'),  # Get ratings for a student

    path('ratingsList/<int:student_id>/', StudentRatingsListView.as_view(), name='student-ratings'), # te3 kach student 





    path('jobs/search-by-type/', SearchJobByTypeView.as_view(), name='search_job_by_type'),
    path('jobs/search-by-location/', SearchJobByLocationView.as_view(), name='search_job_by_location'),
    path('jobs/search-by-salary/', SearchJobBySalaryView.as_view(), name='search_job_by_salary'),
    path('jobs/search-by-date/', SearchJobByStartDateView.as_view(), name='search_job_by_date'),

    path('job_offers/create/', CreateJobOfferView.as_view(), name='job_offer_create'),
    path('enterprise_profiles/create/', CreateEnterpriseProfileView.as_view(), name='enterprise_profile_create'),

        path('team_project2/create/', CreateTeamProjectView2.as_view(), name='create-team-project'),
    path('register/student/', RegisterStudentView.as_view(), name='register-student'),
        path('register/enterprise/', RegisterEnterpriseView.as_view(), name='register-enterprise'),




]






