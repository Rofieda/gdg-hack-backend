from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager that supports user creation with only email, password, and role.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove the default username field
    email = models.EmailField(max_length=100, unique=True,default="email@example.com")
    role = models.CharField(
        max_length=20, 
        choices=[('admin', 'admin'), ('student', 'student'), ('enterprise', 'enterprise')],  # add user roles here 
        default='admin'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Only email is required for user creation

    # Add unique related_name for groups and permissions to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Unique related_name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    # Override the default related_name for user_permissions to avoid conflicts
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()  # Link to custom manager

    def __str__(self):
        return self.email
# User model
#class User(AbstractUser):
 #   email = models.EmailField(unique=True)
  #password = models.CharField(max_length=128)
   # role = models.CharField(max_length=50)  #patient , technicien , admin 








class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name




class StudentProfile(models.Model):
    MAJOR_CHOICES = [
        ("Computer Science", "Computer Science"),
        ("MIT", "MIT"),
        ("Electrical Engineering", "Electrical Engineering"),
        ("Mechanical Engineering", "Mechanical Engineering"),
        ("Civil Engineering", "Civil Engineering"),
        ("Autre", "Autre"),
    ]

    UNIVERSITY_CHOICES = [
        ("ENP", "ENP"),
        ("USTHB", "USTHB"),
        ("ESI", "ESI"),
        ("UMBB", "UMBB"),
        ("Autre", "Autre"),
    ]

    YEAR_CHOICES = [
        ("1st", "1st"),
        ("2nd", "2nd"),
        ("3rd", "3rd"),
        ("4th", "4th"),
        ("Autre", "Autre"),
    ]

    fullname = models.CharField(max_length=100) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, related_name='students', blank=True)  
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    university = models.CharField(max_length=30, choices=UNIVERSITY_CHOICES, blank=True)
    status = models.BooleanField(default=True)
    major = models.CharField(max_length=50, choices=MAJOR_CHOICES)
    year_studying = models.CharField(max_length=20, choices=YEAR_CHOICES)

    def __str__(self):
        return self.user.username

    

class Project(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student') 
    title = models.CharField(max_length=255)  # Added max_length
    description = models.TextField(blank=True, null=True)  # Optional project description
    date_debut = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    date_fin = models.DateTimeField(auto_now_add=True)  # Timestamp for creation


    def __str__(self):
        return self.title
    

class EnterpriseProfile(models.Model):
    name=models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enterprise_profile')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)  # Assuming phone numbers are stored as strings
    email = models.EmailField(unique=True)  # Ensuring email uniqueness
    industry = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    web_site = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username



class TeamProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #members = models.ManyToManyField(StudentProfile, related_name='team_members')

    def __str__(self):
        return self.title



#table de laison between 
class TeamMembership(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    team_project = models.ForeignKey(TeamProject, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('mentor', 'Mentor'),
    ], default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'team_project')  # Prevents duplicate entries

    def __str__(self):
        return f"{self.student.user.username} - {self.team_project.title} ({self.role})"


class VirtualExperience(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='virtual_experiences')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.title


class TaskExchange(models.Model):
    student1 = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='task_exchanges_sent')
    student2 = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='task_exchanges_received')
    task1 = models.CharField(max_length=255)
    task2 = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student1.user.username} ↔ {self.student2.user.username}"


class StudentRating(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='ratings')
    enterprise = models.ForeignKey(EnterpriseProfile, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.IntegerField()
    review = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.rating}/5"


class JobOffer(models.Model):
    JOB_TYPES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('internship', 'Internship'),
    ]
    enterprise = models.ForeignKey(EnterpriseProfile, on_delete=models.CASCADE, related_name='job_offers')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(max_length=15, choices=JOB_TYPES)
    date_start_job = models.DateField()

    def __str__(self):
        return self.title




class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),

    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student.user.username} applied to {self.job.title}"


class Competition(models.Model):
    enterprise = models.ForeignKey(EnterpriseProfile, on_delete=models.CASCADE, related_name='competitions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    prize = models.CharField(max_length=255, blank=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CompetitionParticipation(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('winner', 'Winner'),
        ('lost', 'Lost'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='participations')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='participations')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='registered')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} in {self.competition.title}"













class Hackathon(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    enterprise = models.ForeignKey(
        EnterpriseProfile, 
        on_delete=models.CASCADE, 
        related_name='hackathons'
    )  

    def __str__(self):
        return self.name








