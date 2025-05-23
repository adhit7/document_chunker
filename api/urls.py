from django.urls import path
from . import views

urlpatterns = [
  path('upload', views.upload_markdown_file),
  path('markdown/<int:markdown_id>/chunks', views.get_chunks),
  path('files', views.list_markdown_files),
  path('', views.chunker)
]