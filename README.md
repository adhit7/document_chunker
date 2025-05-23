# Chunk Mate

## Project Overview
Chunk Mate is a web application designed to help users upload markdown files and efficiently chunk them into smaller content units such as paragraphs, headings, tables, and references (links). The backend processes and stores these chunks along with their contextual headings, allowing users to retrieve and manage markdown content easily via REST APIs. The frontend provides an intuitive interface built with React, Vite, and Tailwind CSS for seamless interaction.

## Tech Stack
- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Frontend:** React, Vite, Tailwind CSS  

### Frontend Repository

You can find the frontend React + Vite + Tailwind CSS code here:  
[Frontend Repo](https://github.com/adhit7/chunk_mate)

### Deployed Frontend Link

Check out the live deployed frontend version of the app here:  
[Live Demo](https://chunk-mate.vercel.app/)

https://github.com/user-attachments/assets/dcca8816-a42b-4acb-aa10-3ff56d29e33f

![UI](https://github.com/user-attachments/assets/dcca8816-a42b-4acb-aa10-3ff56d29e33f)
---

## Setup and Installation

### Prerequisites
- Python 3.8+  
- Node.js 16+  
- PostgreSQL  
- Git  

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/adhit7/document_chunker.git
   cd doc-chunker

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install backend dependencies:
    ```bash
    pip install -r requirements.txt

4. Set environment variables:
    ```bash
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

5. Run database migrations:
    ```bash
    python manage.py migrate

6. Start the Django development server:
    ```bash
    python manage.py runserver





