from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.user.username

class Account(models.Model):
    account_number = models.CharField(max_length=10, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.account_number

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('D', 'Deposit'),
        ('W', 'Withdrawal'),
        ('T', 'Transfer'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

class Statement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"Statement for Account: {self.account.account_number}"

class TransactionEntry(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def __str__(self):
        return f"Entry for Transaction: {self.transaction}"

class Report(models.Model):
    GENERATION_TYPES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    )

    report_type = models.CharField(max_length=1, choices=GENERATION_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"Report: {self.report_type}"
    
class Branch(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Loan(models.Model):
    LOAN_TYPES = (
        ('H', 'Home Loan'),
        ('P', 'Personal Loan'),
        ('C', 'Car Loan'),
    )

    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=1, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan - {self.loan_type}"

class CreditCard(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Credit Card - {self.card_number}"
    

class BillPayment(models.Model):
    PAYMENT_STATUS = (
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    biller_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS)

    def __str__(self):
        return f"Bill Payment - {self.biller_name}"
    

class Beneficiary(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=11)

    def __str__(self):
        return self.name

class InterestRate(models.Model):
    account_type = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.account_type

class SecurityQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question

class Feedback(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.customer.username}"