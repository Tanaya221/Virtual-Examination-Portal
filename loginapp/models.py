from django.db import models

# Create your models here.

class Question(models.Model):

    qno=models.IntegerField(primary_key=True)
    qtxt=models.CharField(max_length=100)
    ans=models.CharField(max_length=100)
    op1=models.CharField(max_length=100)
    op2=models.CharField(max_length=100)
    op3=models.CharField(max_length=100)
    op4=models.CharField(max_length=100)
    sub=models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.qno,self.qtxt,self.ans,self.op1,self.op2,self.op3,self.op4,self.sub}"
    
    class Meta:
        db_table='question'



class Result(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    subject=models.CharField(max_length=50)
    score=models.IntegerField()
    login_date=models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.username,self.subject,self.score,self.login_date}"
    
    class Meta:
        db_table="result"

        