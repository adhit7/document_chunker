# serializers.py
from rest_framework import serializers
from .models import MarkdownFile, Chunk, Reference

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'url', 'anchor_text']  


class ChunkSerializer(serializers.ModelSerializer):
    references = ReferenceSerializer(many=True, read_only=True, source='reference_set')

    class Meta:
        model = Chunk
        fields = ['id', 'chunk_number', 'chunk_type', 'content', 'headings', 'meta', 'created_at', 'markdown_file', 'references']


class MarkdownFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkdownFile
        fields = ['id', 'file']

