from django.contrib import admin
from .models import Przepisy
from .models import Skladniki
from .models import Kategorie
# Register your models here.


admin.site.register(Przepisy)
admin.site.register(Skladniki)
admin.site.register(Kategorie)

class PrzepisyInline(admin.TabularInline):
	model = Przepisy
	#extra = 1
	
class KategorieInline(admin.TabularInline):
	model = Kategorie

class FeedAdmin(admin.ModelAdmin):
	inlines = (PrzepisyInline, KategorieInline)