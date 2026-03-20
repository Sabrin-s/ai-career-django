from django.db import models
from apps.users.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    original_filename = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True)
    extracted_skills = models.JSONField(default=list)
    extracted_education = models.JSONField(default=list)
    extracted_experience = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resumes'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.user.email} - {self.original_filename}"


class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='analyses')
    job_description = models.TextField()
    job_title = models.CharField(max_length=255, blank=True)
    match_score = models.FloatField(default=0.0)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resume_analyses'
        ordering = ['-analyzed_at']
