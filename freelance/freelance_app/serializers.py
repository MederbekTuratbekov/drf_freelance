from rest_framework import serializers
from .models import UserProfile, Skill, Category, Project, Offer, Review
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status', 'date_registered')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
# ---------------------------------------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'role', 'bio', 'avatar', 'skills')
        extra_kwargs = {'password': {'write_only': True}}

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'skill_name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name',)

class ProjectSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    skills_required = SkillSerializer(many=True, read_only=True, allow_null=True)
    client = UserProfileSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'budget', 'deadline', 'status')

class ProjectDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    skills_required = SkillSerializer(many=True, read_only=True, allow_null=True)
    client = UserProfileSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'budget', 'deadline', 'status', 'category', 'skills_required', 'client')

class OfferSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    freelancer = UserProfileSerializer(read_only=True)
    class Meta:
        model = Offer
        fields = ('id', 'project', 'freelancer', 'message', 'proposed_budget', 'proposed_deadline')

class ReviewSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    owner_reviewer = UserProfileSerializer(read_only=True)
    target = UserProfileSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'project', 'comment', 'rating_review', 'owner_reviewer', 'target')
