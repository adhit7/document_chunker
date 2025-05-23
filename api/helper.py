import re

def parse_heading(line, current_headings):
    match = re.match(r'^(#{1,10})\s+(.*)', line)
    if match:
        level = len(match.group(1)) # lenght of ###
        text = match.group(2).strip() # Heading text
        current_headings[level - 1] = text # -1 starts from 0
        for i in range(level, 10):
            current_headings[i] = '' # when new headings encounter clears it out and add the new heading
        return True
    return False

def extract_links(paragraph):
    return re.findall(r'\[([^\]]+)\]\(([^)]+)\)', paragraph)

def save_chunk(chunks, references, paragraph, current_headings):
    if not paragraph.strip():
        return
    heading_context = {f'h{i+1}': current_headings[i] for i in range(10) if current_headings[i]}
    chunk_number = len(chunks) + 1

    chunks.append({
        'chunk_number': chunk_number,
        'content': paragraph,
        'headings': heading_context
    })

    links = extract_links(paragraph)
    for text, url in links:
        references.append({
            'chunk_number': chunk_number,
            'text': text,
            'url': url
        })

def parse_table(lines, start_index, chunks, references, current_headings):
    header_line = lines[start_index].strip()
    headers = [h.strip() for h in header_line.split('|') if h.strip()] # Got all the headers

    # Skip separator line (---|---)
    i = start_index + 2

    while i < len(lines) and lines[i].startswith('|'):
        row = [r.strip() for r in lines[i].split('|') if r.strip()] # Got the data cell
        row_text = ', '.join(f'{headers[j]}: {val}' for j, val in enumerate(row)) # Adds into one string
        save_chunk(chunks, references, row_text, current_headings)
        i += 1
    return i

def parse_paragraph(lines, start_index):
    paragraph = lines[start_index].strip()
    i = start_index
    while i + 1 < len(lines) and lines[i + 1].strip():
        i += 1
        paragraph += ' ' + lines[i].strip()
    return paragraph, i + 1


def chunk_markdown(content):
    chunks = []
    references = []
    current_headings = [''] * 10

    lines = content.splitlines()
    
    i = 0
    while(i < len(lines)):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # Check heading
        if parse_heading(line, current_headings):
            i += 1
            continue
        
        # Check table
        if line.startswith('|'):
            i = parse_table(lines, i, chunks, references, current_headings)
            continue
        
        # Check paragraph
        paragraph,i = parse_paragraph(lines, i)
        save_chunk(chunks, references, paragraph, current_headings)
    return chunks, references