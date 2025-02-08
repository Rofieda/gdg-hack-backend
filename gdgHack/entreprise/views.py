from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.models import JobOffer, EnterpriseProfile , Competition
from .serializers import JobOfferSerializer , CompetitionSerializer


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