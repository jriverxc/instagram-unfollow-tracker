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
    context = {'error': None, 'stats': None, 'non_followers': None}

    if request.method == 'POST':
        followers_file = request.FILES.get('followers_file')
        following_file = request.FILES.get('following_file')
        action = request.POST.get('action', 'view')

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

        if action == 'download':
            response = HttpResponse(build_csv(non_followers), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="non_followers.csv"'
            return response

        context['stats'] = stats
        context['non_followers'] = non_followers

    return render(request, 'tracker/index.html', context)
