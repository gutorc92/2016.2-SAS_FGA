from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PasswordForm
from .forms import UserForm, NewUserForm, LoginForm, EditUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from sas.views import index
from django.views import View

class NewUserView(View):
	form_class = NewUserForm
	template_name = 'user/newUser.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class
		return render(request, self.template_name, {'form_user': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user_profile = form.save()
			messages.success(request,_('You have been registered'))
			return index(request)

		return render(request, self.template_name, {'form_user': form})


def list_user(request):
    users = UserProfile.objects.all()
    return render(request, 'user/listUser.html', {'users': users})


def edit_user(request):
	if request.user.is_authenticated() and request.method == "POST":
		form = EditUserForm(request.POST, instance=request.user.profile_user)
		if form.is_valid():
			user = form.save()
			messages.success(request, _('Your data has been updated'))
		return render_edit_user(request, user_form=form)
	elif not request.user.is_authenticated():
		return index(request)
	else:
		return render_edit_user(request)


def render_edit_user(request, user_form=None, change_form=PasswordForm()):
	user = request.user
	initial = {}
	initial['name'] = user.profile_user.full_name()
	initial['email'] = user.email

	if user_form is None:
		user_form = EditUserForm(initial=initial,
								 instance=request.user.profile_user)
	return render(request,
				  'user/editUser.html',
				  {'form_user': user_form, 'change_form': change_form})


def login_user(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.save()
			if user is not None:
				login(request, user);
				return render(request, 'sas/home.html', {})
			else:
				return render(request, 'sas/index.html', {'form': form})
		else:
			return render(request, 'sas/index.html', {'form': form})
	else:
		return index(request)


def logout_user(request):
    logout(request)
    form = LoginForm()
    return render(request, 'sas/index.html', {'form': form})


def delete_user(request):
	if request.user.is_authenticated():
		request.user.delete()
		logout(request)
		return index(request)
	else:
		return index(request)


def change_password(request):
	if request.user.is_authenticated() and request.POST:
		form = PasswordForm(request.POST)
		if form.is_valid() and form.is_password_valid(request.user.username):
			form.save(request.user)
			login(request, request.user)
			messages.success(request, _('Your password has been changed'))
			return render_edit_user(request)
		else:
			return render_edit_user(request, change_form=form)
	if not request.user.is_authenticated():
		return index(request)
	else:
		return render_edit_user(request)
