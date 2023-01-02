from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
import os

from .models import *
from .forms import *

# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-id')[:6]

    context = {
        'title':'Home',
        'home': 'active',
        'products' : products
    }

    return render(request, 'marketpedia/home.html', context)


def products(request):
    products = Product.objects.all().order_by('-id')

    context = {
        'title':'Products',
        'product': 'active',
        'products' : products,
    }

    return render(request, 'marketpedia/products.html', context)


def productdetail(request, market_name, product_name):
    market = Market.objects.get(name=market_name)
    product = Product.objects.filter(seller_id=market.name).get(name=product_name)

    context = {
        'title': product.name,
        'product':product,
        'market':market,
    }

    return render(request, 'marketpedia/product-detail.html', context)


def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

    if request.method=='GET':
        context = {
            'title':'Contact',
            'contact': 'active'
        }

        return render(request, 'marketpedia/contact.html', context)


def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Bad credential')
            return redirect('/signin')

    if request.method=='GET':
        context = {
            'title':'Sign In'
        }

        return render(request, 'marketpedia/signin.html', context)


def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if len(password1)<6:
            messages.error(request, 'You need at least have 6 characters length for your password')

        elif password1 and password2 and password1 != password2:
            messages.error(request, 'Password didn\'t match')

        else:
            username_check_existing = User.objects.filter(username=username).exists()
            email_check_existing = User.objects.filter(email=email).exists()
            
            if username_check_existing:
                messages.error(request, 'Username already exist')

            elif email_check_existing:
                messages.error(request, 'Email already exist')

            else:
                myuser = User.objects.create_user(username=username, email=email, password=password1)
                myuser.save()

                messages.success(request, 'Your account has been created successfully')
                return redirect('/signin')

    if request.method=='GET':
        context = {
            'title':'Sign Up',
        }

        return render(request, 'marketpedia/signup.html', context)


def signout(request):
    logout(request)
    return redirect('/')


@login_required
def myprofile(request):
    p_form = PictureUpdate(instance=request.user.profile)

    if request.method=='POST':
        if 'updatePicture' in request.POST:
            p_form = PictureUpdate(request.POST, request.FILES, instance=request.user.profile)
            if p_form.is_valid():
                p_form.save()

                messages.success(request, 'Your profile has been updated')
                return redirect('/myprofile')

        elif 'deleteAccount' in request.POST:
            user = User.objects.get(id=request.user.id)

            if request.POST['confirmUsername'] == request.user.username:
                user.delete()
                logout(request)

                messages.success(request, 'Your account has been deleted')
                return redirect('/')
            else:
                messages.error(request, 'Cancel delete account')

    if request.method=='GET':
        context = {
            'title':'My Profile',
            'p_form' : p_form,
        }

        return render(request, 'marketpedia/profile.html', context)


@login_required
def removepicture(request):
    profile = Profile.objects.get(id=request.user.profile.id)
    profile.image = 'profile_images/default.png'
    profile.save()
    
    messages.success(request, 'Your profile has been updated')
    return redirect('/myprofile')


@login_required
def editprofile(request):
    if request.method=='POST':
        fullname = request.POST['fullname']
        mobilephone = request.POST['mobilephone']
        address = request.POST['address']
        gender = request.POST['gender']
        
        profile = Profile.objects.get(id=request.user.profile.id)

        profile.fullname = fullname
        profile.mobile_phone = mobilephone
        profile.address = address
        profile.gender = gender
        profile.save()

        messages.success(request, 'Your profile has been updated')
        return redirect('/myprofile')

    if request.method=='GET':
        context = {
            'title':'Edit Profile',
        }

        return render(request, 'marketpedia/profile-account-edit.html', context)


@login_required
def editaccount(request):
    if  request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']

        messages.success(request, 'Your account has been updated')
        return redirect('/myprofile')

    if request.method=='GET':
        context = {
            'title':'Edit Account',
        }

        return render(request, 'marketpedia/profile-account-edit.html', context)


@login_required
def deleteaccount(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    logout(request)

    context = {
        'title':'Delete Account',
    }

    messages.success(request, 'Your account has been deleted')
    return redirect('/')


def market(request, market_name):
    market = Market.objects.get(name=market_name)
    products = Product.objects.filter(seller_id=market.name).order_by('-id')

    context = {
        'title':market.name,
        'market':market,
        'products':products,
    }

    return render(request, 'marketpedia/market.html', context)


@login_required
def check_market(request):
    if Market.objects.filter(user_id=request.user.id).exists():
        return redirect(f'/{request.user.market}')
    else:
        return redirect('/create-market')


@login_required
def createmarket(request):
    if Market.objects.filter(user_id=request.user.id).exists():
        return redirect(f'/{request.user.market.name}')

    initial_data = {
        'mobile_phone':request.user.profile.mobile_phone,
        'address':request.user.profile.address
    }

    form = CreateMarket(initial=initial_data)

    if request.method=='POST':
        form = CreateMarket(request.POST, request.FILES)
        if form.is_valid():
            market = form.save(commit=False)
            market.user_id = request.user.id
            market.save()

            messages.success(request, 'Your Market has been created successfully')
            return redirect(f'/{request.user.market.name}')

    if request.method=='GET':
        context = {
            'title':'Create Market',
            'form':form,
        }

        return render(request, 'marketpedia/market-create.html', context)


@login_required
def editmarket(request):
    market = Market.objects.get(name=request.user.market)
    products = Product.objects.filter(seller_id=market.name).order_by('-id')
    addform = AddProduct()
    initial_data = {
        'name':'cok'
    }
    editform = EditProduct(initial=initial_data)

    if request.method=='POST':
        addform = AddProduct(request.POST, request.FILES)
        if addform.is_valid():
            product = addform.save(commit=False)
            product.seller_id = request.user.market.name
            product.save()

            messages.success(request, 'Your Product has been added successfully')
            return redirect('/edit-market')

    if request.method=='GET':
        context = {
            'title':f'Edit {market.name}',
            'market':market,
            'products':products,
            'addform':addform,
            'editform':editform,
        }
        return render(request, 'marketpedia/market-edit.html', context)


def editproduct(request, product_name):
    product = Product.objects.get(seller_id=request.user.market.name, name=product_name)

    if request.method=='POST':
        if len(request.FILES['image'])>0:
            if os.path.exists(product.image.path):
                os.remove(product.image.path)
            product.image = request.FILES['image']
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.category = request.POST['category']
        product.save()

        messages.success(request, 'Your Product has been updated successfully')
        return redirect('/edit-market')


def deleteproduct(request, product_name):
    product = Product.objects.get(seller_id=request.user.market.name, name=product_name)
    if os.path.exists(product.image.path):
        os.remove(product.image.path)
    product.delete()

    return redirect('edit-market')