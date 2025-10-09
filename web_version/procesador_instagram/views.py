import json
import csv
from io import StringIO
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadForm

def extract_usernames(file_content, file_type):
    data = json.loads(file_content)
    usernames = []
    if file_type == 'followers':
        for user in data:
            try:
                username = user['string_list_data'][0]['value']
                usernames.append(username)
            except (KeyError, IndexError):
                continue
    elif file_type == 'following':
        relationships_following = data.get('relationships_following', [])
        for user in relationships_following:
            try:
                username = user['string_list_data'][0]['value']
                usernames.append(username)
            except (KeyError, IndexError):
                continue
    return usernames

def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            followers_file = request.FILES['followers_file'].read().decode('utf-8')
            following_file = request.FILES['following_file'].read().decode('utf-8')
            
            followers = set(extract_usernames(followers_file, 'followers'))
            following = set(extract_usernames(following_file, 'following'))
            
            non_followers = following - followers
            
            # Genera CSV en memoria
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["Usuario"])
            for user in sorted(non_followers):
                writer.writerow([user])
            
            response = HttpResponse(output.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="non_followers.csv"'
            return response
    else:
        form = UploadForm()
    
    return render(request, 'procesador_instagram/upload.html', {'form': form})