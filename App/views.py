from django.shortcuts import render
import os, re, codecs
import MySQLdb
from .models import Przepisy
from .models import Skladniki
from .models import Kategorie
from .forms import PrzepisForm
from .forms import SkladnikForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.template import loader, Context
from django.db.models import Q
import StringIO, hashlib
from django.core.files import File
from PIL import Image, ImageOps
from django.forms import modelformset_factory
from django.contrib import messages
from klasyfikacja import classifyText
from similarity import compare
from django.shortcuts import render

# Create your views here.

def przepisy(request):
	przepisy = Przepisy.objects.order_by('nazwa')
	return render(request,'cookbook/przepisy.html',{'przepisy' : przepisy.order_by('nazwa')})
	
def nowySkladnik(request):
	if request.method == 'POST':
            form = SkladnikForm(request.POST)
            if form.is_valid():
        		form.save()
        		return HttpResponseRedirect('/')
	else:
            form = SkladnikForm()
        return render(request, 'cookbook/skladnik.html', {'form': form})
	
def nowyPrzepis(request):
	if request.method == 'POST':
		form = PrzepisForm(request.POST, request.FILES)
		if form.is_valid():
				form.save()
				return HttpResponseRedirect('/') # zrobic przekierowanie do nowo dodanego przepisu
        else:
    		form = PrzepisForm()
	return render(request, 'cookbook/przepis.html', {'form':form})

def resizeImg(infile):
	size = 372,279
	outfile = os.path.splitext(infile)[0] + '.thumbnail'
	try:
		im = Image.open(infile)
		im.thumbnail(size, Image.ANTIALIAS)
		im.save(outfile, 'JPEG')
	except IOError:
		print "Cannot create thumbnail for  '%s'" % infile

def post_detail(request, pk):
	taggedWords = getTags(pk)
	return render(request, 'cookbook/post_detail.html', {'przepis': Przepisy.objects.get(id=pk), 'taggedWords':taggedWords})

def getTags(pk):
	encoding = "utf-8"
	on_error = "replace"

	db = MySQLdb.connect('localhost', 'root','mysql','cookbook', charset = 'utf8',use_unicode=True)
	con = db.cursor()
	post = get_object_or_404(Przepisy, pk=pk)

	puncList = [',','.',':','-','!','(',')','\n','\r','?',';']
	txt = post.przygotowanie
	for p in puncList:
		txt = txt.replace(p," ")
		words = txt.split(" ")

	taggedWords = ''
	for word in words:
		con.execute("select id, word from cookbook.words where word ='"+word.lower()+"';")
		if con.rowcount > 0:
			data = con.fetchone()
			taggedWords+=word+','
		else:
			pass
	return taggedWords[:-1]

def simple_search(request):
	query = request.GET['q']
	results =  Przepisy.objects.filter(Q(nazwa__icontains=query) | Q(przygotowanie__icontains=query)) #dodac wyszukiwanie po skladnikach
	template = loader.get_template('cookbook/search_results.html')
	context = Context({'query':query, 'results':results.order_by('nazwa')})
	response = template.render(context)
	return HttpResponse(response)	


def detailed_search(request):
	nazwa = request.GET['n']
	kategoria = request.GET['category']
	sklad = request.GET['s']
	opis = request.GET['p']

	kategoria_id = Kategorie.objects.filter(nazwa__exact = kategoria)

	results =  Przepisy.objects.filter(Q(nazwa__icontains=nazwa) &
										Q(przygotowanie__icontains=opis) &
										Q(przygotowanie__icontains=sklad) &
										Q(kategoria__exact=kategoria_id) )
	template = loader.get_template('cookbook/detailedsearch_results.html')
	context = Context({'nazwa':nazwa, 'kategoria':kategoria,'sklad':sklad, 'opis':opis, 'results':results.order_by('nazwa')})
	response = template.render(context)
	return HttpResponse(response)	


def isNumeric(i): #pomocnicza
    return str(i).replace(",","").isdigit()

def change_ingredients(request, pk):
	value = request.POST['ilosc']
	post = get_object_or_404(Przepisy, pk=pk)
	lines = post.przygotowanie.split("\n")
	regexp = re.compile('\(.*\d*.*\)\r$')
	sklad = []
	for l in lines:
		if regexp.search(l) is not None:
			l = l.replace("\r", "").replace("(", "").replace(")","")
			items = l.split(" ")
			for item in items:
				if isNumeric(item.encode('ascii', 'ignore')):
					index = items.index(item)
					item = item.replace(",", ".")
					ratio = float(value)/float(post.ilosc_porcji)
					items[index] = str(round(float(item)*ratio,2))
				l = " ".join(x.strip() for x in items)
			sklad.append(l)
	return render(request, 'cookbook/post_detail.html', {'przepis': Przepisy.objects.get(id=pk), 'sklad':sklad, 'value':value })


def classify(request, pk):
	#post = get_object_or_404(Przepisy, pk=pk)
	taggedWords = getTags(pk)
	result = classifyText(pk)
	return render(request, 'cookbook/post_detail.html', {'przepis': Przepisy.objects.get(id=pk), 'result':result, 'taggedWords':taggedWords} )

def find_similar(request, pk):
	taggedWords = getTags(pk)
	obj = compare(pk)
	results = []
	for o in obj:
		przepis = Przepisy.objects.get(id=o)
		results.append(przepis)
	return render(request, 'cookbook/post_detail.html', {'przepis':Przepisy.objects.get(id=pk), 'objects':results, 'taggedWords':taggedWords})

def addtag(request, pk):
	taggedWords = getTags(pk)
	phrase = request.POST.get('phrase').strip()
	tag = request.POST.get('tag').strip()
	db = MySQLdb.connect('localhost', 'root','mysql','cookbook', charset = 'utf8',use_unicode=True)
	con = db.cursor()
	con.callproc('new_word',[phrase])
	db.commit()
	con.callproc('new_tag', [tag])
	db.commit()
	con.callproc('new_pair',(phrase,tag))
	db.commit()
	return render(request, 'cookbook/post_detail.html', {'przepis':Przepisy.objects.get(id=pk), 'phrase':phrase,'tag':tag, 'taggedWords':taggedWords})


