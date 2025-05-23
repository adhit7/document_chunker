from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MarkdownFile, Chunk, Reference
from .serializer import MarkdownFileSerializer, ChunkSerializer, ReferenceSerializer
from .helper import chunk_markdown
import os

# /upload -> Upload markdown file
@api_view(['POST'])
def upload_markdown_file(request):
    serializer = MarkdownFileSerializer(data=request.data)
    if serializer.is_valid():
        markdown_file = serializer.save()

        # Read file content
        content = markdown_file.file.read().decode('utf-8')
        markdown_file.content = content
        markdown_file.save()
        
        # Save the uploaded file temporarily to disk
        chunks_data, references_data = chunk_markdown(content)

        chunk_map = {}
        for chunk in chunks_data:
            chunk_obj = Chunk.objects.create(
                markdown_file=markdown_file,
                chunk_number=chunk['chunk_number'],
                content=chunk['content'],
                headings=chunk.get('headings', {}),
                chunk_type=chunk.get('chunk_type', 'paragraph'),
                meta=chunk.get('meta', {})
            )
            chunk_map[chunk['chunk_number']] = chunk_obj

        # Save references to DB with foreign key to the corresponding chunk
        for ref in references_data:
            chunk_obj = chunk_map.get(ref['chunk_number'])
            if chunk_obj:
                Reference.objects.create(
                    markdown_file=markdown_file,
                    chunk=chunk_obj,
                    url=ref['url'],
                    anchor_text=ref['text']
                )

        return Response({"message": "File uploaded and chunked"}, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
# /markdown/<id>/chunks -> Pass the file id then get all the chunks of that     
@api_view(['GET'])
def get_chunks(request, markdown_id):
    try:
        md_file = MarkdownFile.objects.get(id=markdown_id)
        chunks = md_file.chunks.all().order_by('chunk_number')
        serializer = ChunkSerializer(chunks, many=True)

        # Extract filename from file path and capitalize first letter (optional)
        filename = os.path.basename(md_file.file.name)  # e.g. "new.md"
        filename_no_ext = os.path.splitext(filename)[0]  # e.g. "new"
        display_name = filename_no_ext.capitalize()      # e.g. "New"

        response_data = {
            "file_name": display_name,
            "chunks": serializer.data,
            "total_chunks": chunks.count()
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except MarkdownFile.DoesNotExist:
        return Response(
            {"error": "Markdown file not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {"error": "Something went wrong", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

# /files -> Get all the Files - filename and id
@api_view(['GET'])
def list_markdown_files(request):
    files = MarkdownFile.objects.all()
    serializer = MarkdownFileSerializer(files, many=True)
    return Response(serializer.data)


# / -> Just a checker whether bakend server is running or not
@api_view(['GET'])
def chunker(request):
    return Response({"message": "API is running"})