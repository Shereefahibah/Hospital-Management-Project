from django.urls import path
from hospital import views

urlpatterns=[

  path('',views.homepage,name='homepage'),
  path('navbar',views.navbar,name='navbar'),
  path('aboutus',views.aboutus,name='aboutus'),
  path('contact',views.contact,name='contact'),
  path('doctor_signup',views.doctor_signup,name='doctor_signup'),
  path('createdoctor',views.create_doctor,name='create_doctor'),
  path('editdoctor/<int:x>',views.editdoctor,name='editdoctor'),
  path('edit_doctor/<int:x>',views.edit_doctor,name='edit_doctor'),
  path('deletedoctor/<int:x>',views.deletedoctor,name='deletedoctor'),
  path('login_page',views.login_page,name='login_page'),
  path('login',views.login,name='login'),
  path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
  path('doctor_dashboard/<int:pk>',views.doctor_dashboard,name='doctor_dashboard'),
  path('doctor_view',views.doctor_view,name='doctor_view'),
  path('patient_signup',views.patient_signup,name='patient_signup'),
  path('create_patient',views.create_patient,name='create_patient'),
  path('patient_login',views.patient_login,name='patient_login'),
  path('patientlogin',views.patientlogin,name='patientlogin'),
  path('patient_dashboard/<int:pk>',views.patient_dashboard,name='patient_dashboard'),
  path('view_patient',views.view_patient,name='view_patient'),
  path('editpatient/<int:x>',views.editpatient,name='editpatient'),
  path('edit_patient/<int:x>',views.edit_patient,name='edit_patient'),
  path('deletepatient/<int:x>',views.deletepatient,name='deletepatient'),
  path('login_page',views.login_page,name='login_page'),
  path('appoinments',views.appoinments,name='appoinments'),
  path('bookappoinments',views.bookappoinments,name='bookappoinments'),
  path('download_pdf/<int:appointment_id>',views.download_pdf,name='download_pdf'),
  path('viewappoinments',views.viewappoinments,name='viewappoinments'),
  path('editappoinments/<int:x>',views.editappoinments,name='editappoinments'),
  path('appointmentedit/<int:x>', views.appointmentedit, name='appointmentedit'),
  path('deleteappoinments/<int:x>',views.deleteappoinments,name='deleteappoinments'),
  path('accept/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
  path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
  path('logout',views.logout,name='logout'),
  





]