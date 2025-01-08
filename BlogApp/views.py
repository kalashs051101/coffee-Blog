from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from BlogApp.models import *
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
import random
from .utils import *
import uuid
from allauth.account.views import LoginView, SignupView

# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def Registration(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if first_name == "":
                messages.error(request, "First name can't be empty")
                return redirect('Registration')
            if last_name == "":
                messages.error(request, "Last name can't be empty")
                return redirect('Registration')
            if username == "":
                messages.error(request, "Username can't be empty")
                return redirect('Registration')
            if email == "":
                messages.error(request, "Username can't be empty")
                return redirect('Registration')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already taken!")
                return redirect('Registration')
            if password == "":
                messages.error(request, "Password can't be empty")
                return redirect('Registration')
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return redirect('Registration')
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email)
            user.set_password(password)
            # print('uuiiiddd :',type(uuid.uuid4()) )
            user.email_token = str(uuid.uuid4()) 

            print('this is email token : ',type(user.email_token))

            send_email_token(email,user.email_token)

            user.save()
            messages.info(request, "Account created successfully! Please verify your email to log in.")
            return redirect('login_view')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('Registration')
    return render(request, 'Registration.html')

# def verify_email(request,token):
#     print('verify token',token)
#     obj=User.objects.get(email=token)
#     obj.is_verified=True
#     obj.save()
#     return HttpResponse('your account has been verified')

def verify_email(request, token):
    print('Verify token:', token)
    # user = get_object_or_404(User, email_token=token)
    user = get_object_or_404(CustomUser , email_token=token)
    
    if user.is_verified:
        messages.info(request, 'Your account is already verified.')
        return redirect('login_view')
       
    user.is_verified = True
    user.email_token = ''
    user.save()
    
    messages.success(request,'your account created successfully')
    print('after successfull verification')
    return redirect('login_view')


def dashboard(request):
    try:
        show_all = CustomUser.objects.all()
    except Exception as e:
        messages.error(request,f'an error occurred while fetching your data {str(e)}')
    return render(request, 'admin_dashboard.html', {'show_all': show_all})

def update_view(request):
    username = request.GET.get('username')
    obj = CustomUser.objects.filter(username=username).first()
    # print('this is id',obj.id)

    if obj is None:
        messages.error(request, f'User  with username {username} does not exist')
        return redirect('home')

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        new_username=request.POST.get('username')
        print(f"Old Username: {obj.username}")
        print(f"New Username: {new_username}")
        print(f"Email: {email}")

        try:
            if CustomUser.objects.exclude(id=obj.id).filter(username=new_username).exists():
                messages.error(request, "Username already taken!")
                return redirect(f'update_view?username={username}') 
            obj.first_name = firstname
            obj.last_name = lastname
            obj.email = email
            obj.username=new_username
            if CustomUser.objects.exclude(id=obj.id).filter(email=email).exists():
                messages.error(request, "Email already taken!")
                return redirect(f'update_view?username={username}')

            obj.save()  # Save the changes to the user
            messages.success(request, 'Profile updated successfully')
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred while updating: {str(e)}")
            return redirect(f'update_view?username={username}')

    return render(request, 'update.html', {'obj': obj})

def pikachu(request):
    return render(request, 'pikachu.html')
from django.core.exceptions import MultipleObjectsReturned
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        username = request.POST.get('username')
        print(username)         
        user = authenticate(request, username=username, password=password)
        print(user)
        try:
            if user is not None:   
                send_otp(request,email)  # Send OTP for verification
                messages.success(request,'Check your email for otp verification : ') 
                # request.session['username'] = username  # Store email in session
                request.session['email'] = email  # Store email in session
                print('User  authenticated, redirecting to OTP page.')
                return redirect('otp')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login_view')
            
        except MultipleObjectsReturned:
            messages.error(request, 'Multiple object returned error')
            return redirect('login_view')

        except CustomUser.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
            return redirect('login_view')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('login_view')
    
    # If GET request, render the login form (assuming you have a template for it)
    return render(request, 'login.html')

def otp(request):
    print('sdkjflaskj')
    if request.method == "POST":
        print('ookkkkkkk')
        print(request.method)
        otp_input = request.POST.get('otp')
        # username = request.session.get('username')
        email = request.session.get('email')
        print(f"Attempting to retrieve user with username: {email}")

        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_data')

        if otp_secret_key and otp_valid_until:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=120)
                if totp.verify(otp_input):
                    print('Inside verify: OTP is valid.')
                    # Check if the user exists
                    if CustomUser.objects.filter(email=email).exists():
                        user = CustomUser.objects.get(email=email)
                        print('Login successful')
                        login(request, user)
                        return redirect('home')
                        # return HttpResponse('okk')
                    else:
                        print("User  does not exist in the database.")
                        messages.error(request, 'Username does not exist. Please try again.')
                else:
                    messages.error(request, 'invalid otp')
            else:
                messages.error(request, 'expired otp')
        else:
            messages.error(request, 'something wrong.... try again later')

    return render(request, 'otp.html')

def logout_view(request):
    try:
        logout(request)
        # messages.success(request, 'Logged out successfully.')
    except Exception as e:
        print(f"An error occurred during logout: {str(e)}")
        messages.error(request, 'An error occurred for log out. Please try again later.')
    return redirect('home')

def Blog_view(request):
    try:

        blog_all = BlogModel.objects.all()
    except Exception as e:
        messages.error(request,f'something wrong please try again later-- {str(e)}')

    return render(request, 'Blog.html', {'blog_all': blog_all})



@login_required 
def Blog_register(request):
    if request.method == "POST":
        blogname = request.POST.get('blogname')
        description = request.POST.get('description')
        fileinput = request.FILES.get('file')

        try:
            file = BlogModel.objects.create(name=blogname, description=description, image=fileinput,user=request.user)
            file.save()
            messages.success(request, "Blog created successfully!")
            return redirect('Blog_view')

        except Exception as e:
            messages.error(request, f"An error occurred while creating the blog: {str(e)}")
            return redirect('Blog_register')

    return render(request, 'blog_register.html')


def Blog_delete(request):
    id = request.GET.get('id')
    print('Blog ID:', id)
    try:
        obj = BlogModel.objects.get(id=id)
        obj.delete()
        messages.success(request, 'Blog post deleted successfully.')
    except BlogModel.DoesNotExist:
        messages.error(request, 'Blog post not found.')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.error(request, 'Error occured !')
    return redirect('Blog_view')


def Blog_update(request):
    id = request.GET.get('id')
    print(id)
    obj = BlogModel.objects.get(id=id)
    print(obj)
    if request.method == "POST":
        blogname = request.POST.get('blogname')
        description = request.POST.get('description')
        file = request.FILES.get('file') 
        try:
            obj.name = blogname
            obj.description = description
            obj.image = file
            obj.save()  # Save the updated object
            print(f"Updated Object: {obj}")

            return redirect('Blog_view')
        except Exception as e:
            print(f"Error updating blog: {e}")
    return render(request,'Blog_update.html',{'obj':obj})


def individual_show(request):
    try:

        username = request.user.username
        print('this is username',request.user)
        obj = BlogModel.objects.filter(user=request.user).all()
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred: {str(e)}")  # You can replace this with logging
        messages.error(request, 'An error occurred while retrieving your blog posts. Please try again later.')
    return render(request, 'individual_show.html',{'obj':obj})
# import settings



def change_password(request):
    user=request.user
    print(user)
    if request.method=="POST":
        old_password=request.POST['old_password']
        print(old_password)
        new_password=request.POST['new_password']
        print(new_password)
        confirm_password=request.POST['confirm_password']
        print(confirm_password)

        try:
            if not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
                return redirect('change_password')

            if new_password != confirm_password:
                messages.error(request, 'New password and confirm password do not match.')
                return redirect('change_password')

            if len(new_password) < 8:  # Example: minimum length of 8 characters
                messages.error(request, 'New password must be at least 8 characters long.')
                return redirect('change_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Update the session to keep the user logged in
            messages.success(request, 'Your password has been changed successfully.')

            send_mail(
                "Password Notification",
                "your password change successfully.",
                settings.EMAIL_HOST_USER,
                ["manish123@yopmail.com"],
                fail_silently=False,
            )
            return redirect('change_password')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('change_password')
    return render(request,'change_password.html')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = generate_otp()
            send_verification_email(email, otp)
            request.session['otp'] = otp  # Store OTP in session for validation
            request.session['email'] = email  # Store email in session
            print('After forgot password : ')
            return redirect('otp_reset_password')
        except CustomUser.DoesNotExist:
            messages.error(request, "Email does not exist.")
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')




def otp_reset_password(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        print('otp', otp)
        try:
            if str(otp) == str(request.session.get('otp')):
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('otp_reset_password')
        except Exception as e:
            messages.error(request, f"Something wrong {str(e)}")
            return redirect('forgot_password')

    return render(request, 'otp_reset_password.html')

def reset_password(request):
    if request.method == "POST":
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        try:
            if pass1 == pass2:
                email = request.session.get('email')
                user = CustomUser.objects.get(email=email)
                user.password = make_password(pass1)  # Hash the password
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login_view')  # Redirect to login page or wherever appropriate
            else:
                messages.error(request, "Passwords do not match.")
                return redirect('reset_password')
        except Exception as e:
            messages.error(request,f'something wrong {str(e)} ')
    return render(request, 'reset_password.html')



def search_result(request):
    # count=0
    if request.method=="GET":
        query=request.GET.get('query')
        print(query)

        result = BlogModel.objects.filter(name__icontains = query)
        print(result)

        total_result=result.count()


    return render(request,'search_result.html',{'results':result,'query': query,'total_result':total_result})