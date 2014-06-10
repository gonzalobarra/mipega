from django import template

register = template.Library()

@register.inclusion_tag("login-modal.html")
def loginModal(userLabel, passLabel):
	labels = {'user':userLabel,'pass':passLabel}
	return labels

