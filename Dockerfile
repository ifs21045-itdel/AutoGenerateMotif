# Gunakan official Python image dari Docker Hub
FROM python:3.9-slim

# Set environment variabel yang mencegah Python membuat file .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Set environment variabel yang mencegah Python mem-buffer stdout dan stderr
ENV PYTHONUNBUFFERED 1

# Set direktori kerja di dalam container
WORKDIR /app

# Instal gcc dan lainnya libraries yang dibutuhkan
RUN apt-get update && apt-get install -y gcc libmysqlclient-dev

# Salin file requirements.txt ke dalam container
COPY ./requirements.txt /app/requirements.txt

# Instal dependencies Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Salin semua file project ke dalam container
COPY . /app/

# CMD yang akan dijalankan ketika container di-start
CMD ["gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]