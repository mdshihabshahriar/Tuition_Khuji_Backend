from django.urls import path
from .views import TuitionListView, TuitionDetailView, ApplyTuitionView, ApplicantListView, CreateReviewView,TuitionReviewListView

urlpatterns = [
    path('', TuitionListView.as_view()),
    path('<int:pk>/', TuitionDetailView.as_view()),
    path('apply/<int:pk>/', ApplyTuitionView.as_view()),
    path('applicants/<int:pk>', ApplicantListView.as_view()),
    path('review/<int:tuition_id>/', CreateReviewView.as_view()),
    path('all-reviews/<int:tuition_id>/', TuitionReviewListView.as_view(), name='tuition_reviews'),
]
