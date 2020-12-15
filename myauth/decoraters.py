from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('Dash')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return redirect('/')
		return wrapper_func
	return decorator

def allowed_Facilitator_Dashboard():
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.groups.filter(name='Facilitators').exists():
				if request.user.groups.filter(name='Admins').exists():
					return view_func(request, *args, **kwargs)
				if request.user.groups.filter(name='Learners').exists():
					return view_func(request, *args, **kwargs)
				return view_func(request, *args, **kwargs)
			else:
				return redirect('/')
				
		return wrapper_func
	return decorator
def allowed_Learners_Dashboard():
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.groups.filter(name='Learners').exists():
				if request.user.groups.filter(name='Admins').exists():
					return view_func(request, *args, **kwargs)
				if request.user.groups.filter(name='Facilitators').exists():
					return view_func(request, *args, **kwargs)
				return view_func(request, *args, **kwargs)
			else:
				return redirect('/')
				
		return wrapper_func
	return decorator

def allowed_Admins_Dashboard():
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.groups.filter(name='Admins').exists():
				if request.user.groups.filter(name='Learners').exists():
					return view_func(request, *args, **kwargs)
				if request.user.groups.filter(name='Facilitators').exists():
					return view_func(request, *args, **kwargs)
				return view_func(request, *args, **kwargs)
			else:
				return redirect('/')
				
		return wrapper_func
	return decorator


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'Customers':
			return redirect('UserHome')

		if group == 'Admins':
			return view_func(request, *args, **kwargs)

	return wrapper_function