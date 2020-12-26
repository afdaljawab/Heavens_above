from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator #import Paginator
import bcrypt

# Create your views here.
def signup(request):
    return render(request, 'heaven_app/signup.html')
def register(request):
    print('*'*80)
    print("in the register method")
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/signup')
        else:
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())#role = Role.objects.create(isAdmin = True, isUser = False)
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], address=request.POST['address'], role = Role.objects.create(isAdmin = False, isUser = True), password=pw_hash.decode())
            request.session['user']=request.POST['first_name']
            request.session['user_id']=new_user.id
            return redirect ('/')

def login(request):
    print('*'*80)
    print("in the login method")
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/signup')
        else:
            user=User.objects.filter(email=request.POST['login_email'])
            logged_user=user[0]
            request.session['user'] = logged_user.first_name
            request.session['user_id']=logged_user.id
            this_user = User.objects.get(id = request.session['user_id'])
            request.session['user_role'] = this_user.role.isAdmin
            print(this_user.role.isAdmin, '/*/'*15)
            return redirect ('/')

def root(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'product': page_obj,
    }
    
    return render(request, 'heaven_app/index.html',context)

def search(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    print(query, '/*' *15)
    if query:
        products = products.filter(title__contains = query)
    paginator = Paginator(products, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'product': page_obj,
    }
    
    return render(request, 'heaven_app/search.html',context)


def autocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(title__istartswith=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)
        return JsonResponse(titles, safe=False)

def details(request,p_id):
    this_product = Product.objects.get(id=p_id)
    userslike=this_product.like.all()
    this_product_reviews = Review.objects.filter(product_id = p_id)
    print(this_product_reviews, '/*' *15)
    paginator = Paginator(this_product_reviews, 2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    request.session['price']= this_product.price
    context= {
        'myproduct': this_product,
        'myreviews': this_product_reviews,
        'userslikes': userslike,
        'page_review': page_obj,
    }
    return render(request, 'heaven_app/details.html',context)

def order(request,p_id):
    this_product = Product.objects.get(id=p_id)
    context= {
        'myproduct': this_product,
    }
    return render(request, 'heaven_app/order.html',context)


def post_order(request,p_id):
    this_product = Product.objects.get(id=p_id)
    print(this_product, '/*' *15)
    if request.method =='POST':
        errors = User.objects.order_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/order/'+ format(p_id))
        else:
            this_name = request.POST['o_name']
            this_date = request.POST['date_birth']
            this_address = request.POST['address']
            this_phone = request.POST['phone']
            this_price = request.session['price']
            Order.objects.create(name = this_name , date_of_birth =this_date, place_of_birth =this_address, phone = this_phone,total_price = this_price, user_id = User.objects.get(id = request.session['user_id']), product_id = Product.objects.get(id = p_id))
            print(this_price, '/*\/' * 15)
            del request.session['price']
        return redirect('/thankyou')
    else:
        return redirect('/')
def admin(request, u_id):
    if request.session['user_role'] == False:
        return redirect('/')
    else:
        users = User.objects.all()
        products = Product.objects.all()
        orders = Order.objects.all()
        context={
        'myusers':users,
        'myproducts':products,
        'myorders':orders
        }
    return render(request, 'heaven_app/admin.html',context)
def addadmin(request):
    if request.method =='POST':
        errors = User.objects.admin_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/admin/'+ format(request.session['user_id']))
        else:
            first_name_from_form = request.POST['first_name']
            last_name_from_form = request.POST['last_name']
            email_from_form = request.POST['email']
            password_from_form = request.POST['password']
            pw_hash=bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt())
            password=pw_hash.decode()
            address_from_form = request.POST['address']
            User.objects.create(first_name=first_name_from_form,last_name=last_name_from_form,email=email_from_form,password=password,address=address_from_form,role=Role.objects.create(isAdmin = True, isUser = False))
            return redirect('/admin/'+ format(request.session['user_id']))

def deleteuser(request,id):
    user1=User.objects.get(id=id)
    user1.delete()
    return redirect('/admin/'+ format(request.session['user_id']))

def addproduct(request):
    title_from_form = request.POST['title']
    description_from_form = request.POST['description']
    price_from_form = request.POST['price']
    image_from_form = request.POST['image']
    Product.objects.create(title=title_from_form,description=description_from_form,price=price_from_form,image=image_from_form)
    return redirect('/admin/'+ format(request.session['user_id']))

def editproduct(request,id):
    product1=Product.objects.get(id=id)
    context = {
        "myproduct": product1,       
    }
    return render(request, "heaven_app/product.html", context)

def updateproduct(request,id):
    update = Product.objects.get(id=id)
    update.title = request.POST['title']
    update.price = request.POST['price']
    update.image = request.POST['image']
    update.description = request.POST['description']
    update.save()
    return redirect('/admin/'+ format(request.session['user_id']))

def deleteproduct(request,id):
    product1=Product.objects.get(id=id)
    product1.delete()
    return redirect('/admin/'+ format(request.session['user_id']))

def deleteorder(request,id):
    order1=Order.objects.get(id=id)
    order1.delete()
    return redirect('/admin/'+ format(request.session['user_id']))

def account(request,u_id):
    this_user=User.objects.get(id=u_id)
    context={
        'this_user': this_user
    }
    return render(request, 'heaven_app/account.html',context)

def contact(request):
    return render(request, 'heaven_app/contact.html')

def about(request):
    return render(request, 'heaven_app/about.html')

def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect('/')
    
def like(request, p_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_product = Product.objects.get(id=p_id)
    this_user.liked_products.add(this_product)
    return redirect('/details/'+ format(p_id))

def review(request, p_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_product = Product.objects.get(id=p_id)
    content_from_form = request.POST['content']
    Review.objects.create(content=content_from_form,product_id=this_product,user_id=this_user)
    return redirect('/details/'+ format(p_id))

def update(request, u_id):
    print('*'*80)
    print("in the update method")
    if request.method =='POST':
        errors = User.objects.admin_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/account/'+ format(u_id))
        else:
            updates=User.objects.get(id=u_id)
            updates.first_name=request.POST['first_name']
            updates.last_name=request.POST['last_name']
            updates.email=request.POST['email']
            pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            password=pw_hash.decode()
            updates.password=password
            updates.address=request.POST['address']
            updates.save()
            return redirect ('/account/' + format(u_id))

def handler404(request, *args, **argv):
    response = render_to_response('404.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response

def thankyou(request):
    return render(request, 'heaven_app/thankyou.html')