from django.contrib import admin
from .models import MarkdownFile,Chunk
# Register your models here.

admin.site.register([MarkdownFile, Chunk])
