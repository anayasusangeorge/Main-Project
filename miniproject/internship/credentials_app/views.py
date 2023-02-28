from django.contrib import messages
from django.shortcuts import render, redirect
from credentials_app.models import  user_reg,user_logins,c
from hashlib import sha256



def Home(request):
    return render(request,'Home.html')
def LOGIN(request):
    return render(request, 'login.html')
def REG(request):
    return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        pincode = request.POST['pincode']
        gender = request.POST['gender']
        dob = request.POST['dob']
        state = request.POST['state']
        phonenumber = request.POST['phonenumber']
        city = request.POST['city']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        passwords = sha256(password.encode()).hexdigest()
        if password==confirmpassword:
            if user_reg.objects.filter(email=email).exists():
                return redirect('register')

            user = user_reg(first_name=first_name, last_name=last_name, address=address, pincode=pincode, gender=gender, dob=dob, state=state,phonenumber=phonenumber, city=city, email=email,password=passwords)
            user.save()
            login = user_logins(email=email, password=passwords)
            login.save()
            messages.info(request,'Your account has been successfully created!!!!')
            return redirect('login')
        else:
            messages.info(request,"Password not match!!")
            return redirect('register')
    return render(request, 'register.html')
def login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(home)
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        # passwd = sha256(password.encode()).hexdigest()
        user = user_logins.objects.filter(email=email, password=password)

        if user:
            user_details=user_logins.objects.get(email=email, password=password)
            email=user_details.email
            request.session['email']=email
            print("valid")
            return redirect('home')
        else:
            print("invalid")
    return render(request, 'login.html')

# def login(request):
#     request.session.flush()
#     if 'email' in request.session:
#         return redirect(home)
#     if request.method=='POST':
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         # password2 = sha256(password.encode()).hexdigest()
#         user=user_logins.objects.filter(email=email,password=password)
#         if user:
#             user_details=user_logins.objects.get(email=email,password=password)
#             email=user_details.email
#             request.session['email']=email
#             return redirect('home')
#         else:
#             print("Invalid")
#     return render(request,'login.html')
def home(request):
    if 'email' in request.session:
        email = request.session['email']
        return render(request,'index.html',{'email':email})
    return redirect('login')
def demo(request):
    obj=courses.objects.all()
    return render(request,"index.html",{'result':obj})