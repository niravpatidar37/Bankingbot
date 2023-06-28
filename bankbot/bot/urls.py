from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customer/', views.customer_detail, name='customer_detail'),
    path('account/<str:account_number>/', views.account_detail, name='account_detail'),
    path('account/<str:account_number>/transactions/', views.transaction_list, name='transaction_list'),
    path('account/<str:account_number>/deposit/', views.deposit_money, name='deposit_money'),
    path('account/<str:account_number>/withdraw/', views.withdraw_money, name='withdraw_money'),
    path('account/<str:account_number>/transfer/', views.transfer_money, name='transfer_money'),
    path('statement/<int:statement_id>/', views.statement_detail, name='statement_detail'),
    path('reports/', views.report_list, name='report_list'),
    path('branches/', views.branch_list, name='branch_list'),
    path('loans/', views.loan_list, name='loan_list'),
    path('account/<str:account_number>/credit_card/', views.credit_card_detail, name='credit_card_detail'),
    path('bill_payments/', views.bill_payment_list, name='bill_payment_list'),
    path('beneficiaries/', views.beneficiary_list, name='beneficiary_list'),
    path('interest_rates/', views.interest_rate_list, name='interest_rate_list'),
    path('security_questions/', views.security_question_list, name='security_question_list'),
    path('feedback/create/', views.feedback_create, name='feedback_create'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('statement/<int:statement_id>/pdf/', views.generate_statement_pdf, name='generate_statement_pdf'),
    path('chatbot/', views.chatbot, name='chatbot'),

]

