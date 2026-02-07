# GitHub User Metrics Visualizer
##Panger
A modern web application that fetches and visualizes GitHub user metrics, statistics, and contribution data through interactive charts and graphs.

## Features

- **User Profile Information**: Display comprehensive user details including avatar, bio, company, and location
- **Repository Statistics**: Show total repositories, stars, forks, and watchers
- **Programming Language Distribution**: Interactive doughnut chart showing language usage across repositories
- **Activity Analytics**: Visualize user activity with event type breakdown (commits, pull requests, issues)
- **Real-time Data**: Fetches live data directly from GitHub API
- **Modern UI**: Beautiful gradient design with responsive layout
- **Interactive Charts**: Powered by Chart.js for smooth, interactive visualizations

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Chart.js
- **API**: GitHub REST API v3
- **HTTP Client**: Requests library

## Project Structure

```
github-user-metrics-visualizer/
├── app.py                 # Flask application and API endpoints
├── templates/
│   └── index.html        # Frontend HTML template
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/pangerlkr/github-user-metrics-visualizer.git
   cd github-user-metrics-visualizer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up GitHub Token** (optional, for higher rate limits)
   ```bash
   export GITHUB_TOKEN="your_github_personal_access_token"
   # On Windows: set GITHUB_TOKEN=your_github_personal_access_token
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a GitHub username in the search box
2. Click the "Analyze" button
3. View the user's profile information, statistics, and visualizations

### Example Users to Try
- `torvalds` - Linus Torvalds
- `gvanrossum` - Guido van Rossum
- `tj` - TJ Holowaychuk
- `sindresorhus` - Sindre Sorhus

## API Endpoints

### GET /
Serves the main HTML page

### GET /api/user/<username>
Fetches and returns user metrics for the specified GitHub username

**Response Format:**
```json
{
  "user_info": {
    "username": "string",
    "name": "string",
    "bio": "string",
    "company": "string",
    "location": "string",
    "public_repos": 0,
    "followers": 0,
    "following": 0,
    "created_at": "string",
    "avatar_url": "string"
  },
  "repository_stats": {
    "total_stars": 0,
    "total_forks": 0,
    "total_watchers": 0,
    "languages": {}
  },
  "activity_stats": {
    "total_events": 0,
    "event_types": {},
    "commits": 0,
    "pull_requests": 0,
    "issues": 0
  }
}
```

## Configuration

### GitHub API Rate Limits

- **Without authentication**: 60 requests per hour
- **With authentication**: 5,000 requests per hour

To increase rate limits, set a GitHub personal access token:

```bash
export GITHUB_TOKEN="your_token_here"
```

## Development

### Running in Debug Mode

The application runs in debug mode by default during development:

```bash
python app.py
```

### Making Changes

- **Backend**: Modify `app.py` for API logic
- **Frontend**: Edit `templates/index.html` for UI changes
- **Dependencies**: Update `requirements.txt` when adding new packages

## Deployment

### Deploy to Production

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

### Deployment Platforms

- **Heroku**: Add `Procfile` with `web: gunicorn app:app`
- **Render**: Configure as a web service
- **Railway**: Auto-detect Flask application
- **Vercel**: Use serverless function wrapper

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- GitHub API for providing comprehensive user data
- Chart.js for beautiful and interactive charts
- Flask community for the excellent web framework

## Author

**Pangerkumzuk Longkumer**
- GitHub: [@pangerlkr](https://github.com/pangerlkr)
- Company: NEXUSCIPHERGUARD INDIA

## Support

If you found this project helpful, please give it a ⭐️!

---

Made with ❤️ by Pangerkumzuk Longkumer
