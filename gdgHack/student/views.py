# views.py

from rest_framework import generics
from account.models import StudentProfile ,User , Project , TeamProject , TeamMembership  , VirtualExperience , TaskExchange , StudentRating , JobOffer , EnterpriseProfile
from .serializers import StudentProfileSerializer , TeamProjectSerializer ,ProjectSerializer, VirtualExperienceSerializer , TaskExchangeSerializer ,StudentRatingSerializer , JobOfferSerializer , EnterpriseProfileSerializer
 
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
        student1_id = self.request.user.id  # Assuming the logged-in user is student1
        student2_id = self.request.data.get('student2')  # ID of the student to exchange with

        # Validate student1 exists (this is usually the logged-in user)
        try:
            student1 = StudentProfile.objects.get(id=student1_id)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student1 with given ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate student2 exists
        try:
            student2 = StudentProfile.objects.get(id=student2_id)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student2 with given ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Get status from request, default to "pending"
        status_value = self.request.data.get('status', 'pending')
        if status_value not in ['pending', 'completed']:
            return Response({"error": "Invalid status. Choose 'pending' or 'completed'."}, status=status.HTTP_400_BAD_REQUEST)

        # Save TaskExchange with provided students
        task_exchange = serializer.save(student1=student1, student2=student2, status=status_value)

        # Return the newly created task exchange in the response
        return Response(TaskExchangeSerializer(task_exchange).data, status=status.HTTP_201_CREATED)




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
        # Get the authenticated user
        user = self.request.user

        # Find the enterprise linked to this user
        try:
            enterprise = EnterpriseProfile.objects.get(user=user)
        except EnterpriseProfile.DoesNotExist:
            return Response({"error": "You must be an enterprise to add a rating."}, status=status.HTTP_403_FORBIDDEN)

        # Save the rating with the retrieved enterprise ID
        serializer.save(enterprise=enterprise)






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
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fix: Use email instead of username
        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Fix: Remove username, only use email and password
        user = User.objects.create_user(email=email, password=password)
        user.save()

        # Create StudentProfile
        student = StudentProfile.objects.create(user=user, email=email)

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
        role = request.data.get('role')  # Assuming you have a role field in the User model
        description = request.data.get('description', '')
        phone = request.data.get('phone', '')
        industry = request.data.get('industry', '')
        location = request.data.get('location', '')

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
            email=email,
            description=description,
            phone=phone,
            industry=industry,
            location=location
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