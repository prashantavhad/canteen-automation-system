from django.shortcuts import render
# from MyApp.models import User
from MyApp.forms import FormNewUser,FormUserProfileInfo,FormLogin,FormAddProduct,FormEditProfile,FormEditOrder
#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from MyApp.models import UserProfileInfo,Product
from django.contrib.auth.models import User

from django.views.generic import ListView
from MyApp.models import Order


class ProductList(ListView):
    model = Product


# Create your views here.
def index(request):
    userList = UserProfileInfo.objects.all()
    for user in userList:
        print(user.profile_pic)
    userDict = {'users': userList}
    return render(request, 'index.html', userDict)

def add_product(request):
    form = FormAddProduct()
    if request.method == "POST":
        product_form = FormAddProduct(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            product.product_available = True
            product.save()

            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']

            product.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(product_form.errors)

    else:
        product_form = FormAddProduct()
                                        # 'form': form
    return render(request, 'addProduct.html', {'product_form':product_form})

def edit_product(request,pid):
    productList = Product.objects.all()
    product = productList[int(pid)-1]
    if request.method == "POST":
        product_form = FormAddProduct(request.POST,instance = product)   ## add instance
        if product_form.is_valid():
            product = product_form.save()
            product.save()

            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']

            product.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(product_form.errors)

    else:
        product_form = FormAddProduct()   ## add instance

    return render(request, 'addProduct.html', {'product_form':product_form})  # 'form': form

def signup(request):
    form = FormNewUser()
    if request.method == "POST":
        user_form = FormNewUser(request.POST)
        profile_form = FormUserProfileInfo(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = FormNewUser()
        profile_form = FormUserProfileInfo()
                                        # 'form': form
    return render(request, 'users.html', {'user_form':user_form,'profile_form':profile_form})

def user_login(request):
    form = FormLogin()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user = user)
                # return HttpResponse("Account Active")
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Login Failed")
            print("Username:{} Password:{}".format(username,password))

    else:
        return render(request,'login.html',{})

# form = FormLogin(request.POST)
# if form.is_valid():
#     return index(request)
# else:
#     print("ERROR FORM INVALID")

# return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    # return HttpResponse("Logged Out")
    return HttpResponseRedirect(reverse('index'))

def user_profile(request):
    username = request.user.username
    print(username)
    userid = request.user.UserProfileInfo.somaiya_id
    print(userid)
    return render(request, 'userProfile.html', {})

def edit_profile(request):
    if request.method == "POST":
        user_form = FormEditProfile(request.POST, instance=request.user)
        profile_form = FormUserProfileInfo(request.POST, instance = request.user.UserProfileInfo)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = FormEditProfile(instance=request.user)
        profile_form = FormUserProfileInfo(instance=request.user.UserProfileInfo)
                                        # 'form': form
    return render(request, 'editUserProfile.html', {'user_form':user_form,'profile_form':profile_form})

def menuPage(request):
    productList = Product.objects.all()
    productDict = {'products':productList}
    return render(request, 'canteenMenu.html', productDict)


def getProduct(request, pid):
    # print(pid)
    productList = Product.objects.all()
    product = productList[int(pid)-1]
    order = Order(user = request.user, product = product, order_state = "Pending")
    order.save()
    # productDict = {'product':productList}
    return render(request, 'canteenMenu.html', {"product":product})
    # return redirect('http://stackoverflow.com/')

@login_required
def orders(request):
    if request.user.is_staff:
        print("staff")
        order_list = Order.objects.all()
    elif request.user:
        order_list = request.user.User.all()  ## User coz Order-User related name is User
    return render(request, 'orders.html', {"order_list":order_list})


def getOrder(request,oid):
    order_list = Order.objects.all()
    order = order_list[int(oid)-1]
    if request.method == "POST":
        order_form = FormEditOrder(request.POST,instance = order)   ## add instance
        if order_form.is_valid():
            order = order_form.save()
            order.save()
            return HttpResponseRedirect(reverse('orders'))

        else:
            print(product_form.errors)

    else:
        order_form = FormEditOrder()   ## add instance

    return render(request, 'editOrder.html', {'order_form':order_form})  # 'form': form
