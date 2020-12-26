from django.db import models
from urllib import request
import re, bcrypt
# Create your models here.

'''
this command to create a user with the admin role:
User.objects.create(first_name = 'Omar', last_name = 'alqasem', email = 'omar@gmail.com', address = 'tulkarm', password = '123', role = Role.objects.create(isAdmin = True, isUser = False))
----
create new product:
Product.objects.create(title='starsframe',description='thshdishdhasd',image='asdasdasd',price='99.89')
----
create new order:
Order.objects.create(name = 'stars',date_of_birth ='2020-12-23' ,place_of_birth ='ramallah',phone ='0597102030',total_price = 0.0,user_id = User.objects.get(id = 1),product_id = Product.objects.get(id = 1))

---
Create new like:
this_user = User.objects.get(id=1)
this_product = Product.objects.get(id=1)
this_user.liked_products.add(this_product)
---
Create new review:
Review.objects.create(content='asfasbdafdsfbf',product_id=this_product,user_id=this_user)
'''
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        reuser=User.objects.filter(email=postData['email'])
        if reuser:
            errors['email']="There is already a user with this email address."
            return errors
        if len(postData['first_name'])<2:
            errors["first_name"] = "Your first name should be at least 2 characters long."
        if (postData['first_name']).isalpha() !=True:
            errors["first_name2"] = "Your first name should be comprised only of letters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Your last name should be at least 2 characters long."
        if (postData['last_name']).isalpha() !=True:
            errors["last_name2"] = "Your last name should be comprised only of letters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email2'] = ("Your email address is not a valid format.")
        if len(postData['password']) < 8:
            errors["password"] = "Your password should be at least 8 characters long."
        if postData['password'] !=postData['confirm_password']:
            errors["confirm_password"] = "Your password confirmation does not match your password."
        return errors
    def login_validator(self, postData):
        errors ={}
        logged_user=User.objects.filter(email=postData['login_email'])
        if logged_user:
            user=logged_user[0]
        else:
            errors['email']='There is no user that matches this email. Please register.'
            return errors
        if bcrypt.checkpw(postData['login_password'].encode(), user.password.encode()):
            return errors
        else:
            errors['password']='This password does not match this email. Please try again.'
            return errors
    def account_validator(self, postData):
        errors = {}
        reuser=User.objects.filter(email=postData['email'])
        if reuser:
            errors['email']="There is already a user with this email address."
            return errors
        if len(postData['first_name'])<2:
            errors["first_name"] = "first name should be at least 2 characters long."
        if (postData['first_name']).isalpha() !=True:
            errors["first_name2"] = "first name should be comprised only of letters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last name should be at least 2 characters long."
        if (postData['last_name']).isalpha() !=True:
            errors["last_name2"] = "last name should be comprised only of letters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email2'] = ("email address is not a valid format.")
        if len(postData['password']) < 8:
            errors["password"] = "password should be at least 8 characters long."
        return errors
    
    def admin_validator(self, postData):
        errors = {}
        reuser=User.objects.filter(email=postData['email'])
        if reuser:
            errors['email']="There is already a user with this email address."
            return errors
        if len(postData['first_name'])<2:
            errors["first_name"] = "first name should be at least 2 characters long."
        if (postData['first_name']).isalpha() !=True:
            errors["first_name2"] = "first name should be comprised only of letters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last name should be at least 2 characters long."
        if (postData['last_name']).isalpha() !=True:
            errors["last_name2"] = "last name should be comprised only of letters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email2'] = ("email address is not a valid format.")
        if len(postData['password']) < 8:
            errors["password"] = "password should be at least 8 characters long."
        return errors

    def order_validator(self, postData):
        errors = {}
        if len(postData['o_name'])<2:
            errors["o_name"] = "the name should be at least 2 characters long."
        if (postData['o_name']).isalpha() !=True:
            errors["o_name"] = "the name should be comprised only of letters."
            
        if len(postData['date_birth']) < 2:
            errors["date_birth"] = "Make sure of the entered Birth Date syntax."
            
        if len(postData['address']) < 2:
            errors["address"] = "Place of birth should be at least 2 characters long."
        if (postData['address']).isalpha() !=True:
            errors["address"] = "Place of birth should be comprised only of letters."

        if len(postData['phone']) < 10:
            errors["phone"] = "Phone should be 10 numbers long."
        return errors

class Role(models.Model):
    isAdmin = models.BooleanField(null=False)
    isUser = models.BooleanField(null=True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)



class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    address = models.CharField(max_length = 255)
    password = models.CharField(max_length = 45)
    role = models.ForeignKey(Role, related_name='role', on_delete= models.CASCADE, null = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)
    objects = UserManager()

class Product(models.Model):
    title = models.CharField(max_length = 45)
    description = models.TextField()
    image = models.ImageField(blank = True, null = True)
    price = models.FloatField()
    like = models.ManyToManyField(User, related_name = 'liked_products')
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)
    def __str__(self):
        return self.title

class Review(models.Model):
    content= models.TextField(null=False)
    product_id= models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id= models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

class Order(models.Model):
    name = models.CharField(max_length = 60)
    date_of_birth =  models.DateField()
    place_of_birth = models.CharField(max_length = 60)
    phone = models.CharField(max_length = 10)
    total_price = models.FloatField(default= 0.0)
    user_id= models.ForeignKey(User, on_delete=models.CASCADE)
    product_id= models.ForeignKey(Product, on_delete=models.CASCADE)
    
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

