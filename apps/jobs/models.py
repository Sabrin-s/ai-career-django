from django.db import models
from apps.users.models import User


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    job_url = models.URLField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jobs'

    def __str__(self):
        return f"{self.role} at {self.company}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('phone_screen', 'Phone Screen'),
        ('interview', 'Interview'),
        ('technical', 'Technical Round'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='saved')
    applied_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.email} → {self.job} [{self.status}]"
