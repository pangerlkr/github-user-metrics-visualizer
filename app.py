import os
import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')  # Optional: Set for higher rate limits

def get_headers():
    """Get headers for GitHub API requests"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def fetch_user_data(username):
    """Fetch user profile data from GitHub API"""
    url = f"{GITHUB_API_URL}/users/{username}"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None

def fetch_user_repos(username):
    """Fetch user repositories from GitHub API"""
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    params = {'per_page': 100, 'sort': 'updated'}
    response = requests.get(url, headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_user_events(username):
    """Fetch recent user events from GitHub API"""
    url = f"{GITHUB_API_URL}/users/{username}/events"
    params = {'per_page': 100}
    response = requests.get(url, headers=get_headers(), params=params)
    if response.status_code == 200:
        return response.json()
    return []

def calculate_metrics(user_data, repos, events):
    """Calculate various metrics from user data"""
    metrics = {
        'user_info': {
            'username': user_data.get('login', ''),
            'name': user_data.get('name', ''),
            'bio': user_data.get('bio', ''),
            'company': user_data.get('company', ''),
            'location': user_data.get('location', ''),
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'created_at': user_data.get('created_at', ''),
            'avatar_url': user_data.get('avatar_url', '')
        },
        'repository_stats': {
            'total_stars': sum(repo.get('stargazers_count', 0) for repo in repos),
            'total_forks': sum(repo.get('forks_count', 0) for repo in repos),
            'total_watchers': sum(repo.get('watchers_count', 0) for repo in repos),
            'languages': {}
        },
        'activity_stats': {
            'total_events': len(events),
            'event_types': {},
            'commits': 0,
            'pull_requests': 0,
            'issues': 0
        }
    }
    
    # Calculate language distribution
    for repo in repos:
        if repo.get('language'):
            lang = repo['language']
            metrics['repository_stats']['languages'][lang] = \
                metrics['repository_stats']['languages'].get(lang, 0) + 1
    
    # Calculate activity breakdown
    for event in events:
        event_type = event.get('type', 'Unknown')
        metrics['activity_stats']['event_types'][event_type] = \
            metrics['activity_stats']['event_types'].get(event_type, 0) + 1
        
        if event_type == 'PushEvent':
            metrics['activity_stats']['commits'] += len(event.get('payload', {}).get('commits', []))
        elif event_type == 'PullRequestEvent':
            metrics['activity_stats']['pull_requests'] += 1
        elif event_type == 'IssuesEvent':
            metrics['activity_stats']['issues'] += 1
    
    return metrics

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/user/<username>', methods=['GET'])
def get_user_metrics(username):
    """API endpoint to get user metrics"""
    try:
        user_data = fetch_user_data(username)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        repos = fetch_user_repos(username)
        events = fetch_user_events(username)
        
        metrics = calculate_metrics(user_data, repos, events)
        
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
