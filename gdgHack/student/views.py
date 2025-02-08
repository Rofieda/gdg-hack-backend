# views.py

from rest_framework import generics
from account.models import StudentProfile ,User , Project , TeamProject , TeamMembership  , VirtualExperience , TaskExchange , StudentRating , JobOffer , EnterpriseProfile , Skill ,Hackathon
from .serializers import StudentProfileSerializer , TeamProjectSerializer ,ProjectSerializer, VirtualExperienceSerializer , TaskExchangeSerializer ,StudentRatingSerializer , JobOfferSerializer , EnterpriseProfileSerializer , HackatonSerializer
 
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from django.db.models import Q


class StudentProfileCreateView(generics.CreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer



class StudentProfileRetrieveView(generics.RetrieveAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    lookup_field = 'id'  # This will allow us to look up by 'id' in the URL

class CreateTeamProjectView(APIView):
    permission_classes = [IsAuthenticated]  # This ensures that the view is protected by authentication

    def post(self, request, *args, **kwargs):
        # Step 1: Get the data for creating the TeamProject instance
        project_title = request.data.get('title')  # Assuming 'title' is the name of the field
        project_description = request.data.get('description')  # Assuming 'description' is the name of the field
        
        # Step 2: Create the TeamProject instance
        team_project = TeamProject.objects.create(
            title=project_title,
            description=project_description,
            created_at=timezone.now()  # Assuming a 'created_at' field in TeamProject model
        )

        # Step 3: Add the current logged-in student to the TeamMembership table as a leader
        student_profile = StudentProfile.objects.get(user=request.user)  # Get student profile via the logged-in user
        
        # Create the first membership for the logged-in student
        TeamMembership.objects.create(
            student=student_profile,
            team_project=team_project,
            role='leader',  # Assuming the logged-in student is the leader
            joined_at=timezone.now()
        )
        
        # Step 4: Add other students to the TeamMembership table
        # Get other student IDs from the request data (e.g., a list of student user IDs)
        other_students_ids = request.data.get('other_students', [])  # List of student user IDs
        
        # Check if there are no other students added
        if not other_students_ids:
            return Response({"error": "You should add at least one student that you have worked with as a team in this project."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        for student_id in other_students_ids:
            try:
                # Fetch each student by their user ID
                other_student = StudentProfile.objects.get(user_id=student_id)
                
                # Check if the student is already a member of this team project
                existing_membership = TeamMembership.objects.filter(
                    student=other_student, 
                    team_project=team_project
                ).exists()
                
                if existing_membership:
                    # If the student is already a member, skip adding them and notify
                    continue  # Skip to the next student in the list

                # Add the student to the team as a member if not already added
                TeamMembership.objects.create(
                    student=other_student,
                    team_project=team_project,
                    role='member',
                    joined_at=timezone.now()
                )

            except StudentProfile.DoesNotExist:
                # Handle case if the student doesn't exist (optional)
                return Response({"error": f"Student with ID {student_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 5: Return a success response after creating the team project and memberships
        return Response({"message": "Team project created successfully."}, status=status.HTTP_201_CREATED)







class AddMemberToTeamView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can add members

    def post(self, request, *args, **kwargs):
        # Step 1: Get the data from the request (team_project_id and student_id)
        team_project_id = request.data.get('team_project_id')  # ID of the team project
        student_id = request.data.get('student_id')  # ID of the student to add
        
        # Step 2: Ensure both fields are provided
        if not team_project_id or not student_id:
            return Response({"error": "Both 'team_project_id' and 'student_id' must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Step 3: Get the TeamProject instance by ID
            team_project = TeamProject.objects.get(id=team_project_id)
        except TeamProject.DoesNotExist:
            return Response({"error": "Team project not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Step 4: Get the StudentProfile instance by student ID
            student_profile = StudentProfile.objects.get(id=student_id)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        # Step 5: Check if the student is already a member of this team project
        existing_membership = TeamMembership.objects.filter(student=student_profile, team_project=team_project).exists()

        if existing_membership:
            return Response({"error": "This student is already a member of the team."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 6: Add the student to the team as a member
        TeamMembership.objects.create(
            student=student_profile,
            team_project=team_project,
            role='member',  # Assuming the role for added members is 'member'
            joined_at=timezone.now()
        )

        # Step 7: Return a success response
        return Response({"message": f"Student {student_profile.user.username} added to the team successfully."}, status=status.HTTP_201_CREATED)
    




class CreateVirtualExperienceView(CreateAPIView):
    queryset = VirtualExperience.objects.all()
    serializer_class = VirtualExperienceSerializer

    def perform_create(self, serializer):
        student_id = self.request.data.get("student")  # Extract student ID from request data

        if not student_id:
            raise ValidationError({"student": "A student ID must be provided."})
        
        try:
            student = StudentProfile.objects.get(id=student_id)
        except StudentProfile.DoesNotExist:
            raise ValidationError({"student": "Invalid student ID. Student does not exist."})

        serializer.save(student=student)


class VirtualExperienceListView(ListAPIView):
    queryset = VirtualExperience.objects.all()
    serializer_class = VirtualExperienceSerializer



from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView


class StudentVirtualExperienceListView(ListAPIView):
    serializer_class = VirtualExperienceSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        print(f"Debug: Student ID from URL: {student_id}")  # Ensure it's correctly passed

        if student_id is None:
            return VirtualExperience.objects.none()

        queryset = VirtualExperience.objects.filter(student__id=student_id)
        print(f"Debug: Found {queryset.count()} virtual experiences for student {student_id}")  # Ensure filtering works

        return queryset






class VirtualExperienceListCreateView(ListCreateAPIView):
    queryset = VirtualExperience.objects.all()
    serializer_class = VirtualExperienceSerializer





class CreateTaskExchangeView(CreateAPIView):
    queryset = TaskExchange.objects.all()
    serializer_class = TaskExchangeSerializer
    authentication_classes = []  # No authentication required
    permission_classes = []  # Allow anyone to access

    def perform_create(self, serializer):
        student1_id = self.request.data.get('student1')  # Get student1 from request
        student2_id = self.request.data.get('student2')  # Get student2 from request

        if not student1_id or not student2_id:
            raise serializers.ValidationError({"error": "Both student1 and student2 are required."})

        # Validate student1 exists
        try:
            student1 = StudentProfile.objects.get(id=student1_id)
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError({"error": "Student1 does not exist."})

        # Validate student2 exists
        try:
            student2 = StudentProfile.objects.get(id=student2_id)
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError({"error": "Student2 does not exist."})

        # Get status from request, default to "pending"
        status_value = self.request.data.get('status', 'pending')
        if status_value not in ['pending', 'completed']:
            raise serializers.ValidationError({"error": "Invalid status."})

        # Save TaskExchange with provided students
        serializer.save(student1=student1, student2=student2, status=status_value)





class StudentTaskExchangeListView(ListAPIView):
    serializer_class = TaskExchangeSerializer

    def get_queryset(self):
        # Get the student ID from the URL
        student_id = self.kwargs.get('student_id')
        
        if not student_id:
            # Return an empty queryset if no student ID is provided
            return TaskExchange.objects.none()

        # Filter the TaskExchange by student1 or student2
        exchanges = TaskExchange.objects.filter(student1_id=student_id) | TaskExchange.objects.filter(student2_id=student_id)
        
        # Return the filtered queryset
        return exchanges

    def list(self, request, *args, **kwargs):
        """
        This is where the queryset is processed and returned.
        It automatically calls get_queryset() and serializes the data.
        """
        # Fetch the filtered queryset
        queryset = self.get_queryset()

        # If no exchanges are found, return a specific message
        if not queryset.exists():
            return Response({"message": "No task exchanges found for this student."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the queryset and return the response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class AddRatingView(CreateAPIView):
    queryset = StudentRating.objects.all()
    serializer_class = StudentRatingSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can rate

    def perform_create(self, serializer):
        serializer.save()  # Just save the provided data without modifying it





class StudentRatingsListView(ListAPIView):
    serializer_class = StudentRatingSerializer

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')  # Get student ID from the URL parameter
        
        if not student_id:
            return StudentRating.objects.none()  # Return an empty queryset if no student_id is provided
        
        return StudentRating.objects.filter(student_id=student_id)







#############################################################################################################################################"
# Recherche filtré not testé 

class SearchJobByTypeView(generics.ListAPIView):
    serializer_class = JobOfferSerializer

    def get_queryset(self):
        job_type = self.request.query_params.get('job_type', None)
        if job_type:
            return JobOffer.objects.filter(job_type=job_type)
        return JobOffer.objects.all()
    


class SearchJobByLocationView(generics.ListAPIView):
    serializer_class = JobOfferSerializer

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        if location:
            return JobOffer.objects.filter(location__icontains=location)
        return JobOffer.objects.all()
    

class SearchJobBySalaryView(generics.ListAPIView):
    serializer_class = JobOfferSerializer

    def get_queryset(self):
        min_salary = self.request.query_params.get('min_salary', None)
        queryset = JobOffer.objects.all()

        if min_salary:
            queryset = queryset.filter(salary__gte=min_salary)

        return queryset


class SearchJobByStartDateView(generics.ListAPIView):
    serializer_class = JobOfferSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            return JobOffer.objects.filter(date_start_job__gte=start_date)
        return JobOffer.objects.all()







class CreateJobOfferView(CreateAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer

    def perform_create(self, serializer):
        # You can add custom logic to set fields before saving
        serializer.save()



class CreateEnterpriseProfileView(CreateAPIView):
    queryset = EnterpriseProfile.objects.all()
    serializer_class = EnterpriseProfileSerializer

    def perform_create(self, serializer):
        # You can add custom logic to set fields before saving
        serializer.save()
















class CreateTeamProjectView2(CreateAPIView):
    queryset = TeamProject.objects.all()
    serializer_class = TeamProjectSerializer
    permission_classes = [IsAuthenticated] 




class RegisterStudentView(CreateAPIView):
    permission_classes = [AllowAny]  # Allows anyone to register

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password')
        fullname = request.data.get('fullname', '')
        bio = request.data.get('bio', '')
        phone = request.data.get('phone', '')
        university = request.data.get('university', '')
        major = request.data.get('major', '')
        year_studying = request.data.get('year_studying', '')
        status_value = request.data.get('status', True)  # Default to True
        skills_names = request.data.get('skills', [])  #  list of skill names

        # Check required fields
        if not email or not password or not fullname or not major or not year_studying:
            return Response({"error": "Email, password, fullname, major, and year_studying are required."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists (case-insensitive)
        if User.objects.filter(email__iexact=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create User
        user = User.objects.create_user(email=email, password=password)
        user.save()

        # Create StudentProfile
        student = StudentProfile.objects.create(
            user=user,
            email=email,
            fullname=fullname,
            bio=bio,
            phone=phone,
            university=university,
            major=major,
            year_studying=year_studying,
            status=status_value
        )

        # Attach skills if provided
        if skills_names:
            skills = []
            for skill_name in skills_names:
                skill, created = Skill.objects.get_or_create(name=skill_name.strip())  # Create skill if not exists
                skills.append(skill)

            student.skills.set(skills)  # Assign skills to student

        return Response({
            "message": "Student registered successfully!",
            "user_id": user.id,
            "student_id": student.id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

    

class RegisterEnterpriseView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')  # Ensure role is included in the request
        name = request.data.get('name', '')
        description = request.data.get('description', '')
        phone = request.data.get('phone', '')
        industry = request.data.get('industry', '')
        location = request.data.get('location', '')
        web_site = request.data.get('web_site', '')  # Fixed typo

        if not email or not password or not role:
            return Response({"error": "Email, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create User
        user = User.objects.create_user(email=email, password=password, role=role)
        user.save()

        # Create EnterpriseProfile
        enterprise = EnterpriseProfile.objects.create(
            user=user,
            name=name,  # Added missing name field
            email=email,
            description=description,
            phone=phone,
            industry=industry,
            location=location,
            web_site=web_site
        )

        return Response({
            "message": "Enterprise registered successfully!",
            "user_id": user.id,
            "enterprise_id": enterprise.id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

    





####################################################################################################################""
#entrprise part 


class EntrpriseProfileRetrieveView(generics.RetrieveAPIView):
    queryset = EnterpriseProfile.objects.all()
    serializer_class = EnterpriseProfileSerializer
    lookup_field = 'id'  



class SearchStudentAvailaibleView(generics.ListAPIView):
    serializer_class = JobOfferSerializer

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        if location:
            return JobOffer.objects.filter(location__icontains=location)
        return JobOffer.objects.all()
    



class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()  # Save project with given data



class StudentProjectsListView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']  # Get student ID from URL
        return Project.objects.filter(student_id=student_id)  # Filter projects by student ID
    



class UserProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is logged in

    def get_queryset(self):
        """
        Retrieve only the projects of the logged-in user.
        """
        return Project.objects.filter(student=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Custom response to return projects of the authenticated user.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 
  



class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
  #  permission_classes = [permissions.IsAuthenticated]  # Ensure user is logged in

    def get_queryset(self):
        """
        Retrieve projects where the student_id matches the ID in the request.
        """
        student_id = self.kwargs.get('id')  # Get the student ID from the URL

        if not student_id:
            return Project.objects.none()  # Return empty if no student ID is provided

        # Retrieve projects where student_id matches the requested ID
        return Project.objects.filter(student_id=student_id)

    def list(self, request, *args, **kwargs):
        """
        Return a list of projects for the given student ID.
        """
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "No projects found for this student."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




class GetStudentIDView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is logged in

    def get(self, request, *args, **kwargs):
        """
        Retrieve the student ID of the authenticated user.
        """
        user = request.user  # Get the authenticated user

        try:
            student_profile = StudentProfile.objects.get(user=user)  # Find the student's profile
            return Response({"student_id": student_profile.id}, status=status.HTTP_200_OK)
        
        except StudentProfile.DoesNotExist:
            return Response({"message": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)








class StudentSearchView(generics.ListAPIView):
    serializer_class = StudentProfileSerializer

    def get_queryset(self):
        """
        Filters students by university, major, year of study, and skills if query parameters are provided.
        """
        queryset = StudentProfile.objects.all()
        university = self.request.query_params.get('university', None)
        major = self.request.query_params.get('major', None)
        year_studying = self.request.query_params.get('year_studying', None)
        skill_name = self.request.query_params.get('skill', None)  # Get skill from request

        if university:
            queryset = queryset.filter(university=university)
        if major:
            queryset = queryset.filter(major=major)
        if year_studying:
            queryset = queryset.filter(year_studying=year_studying)
        if skill_name:
            queryset = queryset.filter(skills__name__icontains=skill_name)  # Filter by skill name

        return queryset




###############################" 
# "



class CreateHackathonView(generics.CreateAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackatonSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        enterprise_id = self.request.data.get("enterprise")  
        try:
            enterprise = EnterpriseProfile.objects.get(id=enterprise_id)
            serializer.save(enterprise=enterprise)  
        except EnterpriseProfile.DoesNotExist:
            return Response(
                {"error": "Enterprise not found."}, status=status.HTTP_400_BAD_REQUEST
            )



class HackathonsByEnterpriseView(generics.ListAPIView):
    serializer_class = HackatonSerializer
 #   permission_classes = [IsAuthenticated]

    def get_queryset(self):
        enterprise_id = self.kwargs['enterprise_id']
        return Hackathon.objects.filter(enterprise__id=enterprise_id) 
    


class StudentGeneralSearchView(ListAPIView):
    serializer_class = StudentProfileSerializer

    def get_queryset(self):
        queryset = StudentProfile.objects.all()
        query = self.request.query_params.get('q', None)

        if query:
            queryset = queryset.filter(
                Q(fullname__icontains=query) |  
                Q(university__icontains=query) |  
                Q(major__icontains=query) |  
                Q(year_studying__icontains=query) |  
                Q(skills__name__icontains=query) |  
                Q(bio__icontains=query) |    
                Q(phone__icontains=query) |    
                Q(email__icontains=query)  | 
                Q(status__icontains=query)
            ).distinct()

        return queryset