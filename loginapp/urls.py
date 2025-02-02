from django.urls import path
from .import views


urlpatterns = [

    path('signup/',views.signup),
    path('login/',views.login),
    path('nextpage/',views.nextpage),
    path('previouspage/',views.previouspage),
    path('endexam/',views.endexam),
    path('logout/',views.logout),
    path('starttest/',views.starttest),
    path('result_date/',views.result_date),
    path('addquestion/',views.addquestion),
    path('showquestion/',views.showquestion),
    path('showquestion2/',views.showquestion2),
    path('dashboard/',views.dashboard),
    path('viewquestion/',views.viewquestion),
    path('updatequestion/',views.updatequestion),
    path('deletequestion/<int:qno>/',views.deletequestion),
    


]