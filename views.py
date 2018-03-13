from django.http import HttpResponse
from django.template import loader 

from .models import peeringdbnodes
from django.contrib.auth.models import User

# Create your views here.

def peeringlist(request):
	peeringdb_list = peeringdbnodes.objects.all()
	template = get_template('index.html')
	variables = Context ({
		'asn':asn,
		'peeringdb_list': peeringdb_list
	})
		
        output = template.render(variables)
	return HttpResponse (output)
