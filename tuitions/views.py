from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tuition, Application, Review
from .serializers import TuitionSerializer, ApplicationSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from .models import Review
from rest_framework.permissions import AllowAny

class TuitionListView(generics.ListAPIView):
    serializer_class = TuitionSerializer

    def get_queryset(self):
        student_class = self.request.query_params.get('class')
        queryset = Tuition.objects.filter(is_available=True)
        if student_class:
            queryset = queryset.filter(student_class=student_class)
        return queryset

class TuitionDetailView(generics.RetrieveAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer

class ApplyTuitionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tuition = get_object_or_404(Tuition, pk=pk)
        Application.objects.create(tutor=request.user, tuition=tuition)
        return Response({'message': 'Applied successfully'})

class ApplicantListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        applications = Application.objects.filter(tuition_id=pk)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        app_id = request.data.get('application_id')
        application = get_object_or_404(Application, id=app_id, tuition_id=pk)
        application.is_selected = True
        application.save()
        return Response({'message': 'Applicant selected'})

class CreateReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tuition_id):
        application = get_object_or_404(
            Application, 
            tutor=request.user, 
            tuition_id=tuition_id, 
            is_selected=True
        )

        if hasattr(application, 'review'):
            return Response({'error': 'You have already reviewed this tuition.'}, status=400)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(application=application)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TuitionReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        tuition_id = self.kwargs['tuition_id']
        return Review.objects.filter(application__tuition__id=tuition_id)