import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from interapp.models import User, user_course,FeedBackStudents,trainers,Payment,OrderPlaced,video,resumme,requirement,add_subject,Cart,Quizdetail,QuizResult,QuesModel,Document,duration
from django.contrib.auth.models import User, auth, models
from .models import User, FeedBackStudents
from django.http import JsonResponse

from django.http import HttpResponse
from django import forms

from django.shortcuts import render


def index(request):
    obj = user_course.objects.all()
    res = add_subject.objects.all()

    context={
        'obj' : obj,
        'res' : res,
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
        is_comp_approved = False

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
                        pincode=pincode, gender=gender, is_company=is_company,is_comp_approved=is_comp_approved,is_student=is_student, myfile=myfile, state=state,
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
    return render(request, "courses.html", {'result': obj,})

@login_required(login_url='login')
def course_details(request,id):
    user = request.user
    trainer = trainers.objects.all()
    videos = video.objects.all()
    require = requirement.objects.all()
    single = user_course.objects.get(course_id=id)
    orders = OrderPlaced.objects.filter(user=request.user, product=single, is_enrolled=True).order_by('enroll_date')
    context={
        'videos':videos,
        'single':single,
        'require':require,
        'trainer':trainer,
        'orders':orders
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



@login_required(login_url='login')
def addcart(request,id):
      user = request.user
      item=user_course.objects.get(course_id=id)
      if item:
            if Cart.objects.filter(user_id=user,product_id=item).exists():
                  messages.success(request, 'Course Already in the cart ')
                  return redirect(cart)
            else:

                  price=item.price

                  new_cart=Cart(user_id=user.id,product_id=item.course_id,price=price)
                  new_cart.save()
                  messages.success(request, 'Course added to the Cart ')
                  return redirect(cart)


# View Cart Page
@login_required(login_url='login')
def cart(request):

    count = Cart.objects.filter(user=request.user.id).count()
    user = request.user
    cart=Cart.objects.filter(user_id=user)
    totalitem=0
    total=0
    for i in cart:
        total += i.product.price
        totalitem = len(cart)

    return render(request,'cart.html',{'cart':cart,'total':total,'totalitem':totalitem})

# Remove Items From Cart
def de_cart(request,id):
    Cart.objects.get(id=id).delete()
    return redirect(cart)



@login_required(login_url='login')
def checkout(request):
    user = request.user
    product = Cart.objects.filter(user_id=user)
    total = 0
    for i in product:
        total += i.product.price
        cart = Cart.objects.filter(user_id=user)

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

    return render(request, 'shop-checkout.html', { 'product': cart, 'total':total,'razoramount':razoramount})

def payment_done(request):
    order_id=request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)

    payment=Payment.objects.get(razorpay_order_id = order_id)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart=Cart.objects.filter(user=request.user)
    for c in cart:
        OrderPlaced(user=request.user, product=c.product, payment=payment,is_enrolled=True).save()
        c.delete()

    return redirect('courses')



def paymentapproved(request, leave_id):
    appout = Payment.objects.get(id=leave_id)
    appout.status = 1
    appout.save()
    return redirect('course_details')


def paymentdisapprove(request, leave_id):
    appout = Payment.objects.get(id=leave_id)
    appout.status = 2
    appout.save()
    return redirect('course_details')



def admin(request):
    return render(request, "admin.html")


def company(request):
    return render(request, "company.html")

def subjects(request):
    user = request.user
    courses = user_course.objects.filter(user_id=user)
    return render(request,"subjects.html",{'courses':courses})


def students(request):
    user = request.user
    order = OrderPlaced.objects.filter(is_enrolled= True,product__user=user)
    print(order)
    return render(request, "students.html",{'order':order} )


def student_details(request,id):
    company = User.objects.filter(id=id)
    return render(request, "student_details.html", {'company':company})

def add_subjects(request ):
    user = request.user
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        title = request.POST.get('title')
        image = request.FILES['image']
        desc = request.POST.get('desc')
        course_week = request.POST.get('course_week')
        price = request.POST.get('price')
        outcomes = request.POST.get('outcomes')
        assignment = request.POST.get('assignment')
        Certificate = request.POST.get('Certificate')
        user = user_course(user_id=user.id,course_name=course_name, title=title, image=image,
                                        desc=desc, course_week=course_week, price=price,
                                        outcomes=outcomes, assignment=assignment,
                                        Certificate=Certificate)
        user.save()

    return render(request, "add_subject.html")

def view_course(request,id):
    course = user_course.objects.filter(course_id=id)
    return render(request, "edit_course.html",{'course':course})

def edit_course(request,id):

    if request.method == "POST":
        course_name = request.POST.get('course_name')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        course_week = request.POST.get('course_week')
        price = request.POST.get('price')
        outcomes = request.POST.get('outcomes')
        assignment = request.POST.get('assignment')
        Certificate = request.POST.get('Certificate')

        course = user_course.objects.get(course_id=id)
        course.course_name = course_name
        course.title = title
        course.desc = desc
        course.course_week = course_week
        course.outcomes = outcomes
        course.price = price
        course.assignment = assignment
        course.Certificate = Certificate
        course.save()
    return redirect(subjects)

def delete_course(request,id):
    course = user_course.objects.filter(course_id=id)
    course.delete()
    return redirect(subjects)


def add_video(request):
    user = request.user
    single = user_course.objects.all()
    if request.method == "POST":
        cat_id = request.POST.get('course')
        print("cat_id:", cat_id)
        course =  user_course.objects.get(course_id=cat_id)
        title = request.POST.get('title')
        serial_number = request.POST.get('serial_number')
        videos = request.FILES['videos']
        time_duration = request.POST.get('time_duration')

        val = video(
            course=course, title=title, videos=videos, time_duration=time_duration,serial_number=serial_number,
        )
        val.save()
    return render(request,"Add_video.html",{"single":single})

def add_quiz(request):
    user = request.user
    single = user_course.objects.all()
    if request.method == "POST":
        cat_id = request.POST.get('course')
        print("cat_id:", cat_id)
        course = user_course.objects.get(course_id=cat_id)
        question = request.POST.get('question')
        op1 = request.POST.get('op1')
        op2 = request.POST.get('op2')
        op3 = request.POST.get('op3')
        op4 = request.POST.get('op4')
        ans = request.POST.get('ans')
        val = QuesModel(
            course=course, question=question, op1=op1, op2=op2, op3=op3,op4=op4,ans=ans
        )
        val.save()
    return render(request, "Add_quiz.html",{"single":single})

def quiz_details(request):
    user = request.user
    single = user_course.objects.all()
    if request.method == "POST":
        cat_id = request.POST.get('course')
        print("cat_id:", cat_id)
        course = user_course.objects.get(course_id=cat_id)
        duration_minutes = request.POST.get('duration_minutes')
        val = Quizdetail(
            course=course, duration_minutes=duration_minutes
        )
        val.save()
    return render(request, "quiz_details.html",{"single":single})

def feedback(request,id):
    staff_id=User.objects.get(id=request.user.id)
    feedback_data= FeedBackStudents.objects.filter(user=staff_id)
    courses = user_course.objects.filter(course_id=id)
    return render(request,"feedback.html",{'feedback_data':feedback_data,'courses':courses})

def student_feedback_save(request,id):
    if request.method == 'POST':
        feedback_msg=request.POST.get('feedback_msg')
        user=request.user
        course = user_course.objects.get(course_id=id)
        feedbacks=FeedBackStudents(user=user,course_id=course.course_id,feedback=feedback_msg)
        feedbacks.save()
        print('feedback',feedbacks)
        messages.success(request, "Successfully Sent Feedback")
    return redirect('feedback',id=id)

# /////////////////////////////////////////////////////////////////////////////////////
from itertools import groupby

def curriculum(request, id):
    user = request.user
    single = user_course.objects.get(course_id=id)
    orders = OrderPlaced.objects.filter(user=request.user, product=single, is_enrolled=True).order_by('enroll_date')
    videos = video.objects.filter(course=single).order_by('course_week', 'serial_number')
    video_groups = []
    for week, week_videos in groupby(videos, lambda v: v.course_week):
        video_groups.append({
            'week': week,
            'videos': list(week_videos)
        })
    questions = QuesModel.objects.filter(course=single)
    return render(request, "curriculum.html", {'single': single, 'orders': orders, 'video_groups': video_groups, 'questions': questions})

# /////////////////////////////////////////////////////////////////////////////////////////
def video_detail(request,id):
    vid = video.objects.filter(id=id)
    return render(request, "course-details.html", { 'vid': vid})

def mark_video_completed(request, id):
    v = video.objects.get(id=id)
    v.completed = True
    v.save()
    return JsonResponse({'success': True})


# def quiz(request,id):
#     email = request.session['email']
#     if request.method == 'POST':
#             print(request.POST)
#             single = user_course.objects.get(course_id=id)
#             questions = QuesModel.objects.filter(course=single)
#             time = Quizdetail.objects.filter(course=single)
#             score = 0
#             wrong = 0
#             correct = 0
#             total = 0
#             for q in questions:
#                 total += 1
#                 print(request.POST.get(q.question))
#                 print('correct answer:' + q.ans)
#                 print()
#                 if q.ans == request.POST.get(q.question):
#                     score += 1
#                     correct += 1
#                 else:
#                     wrong += 1
#             percent = (score / total) * 100
#             context = {
#                 'score': score,
#                 'correct': correct,
#                 'wrong': wrong,
#                 'percent': percent,
#                 'total': total,
#                 'single': single,
#                 'time': time,
#
#             }
#             r = QuizResult(email=email, score=score, correct=correct,
#                            wrong=wrong, percent=percent, total=total)
#             print(r)
#             r.save()
#             return render(request, 'result.html',context)
#     else:
#         single = user_course.objects.get(course_id=id)
#         questions = QuesModel.objects.filter(course=single)
#         time = Quizdetail.objects.filter(course=single)
#         context = {
#             'questions': questions,
#             'single': single,
#             'time' : time,
#         }
#         return render(request, 'quizpage.html', context)
# ////////////////////////////////////////////////////////////

# def quiz(request, id, week):
#     email = request.session['email']
#     single = user_course.objects.get(course_id=id)
#
#     quiz_results = QuizResult.objects.filter(email=email, course=single)
#
#     # Check if user has attempted quiz three times already
#     if len(quiz_results) >= 3:
#         return HttpResponse("You have already attempted the quiz for this course three times.")
#
#     if request.method == 'POST':
#         print(request.POST)
#         questions = QuesModel.objects.filter(course=single, course_week=week)
#         time = Quizdetail.objects.filter(course=single, duration_minutes=week).first()
#         score = 0
#         wrong = 0
#         correct = 0
#         total = 0
#         for q in questions:
#             total += 1
#             print(request.POST.get(q.question))
#             print('correct answer:' + q.ans)
#             print()
#             if q.ans == request.POST.get(q.question):
#                 score += 1
#                 correct += 1
#             else:
#                 wrong += 1
#         percent = (score / total) * 100
#
#         # Check if user has attempted quiz three times already
#         if len(quiz_results) >= 3:
#             context = {
#                 'score': score,
#                 'correct': correct,
#                 'wrong': wrong,
#                 'percent': percent,
#                 'total': total,
#                 'single': single,
#                 'time': time,
#                 'error_message': "You have already attempted the quiz for this course three times."
#             }
#             return render(request, 'result.html', context)
#         context = {
#             'score': score,
#             'correct': correct,
#             'wrong': wrong,
#             'percent': percent,
#             'total': total,
#             'single': single,
#             'time': time,
#         }
#         # week = QuesModel.objects.filter(course_week_id=week)
#         # print("week:                                  ", week)
#
#         # week = QuesModel.objects.filter(course_id=id)
#         # weeks=week.course_week_id
#         # print("week:                                  ", weeks)
#         r = QuizResult(email=email, course=single, score=score, correct=correct,
#                        wrong=wrong, percent=percent, total=total)
#         print(r)
#         r.save()
#         return render(request, 'result.html', context)
#
#     else:
#         questions = QuesModel.objects.filter(course=single, course_week=week)
#         time = Quizdetail.objects.filter(course=single, duration_minutes=week).first()
#         context = {
#             'questions': questions,
#             'single': single,
#             'time' : time,
#         }
#         return render(request, 'quizpage.html', context)

def quiz(request, id, week):
    email = request.session['email']
    single = user_course.objects.get(course_id=id)
    week_obj = duration.objects.get(id=week)

    quiz_results = QuizResult.objects.filter(email=email, course=single, course_week=week_obj).count()

    # Check if user has attempted quiz three times already
    if quiz_results >= 3:
        return HttpResponse("You have already attempted the quiz for this course three times.")

    if request.method == 'POST':
        print(request.POST)
        questions = QuesModel.objects.filter(course=single, course_week=week)
        time = Quizdetail.objects.filter(course=single, duration_minutes=week).first()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print('correct answer:' + q.ans)
            print()
            if q.ans == request.POST.get(q.question):
                score += 1
                correct += 1
            else:
                wrong += 1
        percent = (score / total) * 100

        # Check if user has attempted quiz three times already
        if (quiz_results) >= 3:
            context = {
                'score': score,
                'correct': correct,
                'wrong': wrong,
                'percent': percent,
                'total': total,
                'single': single,
                'time': time,
                'error_message': "You have already attempted the quiz for this course three times."
            }
            return render(request, 'result.html', context)
        context = {
            'score': score,
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total,
            'single': single,
            'time': time,
        }
        # week = QuesModel.objects.filter(course_week_id=week)
        # print("week:                                  ", week)

        # week = QuesModel.objects.filter(course_id=id)
        # weeks=week.course_week_id
        # print("week:                                  ", weeks)
        r = QuizResult(email=email, course=single, course_week=week_obj, score=score, correct=correct,
                       wrong=wrong, percent=percent, total=total)
        print(r)
        r.save()
        return render(request, 'result.html', context)

    else:
        questions = QuesModel.objects.filter(course=single, course_week=week)
        time = Quizdetail.objects.filter(course=single, duration_minutes=week).first()
        context = {
            'questions': questions,
            'single': single,
            'time' : time,
        }
        return render(request, 'quizpage.html', context)

# //////////////////////////////////////////////////////////////////////////////////////////

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from io import BytesIO

def generate_certificate(request, percent, course_name, user_name):
    # Get the HTML template for the certificate
    user = request.user
    name=user.first_name
    template = get_template('certi.html')

    # Create a context for the template
    context = {
        'percent': percent,
        'course_name': course_name,
        'user_name': user_name,
        'name': name,
    }
    percentage=float(percent)
    percentag = int(percentage)
    if percentag < 80:
        return HttpResponse("Sorry, you are not eligible for the certificate.")
    # Render the template with the context
    html = template.render(context)

    # Create a PDF from the HTML using xhtml2pdf
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Return the PDF as a response
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=certificate.pdf'
    return response
# /////////////////////////////////////////////////////////////////////////////////////////////////////
# from django.http import HttpResponse
# from django.template.loader import get_template
# from django.template import Context
# from xhtml2pdf import pisa
# from io import BytesIO
# from .models import QuizResult
#
# def generate_certificate(request, percent, course_name, user_name):
#     course_id=user_course.course_id
#     email = request.session['email']
#     quiz_result = QuizResult.objects.filter(email=email, course_id=course_id).first()
#     print('percent',quiz_result.percent)
#     # Check if the user has attempted the quiz for the given course and their score is above 80%
#     if quiz_result.percent < 80 :
#         return HttpResponse("Sorry, you are not eligible for the certificate.")
#
#     # Get the HTML template for the certificate
#     template = get_template('certificate_template.html')
#
#     # Create a context for the template
#     context = {
#         'percent': quiz_result.percent,
#         'course_name': course_name,
#         'user_name': user_name,
#     }
#
#     # Render the template with the context
#     html = template.render(context)
#
#     # Create a PDF from the HTML using xhtml2pdf
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#
#     # Return the PDF as a response
#     response = HttpResponse(result.getvalue(), content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=certificate.pdf'
#     return response

# /////////////////////////////////////////////////////////////////////////////////////////////////////

# from django.http import HttpResponse, Http404
# from django.conf import settings
# import os
# def certificate_download(request, filename):
#     if not filename:
#         # Handle the case where the filename is empty or invalid
#         return HttpResponse("Invalid file name")
#     try:
#         filepath = os.path.join(settings.BASE_DIR, 'path/to/certificates', filename)
#         with open(filepath, 'rb') as f:
#             response = HttpResponse(f.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
#             return response
#     except IOError:
#         # Handle the case where the file cannot be opened or read
#         raise Http404


# def terms_and_conditions(request,id):
#     single = user_course.objects.get(course_id=id)
#     questions = QuesModel.objects.filter(course=single)
#     context = {
#         'questions': questions,
#         'single': single
#     }
#     return render(request, 'terms_and_conditions.html',context)

# def resume_parser(request):
#     user = User.objects.filter(is_student=True)
#     if request.method == 'POST':
#         resume_file = request.FILES.get('resume')
#         job_description_file = request.FILES.get('job_description')
#
#         # Save uploaded files as Document objects in the database
#         resume_doc = Document.objects.create(
#             title=resume_file.name,
#             file=resume_file
#         )
#         job_description_doc = Document.objects.create(
#             title=job_description_file.name,
#             file=job_description_file
#         )
#
#         # Extract text from the uploaded files
#         resume = process(resume_doc.file.path)
#         job_description = process(job_description_doc.file.path)
#
#         # Calculate similarity score using CountVectorizer and cosine_similarity
#         text = [resume, job_description]
#         cv = CountVectorizer()
#         count_matrix = cv.fit_transform(text)
#         similarity_score = cosine_similarity(count_matrix)[0][1] * 100
#         similarity_score = round(similarity_score, 2)
#     return render(request, 'resume_parser.html',{'user':user,'similarity_score':similarity_score})

from docx2txt import process
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Document


def document_similarity(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_description_file = request.FILES.get('job_description')

        # Save uploaded files as Document objects in the database
        resume_doc = Document.objects.create(
            title=resume_file.name,
            file=resume_file
        )
        job_description_doc = Document.objects.create(
            title=job_description_file.name,
            file=job_description_file
        )

        # Extract text from the uploaded files
        resume = process(resume_doc.file.path)
        job_description = process(job_description_doc.file.path)

        # Calculate similarity score using CountVectorizer and cosine_similarity
        text = [resume, job_description]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        similarity_score = cosine_similarity(count_matrix)[0][1] * 100
        similarity_score = round(similarity_score, 2)

        # Render the result in the template
        return render(request, 'results.html', {'score': similarity_score})

    # Render the form for uploading files
    return render(request, 'home.html')

# from django.contrib.auth.models import User
# from django.db.models import Q
# from .models import Document
#
# def document_similarity(request):
#     if request.method == 'POST':
#         job_description_file = request.FILES.get('job_description')
#
#         # Save uploaded job description as a Document object in the database
#         job_description_doc = Document.objects.create(
#             title=job_description_file.name,
#             file=job_description_file
#         )
#
#         # Extract text from the uploaded job description
#         job_description = process(job_description_doc.file.path)
#
#         # Retrieve resumes from the User table for enrolled students
#         resumes = User.objects.filter(
#             Q(User__is_student=True) & Q(OrderPlaced__is_enrolled=True)
#         ).values_list('User__myfile', flat=True)
#
#         # Calculate similarity score for each resume using CountVectorizer and cosine_similarity
#         cv = CountVectorizer()
#         job_desc_matrix = cv.fit_transform([job_description])
#         similarity_scores = []
#         for resume in resumes:
#             count_matrix = cv.transform([resume])
#             similarity_score = cosine_similarity(count_matrix, job_desc_matrix)[0][0] * 100
#             similarity_score = round(similarity_score, 2)
#             similarity_scores.append(similarity_score)
#
#         # Render the results in the template
#         return render(request, 'results.html', {'scores': similarity_scores})
#
#     # Render the form for uploading files
#     return render(request, 'home.html')

# ///////////////////////////////////////////////////////////////////////////////////////////////////////

def my_view(request):
    # Retrieve data from the database
            data1=resumme.objects.filter(user_id = request.user.id)
            data2=request.user.image
    # Render an HTML template using the retrieved data
            template = get_template('res.html')
            html = template.render({'data1': data1,'data2': data2})

            # Generate a PDF from the HTML using xhtml2pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="my_pdf.pdf"'

            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('Error generating PDF file')
            return response


def ress(request):
    data1 = resumme.objects.filter(user_id=request.user.id)
    return render(request, 'ress.html',{'data1':data1})


def res(request):
    data1=resumme.objects.filter(user_id = request.user.id)
    return render(request,'res.html',{'data1':data1})

def resdetails(request):
    return render(request,'resdetails.html')


def resubmit(request):
    # Get the current user's resume (if it exists)
    try:
        user_resume = resumme.objects.get(user_id=request.user.id)
    except resumme.DoesNotExist:
        user_resume = None

    # If the user has a resume, update it
    if user_resume:
        user_resume.name = request.POST['name']
        user_resume.position = request.POST['position']
        user_resume.carobj = request.POST['carobj']
        user_resume.email = request.POST['email']
        user_resume.college = request.POST['college']
        user_resume.plus = request.POST['plus']
        user_resume.ten = request.POST['ten']
        user_resume.projects = request.POST['projects']
        user_resume.certi = request.POST['certi']

        user_resume.interns = request.POST['interns']
        user_resume.refe = request.POST['refe']
        user_resume.phone = request.POST['phone']

        user_resume.skills = request.POST['skills']
        user_resume.lang = request.POST['lang']
        user_resume.hob = request.POST['hob']



        user_resume.save()
    # Otherwise, create a new resume for the user
    else:
            name=request.POST['name'],
            position=request.POST['position'],
            carobj=request.POST['carobj'],
            email=request.POST['email'],
            college=request.POST['college'],
            plus=request.POST['plus'],
            ten=request.POST['ten'],
            projects=request.POST['projects'],
            certi=request.POST['certi'],
            interns=request.POST['interns'],
            refe=request.POST['refe'],
            phone=request.POST['phone'],
            skills=request.POST['skills'],
            lang=request.POST['lang'],
            hob=request.POST['hob'],
            user_id = request.user # <-- get the current user's ID
            userr = resumme(name=name, position=position, email=email, carobj=carobj, college=college, plus=plus, ten=ten, projects=projects,
                    certi=certi, interns=interns, refe=refe, phone=phone,
                    skills=skills, lang=lang, hob=hob, user_id=user_id)
            userr.save()
    return redirect('res')



from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr
import moviepy.editor as mp
def transcribe_video(request, id):
    # single = user_course.objects.get(course_id=id)
    # videoss = video.objects.get(id=single.course_id)
    # Load the video file
    videoss = video.objects.get(id=id)
    clip = mp.VideoFileClip(videoss.videos.path)
    # Extract the audio from the video file
    audio_file = 'audio.wav'
    clip.audio.write_audiofile(audio_file)
    # Initialize the recognizer
    r = sr.Recognizer()
    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
    # Use Google's Speech Recognition API to transcribe the audio data
    text = r.recognize_google(audio_data)
    print(text)
    # Return the transcribed text as an HTTP response
    return HttpResponse(text)


def certi(request):
    return render(request,'certi.html')


