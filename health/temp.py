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
    try:
        a = Searched_symptom2.objects.get(id=1)
    except:
        pass
    if not a:
        a = Searched_symptom2.objects.create(idso="",name="",name1="",name2="",num=0)
    li = []
    doc = ""
    count=0
    count2=""
    dis = ""
    symp = ""
    ids = []
    if pid != "None":
        if request.method == "POST":
            se = request.POST['sym']
            a.name1 += se + ","
            a.name2 += se + ","
            a.save()
            if a.idso:
                for k in a.idso.split(','):
                    if not k:
                        pass
                    else:
                        ids.append(int(k))
                symp = Disease.objects.filter(symptom__icontains=se, id__in=ids)
                for i in symp:
                    e = 0
                    if not str(i.id) in a.idso:
                        a.idso += str(i.id) + ","
                        a.save()
                    c = i.symptom
                    c = c.split(',')
                    for g in c:
                        try:
                            if not g in a.name:
                                if not g in a.name2:
                                    if not g in a.name1:
                                        a.name += g + ","
                                        a.save()
                                        break
                        except:
                            pass
                a.name1 += a.name
                a.save()
                terror = "start"
                count = 0
                if a.name == "":
                    li = a.name2.split(',')[-2]
                    count += 1
                    count2 = li
                else:
                    li = a.name.split(',')
                    a.name = ""
                    a.save()
                    for j in li:
                        if j != "":
                            count += 1
                            count2 = j
                if count == 1:
                    terror = "End"
                    try:
                        dis = Disease.objects.get(symptom__icontains=count2,id__in=ids)
                        doc = Doctor.objects.filter(category=dis.type.name)
                        for o in doc:
                            searched = Searched_Patient.objects.create(doctor=o, user=sign,
                                                                       date1=datetime.datetime.today(),
                                                                       type=dis.type, disease=dis.name,
                                                                       symptom=a.name2)
                    except:
                        pass

                    a.idso = ""
                    a.name1 = ""
                    a.name2 = ""
                    a.name = ""
                    a.num = 0
                    a.save()
            else:
                symp = Disease.objects.filter(symptom__icontains=se)
                for i in symp:
                    a.idso += str(i.id) + ","
                    ids.append(i.id)
                    a.save()
                    c = i.symptom
                    c = c.split(',')
                    f = 0
                    for g in c:
                        try:
                            if not g in a.name:
                                if not g in a.name2:
                                    if not g in a.name1:
                                        a.name += g + ","
                                        a.save()
                                        break
                        except:
                            pass
                a.name1 += a.name
                a.save()
                terror = "start"
                count = 0
                if a.name == "":
                    li = a.name2.split(',')[-2]
                    count += 1
                    count2 = li
                else:
                    li = a.name.split(',')
                    a.name = ""
                    a.save()
                    for j in li:
                        if j != "":
                            count += 1
                            count2 = j
                if count == 1:
                    terror = "End"
                    try:
                        dis = Disease.objects.get(symptom__icontains=count2,id__in=ids)
                        doc = Doctor.objects.filter(category=dis.type.name)
                        for o in doc:
                            searched = Searched_Patient.objects.create(doctor=o, user=sign,
                                                                       date1=datetime.datetime.today(),
                                                                       type=dis.type, disease=dis.name,
                                                                       symptom=a.name1)

                    except:
                        pass
                    a.idso = ""
                    a.name1 = ""
                    a.name2 = ""
                    a.name = ""
                    a.num = 0
                    a.save()

    else:
        terror = "start"
        for k in a.idso.split(','):
            if not k:
                pass
            else:
                ids.append(int(k))
        symp = Disease.objects.filter(id__in=ids)
        for i in symp:
            c = i.symptom
            c = c.split(',')
            for g in c:
                try:
                    if not g in a.name:
                            if not g in a.name2:
                                if not g in a.name1:
                                    a.name += g + ","
                                    a.save()
                                    break
                except:
                    pass
        a.name1 += a.name
        a.save()
        count = 0
        if a.name == "":
            li = a.name2.split(',')[-2]
            count += 1
            count2 = li
        else:
            li = a.name.split(',')
            a.name = ""
            a.save()
            for j in li:
                if j != "":
                    count += 1
                    count2 = j
        if count == 1:
            terror = "End"
            try:
                dis = Disease.objects.get(symptom__icontains=count2,id__in=ids)
                doc = Doctor.objects.filter(category=dis.type.name)
                for o in doc:
                    searched = Searched_Patient.objects.create(doctor=o, user=sign, date1=datetime.datetime.today(),
                                                               type=dis.type, disease=dis.name, symptom=a.name1)
            except:
                pass

            a.idso = ""
            a.name1 = ""
            a.name2 = ""
            a.name = ""
            a.num = 0
            a.save()
    d = {'error': error,'terror': terror,'pro':sign,'li':li,'count2':count2,'dis':dis,'doc':doc}
    return render(request,'predict_disease.html',d)
