from rest_framework import serializers
from account.models import JobOffer , Competition

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


