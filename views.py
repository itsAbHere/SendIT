from email import message
import boto3
from django.conf import settings
from .forms import FileUploadForm
from django.http import JsonResponse
from django.shortcuts import render
from .forms import FileUploadForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import File


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the file from the form
            uploaded_file = request.FILES['file']
            
            # Upload file to S3
            s3 = boto3.client('s3',
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_S3_REGION_NAME)
            try:
                # Open the file in read mode
                with uploaded_file.open('rb') as file_data:
                    # Upload file data to S3 bucket
                    s3.upload_fileobj(file_data, settings.AWS_STORAGE_BUCKET_NAME, uploaded_file.name)
            except Exception as e:
                # Handle upload failure
                return JsonResponse({'error': 'Failed to upload file to S3'}, status=500)
            return redirect(upload_success)
        else:
            form=FileUploadForm()
            return render(request,'upload_file.html',{'form':form})
            
            # Save file info to the database
            file_instance = form.save(commit=False)
            file_instance.uploaded_by = request.user if request.user.is_authenticated else None  # Assign the user instance or None if not authenticated
            file_instance.save()
            return JsonResponse({'message': 'File uploaded successfully'})
def index(request):
    return render(request, 'index.html')

def file_list(request):
    files = File.objects.all()  # Retrieve all uploaded files from the database
    return render(request, 'file_list.html', {'files': files})

def upload_success(request):
    return render(request, 'upload_success.html')