import os
import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
from collections import defaultdict

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
    """Fetch user repositories"""
    url = f"{GITHUB_API_URL}/users/{username}/repos?per_page=100"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []

def fetch_user_events(username):
    """Fetch user recent events for activity analysis"""
    url = f"{GITHUB_API_URL}/users/{username}/events?per_page=100"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []

def calculate_language_stats(repos):
    """Calculate programming language statistics"""
    languages = {}
    for repo in repos:
        if repo['language']:
            languages[repo['language']] = languages.get(repo['language'], 0) + 1
    return languages

def calculate_activity_stats(events):
    """Calculate activity statistics from events"""
    activity = {}
    for event in events:
        event_type = event['type']
        activity[event_type] = activity.get(event_type, 0) + 1
    return activity

def calculate_contribution_stats(events):
    """Calculate detailed contribution statistics"""
    stats = {
        'commits': 0,
        'pull_requests': 0,
        'issues': 0,
        'reviews': 0,
        'total_contributions': 0
    }
    
    for event in events:
        if event['type'] == 'PushEvent':
            stats['commits'] += len(event.get('payload', {}).get('commits', []))
        elif event['type'] == 'PullRequestEvent':
            stats['pull_requests'] += 1
        elif event['type'] == 'IssuesEvent':
            stats['issues'] += 1
        elif event['type'] == 'PullRequestReviewEvent':
            stats['reviews'] += 1
    
    stats['total_contributions'] = stats['commits'] + stats['pull_requests'] + stats['issues'] + stats['reviews']
    return stats

def analyze_activity_times(events):
    """Analyze most active times of day"""
    hours = defaultdict(int)
    for event in events:
        created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        hour = created_at.hour
        hours[hour] += 1
    
    # Return top 5 most active hours
    sorted_hours = sorted(hours.items(), key=lambda x: x[1], reverse=True)[:5]
    return [{'hour': h, 'count': c} for h, c in sorted_hours]

def calculate_streak_data(events):
    """Calculate contribution streak information"""
    if not events:
        return {'current_streak': 0, 'longest_streak': 0, 'total_days': 0}
    
    dates = set()
    for event in events:
        created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        dates.add(created_at.date())
    
    sorted_dates = sorted(dates, reverse=True)
    current_streak = 0
    longest_streak = 0
    temp_streak = 1
    
    # Calculate current streak
    today = datetime.now().date()
    if sorted_dates and (today - sorted_dates[0]).days <= 1:
        current_streak = 1
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i-1] - sorted_dates[i]).days == 1:
                current_streak += 1
            else:
                break
    
    # Calculate longest streak
    for i in range(1, len(sorted_dates)):
        if (sorted_dates[i-1] - sorted_dates[i]).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1
    
    longest_streak = max(longest_streak, current_streak)
    
    return {
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'total_days': len(dates)
    }

def calculate_achievements(user_data, repos, events, contribution_stats):
    """Calculate user achievements based on their activity"""
    achievements = []
    
    # Follower achievements
    followers = user_data.get('followers', 0)
    if followers >= 100:
        achievements.append({'name': 'Popular', 'description': '100+ followers', 'icon': '⭐'})
    elif followers >= 50:
        achievements.append({'name': 'Influential', 'description': '50+ followers', 'icon': '🌟'})
    
    # Repository achievements
    public_repos = user_data.get('public_repos', 0)
    if public_repos >= 50:
        achievements.append({'name': 'Prolific', 'description': '50+ repositories', 'icon': '📚'})
    elif public_repos >= 20:
        achievements.append({'name': 'Builder', 'description': '20+ repositories', 'icon': '🏗️'})
    
    # Star achievements
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
    if total_stars >= 100:
        achievements.append({'name': 'Star Collector', 'description': '100+ stars', 'icon': '⭐'})
    elif total_stars >= 50:
        achievements.append({'name': 'Rising Star', 'description': '50+ stars', 'icon': '✨'})
    
    # Contribution achievements
    if contribution_stats['commits'] >= 100:
        achievements.append({'name': 'Committed', 'description': '100+ commits', 'icon': '💪'})
    
    if contribution_stats['pull_requests'] >= 20:
        achievements.append({'name': 'Collaborator', 'description': '20+ pull requests', 'icon': '🤝'})
    
    # Activity achievements
    if len(events) >= 50:
        achievements.append({'name': 'Active', 'description': '50+ recent activities', 'icon': '🔥'})
    
    # Account age achievements
    created_at = datetime.strptime(user_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    account_age = (datetime.now() - created_at).days
    if account_age >= 365 * 3:
        achievements.append({'name': 'Veteran', 'description': '3+ years on GitHub', 'icon': '🎖️'})
    elif account_age >= 365:
        achievements.append({'name': 'Member', 'description': '1+ year on GitHub', 'icon': '🎉'})
    
    return achievements

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user/<username>', methods=['GET'])
def get_user_stats(username):
    """Get comprehensive user statistics"""
    user_data = fetch_user_data(username)
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    
    repos = fetch_user_repos(username)
    events = fetch_user_events(username)
    
    language_stats = calculate_language_stats(repos)
    activity_stats = calculate_activity_stats(events)
    contribution_stats = calculate_contribution_stats(events)
    activity_times = analyze_activity_times(events)
    streak_data = calculate_streak_data(events)
    achievements = calculate_achievements(user_data, repos, events, contribution_stats)
    
    # Calculate total stars and forks
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
    total_forks = sum(repo.get('forks_count', 0) for repo in repos)
    
    return jsonify({
        'user': {
            'name': user_data.get('name', username),
            'login': user_data['login'],
            'avatar_url': user_data['avatar_url'],
            'bio': user_data.get('bio', ''),
            'location': user_data.get('location', ''),
            'company': user_data.get('company', ''),
            'blog': user_data.get('blog', ''),
            'twitter_username': user_data.get('twitter_username', ''),
            'followers': user_data['followers'],
            'following': user_data['following'],
            'public_repos': user_data['public_repos'],
            'created_at': user_data['created_at']
        },
        'stats': {
            'total_stars': total_stars,
            'total_forks': total_forks,
            'languages': language_stats,
            'activity': activity_stats,
            'contributions': contribution_stats,
            'activity_times': activity_times,
            'streak': streak_data
        },
        'achievements': achievements
    })

if __name__ == '__main__':
    app.run(debug=True)
