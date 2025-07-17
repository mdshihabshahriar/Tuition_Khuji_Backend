from rest_framework import serializers
from .models import Tuition, Application, Review

class TuitionSerializer(serializers.ModelSerializer):
    posted_by = serializers.SerializerMethodField()
    
    class Meta:
        model = Tuition
        exclude = ['selected_tutor']
        read_only_fields = ['posted_by']
        
    def get_posted_by(self, obj):
        if obj.posted_by:
            return f"{obj.posted_by.first_name} {obj.posted_by.last_name}"
        return None
    
    def get_selected_tutor(self, obj):
        if obj.selected_tutor:
            return f"{obj.selected_tutor.first_name} {obj.selected_tutor.last_name}"
        return None
    

class ApplicationSerializer(serializers.ModelSerializer):
    tutor_name = serializers.SerializerMethodField()
    tuition_title = serializers.CharField(source='tuition.title', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'tutor_name', 'tuition_title', 'is_selected']
        
    def get_tutor_name(self, obj):
        return f"{obj.tutor.first_name} {obj.tutor.last_name}" if obj.tutor else "N/A"

# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['comment', 'rating']

class ReviewSerializer(serializers.ModelSerializer):
    tutor = serializers.CharField(source='application.tutor.username', read_only=True)
    reviewer = serializers.CharField(source='reviewer.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment','reviewer','tutor', 'created_at']
        read_only_fields = ['tutor', 'created_at']
