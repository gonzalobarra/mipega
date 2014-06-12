from django import template

register = template.Library()


def loginModal():
	labels = {'user':"RUT",'pass':"Password"}
	return labels

register.inclusion_tag('modal-login.html')(loginModal)