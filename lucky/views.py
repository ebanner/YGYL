import random
import urllib

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    """Return a hard-coded webm

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): the request object

    """
    template = loader.get_template('lucky/index.html')
    html = template.render()
    download_webm()
    return HttpResponse(html)

def get_ygyl_id():
    """Fetch a YGYL thread ID from the 4chan API

    Returns:
        `thread_id` where http://boards.4chan.org/gif/thread/{thread_id} is a
        YGYL thread

    """
    pages = requests.get('https://a.4cdn.org/gif/catalog.json').json()
    for page in pages:
        for thread in page['threads']:
            if 'ygyl' in thread.get('sub', 'ylyl').lower():
                return thread['no']

def get_ygyl_thread_posts():
    """Get the posts from a YGYL thread"""
    ygyl_id = get_ygyl_id()
    thread = requests.get(f'https://a.4cdn.org/gif/thread/{ygyl_id}.json').json()
    return thread['posts']

def download_webm(lucky=True, dirpath='lucky/static/lucky', filename='example.webm'):
    """Download a YGYL webm

    Arguments:
        lucky (bool): pick a random webm if True and the first one otherwise
        dirpath (str): path to save the webm in
        filename (str): name to give to the downloaded webm

    """
    posts = get_ygyl_thread_posts()
    post = pick_random_post(posts) if lucky else pick_first_post(posts)
    tim = post['tim']
    webm_url = f'http://i.4cdn.org/gif/{tim}.webm'
    path, response = urllib.request.urlretrieve(webm_url, f'{dirpath}/{filename}')
    return response

def pick_first_post(posts):
    """Pick the first post

    Arguments:
        posts (dict): posts in a YGYL thread

    The winning post must have a webm attached to it.

    >>> posts = get_ygyl_thread_posts()

    """
    for post in posts:
        if post.get('ext', None) == '.webm':
            return post

def pick_random_post(posts):
    """Pick a random post

    Arguments:
        posts (dict): posts in a YGYL thread

    The winning post must have a webm attached to it.

    >>> posts = get_ygyl_thread_posts()

    """
    while True:
        post = random.choice(posts)
        if post.get('ext', None) == '.webm':
            break
    return post

def loop():
    pass
