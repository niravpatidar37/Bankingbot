from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.pdfgen import canvas
from .models import Customer, Account, Transaction, Statement, TransactionEntry, Report, Branch, Loan, CreditCard, BillPayment, Beneficiary, InterestRate, SecurityQuestion, Feedback
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if request.POST['password'] == request.POST['confirmPassword']:
                form.save()
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = form.get_user()
            login(request, user)
            request.session['User'] = username
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    del request.session['User']
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required
def customer_detail(request):
    customer = Customer.objects.get(user=request.user)
    return render(request, 'customer_detail.html', {'customer': customer})

@login_required
def account_detail(request, account_number):
    account = Account.objects.get(account_number=account_number)
    return render(request, 'account_detail.html', {'account': account})

@login_required
def transaction_list(request, account_number):
    account = Account.objects.get(account_number=account_number)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'transaction_list.html', {'transactions': transactions})


@login_required
def deposit_money(request, account_number):
    account = get_object_or_404(Account, account_number=account_number)

    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        if amount > 0:
            account.balance += amount
            account.save()

            # Create a transaction record
            transaction = Transaction.objects.create(account=account, transaction_type='D', amount=amount)
            transaction.save()

            return redirect('transaction_list', account_number=account_number)

    return render(request, 'deposit_money.html', {'account': account})

@login_required
def withdraw_money(request, account_number):
    account = get_object_or_404(Account, account_number=account_number)
    form = WithdrawalForm()

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()

                # Create a transaction record
                transaction = Transaction.objects.create(account=account, transaction_type='W', amount=amount)
                transaction.save()

                return redirect('transaction_list', account_number=account_number)

    return render(request, 'withdraw_money.html', {'account': account, 'form': form})

@login_required
def transfer_money(request, account_number):
    account = get_object_or_404(Account, account_number=account_number)
    form = TransferForm()

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_account_number = form.cleaned_data['recipient_account_number']

            # Check if the recipient account exists
            recipient_account = get_object_or_404(Account, account_number=recipient_account_number)

            if amount <= account.balance:
                account.balance -= amount
                account.save()

                recipient_account.balance += amount
                recipient_account.save()

                # Create a transaction record for sender
                transaction_sender = Transaction.objects.create(account=account, transaction_type='T', amount=amount)
                transaction_sender.save()

                # Create a transaction record for recipient
                transaction_recipient = Transaction.objects.create(account=recipient_account, transaction_type='T', amount=amount)
                transaction_recipient.save()

                return redirect('transaction_list', account_number=account_number)

    return render(request, 'transfer_money.html', {'account': account, 'form': form})

@login_required
def statement_detail(request, statement_id):
    statement = Statement.objects.get(pk=statement_id)
    entries = TransactionEntry.objects.filter(statement=statement)
    return render(request, 'statement_detail.html', {'statement': statement, 'entries': entries})

@login_required
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'report_list.html', {'reports': reports})

@login_required
def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branch_list.html', {'branches': branches})

@login_required
def loan_list(request):
    loans = Loan.objects.filter(account__customer=request.user)
    return render(request, 'loan_list.html', {'loans': loans})

@login_required
def credit_card_detail(request, account_number):
    credit_card = CreditCard.objects.get(account__account_number=account_number)
    return render(request, 'credit_card_detail.html', {'credit_card': credit_card})

@login_required
def bill_payment_list(request):
    bill_payments = BillPayment.objects.filter(customer=request.user)
    return render(request, 'bill_payment_list.html', {'bill_payments': bill_payments})

@login_required
def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.filter(customer=request.user)
    return render(request, 'beneficiary_list.html', {'beneficiaries': beneficiaries})

@login_required
def interest_rate_list(request):
    interest_rates = InterestRate.objects.all()
    return render(request, 'interest_rate_list.html', {'interest_rates': interest_rates})

@login_required
def security_question_list(request):
    security_questions = SecurityQuestion.objects.all()
    return render(request, 'security_question_list.html', {'security_questions': security_questions})

@login_required
def feedback_create(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        feedback = Feedback.objects.create(customer=request.user, subject=subject, message=message)
        feedback.save()
        return redirect('feedback_list')
    return render(request, 'feedback_create.html')

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.filter(customer=request.user)
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})


def generate_statement_pdf(request, statement_id):
    statement = get_object_or_404(Statement, id=statement_id)
    entries = TransactionEntry.objects.filter(statement=statement)

    # Create a response object with PDF mime type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="statement.pdf"'

    # Create the PDF object, using the response object as its file
    p = canvas.Canvas(response)

    # Add content to the PDF
    p.setFont('Helvetica', 12)
    p.drawString(30, 750, f"Statement for Account: {statement.account.account_number}")
    p.drawString(30, 720, f"Period: {statement.start_date} - {statement.end_date}")
    p.drawString(30, 690, "Transaction Entries:")

    # Iterate through the transaction entries and add them to the PDF
    y = 660
    for entry in entries:
        p.drawString(30, y, f"Transaction: {entry.transaction}")
        y -= 30

    # Close the PDF object
    p.showPage()
    p.save()

    return response



#Bot

def chatbot(request):
    response = ''

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        if user_input.lower() == 'hello':
            response = 'Hello! How can I help you?'
        elif user_input.lower() == 'time':
            current_time = datetime.now().strftime('%H:%M:%S')
            response = 'The current time is ' + current_time
        elif user_input.lower() == 'exit':
            response = 'Thank you for using the Bank Chatbot. Goodbye!'
        else:
            response = "I'm sorry, I didn't understand. Could you please rephrase?"

    return render(request, 'bot.html', {'response': response})