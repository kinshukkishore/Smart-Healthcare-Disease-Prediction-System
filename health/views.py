from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
import datetime
from collections import Counter

# Create your views here.
def Home(request):
    return render(request,'carousel.html')

def Admin_Home(request):
    doc=0
    pat=0
    feed=0
    dis=0
    for i in Disease.objects.all():
        dis+=1
    for i in Patient.objects.all():
        pat+=1
    for i in Doctor.objects.all():
        doc+=1
    for i in Feedback.objects.all():
        feed+=1
    d = {'doc':doc,'pat':pat,'feed':feed,'dis':dis}
    return render(request,'admin_home.html',d)

def User_Home(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error':error}
    return render(request,'patient_home.html',d)

def Doctor_Home(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error': error}
    return render(request,'doctor_home.html',d)


def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def Gallery(request):
    return render(request,'gallery.html')

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Patient.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
            else:
                stat = Status.objects.get(status="Accept")
                pure=False
                try:
                    pure = Doctor.objects.get(status=stat,user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                else:
                    login(request, user)
                    error="notmember"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            error="pat"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        d = request.POST['dob']
        con = request.POST['contact']
        add = request.POST['add']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type=="Patient":
            Patient.objects.create(user=user,contact=con,address=add,image=im,dob=d)
        else:
            stat = Status.objects.get(status='pending')
            Doctor.objects.create(dob=d,image=im,user=user,contact=con,address=add,status=stat)
        error = "create"
    d = {'error':error}
    return render(request,'register.html',d)

def Add_Doctor(request):
    error = ""
    type=Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        cat = request.POST['type']
        add = request.POST['add']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        stat = Status.objects.get(status='Accept')
        Doctor.objects.create(category=cat,image=im,user=user,contact=con,address=add,status=stat)
        error = "create"
    d = {'error':error,'type':type}
    return render(request,'add_doctor.html',d)

def Add_Disease(request):
    type = Type.objects.all()
    error = ""
    if request.method == 'POST':
        d = request.POST['d_name']
        s = request.POST['sym']
        t = request.POST['type']
        dat = datetime.date.today()
        ty = Type.objects.get(name=t)
        Disease.objects.create(name=d,symptom=s,type=ty)
        error = "create"
    d = {'error':error,'type':type}
    return render(request,'add_disease.html',d)

def Edit_Doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    error = ""
    type = Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        cat = request.POST['type']
        try:
            im = request.FILES['image']
            doc.image=im
            doc.save()
        except:
            pass
        dat = datetime.date.today()
        doc.user.first_name = f
        doc.user.last_name = l
        doc.user.email = e
        doc.contact = con
        doc.category = cat
        doc.address = add
        doc.user.save()
        doc.save()
        error = "create"
    d = {'error':error,'doc':doc,'type':type}
    return render(request,'edit_doctor.html',d)

def Edit_My_deatail(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    type = Type.objects.all()
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        try:
            im = request.FILES['image']
            sign.image = im
            sign.save()
        except:
            pass
        to1 = datetime.date.today()
        sign.user.first_name = f
        sign.user.last_name = l
        sign.user.email = e
        sign.contact = con
        if error != "pat":
            cat = request.POST['type']
            sign.category = cat
            sign.save()
        sign.address = add
        sign.user.save()
        sign.save()
        terror = "create"
    d = {'error':error,'terror':terror,'doc':sign,'type':type}
    return render(request,'edit_profile.html',d)

def Edit_Disease(request,pid):
    doc = Disease.objects.get(id=pid)
    type = Type.objects.all()
    error = ""
    if request.method == 'POST':
        d = request.POST['d_name']
        s = request.POST['sym']
        t = request.POST['type']
        dat = datetime.date.today()
        doc.name = d
        doc.symptom = s
        ty = Type.objects.get(name=t)
        doc.type = ty
        doc.save()
        error = "create"
    d = {'error':error,'doc':doc,'type':type}
    return render(request,'edit_disease.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def View_Doctor(request):
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html',d)

def View_Patient(request):
    patient = Patient.objects.all()
    d = {'patient':patient}
    return render(request,'view_patient.html',d)

def View_Disease(request):
    dis = Disease.objects.all()
    d = {'dis':dis}
    return render(request,'view_disease.html',d)

def View_Feedback(request):
    dis = Feedback.objects.all()
    d = {'dis':dis}
    return render(request,'view_feedback.html',d)

def View_Notification(request):
    dis = Searched_Patient.objects.all()
    d = {'dis':dis}
    return render(request,'view_notify.html',d)

def View_My_Detail(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error': error,'pro':sign}
    return render(request,'profile_doctor.html',d)

def find_doctors(disease):
    type = Disease.objects.filter(name=disease)[0].type
    doctors = Doctor.objects.filter(category=type)
    return doctors

def find_possible_diseases(searched_symptoms):
    possible_diseases = Counter()
    for disease in [d.name for d in Disease.objects.filter(symptom__in=searched_symptoms)]:
        disease_symptoms = [d.symptom for d in Disease.objects.filter(name=disease)]
        missing = False
        for symptom in searched_symptoms:
            if symptom not in disease_symptoms:
                missing = True
                break
        if not missing:
            possible_diseases.update([disease])
    return possible_diseases

def Predict_disease(request,pid):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    a = ""

    li = []
    doc = ""
    count=0
    count2=""
    dis = ""
    symp = ""
    ids = []
    if pid == "Search":
        Searched_symptom2.objects.all().delete()
        if request.method == "POST":
            symptom = request.POST['sym']
            symptoms = set([d.symptom for d in Disease.objects.filter(symptom__icontains=symptom)])
            li = symptoms
            terror = 'start'

    elif pid == "Next":
        if request.method == "POST":
            symptom = request.POST['sym']
            searched_symptoms = [sym.name for sym in Searched_symptom2.objects.all()]
            if symptom not in searched_symptoms:
                Searched_symptom2.objects.create(name=symptom)
                searched_symptoms.append(symptom)

            possible_diseases = find_possible_diseases(searched_symptoms)

            if len(searched_symptoms) >= 5 or len(possible_diseases) == 1:
                dis = possible_diseases.most_common(1)[0][0]
                doc = find_doctors(dis)
                terror = 'end'

                d = {'error': error, 'terror': terror, 'pro': sign, 'li': li, 'count2': count2, 'dis': dis, 'doc': doc}
                return render(request, 'predict_disease.html', d)


            possible_symptoms = set()
            for disease in possible_diseases.keys():
                symptoms = set([d.symptom for d in Disease.objects.filter(name__iexact=disease)
                             if d.symptom not in searched_symptoms])
                possible_symptoms = possible_symptoms.union(symptoms)
            li = possible_symptoms
            terror = 'start'
    else:
        searched_symptoms = [sym.name for sym in Searched_symptom2.objects.all()]
        if len(searched_symptoms) != 0:
            possible_diseases = find_possible_diseases(searched_symptoms)
            possible_diseases = possible_diseases.keys()
            dis = ', '.join(possible_diseases)
            doc = set()
            for disease in possible_diseases:
                doc.update(find_doctors(disease))
            terror = 'end'
            d = {'error': error, 'terror': terror, 'pro': sign, 'li': li, 'count2': count2, 'dis': dis, 'doc': doc}
            return render(request, 'predict_disease.html', d)


    d = {'error': error,'terror': terror,'pro':sign,'li':li,'count2':count2,'dis':dis,'doc':doc}
    return render(request,'predict_disease.html',d)

def View_My_Notification(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    search = Searched_Patient.objects.filter(doctor=sign)
    d = {'error': error,'pro':search}
    return render(request,'notification.html',d)

def delete_doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    doc.delete()
    return redirect('view_doctor')

def delete_notification(request,pid):
    doc = Searched_Patient.objects.get(id=pid)
    doc.delete()
    if request.user.is_staff:
        return redirect('view_notify')
    else:
        return redirect('notification')

def delete_feedback(request,pid):
    doc = Feedback.objects.get(id=pid)
    doc.delete()
    return redirect('view_feedback')

def delete_patient(request,pid):
    doc = Patient.objects.get(id=pid)
    doc.delete()
    return redirect('view_patient')

def delete_disease(request,pid):
    doc = Disease.objects.get(id=pid)
    doc.delete()
    return redirect('view_disease')


def Search_Doctor(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    doc = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    li=[]
    t = ""
    if request.method == "POST":
        t = request.POST['type']
        te = request.POST['tex']
        te1 = te.lower()
        if t == "Name":
            user1 = User.objects.filter(first_name__icontains=te1)|User.objects.filter(last_name__icontains=te1)
            for i in user1:
                li.append(i.id)
            doc= Doctor.objects.all()
        elif t == "Type":
            doc = Doctor.objects.filter(category__icontains=te)
        else:
            doc = Doctor.objects.filter(address__icontains=te)
        for i in doc:
            Searched_Patient.objects.create(user=sign,doctor=i,date1=datetime.datetime.today())
    d = {'error': error,'pro':sign,'li':li,'doc':doc,'t':t}
    return render(request,'search_doctor.html',d)

def sent_feedback(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    to1 = datetime.date.today()
    if request.method == "POST":
        t = request.POST['uname']
        te = request.POST['msg']
        Feedback.objects.create(user=sign,messages=te,date=to1)
        terror = "create"
    d = {'error': error,'user':sign,'terror':terror}
    return render(request,'sent_feedback.html',d)

def Change_Password(request):
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    if not request.user.is_staff:
        try:
            sign = Patient.objects.get(user=user)
            if sign:
                error = "pat"
        except:
            sign = Doctor.objects.get(user=user)
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'data':sign}
    return render(request,'change_password.html',d)

def Assign_Status(request,pid):
    a = Doctor.objects.get(id=pid)
    terror = False
    if request.method =="POST":
        s = request.POST['stat']
        u = request.POST['uname']
        stat = Status.objects.get(status=s)
        a.status = stat
        a.save()
        terror=True
    d = {'prod': a,'terror':terror}
    return render(request,'assign_status.html',d)
