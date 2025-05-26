from django.contrib.auth.models import AbstractUser
from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.skill_name}'

class UserProfile(AbstractUser):
    CHOICES_ROLE = (
        ('client', 'client'),
        ('freelancer', 'freelancer'))
    role = models.CharField(choices=CHOICES_ROLE, default='client')
    bio = models.CharField(blank=True, null=True)
    avatar = models.FileField(upload_to='avatar/',blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.role}'

class SocialLinks(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    social_name = models.CharField(max_length=20, blank=True, null=True)
    social_links = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} {self.social_name}'

class Category(models.Model):
    category_name  = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.category_name}'

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    budget = models.DecimalField(max_digits=7, decimal_places=0)
    deadline = models.DateField()
    CHOICES_STATUS = (
        ('open', 'open'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'))
    status = models.CharField(choices=CHOICES_STATUS, default='open')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    skills_required = models.ManyToManyField(Skill)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.budget}'

class Offer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=50, blank=True, null=True)
    proposed_budget = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    proposed_deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.freelancer} {self.project}'

class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    rating_review = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    owner_review = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner_reviewer')
    target = models.ForeignKey(UserProfile, models.CASCADE, related_name='target')

    def __str__(self):
        return f'{self.owner_review} {self.project} {self.rating_review}'
