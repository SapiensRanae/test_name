from django.urls import path
from apps.core import views as core_views

urlpatterns = [
    path('about/', core_views.about_view, name='about'),
    path('', core_views.welcome_view, name='welcome'),

    path('creator/', core_views.creator_view, name='creator'),
    path('creator/<int:pk>/', core_views.CreatorDetailView.as_view(), name='creator_detail'),

    path('quiz/', core_views.quiz_view, name='quiz'),
    path('quiz/<int:pk>/', core_views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:pk>/delete/', core_views.QuizDeleteView.as_view(), name='quiz_delete'),
    path('quiz/<int:pk>/public-toggle/', core_views.QuizPublicToggleView.as_view(), name='quiz_public_toggle'),
    path('quiz/<int:pk>/results/', core_views.QuizResultsView.as_view(), name='quiz_results'),
    path('quiz/<int:quiz_pk>/results/<int:attempt_pk>/', core_views.QuizAttemptDetailView.as_view(),
         name='quiz_attempt_detail'),
    path('quiz/<int:pk>/collaborators/', core_views.QuizCollaboratorsView.as_view(), name='quiz_collaborators'),

    path('attempts/', core_views.AttemptsAdminListView.as_view(), name='attempts_admin_list'),
    path('attempts/<int:attempt_pk>/', core_views.AttemptsAdminDetailView.as_view(), name='attempts_admin_detail'),

    path('quiz/<int:quiz_pk>/question/create/', core_views.QuestionCreateView.as_view(), name='question_create'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/', core_views.QuestionDetailView.as_view(),
         name='question_detail'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', core_views.QuestionDeleteView.as_view(),
         name='question_delete'),

    path('quiz/<int:pk>/<uuid:token>/', core_views.PublicQuizTakeView.as_view(), name='public_quiz_take'),
    path('quiz/<int:pk>/<uuid:token>/start/', core_views.PublicQuizStartView.as_view(), name='public_quiz_start'),
    path('quiz/<int:pk>/<uuid:token>/submit/', core_views.PublicQuizSubmitView.as_view(), name='public_quiz_submit'),
]
