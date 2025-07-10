from rest_framework import serializers
from .models import Tuition, Application, Review

class TuitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tuition
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'tutor', 'tuition', 'is_selected']

# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['comment', 'rating']

class ReviewSerializer(serializers.ModelSerializer):
    tutor = serializers.CharField(source='application.tutor.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'tutor', 'created_at']
