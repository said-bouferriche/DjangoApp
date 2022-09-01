import imp
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from expenses.models import Category, Expense
from django.core.paginator import Paginator
# from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='/authentification/login')
def index(request):
    categories=Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user)
    
    context={
        'expenses': expenses
    }
    return render(request,'expenses/index.html',context)

@login_required
def add_expense(request):
    categories=Category.objects.all()
    context={
        'categories' : categories,
        'values' : request.POST
    }
    if request.method=='GET':
        return render(request, 'expenses/add_expenses.html', context)
    
    if request.method=='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        # description=request.POST['description']
        date=request.POST['date_expense']
        category=request.POST['category']
        # values=[amount,description,date,category]
        values = {
            'amount': amount,
            'description': description,
            'date': date,
            'category': category
        }
        missing_values=[]
        message = ''
        for k , V in values.items():
            if V:
                pass
            else:
                missing_values.append(k)
        if len(missing_values)==1:
            for v in missing_values:
                message += str(v) +' is required'
            messages.error(request, message)
            return render(request, 'expenses/add_expenses.html', context)
        elif len(missing_values)>1:
            for v in missing_values:
                message += str(v) +' '
            message +=' are required'
            messages.error(request, message)
            return render(request, 'expenses/add_expenses.html', context)
        Expense.objects.create(amount=amount,description=description,date=date,category=category,owner=request.user)
        messages.success(request,'Expense saved succesfully')
        return redirect('expenses')

@login_required
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories=Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }

    if request.method=='GET':
        return render(request,'expenses/edit_expense.html',context)
    
    if request.method=='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        # description=request.POST['description']
        date=request.POST['date_expense']
        category=request.POST['category']
        # values=[amount,description,date,category]
        values = {
            'amount': amount,
            'description': description,
            'date': date,
            'category': category
        }
        missing_values=[]
        message = ''
        for k , V in values.items():
            if V:
                pass
            else:
                missing_values.append(k)
        if len(missing_values)==1:
            for v in missing_values:
                message += str(v) +' is required'
            messages.error(request, message)
            return render(request, 'expenses/edit_expense.html', context)
        elif len(missing_values)>1:
            for v in missing_values:
                message += str(v) +' '
            message +=' are required'
            messages.error(request, message)
            return render(request, 'expenses/edit_expense.html', context)
        Expense.objects.filter(pk=id).update(amount=amount,description=description,date=date,category=category,owner=request.user)
        messages.success(request,'Expense modified succesfully')
        return redirect('expenses')
    
@login_required
def delete_expense(request,id):
    if request.method=='POST':
        Expense.objects.filter(pk=id).delete()
        
    messages.success(request,'Expense seleted succesfully')
    return redirect('expenses')