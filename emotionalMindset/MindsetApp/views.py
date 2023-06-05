from django.shortcuts import render,redirect, get_object_or_404
from .forms import PatientForm,ContactForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from emotionalMindset import settings
from django.core.mail import send_mail
from .models import Questions,Patient,Output,Hospital,ChatRoom,Chat
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.http import HttpResponse
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from .models import Patient,Disease
from django.db.models import Count
from django.http import JsonResponse
import numpy as np
from django.core.cache import cache
from django.core.management.base import BaseCommand
from pprint import pprint
# Create your views here.
def homepage(request):
    cache.clear()
    hospital = Hospital.objects.all()[:3]
    return render(request,"MindsetApp/index.html", {'hospital':hospital})
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password1 = request.POST.get("pass1")
        password2 = request.POST.get("pass2")
        if User.objects.filter(username=username):
            messages.error(request,"Username already exists")
            return redirect("/")
        if User.objects.filter(email=email):
            messages.error(request,"Email already exists")
            return redirect("/")
        if len(username)>15:
            messages.error(request,"Username must be under 15 characters")
            return redirect("/")
        if password1 != password2:
            messages.error(request,"Passwords do not match")
            return redirect("/")
        if len(password1)<8:
            messages.error(request,"Password must be atleast 8 characters")
            return redirect("/")
        
        myUser = User.objects.create_user(username,email,password1)
        myUser.first_name = fname
        myUser.last_name = lname

        myUser.save()
        messages.success(request,"Your account has been created successfully")
        return redirect("/login")
    return render(request,"MindsetApp/register.html")

def login_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        user = authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect("/quiz")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/login")
    return render(request,"MindsetApp/login.html")

def logout_request(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("/login")

def patient_register(request):
    if request.method == "POST":
        form =  PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your account has been created successfully")

            patient_name = form.cleaned_data['name']
            # patient_id = form.cleaned_data['id']
            request.session['patient_name'] = patient_name
            request.session['patient_id'] = Patient.objects.latest('id').id
            return redirect("/question")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/patient_register")
        
    return render(request,"MindsetApp/patient_register.html", {'form':PatientForm})  
def quiz(request,disease_id):
    disease_id = get_object_or_404(Disease, pk=disease_id).id
    if request.method == "POST":
        question = Questions.objects.filter(disease_id=disease_id)
        for i in question:
            patient_id = request.POST.get('patient_id')
            disease_id = request.POST.get('disease_id')
            question_id = i.id
            patient = get_object_or_404(Patient, pk=patient_id)
            question = get_object_or_404(Questions, pk=question_id)
            disease = get_object_or_404(Disease, pk=disease_id)
            always = request.POST.get(f'always_{i.id}')
            often = request.POST.get(f'often_{i.id}')
            sometimes = request.POST.get(f'sometimes_{i.id}')
            none = request.POST.get(f'none_{i.id}')
            alwaysValue = 4 if always else 0
            oftenValue = 3 if often else 0
            sometimesValue = 2 if sometimes else 0
            noneValue = 1 if none else 0
            prediction = alwaysValue + oftenValue + sometimesValue + noneValue
            if prediction == 4 or prediction == 3:
                prediction = 'yes'
            else:
                prediction = 'no'
             
            myOutput = Output.objects.create(patient_id=patient,
                                             question_id=question,
                                             always=alwaysValue,
                                             often=oftenValue,
                                             sometimes=sometimesValue,
                                             none=noneValue,
                                             prediction=prediction,
                                             disease_id=disease
                                             )
            myOutput.save()
        
        
        return redirect("/output")
    else:
        patient_id = request.session.get('patient_id',None)
        patient_name = request.session.get('patient_name', None)
        disease_name = get_object_or_404(Disease, pk=disease_id).name
        data = Questions.objects.filter(disease_id=disease_id)
    return render(request,"MindsetApp/question.html",{'data':data,'patient_name':patient_name,'patient_id':patient_id,'disease_id':disease_id, 'disease_name':disease_name})
def output(request):
    #getting the data from the database
    conn = psycopg2.connect(
        host="localhost",
        database="DBemotion",
        user="postgres",
        password="Sudeepa0613$"
        )
    cur = conn.cursor()
    query = 'SELECT patient_id_id, always,none,often,sometimes,prediction FROM public."MindsetApp_output" WHERE patient_id_id = %s'
    patient_id = Patient.objects.latest('id').id
    cur.execute(query,[patient_id])
    rows = cur.fetchall()
    # for preprocessing the data
    X = []
    y = []
    for row in rows:
        feature2 = row[1]
        feature3 = row[2]
        feature4 = row[3]
        feature5 = row[4]

        target = row[5]
        X.append([feature2,feature3,feature4,feature5])
        y.append(target)
    # splitting the data into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # creating the model
    model = DecisionTreeClassifier()
    # training the model
    fitted_data = model.fit(X_train, y_train)
    # predicting the output
    accuracy = fitted_data.score(X_test, y_test) * 100
    predict = fitted_data.predict(X_test)

    #to show the data in the output page
    patient_name = Patient.objects.latest('id')
    disease_id = Output.objects.latest('id').disease_id
    # disease_name = Disease.objects.filter(id=disease_id)
    # if predict == ['yes' '']:
    #     predict = 'You are suffering from depression'    
    # if predict == ['yes' 'yes']:
    #     predict = 'You are suffering from depression'
    #     return predict
    result_data = predict
    result_data = result_data.tolist()
    result_data1 = result_data[0]
    result_data2 = result_data[1]
    if result_data1 == 'yes' and result_data2 == 'yes':
        result_data = 'You are suffering from depression'
    elif result_data1 == 'yes' and result_data2 == 'no':
        result_data = 'You maybe suffering from depression or stressed'
    elif result_data1 == 'no' and result_data2 == 'yes':
        result_data = 'You maybe suffering from depression or stressed'
    elif result_data1 == 'no' and result_data2 == 'no':
        result_data = 'You are not suffering from depression'
    else:
        result_data = 'You are not suffering from depression' 
    always_count = Output.objects.filter(always=4, patient_id_id = patient_id).count()
    often_count = Output.objects.filter(often=3, patient_id_id = patient_id).count()
    sometimes_count = Output.objects.filter(sometimes=2, patient_id_id = patient_id).count()
    none_count = Output.objects.filter(none=1, patient_id_id = patient_id).count()

    return render(request,"MindsetApp/output.html",{'result':result_data, 'patient_id':patient_id, 'accuracy':accuracy, 'always_count':always_count, 
                                                    'often_count':often_count, 'sometimes_count':sometimes_count, 'none_count':none_count, 
                                                    'patient_name':patient_name, 'disease_name':disease_id , 'result_data1':result_data1, 'result_data2':result_data2   })

def question(request):
    disease = Disease.objects.all()
    return render(request,"MindsetApp/quiz.html",{ 'disease': disease })
def about(request):
    return render(request,"MindsetApp/about.html")
def hospital(request):
    hospital = Hospital.objects.all()
    return render(request,"MindsetApp/hospital.html", {'hospital':hospital})
def chatroom(request, hospital_id):
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    messages = Chat.objects.filter(hospital_id=hospital).order_by('created_at')
    return render(request,"MindsetApp/chatroom.html", {'hospital':hospital, 'messages':messages})
def recommendation(request):
    data = request.GET.get('location')
    hospital = Hospital.objects.filter(address__contains=data)
    return render(request,"MindsetApp/recommendation.html", {'hospital':hospital, 'data':data})
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your message has been sent successfully")
            return redirect("/contact")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/contact")
    return render(request,"MindsetApp/contactus.html")
def disease_detail(request, disease_id):
    disease = get_object_or_404(Disease, pk=disease_id)
    return render(request,"MindsetApp/disease_detail.html", {'disease':disease})