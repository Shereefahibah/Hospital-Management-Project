from django.shortcuts import render
from hospital.models import Doctor,Patient,Appointment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout as django_logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


# Create your views here.
def navbar(request):
    return render(request, 'navbar.html')

def homepage(request):
    return render(request, 'homepage.html')
def aboutus(request):
    return render(request, 'aboutus.html')
def contact(request):
    return render(request, 'contactus.html')

def doctor_signup(request):
    return render(request,"doctorsignup.html")
def create_doctor(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        contact=request.POST['nmbr']
        specification=request.POST['docspec']
        password=request.POST['pswrd']
        cpassword=request.POST['cpswrd']
        image=request.FILES['img']
        email=request.POST['email']
        if not all([first_name, last_name, email, specification, contact, password, cpassword]):
            messages.error(request, 'Please fill in all fields.')
            return redirect('doctorsignup')
        
        if password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('doctorsignup')
        if not (any(char.isupper() for char in password) and
                    any(char.islower() for char in password) and
                    any(char.isdigit() for char in password)):
                messages.error(request, 'Password must contain at least one uppercase letter, one lowercase letter, and one digit.')
                return redirect('doctor_signup')
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Username already exists.')
            return redirect('doctor_signup')
        doctor = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=email,
                        email=email,
                        password = password)
        
        user = User.objects.get(username=email)
        doctor = Doctor(
                        phonenumber = contact,
                        specification = specification,
                        doctorimage=image,
                        doctordetails = user,)     
                            
        doctor.save()
        subject = 'REGISTRATION COMPLETED'
        message = f'Your username is {email} and Password is {password}. You are successfully registered as a doctor in our portal. Thank you for choosing our hospital.'
        recipient = email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
        
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login_page')
    else:  return redirect('doctor_signup')
    
def login_page(request):
    return render(request,"login.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pswrd']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            admin = User.objects.get(username=username)
            if admin.is_staff :
                return redirect('admin_dashboard')
            
            else:
                doctor = Doctor.objects.get(doctordetails=user.id)
                return redirect('doctor_dashboard',doctor.id)
        else:
            messages.info(request,"INVALID CREDENTIALS!!!")
            return redirect('login_page')
@login_required
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')
@login_required
def doctor_dashboard(request,pk):
  doctor = get_object_or_404(Doctor, id=pk, doctordetails=request.user)
    
    # Get all appointments for this doctor
  appointments = Appointment.objects.filter(doctor=doctor)
    
    # Get distinct patients associated with these appointments
  patients = Patient.objects.filter(appointments__in=appointments).distinct()
    
    # Count patients and appointments
  patient_count = patients.count()
  appointment_count = appointments.count()
    
  return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
    })
    
    
def doctor_view(request):
    doctors=Doctor.objects.all()
    return render(request,'viewdoctor.html',{'doctors':doctors})
def editdoctor(request,x):
    doctors=Doctor.objects.get(id=x)   
    return render(request,'editdoctor.html',{'doctors':doctors})
def edit_doctor(request, x):
    
    doctor_obj = get_object_or_404(Doctor, id=x)

    if request.method == 'POST':
        
        user = doctor_obj.doctordetails


        user.first_name = request.POST['docfname']
        user.last_name = request.POST['docsname']
        user.email = request.POST['email']
        user.save()

      
        doctor_obj.specification = request.POST['docspec']
        doctor_obj.phonenumber = request.POST['nmbr']
        doctor_obj.doctorimage=request.FILES.get('img')
        doctor_obj.save()

       
        return redirect('doctor_view')
def deletedoctor(request,x):
   
    doctors=Doctor.objects.get(id=x)
    doctors.delete()
    return redirect('doctor_view')
#PATIENT
def patient_signup(request):
    return render(request, 'patient_signup.html')
def create_patient(request):
      if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        contact=request.POST['nmbr']
        email=request.POST['email']
        gender=request.POST['gender']
        password=request.POST['pswrd']
        cpassword=request.POST['cpswrd']
        image=request.FILES['img']
        if not all([first_name, last_name, email, image, gender, contact, password, cpassword]):
            messages.error(request, 'Please fill in all fields.')
            return redirect('patient_signup')
        
        if password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('patient_signup')
        if not (any(char.isupper() for char in password) and
                    any(char.islower() for char in password) and
                    any(char.isdigit() for char in password)):
                messages.error(request, 'Password must contain at least one uppercase letter, one lowercase letter, and one digit.')
                return redirect('patient_signup')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Username already exists.')
            return redirect('patient_signup')
        patient = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=email,
                    email=email,
                    password = password)  
        user = User.objects.get(username=email)
        patient = Patient(
                        phonenumber=contact,
                        gender=gender,
                        patientimage=image,
                        patientdetails = user)  
                                
        patient.save()
        return redirect('patient_login')
   
      return redirect('patient_signup')
def patientlogin(request):
    return render(request,'patientloginpage.html')
def patient_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pswrd']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            admin = User.objects.get(username=username)
            if admin.is_staff :
                return redirect('admin_dashboard')
            
            else:
                patient = Patient.objects.get(patientdetails=user.id)
                return redirect('patient_dashboard',patient.id)
        else:
            messages.info(request,"INVALID CREDENTIALS!!!")
            return redirect('patientlogin')
@login_required
def patient_dashboard(request,pk):
    patient = Patient.objects.get(id=pk)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request,"patient_dashboard.html",{"patient":patient,'appointments':appointments})
def view_patient(request):
    patients=Patient.objects.all()
    return render(request,'viewpatients.html',{'patients':patients})
def editpatient(request,x):
    patients=Patient.objects.get(id=x)   
    return render(request,'editpatients.html',{'patients':patients})
def edit_patient(request, x):
    
    patient_obj = get_object_or_404(Patient, id=x)

    if request.method == 'POST':
        
        user = patient_obj.patientdetails


        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.save()

      
        patient_obj.gender = request.POST['gender']
        patient_obj.phonenumber = request.POST['nmbr']
        patient_obj.patientimage=request.FILES.get('img')
        patient_obj.save()

       
        return redirect('view_patient')
def deletepatient(request,x):
   
    patients=Patient.objects.get(id=x)
    patients.delete()
    return redirect('view_patient')
#Appointments
def appoinments(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'bookappoinments.html', {'patients': patients, 'doctors': doctors})
def bookappoinments(request):
    if request.method == 'POST':
        patient = request.POST.get('patient')
        getpatient = Patient.objects.get(id=patient)
        
        doctor = request.POST.get('doctor')
        getdoctor = Doctor.objects.get(id=doctor)
        
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        appointment_obj = Appointment.objects.create(doctor=getdoctor, patient=getpatient, date=date, time=time)
        
        subject = 'BOOKING COMPLETED'
        message = f'Your booking for Dr. {getdoctor.doctordetails.first_name} {getdoctor.doctordetails.last_name} is confirmed on {date} at {time}. Thank you for choosing our hospital.'
        recepient = email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recepient])
        messages.success(request, 'Appointment booked successfully.')
        return render(request, 'confirmation.html', {'appointment': appointment_obj})
    return redirect('homepage')
def download_pdf(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Render HTML template
    template = get_template('appoinment_receipt.html')
    context = {'appointment': appointment}
    html_template = template.render(context)

    # Create PDF
    result = BytesIO()
    pdf = pisa.CreatePDF(html_template, dest=result)

    if not pdf.err:
        # Send the PDF as response
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Appointment_Receipt.pdf"'
        return response
    
    return redirect('homepage')
  
   

  
   
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if appointment.status == 'Pending':
        appointment.status = 'Accepted'
        appointment.save()
        
        # Send email to patient
        send_mail(
            'Appointment Accepted',
            f'Your appointment with Dr. {appointment.doctor.doctordetails.first_name} {appointment.doctor.doctordetails.last_name} on {appointment.date} has been accepted.',
            'from@example.com',  
            [appointment.patient.patientdetails.email], 
            fail_silently=False
        )
        
    return redirect('doctor_dashboard', doctor_id=appointment.doctor.pk)

def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if appointment.status == 'Pending':
        appointment.status = 'Rejected'
        appointment.save()
        
        # Send email to patient
        send_mail(
            'Appointment Rejected',
            f'Your appointment with Dr. {appointment.doctor.doctordetails.first_name} on {appointment.date} has been rejected.',
             
            [appointment.patient.patientdetails.email],  
            fail_silently=False,
        )
        
    return redirect('doctor_dashboard', doctor_id=appointment.doctor.pk)
    


def logout(request):
    django_logout(request)
    return redirect('homepage')
def viewappoinments(request):
    appoinments=Appointment.objects.all()
    return render(request,'viewappoinments.html',{'appoinments':appoinments})
def editappoinments(request,x):
    appoinments=Appointment.objects.get(id=x)
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'editappoinments.html', {'patients': patients, 'doctors': doctors, 'appoinments':appoinments})



def appointmentedit(request, x):
    
    appointment_obj = get_object_or_404(Appointment, id=x)
    
    if request.method == 'POST':

        doctor_user = appointment_obj.doctor.doctordetails
        doctor_user.first_name = request.POST['docfname']
        doctor_user.last_name = request.POST['docfname']
        doctor_user.save()

        
        patient_user = appointment_obj.patient.patientdetails
        patient_user.first_name = request.POST['fname']
        patient_user.last_name = request.POST['lname']
        patient_user.save()

       
        appointment_obj.date = request.POST['date']
        appointment_obj.time = request.POST['time']
        appointment_obj.save()

        
        return redirect('viewappointments')
    
def deleteappoinments(request,x):
        appoinments=Appointment.objects.get(id=x)
        appoinments.delete()
        return redirect('viewappoinments')
