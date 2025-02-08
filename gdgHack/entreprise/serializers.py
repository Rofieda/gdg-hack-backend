from rest_framework import serializers
from account.models import JobOffer , Competition , Hackathon , Internship


class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'  # Include all fields, modify if needed




class JobOfferSerializer(serializers.ModelSerializer):
    enterprise_name = serializers.CharField(source='enterprise.name', read_only=True)  # Include enterprise name

    class Meta:
        model = JobOffer
        fields = [
            'id',
            'enterprise',
            'enterprise_name',
            'title',
            'description',
            'requirements',
            'salary',
            'location',
            'job_type',
            'date_start_job'
        ]




class CompetitionSerializer(serializers.ModelSerializer):
    enterprise_name = serializers.CharField(source='enterprise.name', read_only=True)  # Fetch enterprise name

    class Meta:
        model = Competition
        fields = '__all__'


class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'


