
from django.db import models
from django.shortcuts import redirect

from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime

from django.contrib.auth.models import User
from django.urls.base import reverse


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name,last_name,email,address,pincode,gender, myfile,phonenumber,is_company, is_comp_approved,is_student, state,city,password=None):
        if not email:
            raise ValueError('User must have an email address')


        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
            pincode=pincode,
            gender=gender,
            is_company=is_company,
            is_comp_approved= is_comp_approved,
            is_student=is_student,
            myfile=myfile,
            phonenumber=phonenumber,
            state=state,
            city=city,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password,email,**extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,**extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    role_choices = (('is_company', 'is_company'),('is_student', 'is_student'), ('is_admin', 'is_admin'), ('None', 'None'))
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='')
    pincode = models.IntegerField(default=0)
    gender = models.CharField(max_length=20,choices=gender_choices,default='None')
    myfile = models.FileField(upload_to='media',default='')
    phonenumber = models.CharField(max_length=10, default='')
    state = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=20, default='')
    roles = models.CharField(max_length=100, choices=role_choices, default='')
    email = models.EmailField(max_length=100, unique=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_comp_approved = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','address','pincode','gender','is_company','is_student','phonenumber','state','city']
    # object=MyAccount()
    objects = MyAccountManager()

    # objects = models.Manager()

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class duration(models.Model):
    weeks=models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.weeks

class trainers(models.Model):
        mentor_id = models.AutoField(primary_key=True)
        mentor_name = models.CharField(max_length=200)
        qualification = models.CharField(max_length=200)
        image1 = models.ImageField(upload_to='pics')
        experience = models.CharField(max_length=200)

        def __str__(self):
            return self.mentor_name

class user_course(models.Model):
    STATUS = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    course_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200,unique=True)
    title = models.CharField(max_length=200, default='')
    image=models.ImageField(upload_to='pics')
    desc = models.TextField(blank=True)
    course_week = models.ForeignKey(duration,on_delete=models.CASCADE)
    price = models.IntegerField(default='')
    outcomes = models.TextField()
    assignment = models.TextField(default='')
    Certificate = models.CharField(choices=STATUS,max_length=200,null=True,default='')

    def __str__(self):
        return self.course_name
    def get_url(self):
        return reverse('course_details')




class video(models.Model):
    serial_number = models.IntegerField(null=True)
    # thumbnail = models.ImageField(upload_to='pics')
    course = models.ForeignKey(user_course, on_delete=models.CASCADE)
    course_week = models.ForeignKey(duration, on_delete=models.CASCADE,default='')
    title = models.CharField(max_length=500)
    videos = models.FileField(upload_to='video')
    time_duration = models.CharField(max_length=500)
    preview = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)



class requirement(models.Model):
    course = models.ForeignKey(user_course, on_delete=models.CASCADE)
    points = models.CharField(max_length=200)

    def __str__(self):
        return self.points

class FeedBackStudents(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(user_course,on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.feedback

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(user_course,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=20,decimal_places=2,default=0)

    def get_product_price(self):
        price=[self.product.price]
        return sum(price)

class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(user_course, on_delete=models.CASCADE)
    is_enrolled = models.BooleanField(default=False)
    enroll_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)





class add_subject(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200,unique=True)
    title = models.CharField(max_length=200, default='')
    image=models.ImageField(upload_to='img/')
    description=models.TextField(default='')
    desc = models.TextField(blank=True)
    course_week = models.CharField(max_length=20,default='' )
    price = models.IntegerField(default='')
    outcomes = models.TextField()
    assignment = models.TextField(default='')
    Certificate = models.CharField(max_length=200,null=True,default='')
    def __str__(self):
        return str(self.course_name)

class QuizResult(models.Model):
    email = models.EmailField(max_length=70, default=0)
    course = models.ForeignKey(user_course, on_delete=models.CASCADE)
    course_week = models.ForeignKey(duration, on_delete=models.CASCADE)
    score = models.CharField(max_length=10, default=0)
    time = models.CharField(max_length=10, default=0)
    correct = models.CharField(max_length=10, default=0)
    wrong = models.CharField(max_length=10, default=0)
    percent = models.CharField(max_length=10, default=0)
    total = models.CharField(verbose_name='total questions', max_length=10, default=0)

    class Meta:
        verbose_name_plural = 'Quiz - Result'

    def str(self):
        return self.email


class QuesModel(models.Model):
    course = models.ForeignKey(user_course, on_delete=models.CASCADE)
    course_week = models.ForeignKey(duration, on_delete=models.CASCADE,default='')
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)


    def str(self):
        return self.question

class Quizdetail(models.Model):
    course = models.ForeignKey(user_course, on_delete=models.CASCADE)
    duration_minutes = models.IntegerField()





# class Document(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     resume = models.FileField(upload_to='documents/')
#     job_description = models.FileField(upload_to='documents/')

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')


class Resume(models.Model):
    name = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class resumme(models.Model):
    res_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,blank=True)
    position=models.CharField(max_length=100,blank=True)
    email=models.EmailField(blank=True, null=True)
    carobj=models.TextField(blank=True)
    college=models.CharField(max_length=100,blank=True)
    plus=models.CharField(max_length=100,blank=True)
    ten=models.CharField(max_length=100,blank=True)
    projects=models.TextField(blank=True)
    certi=models.TextField(blank=True)
    achi=models.TextField(blank=True)
    interns=models.TextField(blank=True)
    refe=models.TextField(blank=True)
    phone=models.CharField(max_length=200,blank=True,default='')
    address=models.TextField(blank=True)
    strength=models.TextField(null=True,blank=True)
    skills=models.TextField(null=True,blank=True)
    lang=models.TextField(null=True,blank=True)
    hob=models.TextField(null=True,blank=True)
    soci=models.CharField(max_length=100,blank=True)
    coun=models.CharField(max_length=100,blank=True)
    status=models.BooleanField('status', default=0)
    gender=models.CharField(max_length=100,null=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)