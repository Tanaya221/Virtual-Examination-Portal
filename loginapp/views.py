from django.shortcuts import  render,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from loginapp.models import Question,Result
from django.utils import timezone
from datetime import timedelta


# # Create your views here.

# # -----------------------------------------------------------------------------------------------------
def signup(request):
    if request.method=='GET':
        return render(request,'onlineexam/signup.html')
    
    if request.method=='POST':

        username=request.POST.get('username')
        request.session['username']=username
        
        if User.objects.filter(username=username).exists():
              message='username are already present'
              return render(request,'onlineexam/signup.html',{'message':message})
        else:
            user=User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password'),email=request.POST.get('email'))
            user.save()
            return redirect('/onlineexam/login')
    
    
        
def login(request):
        if request.method=='GET':
            return render(request,'onlineexam/login.html')
        
        user=auth.authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
        
        if user is not None:
            
            auth.login(request,user)
            request.session['ans']={}
            
            request.session['questionindex']=0
            request.session['score']=0
          
            request.session['sub']={}
            
            
        if request.method=='POST':
             username=request.POST.get('username')
             request.session['username']=username
             admin=User.objects.filter(username=username,is_superuser=1).exists()

             if admin:
                 return render(request,'onlineexam/admin.html')
            
             return render(request,'onlineexam/subject.html')
        else:
            messages.error(request,'invalied data')
            return redirect('/login')
       


# --------------------------------------------------------------------------------------------------

def starttest(request):
     request.session['ans']={}
     request.session['questionindex']=0
     subjectname=request.GET['sub']
     request.session['sub']=subjectname
     request.session['qno']=1


     queryset=Question.objects.filter(sub=subjectname).values()
     questionlist=list(queryset)

     request.session['questionlist']=questionlist
     question=questionlist[0]

     qno=request.session['qno']
     return render(request,'onlineexam/question.html',{'question':question,'qno':qno})



def nextpage(request):
    if 'op' in request.GET:
        Qdict = request.session.get('ans', {})
        question_no = request.GET['qno']  
        selected_option = request.GET['op']  
        correct_answer = request.GET['ans']  
        question_text = request.GET['qtxt']  

        Qdict[question_no] = [
            question_no,  
            question_text,  
            correct_answer,  
            selected_option 
        ]

        
        request.session['ans'] = Qdict

   
    queryset = Question.objects.filter(sub=request.session['sub'])
    allquestion = list(queryset)

    if request.session['questionindex'] < len(allquestion) - 1:
        request.session['questionindex'] += 1
        question = allquestion[request.session['questionindex']]
        qno = request.session['questionindex'] + 1

       
        save = request.session.get('ans', {})
        previousanswer = ' '
        if str(question.qno) in save:
            previousanswer = save[str(question.qno)][3] 

        return render(request, 'onlineexam/question.html', {
            'question': question,
            'previousanswer': previousanswer, 
            'qno': qno
        })
    else:
       
        return render(request, 'onlineexam/question.html', {
            'question': allquestion[len(allquestion) - 1]
        })
     


def previouspage(request):
    
    queryset = Question.objects.filter(sub=request.session['sub'])
    allquestion = list(queryset)


    if request.session['questionindex'] > 0:
        request.session['questionindex'] -= 1
    else:
        request.session['questionindex'] = 0

  
    question = allquestion[request.session['questionindex']]
    qno = request.session['questionindex'] + 1 

    save = request.session.get('ans', {})
    previousanswer = ' '  
    if str(question.qno) in save:
        previousanswer = save[str(question.qno)][3]  

    return render(request, 'onlineexam/question.html', {
        'question': question,
        'previousanswer': previousanswer,  
        'qno': qno
    })



def endexam(request):
    if 'ans' in request.session:
        if 'op' in request.GET:
            Qdict=request.session['ans']
            Qdict[request.GET['qno']]=[
                request.GET['qno'],
                request.GET['qtxt'],
                request.GET['ans'],
                request.GET['op']
            ]
        ansdict=request.session['ans']
        lists=ansdict.values()
        request.session['score']=0
        
        for list in lists:
            if list[3]==list[2]:
                request.session['score']=request.session['score']+1

        score=request.session['score']
        username=request.session.get('username')
        
        subjectname=request.session['sub']
        data=Result.objects.create(username=username,subject=subjectname,score=score)
        data.save()
           
        
        wrong=len(lists)-score
        wrong_ans=int(wrong) 
        auth.logout(request)

        return render(request,'onlineexam/result.html',{'score':score,'lists':lists,'wrong_ans':wrong_ans})
    else:
        
        return render(request,'onlineexam/login.html')
    

def result_date(request):
     today=timezone.now().date()
     yesterday=today - timedelta(days=1)

     date_filter=request.POST.get('date_filter')
     specific_date=request.POST.get('specific_date')

     if date_filter=='today':
          data1=Result.objects.filter(login_date=today)
          
     elif date_filter=='yesterday':
          data1=Result.objects.filter(login_date=yesterday)
     elif specific_date:
          specific_date = specific_date
          data1=Result.objects.filter(login_date=specific_date)
     else:
          data1=Result.objects.all()
          
     return render(request,'onlineexam/admin.html',{'data1':data1,'today':today,'yesterday':yesterday})




def dashboard(request):   
     return render(request,'onlineexam/dashboard.html')


def addquestion(request):
     if request.method=="POST":
          qno=request.POST["qno"]
          qtxt=request.POST["qtxt"]
          ans=request.POST["ans"]
          op1=request.POST["op1"]
          op2=request.POST["op2"]
          op3=request.POST["op3"]
          op4=request.POST["op4"]
          sub=request.POST["sub"]

          d=Question.objects.create(qno=qno,qtxt=qtxt,ans=ans,op1=op1,op2=op2,op3=op3,op4=op4,sub=sub)
          d.save()
          return render(request,'onlineexam/dashboard.html')
     return render(request,'onlineexam/addquestion.html')
     
     
def showquestion(request):   
     return render(request,'onlineexam/addquestion.html')

def showquestion2(request):
     return render(request, 'onlineexam/updatequestion.html')




def viewquestion(request):
     q=Question.objects.all()
     return render(request,'onlineexam/viewquestion.html',{'questions':q})


def updatequestion(request):    
     if request.method=="POST":
        
        qno=request.POST.get("qno")
        sub=request.POST.get('sub')
        qtxt=request.POST.get('qtxt')
        ans=request.POST.get('ans')
        op1=request.POST["op1"]
        op2=request.POST["op2"]
        op3=request.POST["op3"]
        op4=request.POST["op4"]
         
        que=Question.objects.get(qno=qno)
        que.sub=sub
        que.qtxt=qtxt
        que.ans=ans
        que.op1=op1
        que.op2=op2
        que.op3=op3
        que.op4=op4
      
        que.save()
        message="Update Successfully!!!"
        return render(request,'onlineexam/dashboard.html',{'message':message})    
     return render(request, 'onlineexam/updatequestion.html')


def deletequestion(request,qno):
     de=Question.objects.get(qno=qno)
     de.delete()
     return render(request, 'onlineexam/delete.html')


def logout(request):
     auth.logout(request)
     return redirect('/signup')


