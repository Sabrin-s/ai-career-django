from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resume, ResumeAnalysis
from .utils import (extract_text_from_pdf, extract_skills, extract_education,
                    extract_experience, calculate_match_score, generate_suggestions)


@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    analyses = ResumeAnalysis.objects.filter(resume__user=request.user)[:10]
    latest = analyses.first()
    return render(request, 'resume/resume.html', {
        'resumes': resumes,
        'analyses': analyses,
        'latest': latest,
    })


@login_required
def resume_upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'Please select a PDF file.')
            return redirect('resume')
        if not file.name.lower().endswith('.pdf'):
            messages.error(request, 'Only PDF files are accepted.')
            return redirect('resume')
        if file.size > 5 * 1024 * 1024:
            messages.error(request, 'File must be under 5MB.')
            return redirect('resume')

        extracted_text = extract_text_from_pdf(file)
        skills = extract_skills(extracted_text)
        education = extract_education(extracted_text)
        experience = extract_experience(extracted_text)

        Resume.objects.filter(user=request.user, is_active=True).update(is_active=False)
        Resume.objects.create(
            user=request.user,
            file=file,
            original_filename=file.name,
            extracted_text=extracted_text,
            extracted_skills=skills,
            extracted_education=education,
            extracted_experience=experience,
        )
        messages.success(request, f'Resume uploaded! Found {len(skills)} skills.')
    return redirect('resume')


@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.file.delete()
    resume.delete()
    messages.success(request, 'Resume deleted.')
    return redirect('resume')


@login_required
def resume_analyze(request):
    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        job_description = request.POST.get('job_description', '')
        job_title = request.POST.get('job_title', '')

        if len(job_description) < 50:
            messages.error(request, 'Job description must be at least 50 characters.')
            return redirect('resume')

        resume = get_object_or_404(Resume, pk=resume_id, user=request.user)
        score, matched, missing = calculate_match_score(resume.extracted_text, job_description)
        suggestions = generate_suggestions(missing, score)

        ResumeAnalysis.objects.create(
            resume=resume,
            job_description=job_description,
            job_title=job_title,
            match_score=score,
            matched_skills=matched,
            missing_skills=missing,
            suggestions=suggestions,
        )
        messages.success(request, f'Analysis complete! Match score: {score}%')
    return redirect('resume')


@login_required
def skill_gap(request):
    resumes = Resume.objects.filter(user=request.user)
    selected_id = request.GET.get('resume_id')
    gap = None
    selected_resume = None

    if selected_id:
        selected_resume = Resume.objects.filter(pk=selected_id, user=request.user).first()
        gap = ResumeAnalysis.objects.filter(resume__user=request.user, resume_id=selected_id).first()
    elif resumes.exists():
        selected_resume = resumes.filter(is_active=True).first() or resumes.first()
        gap = ResumeAnalysis.objects.filter(resume__user=request.user).first()

    return render(request, 'skills/skills.html', {
        'resumes': resumes,
        'gap': gap,
        'selected_resume': selected_resume,
    })
