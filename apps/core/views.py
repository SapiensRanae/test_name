import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.views import View

from apps.core.Forms.CreatorForm import CreatorForm
from apps.core.Forms.QuestionForm import QuestionForm
from apps.core.Forms.QuizForm import QuizForm
from apps.core.models import Creator, Question, Quiz, QuizAttempt, QuizAttemptAnswer, QuizCollaborator


def _parse_answer_options(question):
    try:
        options = json.loads(question.answerOptions or '[]')
        if not isinstance(options, list):
            return []
        return options[:6]
    except Exception:
        return []


def _is_admin(user):
    return user.is_authenticated and getattr(user, 'role', '') == 'admin'


def _is_creator(user, creator):
    return user.is_authenticated and user.email and user.email.casefold() == creator.email.casefold()


def _can_access_creator(user, creator):
    return _is_admin(user) or _is_creator(user, creator)


def _can_access_quiz(user, quiz):
    if _is_admin(user):
        return True
    if not user.is_authenticated or not user.email:
        return False
    if quiz.creator.filter(email__iexact=user.email).exists():
        return True
    return quiz.collaborators.filter(creator__email__iexact=user.email, role__in=['owner', 'editor']).exists()


def _can_view_results(user, quiz):
    if _is_admin(user):
        return True
    if not user.is_authenticated or not user.email:
        return False
    if quiz.creator.filter(email__iexact=user.email).exists():
        return True
    return quiz.collaborators.filter(creator__email__iexact=user.email,
                                     role__in=['owner', 'editor', 'results_viewer']).exists()


def about_view(request):
    return render(request, 'about-project.html')


def welcome_view(request):
    quizzes = []
    if request.user.is_authenticated and request.user.email:
        if _is_admin(request.user):
            quizzes = Quiz.objects.all().order_by('-createdAt')[:10]
        else:
            quizzes = Quiz.objects.filter(
                creator__email__iexact=request.user.email,
                publicTokenEnabled=True
            ).order_by('-createdAt')[:10]
    return render(request, 'core/welcome.html', {'quizzes': quizzes})


def creator_view(request):
    if not _is_admin(request.user):
        return redirect('welcome')

    errors = {}
    if request.method == 'POST':
        form = CreatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('creator')
        else:
            errors = form.errors
    else:
        form = CreatorForm()

    creators = Creator.objects.all()
    return render(request, 'core/creator.html', {"errors": errors, "form": form, "creators": creators})


def quiz_view(request):
    if not request.user.is_authenticated:
        return redirect('welcome')

    errors = {}
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            if not _is_admin(request.user) and request.user.email:
                creator, _ = Creator.objects.get_or_create(email=request.user.email)
                quiz.creator.add(creator)
            return redirect('quiz')
        else:
            errors = form.errors
    else:
        form = QuizForm()

    if _is_admin(request.user):
        quizzes = Quiz.objects.all()
    else:
        quizzes = Quiz.objects.filter(creator__email__iexact=request.user.email)
    return render(request, 'core/quiz.html', {"errors": errors, "form": form, "quizzes": quizzes})


class CreatorDetailView(View):
    def get(self, request, pk):
        creator = get_object_or_404(Creator, pk=pk)
        if not _can_access_creator(request.user, creator):
            return redirect('welcome')
        quizzes = Quiz.objects.filter(creator=creator)
        form = CreatorForm(instance=creator)
        return render(
            request,
            'core/creator_detail.html',
            {'creator': creator, 'form': form, 'quizzes': quizzes}
        )

    def post(self, request, pk):
        creator = get_object_or_404(Creator, pk=pk)
        if not _can_access_creator(request.user, creator):
            return redirect('welcome')
        form = CreatorForm(request.POST, instance=creator)
        if form.is_valid():
            form.save()
            return redirect('creator_detail', pk=pk)
        quizzes = Quiz.objects.filter(creator=creator)
        return render(
            request,
            'core/creator_detail.html',
            {'creator': creator, 'form': form, 'quizzes': quizzes}
        )


class QuizDetailView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        quiz_form = QuizForm(instance=quiz)
        questions = Question.objects.filter(InQuiz=quiz)
        return render(
            request,
            'core/quiz_detailed.html',
            {'quiz': quiz, 'quiz_form': quiz_form, 'questions': questions}
        )

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        quiz_form = QuizForm(request.POST, instance=quiz)

        if quiz_form.is_valid():
            quiz_form.save()
            return redirect('quiz_detail', pk=pk)

        questions = Question.objects.filter(InQuiz=quiz)
        return render(
            request,
            'core/quiz_detailed.html',
            {'quiz': quiz, 'quiz_form': quiz_form, 'questions': questions}
        )


class QuizDeleteView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        return render(request, 'core/quiz_confirm_delete.html', {'quiz': quiz})

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        quiz.delete()
        return redirect('quiz')


class QuizPublicToggleView(View):
    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        quiz.publicTokenEnabled = not quiz.publicTokenEnabled
        quiz.save(update_fields=['publicTokenEnabled'])
        return redirect('quiz_detail', pk=quiz.id)


class QuestionCreateView(View):
    def get(self, request, quiz_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        form = QuestionForm()
        return render(
            request,
            'core/question_create.html',
            {'quiz': quiz, 'form': form}
        )

    def post(self, request, quiz_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.InQuiz = quiz
            question.save()
            return redirect('quiz_detail', pk=quiz_pk)

        return render(
            request,
            'core/question_create.html',
            {'quiz': quiz, 'form': form}
        )


class QuestionDetailView(View):
    def get(self, request, quiz_pk, question_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        question = get_object_or_404(Question, pk=question_pk, InQuiz=quiz)
        form = QuestionForm(instance=question)
        return render(
            request,
            'core/question_detail.html',
            {'quiz': quiz, 'question': question, 'form': form}
        )

    def post(self, request, quiz_pk, question_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        question = get_object_or_404(Question, pk=question_pk, InQuiz=quiz)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_detail', quiz_pk=quiz_pk, question_pk=question_pk)

        return render(
            request,
            'core/question_detail.html',
            {'quiz': quiz, 'question': question, 'form': form}
        )


class QuestionDeleteView(View):
    def get(self, request, quiz_pk, question_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        question = get_object_or_404(Question, pk=question_pk, InQuiz=quiz)
        return render(
            request,
            'core/question_confirm_delete.html',
            {'quiz': quiz, 'question': question}
        )

    def post(self, request, quiz_pk, question_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        question = get_object_or_404(Question, pk=question_pk, InQuiz=quiz)
        question.delete()
        return redirect('quiz_detail', pk=quiz_pk)


class PublicQuizStartView(View):
    def post(self, request, pk, token):
        quiz = get_object_or_404(Quiz, pk=pk, publicToken=token, publicTokenEnabled=True)
        taker_name = (request.POST.get('takerName') or '').strip()
        if not taker_name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        questions_count = Question.objects.filter(InQuiz=quiz).count()
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user if request.user.is_authenticated else None,
            takerName=taker_name,
            maxScore=questions_count,
        )
        return JsonResponse({'attempt_id': attempt.id})


class PublicQuizTakeView(View):
    def get(self, request, pk, token):
        quiz = get_object_or_404(Quiz, pk=pk, publicToken=token, publicTokenEnabled=True)
        request.session['public_quiz_started_at'] = timezone.now().isoformat()
        questions = list(Question.objects.filter(InQuiz=quiz).order_by('id'))
        context_questions = []
        for q in questions:
            context_questions.append(
                {
                    'id': q.id,
                    'title': q.title,
                    'options': _parse_answer_options(q),
                }
            )

        return render(
            request,
            'core/public_quiz_take.html',
            {
                'quiz': quiz,
                'questions': context_questions,
            },
        )


class PublicQuizSubmitView(View):
    def post(self, request, pk, token):
        quiz = get_object_or_404(Quiz, pk=pk, publicToken=token, publicTokenEnabled=True)
        taker_name = (request.POST.get('takerName') or '').strip()
        attempt_id = request.POST.get('attempt_id')

        if not taker_name:
            return redirect('public_quiz_take', pk=pk, token=token)

        questions = list(Question.objects.filter(InQuiz=quiz).order_by('id'))

        if attempt_id:
            attempt = get_object_or_404(QuizAttempt, pk=attempt_id, quiz=quiz)
            attempt.takerName = taker_name
            attempt.maxScore = len(questions)
        else:
            attempt = QuizAttempt.objects.create(
                quiz=quiz,
                user=request.user if request.user.is_authenticated else None,
                takerName=taker_name,
                maxScore=len(questions),
            )

        results = []
        score = 0
        for q in questions:
            key = f"q_{q.id}"
            selected_raw = request.POST.get(key)
            selected_index = None
            try:
                if selected_raw is not None:
                    selected_index = int(selected_raw)
            except Exception:
                selected_index = None

            is_correct = selected_index is not None and selected_index == q.answerRight
            if is_correct:
                score += 1

            QuizAttemptAnswer.objects.update_or_create(
                attempt=attempt,
                question=q,
                defaults={
                    'selectedIndex': selected_index,
                    'isCorrect': is_correct,
                }
            )

            options = _parse_answer_options(q)
            selected_text = None
            if selected_index is not None and 0 <= selected_index < len(options):
                selected_text = options[selected_index]

            correct_text = None
            if 0 <= q.answerRight < len(options):
                correct_text = options[q.answerRight]

            results.append(
                {
                    'question': q.title,
                    'selectedIndex': selected_index,
                    'selectedText': selected_text,
                    'correctIndex': q.answerRight,
                    'correctText': correct_text,
                    'isCorrect': is_correct,
                    'explanation': q.explanation,
                }
            )

        attempt.score = score
        attempt.submittedAt = timezone.now()
        attempt.save(update_fields=['score', 'submittedAt', 'takerName', 'maxScore'])

        if getattr(settings, 'QUIZ_RESULTS_EMAIL_ENABLED', False):
            to_emails = set(quiz.creator.values_list('email', flat=True))
            to_emails.update(
                quiz.collaborators.filter(role='owner').values_list('creator__email', flat=True)
            )
            to_emails = [e for e in to_emails if e]
            if to_emails:
                subject = f"Quiz submission: {quiz.title}"
                message = f"{taker_name} submitted '{quiz.title}' with score {score}/{len(questions)}."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to_emails, fail_silently=True)

        return render(
            request,
            'core/public_quiz_result.html',
            {
                'quiz': quiz,
                'takerName': taker_name,
                'submittedAt': timezone.now(),
                'score': score,
                'maxScore': len(questions),
                'results': results,
            },
        )


class QuizResultsView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_view_results(request.user, quiz):
            return redirect('welcome')

        attempts = QuizAttempt.objects.filter(quiz=quiz).order_by('-startedAt')
        return render(
            request,
            'core/quiz_results.html',
            {
                'quiz': quiz,
                'attempts': attempts,
            },
        )


class QuizAttemptDetailView(View):
    def get(self, request, quiz_pk, attempt_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        if not _can_view_results(request.user, quiz):
            return redirect('welcome')

        attempt = get_object_or_404(QuizAttempt, pk=attempt_pk, quiz=quiz)
        answers = QuizAttemptAnswer.objects.filter(attempt=attempt).select_related('question').order_by('question_id')

        rows = []
        for ans in answers:
            options = _parse_answer_options(ans.question)
            selected_text = None
            if ans.selectedIndex is not None and 0 <= ans.selectedIndex < len(options):
                selected_text = options[ans.selectedIndex]
            correct_text = None
            if 0 <= ans.question.answerRight < len(options):
                correct_text = options[ans.question.answerRight]
            rows.append(
                {
                    'question': ans.question.title,
                    'selectedText': selected_text,
                    'correctText': correct_text,
                    'isCorrect': ans.isCorrect,
                    'explanation': ans.question.explanation,
                }
            )

        return render(
            request,
            'core/quiz_attempt_detail.html',
            {
                'quiz': quiz,
                'attempt': attempt,
                'rows': rows,
            },
        )


class AttemptsAdminListView(View):
    def get(self, request):
        if not _is_admin(request.user):
            return redirect('welcome')
        attempts = QuizAttempt.objects.all().select_related('quiz', 'user').order_by('-startedAt')
        return render(request, 'core/includes/attempts_admin_list.html', {'attempts': attempts})


class AttemptsAdminDetailView(View):
    def get(self, request, attempt_pk):
        if not _is_admin(request.user):
            return redirect('welcome')
        attempt = get_object_or_404(QuizAttempt, pk=attempt_pk)
        quiz = attempt.quiz
        answers = QuizAttemptAnswer.objects.filter(attempt=attempt).select_related('question').order_by('question_id')

        rows = []
        for ans in answers:
            options = _parse_answer_options(ans.question)
            selected_text = None
            if ans.selectedIndex is not None and 0 <= ans.selectedIndex < len(options):
                selected_text = options[ans.selectedIndex]
            correct_text = None
            if 0 <= ans.question.answerRight < len(options):
                correct_text = options[ans.question.answerRight]
            rows.append(
                {
                    'question': ans.question.title,
                    'selectedText': selected_text,
                    'correctText': correct_text,
                    'isCorrect': ans.isCorrect,
                    'explanation': ans.question.explanation,
                }
            )

        return render(request, 'core/attempts_admin_detail.html', {'quiz': quiz, 'attempt': attempt, 'rows': rows})


class QuizCollaboratorsView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')
        collaborators = quiz.collaborators.select_related('creator').order_by('createdAt')
        creators = Creator.objects.all().order_by('email')
        return render(
            request,
            'core/quiz_collaborators.html',
            {
                'quiz': quiz,
                'collaborators': collaborators,
                'creators': creators,
            },
        )

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        if not _can_access_quiz(request.user, quiz):
            return redirect('welcome')

        action = request.POST.get('action')
        if action == 'add':
            creator_id = request.POST.get('creatorId')
            role = request.POST.get('role')
            if creator_id and role in ['owner', 'editor', 'results_viewer']:
                creator = get_object_or_404(Creator, pk=int(creator_id))
                QuizCollaborator.objects.update_or_create(
                    quiz=quiz,
                    creator=creator,
                    defaults={'role': role},
                )

        if action == 'update':
            collab_id = request.POST.get('collabId')
            role = request.POST.get('role')
            if collab_id and role in ['owner', 'editor', 'results_viewer']:
                collab = get_object_or_404(QuizCollaborator, pk=int(collab_id), quiz=quiz)
                collab.role = role
                collab.save(update_fields=['role'])

        if action == 'remove':
            collab_id = request.POST.get('collabId')
            if collab_id:
                QuizCollaborator.objects.filter(pk=int(collab_id), quiz=quiz).delete()

        return redirect('quiz_collaborators', pk=quiz.id)
