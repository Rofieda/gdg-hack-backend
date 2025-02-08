from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.models import  EnterpriseProfile , Competition , Internship
from .serializers import JobOfferSerializer , CompetitionSerializer , HackathonSerializer , InternshipSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView




class CreateCompetitionView(CreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()



class ListEnterpriseCompetitionsView(ListAPIView):
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        enterprise_id = self.kwargs.get('enterprise_id')
        return Competition.objects.filter(enterprise_id=enterprise_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "Aucune compétition trouvée pour cette entreprise."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateInternshipView(generics.CreateAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create internships

    def perform_create(self, serializer):
        enterprise_id = self.request.data.get("enterprise")
        if enterprise_id:
            enterprise_profile = get_object_or_404(EnterpriseProfile, id=enterprise_id)
        else:
            enterprise_profile = get_object_or_404(EnterpriseProfile, user=self.request.user)
        
        serializer.save(enterprise=enterprise_profile)




class StudentInternshipListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, enterprise_id):
        # Ensure the enterprise exists
        enterprise = get_object_or_404(EnterpriseProfile, id=enterprise_id)

        # Fetch all internships related to this enterprise
        internships = Internship.objects.filter(enterprise=enterprise)

        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data)