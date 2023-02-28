import razorpay
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from interapp.models import User, user_course,duration,trainers,Payment,OrderPlaced,video,requirement,add_subject
from django.contrib.auth.models import User, auth, models
from django.http import JsonResponse
from .models import User
from django.http import HttpResponse
from django import forms
from .models import Resume
from django.shortcuts import render

# from .forms import ResumeForm

def index(request):
    obj = user_course.objects.all()
    mentor = trainers.objects.all()
    context={
        'obj' : obj,
        'mentor' : mentor
    }
    return render(request, "index.html", context)


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        gender = request.POST.get('gender')
        roles=request.POST['roles']
        myfile = request.POST.get('myfile')
        state = request.POST.get('state')
        phonenumber = request.POST.get('phonenumber')
        city = request.POST.get('city')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        is_company = is_student = False
        if roles == 'is_admin':
            is_admin=True
        elif roles =='is_student':
            is_student=True
        else:
            is_company=True

        if password==confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, '!!!Email already taken!!!!')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, address=address,
                                                pincode=pincode, gender=gender, is_company=is_company,is_student=is_student, myfile=myfile, state=state,
                                                phonenumber=phonenumber, city=city, email=email,password=password)

                user.save()
                messages.success(request, 'Please verify your email for login!')

                current_site = get_current_site(request)
                message = render_to_string('account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

                send_mail(
                    'Please activate your account',
                    message,
                    'online.training.platform99@gmail.com',
                    [email],
                    fail_silently=False,
                )

                return redirect('/login/?command=verification&email=' + email)
        else:
            print('password is not matching')
            messages.info(request, '!!!Password and Confirm Password are not  match!!!')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            request.session['email'] = email
            if user.is_admin:
                return redirect('admin/')
            elif user.is_comp_approved:
                return redirect('company')
            elif user.is_student:
                return redirect('index')

        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')

# @login_required
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            user = User.objects.get(email__exact=request.user.email)
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.info(request, 'Password updated successfully.')
                return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'changepassword.html')


def courses(request):
    obj = user_course.objects.all()
    res = add_subject.objects.all()
    return render(request, "courses.html", {'result': obj,'res':res})

def course_details(request, course_slug):
    trainer = trainers.objects.all()
    videos = video.objects.all()
    require = requirement.objects.all()
    single = user_course.objects.get(slug=course_slug)
    context={
        'videos':videos,
        'single':single,
        'require':require,
        'trainer':trainer,
    }
    return render(request, "course-single-v1.html",context)


def about(request):
    return render(request, "about.html")
def contact(request):
    return render(request, "contact.html")
def pricing(request):
    return render(request, "pricing.html")
def trainer(request):
    obj = trainers.objects.all()
    return render(request, "trainers.html", {'result': obj})
def logout(request):
    auth.logout(request)
    return redirect('/')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email

            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'online.training.platform99@gmail.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def profile(request):
    return render(request,'profile.html')

def profile_update(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        myfile = request.POST.get('myfile')
        dob = request.POST.get('dob')
        phonenumber = request.POST.get('phonenumber')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.phonenumber = phonenumber
        user.email = email
        user.myfile = myfile

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')

def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(course_name__icontains=query))
            products = user_course.objects.filter(multiple_q)
            return render(request, 'searchbar.html', {'result':products})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
    return render(request, 'searchbar.html', {})

def checkout(request):
    user = request.user
    product = user_course.objects.all()
    total = 0
    for i in product:
        total = i.price

    razoramount = total * 100
    print(razoramount)
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))

    data = {
        "amount": total,
        "currency": "INR",
        "receipt": "order_rcptid_11"

    }
    payment_response = client.order.create(data=data)
    print(payment_response)
    order_id = payment_response['id']
    request.session['order_id'] = order_id
    order_status = payment_response['status']
    if order_status == 'created':
        payment = Payment(user=request.user,
                          amount=total,
                          razorpay_order_id=order_id,
                          razorpay_payment_status=order_status)
        payment.save()

    return render(request, 'shop-checkout.html', { 'product': product, 'total':total,'razoramount':razoramount})

def payment_done(request):
    order_id=request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)

    payment=Payment.objects.get(razorpay_order_id = order_id)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()



    return redirect('orders')

def enroll_course(request):

        orders = OrderPlaced.objects.filter(
            user=request.user, is_enrolled=True).order_by('enroll_date')
        context = {
            'orders': orders,
        }
        return render(request,'Enroll_courses.html',context)





def chatbot(request):
    # if request.method == 'POST':
    #     message = request.POST.get('message')
        # response = process_message(message)
    #     return JsonResponse({'message': response})
    # else:
        return render(request, 'resume.html')
#
# def process_message(message):
#     # Your chatbot logic goes here
#     # You can use the Resume model to retrieve and manipulate data
#     # Return a response message
#     return 'I received your message: ' + message


def company(request):
    return render(request, "company.html")

def subjects(request):

    obj = user_course.objects.all()
    res = add_subject.objects.all()
    return render(request,"subjects.html", {'obj':obj,'res':res })



def students(request):
    company = User.objects.filter(is_student = True)
    return render(request, "students.html",{'company':company} )


def student_details(request,id):
    company = User.objects.filter(id=id)
    return render(request, "student_details.html", {'company':company})

def add_subjects(request ):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        title = request.POST.get('title')
        image = request.POST.get('image')
        description = request.POST.get('description')
        course_week = request.POST.get('course_week')
        price = request.POST.get('price')
        outcomes = request.POST.get('outcomes')
        assignment = request.POST.get('assignment')
        Certificate = request.POST.get('Certificate')
        user = add_subject(course_name=course_name, title=title, image=image,
                                        description=description, course_week=course_week, price=price,
                                        outcomes=outcomes, assignment=assignment,
                                        Certificate=Certificate)
        user.save()
    return render(request, "add_subject.html")

def subject_details(request, id):
    add = add_subject.objects.filter(course_id=id)
    res = add_subject.objects.all()
    videos = video.objects.all()
    require = requirement.objects.all()
    return render(request, "subject_details.html", {'add':add,'res':res,'videos':videos,'require':require})