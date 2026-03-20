import re
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import QuestionBank, InterviewSession, InterviewLog


def evaluate_answer(user_answer, expected_keywords):
    if not user_answer or not user_answer.strip():
        return 0.0, [], 'No answer provided.'
    answer_lower = user_answer.lower()
    matched = [kw for kw in expected_keywords if re.search(r'\b' + re.escape(kw.lower()) + r'\b', answer_lower)]
    keyword_score = (len(matched) / len(expected_keywords) * 60) if expected_keywords else 0
    word_count = len(user_answer.split())
    length_score = 20 if word_count >= 80 else 15 if word_count >= 40 else 10 if word_count >= 20 else 5 if word_count >= 10 else 0
    structure_score = 0
    for pattern, pts in [(r'\b(first|second|third|finally)\b', 8), (r'\b(because|therefore|however)\b', 6), (r'\b(for example|such as)\b', 6)]:
        if re.search(pattern, answer_lower):
            structure_score = min(structure_score + pts, 20)
    total = round(keyword_score + length_score + structure_score, 2)
    if total >= 80:
        fb = 'Excellent answer!'
    elif total >= 60:
        fb = 'Good answer with room for improvement.'
    elif total >= 40:
        fb = 'Partial answer. Try to be more comprehensive.'
    else:
        fb = 'Weak answer. Review the topic carefully.'
    if matched:
        fb += f' Key concepts covered: {", ".join(matched)}.'
    missing = [kw for kw in expected_keywords if kw not in matched]
    if missing:
        fb += f' Missing: {", ".join(missing[:4])}.'
    return total, matched, fb


@login_required
def interview_home(request):
    categories = []
    for key, label in QuestionBank.CATEGORY_CHOICES:
        count = QuestionBank.objects.filter(category=key).count()
        categories.append({'key': key, 'label': label, 'count': count})
    sessions = InterviewSession.objects.filter(user=request.user)[:10]
    return render(request, 'interview/interview.html', {'categories': categories, 'sessions': sessions})


@login_required
def interview_start(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty', 'medium')
        num_q = int(request.POST.get('num_questions', 5))
        questions = list(QuestionBank.objects.filter(category=category, difficulty=difficulty))
        if not questions:
            messages.error(request, f'No questions found for {category} at {difficulty} difficulty.')
            return redirect('interview')
        selected = random.sample(questions, min(num_q, len(questions)))
        session = InterviewSession.objects.create(
            user=request.user, category=category,
            difficulty=difficulty, total_questions=len(selected)
        )
        request.session['interview_session_id'] = session.id
        request.session['interview_questions'] = [q.id for q in selected]
        request.session['interview_index'] = 0
        return redirect('interview_question')
    return redirect('interview')


@login_required
def interview_question(request):
    session_id = request.session.get('interview_session_id')
    question_ids = request.session.get('interview_questions', [])
    index = request.session.get('interview_index', 0)

    if not session_id or index >= len(question_ids):
        return redirect('interview')

    session = get_object_or_404(InterviewSession, pk=session_id, user=request.user)
    question = get_object_or_404(QuestionBank, pk=question_ids[index])
    feedback = None

    if request.method == 'POST':
        answer = request.POST.get('answer', '')
        score, matched, fb = evaluate_answer(answer, question.expected_keywords)
        InterviewLog.objects.create(
            session=session, question=question,
            user_answer=answer, score=score,
            feedback=fb, matched_keywords=matched
        )
        session.completed_questions += 1
        session.total_score += score
        session.average_score = round(session.total_score / session.completed_questions, 2)
        next_index = index + 1
        if next_index >= len(question_ids):
            session.is_completed = True
            session.completed_at = timezone.now()
            session.save()
            request.session.pop('interview_session_id', None)
            request.session.pop('interview_questions', None)
            request.session.pop('interview_index', None)
            return render(request, 'interview/result.html', {
                'session': session, 'score': score, 'feedback': fb,
                'matched': matched, 'sample_answer': question.sample_answer,
                'question': question,
            })
        else:
            session.save()
            request.session['interview_index'] = next_index
            feedback = {'score': score, 'feedback': fb, 'matched': matched, 'sample_answer': ''}
            question_next = get_object_or_404(QuestionBank, pk=question_ids[next_index])
            return render(request, 'interview/question.html', {
                'session': session, 'question': question_next,
                'index': next_index, 'total': len(question_ids),
                'prev_feedback': feedback,
            })

    return render(request, 'interview/question.html', {
        'session': session, 'question': question,
        'index': index, 'total': len(question_ids),
        'prev_feedback': None,
    })
