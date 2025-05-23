from django.db import models

class MarkdownFile(models.Model):
    file = models.FileField(upload_to='markdown_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Use the filename from the FileField for display
        return self.file.name.split('/')[-1]

class Chunk(models.Model):
    CHUNK_TYPES = [
        ('heading', 'Heading'),
        ('paragraph', 'Paragraph'),
        ('table', 'Table'),
        ('code', 'Code Block'),
        ('list', 'List'),
        ('image', 'Image'),
    ]

    markdown_file = models.ForeignKey(MarkdownFile, on_delete=models.CASCADE, related_name='chunks')
    chunk_number = models.PositiveIntegerField()
    chunk_type = models.CharField(max_length=20, choices=CHUNK_TYPES)
    content = models.TextField()
    headings = models.JSONField(default=dict, blank=True)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('markdown_file', 'chunk_number')
        ordering = ['chunk_number']

class Reference(models.Model):
    markdown_file = models.ForeignKey(MarkdownFile, on_delete=models.CASCADE)
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE)
    url = models.URLField()
    anchor_text = models.CharField(max_length=255, blank=True)
