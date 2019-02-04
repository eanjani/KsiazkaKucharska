# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib import admin
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
import StringIO, os, re
from django import template



register = template.Library()

global_words = {}

def isNumeric(i): #pomocnicza
        return str(i).replace(".", "").isdigit()

class Skladniki(models.Model):
        id = models.AutoField(primary_key = True)
        nazwa = models.CharField(
                max_length = 50,
                )
        
        UNIT_CHOICES = (
                ('kg','kg'),
                ('daq','dag'),
                ('l','l'),
                ('ml','ml'),
                ('lyz','lyz'),
                ('op','op'),
                ('szt','szt'),
				('szkl','szkl'),
                )

	miara = models.CharField(
                max_length = 10,
                choices = UNIT_CHOICES,
                default = 'szt',
                )

        ilosc  = models.DecimalField(
                max_digits = 3,
                decimal_places = 2,
                default = 1,
                )
		
        def __str__(self):
			return self.nazwa.encode('utf8') #return ' '.join([str(self.id),self.name,self.unit,str(self.amount),])- zwraca np: 6 Maslo op 1.00

        class Meta:
                verbose_name_plural="skladniki"
                verbose_name = "skladnik"


class Kategorie(models.Model):
	id = models.AutoField(primary_key = True)
	nazwa = models.CharField(max_length = 25,)
	
	def __str__(self):
		return self.nazwa

        class Meta:
                verbose_name_plural="Kategorie"
	
class Przepisy(models.Model):

        id = models.AutoField(primary_key = True)
        nazwa = models.CharField(max_length = 60,)
	kategoria = models.ForeignKey(Kategorie, blank=True, null = True)
        #lista_skladnikow = models.ManyToManyField(Skladniki)
        ilosc_porcji = models.DecimalField(
                max_digits = 2,
                decimal_places = 0,
                default = 1,
                )
	przygotowanie = models.TextField()
	#fotografia = models.ImageField(upload_to = 'foto/', default = '/static/foto/no_image.jpg', blank = True)
        #fotografia_url = models.URLField(null = True, blank = True)
	


        #resize image
        ''' def save(self, *args, **kwargs):
                self.przygotowanie = self.przygotowanie.replace('WINIARY', '')
                if self.fotografia_url:
                        import urllib, os
                        from urlparse import urlparse
                        file_save_dir = 'D:/KsiazkaKucharska/KsiazkaKucharska/static/'
                        filename = urlparse(self.fotografia_url).path.split('/')[-1]
                        urllib.urlretrieve(self.fotografia_url, os.path.join(file_save_dir, filename))
                        self.fotografia= os.path.join(file_save_dir, filename)
                        self.fotografia_url = ''
                if self.fotografia:
                        image = Image.open(StringIO.StringIO(self.fotografia.read()))
                        image.thumbnail((372,279), Image.ANTIALIAS)
                        output = StringIO.StringIO()
                        image.save(output, format='JPEG', quality=75)
                        output.seek(0)
                        self.fotografia = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.fotografia.name, 'image/jpeg', output.len, None)
                super(Przepisy, self).save(*args, **kwargs) '''


	def __str__(self):
                return self.nazwa.encode('utf8') 

        def tags(self):
                chars =['.','-',',',';','?',':','!','...',"(",")",'"']

                stop_words = """a, aby, ale, bardziej, bardzo, bez, bo, bowiem, 
                                był, była, było, były, będzie, co, czy, czyli, 
                                dla, dlatego, do, gdy, gdzie, go, i, ich, im, 
                                innych, iż, jak, jako, jednak, jego, jej, jemu, jest, 
                                jeszcze, jeśli, już, kiedy, kilka, która, które, 
                                którego,której, który, których, którym, którzy, 
                                lub, ma, mi, między, mnie, mogą, może, można, na, 
                                nad, nam, nas, naszego, naszych, nawet, nich, nie, niego,
                                nim, niż, o, od, ono, oni, oraz, po, pod, poza, przed, przede,
                                przez, przy, również, się, sobie, swoje, są, ta, 
                                tak, takie, także, tam, te, tego, tej, temu, ten, też, 
                                to, tu, tych, tylko, tym, u, w, we, wiele, wielu, 
                                więc, właśnie, właściwie, wszystkich, wszystkim, wszystko, z, 
                                za, zawsze, ze, że ,żadny, żaden, zupełnie, zupełny, zupełności """

                stop_words = stop_words.replace(" ","").split(",")
                raw_text = self.przygotowanie.encode('utf8')
                result = []

                for char in chars:
                        raw_text = raw_text.replace(char, "")

                for w in raw_text.split(" "):
                        if w not in stop_words:
                                result.append(w)

                before = len(raw_text.split(" "))
                after = len(result)

                for word in result:
                        if word not in global_words.keys():
                                if not isNumeric(word):
                                        global_words[word] = 1
                        else:
                                global_words[word] = global_words[word]+1
                return global_words.keys()

        class Meta:
                verbose_name_plural="przepisy"
                verbose_name = "przepis"