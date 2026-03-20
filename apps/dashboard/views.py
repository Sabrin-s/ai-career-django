from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from apps.jobs.models import Application
from apps.resume.models import Resume, ResumeAnalysis
from apps.interview.models import InterviewSession


@login_required
def dashboard(request):
    if request.path == '/':
        return redirect('dashboard')

    user = request.user

    # Applications
    apps = Application.objects.filter(user=user)
    total = apps.count()
    by_status = dict(apps.values_list('status').annotate(c=Count('status')).values_list('status', 'c'))
    interview_count = sum([by_status.get('phone_screen', 0), by_status.get('interview', 0), by_status.get('technical', 0)])
    interview_rate = round(interview_count / total * 100, 1) if total else 0
    offer_rate = round(by_status.get('offer', 0) / total * 100, 1) if total else 0
    rejection_rate = round(by_status.get('rejected', 0) / total * 100, 1) if total else 0
    recent_apps = apps.order_by('-updated_at').select_related('job')[:5]

    # Resume
    active_resume = Resume.objects.filter(user=user, is_active=True).first()
    latest_analysis = ResumeAnalysis.objects.filter(resume__user=user).order_by('-analyzed_at').first()

    # Interview
    sessions = InterviewSession.objects.filter(user=user, is_completed=True)
    total_sessions = sessions.count()
    avg_score = sessions.aggregate(avg=Avg('average_score'))['avg'] or 0
    best_session = sessions.order_by('-average_score').first()
    category_scores = list(sessions.values('category').annotate(avg_score=Avg('average_score')))

    return render(request, 'dashboard/dashboard.html', {
        'total_apps': total,
        'by_status': by_status,
        'interview_rate': interview_rate,
        'offer_rate': offer_rate,
        'rejection_rate': rejection_rate,
        'recent_apps': recent_apps,
        'active_resume': active_resume,
        'latest_analysis': latest_analysis,
        'total_sessions': total_sessions,
        'avg_score': round(avg_score, 1),
        'best_session': best_session,
        'category_scores': category_scores,
    })
