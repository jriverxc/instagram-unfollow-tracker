import csv
import io
import json
from typing import Iterable, Set

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def extract_followers(data: Iterable[dict]) -> Set[str]:
    followers = set()
    for user in data:
        try:
            followers.add(user['string_list_data'][0]['value'])
        except (KeyError, IndexError, TypeError):
            continue
    return followers


def extract_following(data: dict) -> Set[str]:
    following = set()
    for user in data.get('relationships_following', []):
        username = user.get('title')
        if username:
            following.add(username)
    return following


def non_followers_from_payloads(followers_payload: object, following_payload: object) -> tuple[list[str], dict]:
    followers = extract_followers(followers_payload if isinstance(followers_payload, list) else [])
    following = extract_following(following_payload if isinstance(following_payload, dict) else {})
    non_followers = sorted(following - followers)
    stats = {
        'following_count': len(following),
        'followers_count': len(followers),
        'non_followers_count': len(non_followers),
    }
    return non_followers, stats


def build_csv(usernames: list[str]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Usuario'])
    for user in usernames:
        writer.writerow([user])
    return output.getvalue()


def index(request: HttpRequest) -> HttpResponse:
    context = {'error': None, 'stats': None, 'non_followers': None, 'non_followers_json': None}

    if request.method == 'POST':
        followers_file = request.FILES.get('followers_file')
        following_file = request.FILES.get('following_file')

        if not followers_file or not following_file:
            context['error'] = 'Debes subir ambos archivos JSON.'
            return render(request, 'tracker/index.html', context)

        try:
            followers_payload = json.load(followers_file)
            following_payload = json.load(following_file)
        except json.JSONDecodeError:
            context['error'] = 'Uno de los archivos no tiene formato JSON válido.'
            return render(request, 'tracker/index.html', context)

        non_followers, stats = non_followers_from_payloads(followers_payload, following_payload)
        context['stats'] = stats
        context['non_followers'] = non_followers
        context['non_followers_json'] = json.dumps(non_followers)

    return render(request, 'tracker/index.html', context)


def download_csv(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse(status=405)

    raw_usernames = request.POST.get('non_followers_json', '[]')
    try:
        usernames = json.loads(raw_usernames)
    except json.JSONDecodeError:
        usernames = []

    if not isinstance(usernames, list):
        usernames = []

    usernames = [user for user in usernames if isinstance(user, str)]

    response = HttpResponse(build_csv(usernames), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="non_followers.csv"'
    return response
