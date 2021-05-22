from django.db import models
import re
import bcrypt
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['firstName']) < 2:
            errors['firstName'] = "First name must be at least 2 characters!"

        if len(form['lastName']) < 2:
            errors['lastName'] = "Last name must be at least 2 characters!"

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid email address!'

        checkEmail = self.filter(email=form['email'])
        if checkEmail:
            errors['email'] = "That email has already been taken"

        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"

        if form['password'] != form['confirmpassword']:
            errors['password'] = "Passwords do not match!"
        return errors

    def auth(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode().user.password.encode())


class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
