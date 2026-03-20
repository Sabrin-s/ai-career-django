from django.contrib import admin
from .models import QuestionBank, InterviewSession, InterviewLog

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('category', 'difficulty', 'question')
    list_filter = ('category', 'difficulty')

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'average_score', 'is_completed', 'started_at')

@admin.register(InterviewLog)
class InterviewLogAdmin(admin.ModelAdmin):
    list_display = ('session', 'score', 'answered_at')
