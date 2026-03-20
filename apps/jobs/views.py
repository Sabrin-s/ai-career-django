from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Job, Application


@login_required
def jobs_list(request):
    apps = Application.objects.filter(user=request.user).select_related('job')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    if status_filter:
        apps = apps.filter(status=status_filter)
    if search:
        apps = apps.filter(Q(job__company__icontains=search) | Q(job__role__icontains=search))

    total = Application.objects.filter(user=request.user).count()
    by_status = dict(Application.objects.filter(user=request.user)
                     .values_list('status').annotate(c=Count('status')).values_list('status', 'c'))
    interview_count = sum([by_status.get('phone_screen', 0), by_status.get('interview', 0), by_status.get('technical', 0)])
    interview_rate = round(interview_count / total * 100, 1) if total else 0

    return render(request, 'jobs/jobs.html', {
        'applications': apps,
        'status_choices': Application.STATUS_CHOICES,
        'status_filter': status_filter,
        'search': search,
        'total': total,
        'by_status': by_status,
        'interview_rate': interview_rate,
        'offer_count': by_status.get('offer', 0),
        'rejected_count': by_status.get('rejected', 0),
    })


@login_required
def job_add(request):
    if request.method == 'POST':
        job = Job.objects.create(
            user=request.user,
            company=request.POST.get('company'),
            role=request.POST.get('role'),
            description=request.POST.get('description', ''),
            location=request.POST.get('location', ''),
            job_url=request.POST.get('job_url', ''),
            salary_range=request.POST.get('salary_range', ''),
        )
        applied_date = request.POST.get('applied_date') or None
        follow_up_date = request.POST.get('follow_up_date') or None
        Application.objects.create(
            user=request.user,
            job=job,
            status=request.POST.get('status', 'applied'),
            applied_date=applied_date,
            follow_up_date=follow_up_date,
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Application added successfully!')
    return redirect('jobs')


@login_required
def job_update_status(request, pk):
    if request.method == 'POST':
        app = get_object_or_404(Application, pk=pk, user=request.user)
        app.status = request.POST.get('status', app.status)
        app.notes = request.POST.get('notes', app.notes)
        app.save()
        messages.success(request, 'Status updated.')
    return redirect('jobs')


@login_required
def job_delete(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    app.job.delete()
    messages.success(request, 'Application deleted.')
    return redirect('jobs')
