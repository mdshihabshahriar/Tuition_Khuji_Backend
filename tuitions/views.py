from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tuition, Application, Review
from .serializers import TuitionSerializer, ApplicationSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from .models import Review
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudentParent, IsTutor
from accounts.permissions import IsAdminOrStudentParent

class TuitionListView(generics.ListAPIView):
    serializer_class = TuitionSerializer

    def get_queryset(self):
        student_class = self.request.query_params.get('class')
        queryset = Tuition.objects.filter(is_available=True)
        if student_class:
            queryset = queryset.filter(student_class=student_class)
        return queryset
    
class TuitionCreateView(generics.CreateAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer
    permission_classes = [IsAdminOrStudentParent] 
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class TuitionDetailView(generics.RetrieveAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer

class ApplyTuitionView(APIView):
    permission_classes = [IsTutor]

    def post(self, request, pk):
        tuition = get_object_or_404(Tuition, pk=pk)
        
        if not tuition.is_available:
            return Response({'error': 'This tuition is no longer available.'}, status=400)

        if Application.objects.filter(tutor=request.user, tuition=tuition).exists():
            return Response({'error': 'You have already applied for this tuition.'}, status=400)

        Application.objects.create(tutor=request.user, tuition=tuition)
        return Response({'message': 'Applied successfully'}, status=201)

class ApplicantListView(APIView):
    permission_classes = [IsAdminOrStudentParent]

    def get(self, request, pk):
        tuition = get_object_or_404(Tuition, pk=pk)

        if request.user != tuition.posted_by and not request.user.is_staff:
            return Response({'error': 'You are not authorized to view applicants for this tuition.'}, status=403)

        applications = Application.objects.filter(tuition=tuition)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

class CreateReviewView(APIView):
    permission_classes = [IsStudentParent]

    def post(self, request, tuition_id):
        user = request.user
        tuition = get_object_or_404(Tuition, id=tuition_id, posted_by=user)

        try:
            application = Application.objects.get(tuition=tuition, is_selected=True)
        except Application.DoesNotExist:
            return Response({'error': 'No selected tutor for this tuition.'}, status=400)

        if hasattr(application, 'review'):
            return Response({'error': 'You have already reviewed this tutor.'}, status=400)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(application=application)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class TutorReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tutor_id = self.kwargs['tutor_id']
        return Review.objects.filter(application__tutor__id=tutor_id)

class SelectTutorView(APIView):
    permission_classes = [IsAdminOrStudentParent]

    def post(self, request, pk):
        tuition = get_object_or_404(Tuition, pk=pk)

        if tuition.posted_by != request.user and not request.user.is_staff:
            return Response({"error": "You are not allowed to select tutor for this tuition."}, status=403)

        if tuition.selected_tutor is not None:
            return Response({"error": "A tutor has already been selected for this tuition."}, status=400)

        app_id = request.data.get('application_id')
        if not app_id:
            return Response({"error": "Application ID is required."}, status=400)

        application = get_object_or_404(Application, id=app_id, tuition=tuition)

        if application.tuition != tuition:
            return Response({"error": "Invalid application for this tuition."}, status=400)

        application.is_selected = True
        application.save()

        tuition.selected_tutor = application.tutor
        tuition.is_available = False
        tuition.save()

        return Response({"message": "Tutor selected successfully"})
