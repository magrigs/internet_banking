from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import role, user, city, state, country
from django.contrib import messages
from django.db import connection
from internet_banking_system.utils import getDropDown, dictfetchall
import json


# login
# def loginCheck(request):
# return render(request, 'logincheck.html')
def test(request, id):
    return render('test.html')


# Dashboard of User
def dashboard(request):
    currentBalance = getData(int(request.session.get('user_id', None)))
    futureBalance = int(currentBalance['account_amount']) + (int(currentBalance['account_amount']) * 0.07 * 1)
    context = {
        "fn": "add",
        "balance": currentBalance['account_amount'],
        "future": futureBalance
    };
    return render(request, 'dashboard.html', context)


# Dashboard of User
def estimated_balance(request):
    currentBalance = getData(int(request.session.get('user_id', None)))
    futureBalance = int(currentBalance['account_amount']) + (int(currentBalance['account_amount']) * 0.07 * 1)
    context = {
        "fn": "add",
        "balance": currentBalance['account_amount'],
        "future": futureBalance
    };
    return render(request, 'estimated_balance.html', context)


# Transactions Reports
def transactions(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM transaction WHERE transaction_user_id =" + str(request.session.get('user_id', None)) + "")
    datalist = dictfetchall(cursor)
    json_output = getTransactionJSON(request)
    graphData = {
        "linecolor": "#152c3f",
        "title": "Transactions",
        "values": json_output
    };
    json_string = json.dumps(graphData)
    context = {
        "datalist": datalist,
        "graphData": json_string,
        "json_output": request.session.get('user_id', None)
    }

    # Message according Salary #
    context['heading'] = "Transactions Details";
    return render(request, 'transaction-list.html', context)


def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;


# Dashboard of User
def transfer(request):
    context = {
        "fn": "add",
        "employeetypelist": getDropDown('users_user', 'user_id'),
    };
    cursor = connection.cursor()
    if (request.method == "POST"):
        # Credit the amount to Destination Account
        currentBalance = getData(request.POST['transfer_user_id'])
        amount = int(currentBalance['account_amount']) + int(request.POST['transfer_amount'])
        cursor.execute("""
            UPDATE account
            SET account_amount=%s WHERE  account_user_id=%s  
        """, (amount, request.POST['transfer_user_id']))

        cursor.execute("""
            INSERT INTO `transaction`
            SET transaction_user_id=%s, transaction_type=%s, transaction_amount=%s, transaction_description=%s, transaction_date=%s   
        """, (request.POST['transfer_user_id'], "Credit", request.POST['transfer_amount'],
              request.POST['transfer_amount'] + " credited to your account", "dfsdf"))

        # Debit the amount from source Account
        context = {
            "fn": "add",
            "data": request.session.get('user_id', None),
            "employeetypelist": getDropDown('users_user', 'user_id'),
        };
        currentBalance = getData(int(request.session.get('user_id', None)))
        amount = int(currentBalance['account_amount']) - int(request.POST['transfer_amount'])
        cursor.execute("""
            UPDATE account
            SET account_amount=%s WHERE  account_user_id=%s  
        """, (amount, request.session.get('user_id', None)))

        cursor.execute("""
            INSERT INTO `transaction`
            SET transaction_user_id=%s, transaction_type=%s, transaction_amount=%s, transaction_description=%s, transaction_date=%s   
        """, (request.session.get('user_id', None), "Debit", request.POST['transfer_amount'],
              request.POST['transfer_amount'] + " debited from your account", "dfsdf"))

        messages.add_message(request, messages.INFO, "Transfer of " + request.POST[
            'transfer_amount'] + "/- has been done succesfully to user account.")

    return render(request, 'transfer.html', context)


def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM account WHERE account_user_id = " + str(id))
    dataList = dictfetchall(cursor)
    return dataList[0];


def getInsertID():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users_user ORDER BY user_id DESC LIMIT 0,1")
    dataList = dictfetchall(cursor)
    dataList = dataList[0]
    return dataList['user_id'];


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def getTransactionJSON(request, one=False):
    cur = connection.cursor()
    cur.execute("SELECT transaction_amount FROM transaction WHERE transaction_user_id =" + str(
        request.session.get('user_id', None)) + "")
    dataList = dictfetchall(cur)
    transactionJson = {'list': []}
    i = 0
    for key in dataList:
        transactionJson['list'].append({"X": i + 1, "Y": int(key['transaction_amount'])})
        i = i + 1
    return transactionJson['list']


# Dashboard of User
def deposit(request):
    currentBalance = getData(int(request.session.get('user_id', None)))
    context = {
        "message": "Please Log in",
        "error": False,
        "data": ""
    }
    cursor = connection.cursor()
    amount = int(currentBalance['account_amount']) + 500

    # Update the Amount
    cursor.execute("""
        UPDATE account
        SET account_amount=%s WHERE  account_user_id=%s  
    """, (amount, request.session.get('user_id', None)))

    # Update the Transactions
    cursor.execute("""
        INSERT INTO `transaction`
        SET transaction_user_id=%s, transaction_type=%s, transaction_amount=%s, transaction_description=%s, transaction_date=%s   
    """, (request.session.get('user_id', None), "Credit", "500", "500 Credited to your account", "dfsdf"))

    messages.add_message(request, messages.INFO, "Your account has been credited with 500/-")

    return redirect('/users/dashboard')


# Create your views here.
def index(request):
   # if (request.session.get('authenticated', False) == True):
       # return redirect('/users/report') le vrai code
     #  return redirect('/users/login')

    context = {
        "message": "Please Log in",
        "error": False
    }
    if (request.method == "POST"):
        try:
            getUser = user.objects.get(user_username=request.POST['username'])
            context['msg'] = getUser
        except:
            context['message'] = "Wrong username"
            context['error'] = True
            return render(request, 'login.html', context)
        if (getUser.user_password == request.POST['password']):
            request.session['authenticated'] = True
            request.session['user_id'] = getUser.user_id
            request.session['user_level_id'] = getUser.user_level_id
            request.session['user_name'] = getUser.user_name
            return redirect('/users/dashboard')
        else:
            context['message'] = "Wrong Password"
            context['error'] = True
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)


def listing(request, userId):
    if (request.session.get('authenticated', False) != True):
        return redirect('/')
    try:
        userlist = user.objects.filter(Q(user_level_id=userId))
    except Exception, e:
        return HttpResponse('Something went wrong. Error Message : ' + str(e))

    context = {
        "showmsg": True,
        "message": "User Updated Successfully",
        "userlist": userlist
    }
    # Message according Users Role #
    if (userId == "1"):
        context['heading'] = "System Admin Report";
    if (userId == "2"):
        context['heading'] = "Manager Report";
    if (userId == "3"):
        context['heading'] = "Employees Report";
    if (userId == "4"):
        context['heading'] = "Accountant Report";
    return render(request, 'user-report.html', context)


def forgot(request):
    return render(request, 'forgotpass.html')


def update(request, userId):
    userDetails = user.objects.get(user_id=userId)

    context = {
        "fn": "update",
        "userdetails": userDetails
    }
    currentUserDetails = user.objects.get(user_id=userId)
    context['sub_heading'] = "Update Details of " + currentUserDetails.user_name;
    # Message according Users Role #
    if (currentUserDetails.user_level_id == 1):
        context['heading'] = "System Admin Management";
    if (currentUserDetails.user_level_id == 2):
        context['heading'] = "Manager Management";
    if (currentUserDetails.user_level_id == 3):
        context['heading'] = "Employee Management";
    if (currentUserDetails.user_level_id == 4):
        context['heading'] = "Accountant Management";

    if (request.method == "POST"):
        try:
            addUser = user(
                user_id=userId,
                user_name=request.POST['user_name'],
                user_email=request.POST['user_email'],
                user_mobile=request.POST['user_mobile'],
                user_level_id="2",
                user_username=request.POST['user_username'],
                user_password=request.POST['user_password'],
                user_ifsc_code=request.POST['user_ifsc_code'],
                user_account_no=request.POST['user_account_no'],
                user_aadhar=request.POST['user_aadhar']
            )

            addUser.save()
        except Exception, e:
            return HttpResponse('Something went wrong. Error Message : ' + str(e))

        context["userdetails"] = user.objects.get(user_id=userId)
        messages.add_message(request, messages.INFO, "Your Account Updated Successfully !!!")
        return render(request, 'user.html', context)
    else:
        return render(request, 'user.html', context)


def link_aadhar_card(request):
    userId = request.session.get('user_id', None)
    userDetails = user.objects.get(user_id=userId)
    cursor = connection.cursor()

    context = {
        "fn": "update",
        "userdetails": userDetails
    }
    currentUserDetails = user.objects.get(user_id=userId)
    context['sub_heading'] = "Update Details of " + currentUserDetails.user_name;
    # Message according Users Role #
    if (request.method == "POST"):
        try:
            cursor.execute("""
                UPDATE users_user
                SET user_aadhar=%s WHERE user_id=%s  
            """, (request.POST['user_aadhar'], userId))
        except Exception, e:
            return HttpResponse('Something went wrong. Error Message : ' + str(e))

        context["userdetails"] = user.objects.get(user_id=userId)
        messages.add_message(request, messages.INFO, "Your Aadhar Card Updated Successfully !!!")
        return render(request, 'aadhar.html', context)
    else:
        return render(request, 'aadhar.html', context)


def add(request):
    cursor = connection.cursor()
    context = {
        "fn": "add",
        "heading": 'Users Management',
        "sub_heading": 'Users',
    }
    if (request.method == "POST"):
        try:
            addUser = user(
                user_name=request.POST['user_name'],
                user_username=request.POST['user_username'],
                user_password=request.POST['user_password'],
                user_email=request.POST['user_email'],
                user_mobile=request.POST['user_mobile'],
                user_level_id=1,
                user_ifsc_code=request.POST['user_ifsc_code'],
                user_account_no=request.POST['user_account_no']
            )
            addUser.save()

            # Insert the Amount
            cursor.execute("""
                INSERT INTO account
                SET account_amount=%s, account_user_id=%s  
            """, ("0", getInsertID()))


        except Exception, e:
            return HttpResponse('Something went wrong. Error Message : ' + str(e))
        messages.add_message(request, messages.INFO,
                             "Your account has been registered successfully. Login with your username and password")
        return redirect('/users/')

    else:
        return render(request, 'user.html', context)


def logout(request):
    request.session['authenticated'] = False
    request.session['user_id'] = False
    request.session['user_level_id'] = False
    request.session['user_name'] = False
    return redirect('/')


def changepassword(request):
    if (request.method == "POST"):
        try:
            addUser = user(
                user_id=request.session.get('user_id', None),
                user_password=request.POST['user_new_password']
            )
            addUser.save(update_fields=["user_password"])
        except Exception, e:
            return HttpResponse('Something went wrong. Error Message : ' + str(e))
        messages.add_message(request, messages.INFO, "Your Password has been changed successfully !!!")
        return render(request, 'change-password.html')

    else:
        return render(request, 'change-password.html')
    return render(request, 'change-password.html')


def delete(request, userId):
    try:
        deleteUser = user.objects.get(user_id=userId)
        deleteUser.delete()
    except Exception, e:
        return HttpResponse('Something went wrong. Error Message : ' + str(e))
    messages.add_message(request, messages.INFO, "User Deleted Successfully !!!")
    return redirect('listing')
