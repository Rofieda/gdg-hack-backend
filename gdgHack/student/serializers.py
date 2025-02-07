# serializers.py

from rest_framework import serializers
from account.models import StudentProfile, Skill ,TeamProject , VirtualExperience , Project , TaskExchange , StudentRating , JobOffer , EnterpriseProfile , TeamMembership , TeamMembership

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']

class StudentProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)  # Nested skills representation

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'bio', 'skills', 'phone', 'email', 'university']



class TeamProjectSerializer(serializers.ModelSerializer):
    students = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = TeamProject
        fields = ['id', 'title', 'description', 'students']

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        team_project = TeamProject.objects.create(**validated_data)
        return team_project




class VirtualExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualExperience
        fields = '__all__'  # This will serialize all fields in the model

    # Optional: You can add custom validation or other logic here


class TaskExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskExchange
        fields = ['id', 'student2', 'task1', 'task2', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']



class StudentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRating
        fields = ['review' , 'rating' ,'student' ,'enterprise']  # Include all fields





class EnterpriseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseProfile
        fields = ['id', 'user', 'description', 'phone', 'email', 'industry', 'location']

    def validate(self, data):
        # You can add custom validation logic here if necessary
        return data

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = '__all__'  # Includes all fields from the JobOffer model

    def validate(self, data):
        # You can add custom validation logic here if necessary
        if data.get('job_type') not in ['full-time', 'part-time', 'internship']:
            raise serializers.ValidationError("Invalid job type.")
        return data
    

























class TeamProjectSerializer(serializers.ModelSerializer):
    members = serializers.ListField(write_only=True, child=serializers.IntegerField())

    class Meta:
        model = TeamProject
        fields = ['id', 'title', 'description', 'created_at', 'members']

    def create(self, validated_data):
        members_ids = validated_data.pop('members', [])
        user = self.context['request'].user

        # Get the student profile of the connected user
        student = StudentProfile.objects.get(user=user)

        # Ensure at least one member is added
        if not members_ids or student.id not in members_ids:
            raise serializers.ValidationError("A team must have at least 2 members including the creator.")

        # Create the TeamProject
        team_project = TeamProject.objects.create(**validated_data)

        # Add all members to TeamMembership (ensuring no duplicates)
        unique_members_ids = set(members_ids)  # Ensure no duplicates in request
        for student_id in unique_members_ids:
            student_instance = StudentProfile.objects.get(id=student_id)
            TeamMembership.objects.get_or_create(student=student_instance, team_project=team_project)

        return team_project
    




#################################################################################################""
#entrprise part 

class EntrpriseProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)  # Nested skills representation

    class Meta:
        model = EnterpriseProfile
        fields = ['id', 'user', 'location', 'industry', 'phone', 'email', 'description' ]
    


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'  # Include all fields