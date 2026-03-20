from django.db import models
from apps.users.models import User


class QuestionBank(models.Model):
    CATEGORY_CHOICES = [
        ('python', 'Python'), ('java', 'Java'), ('javascript', 'JavaScript'),
        ('django', 'Django'), ('react', 'React'), ('sql', 'SQL'),
        ('system_design', 'System Design'), ('hr', 'HR / Behavioural'),
        ('dsa', 'Data Structures & Algorithms'), ('general', 'General'),
    ]
    DIFFICULTY_CHOICES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    question = models.TextField()
    expected_keywords = models.JSONField(default=list)
    sample_answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question_bank'

    def __str__(self):
        return f"[{self.category}] {self.question[:60]}"


class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=10, default='medium')
    total_questions = models.IntegerField(default=0)
    completed_questions = models.IntegerField(default=0)
    total_score = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'interview_sessions'
        ordering = ['-started_at']


class InterviewLog(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='logs')
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    user_answer = models.TextField()
    score = models.FloatField(default=0.0)
    feedback = models.TextField(blank=True)
    matched_keywords = models.JSONField(default=list)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interview_logs'
