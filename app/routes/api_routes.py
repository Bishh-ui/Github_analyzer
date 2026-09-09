from flask import Blueprint, jsonify, request
from ..services.advanced_github_service import AdvancedGitHubService

api_bp = Blueprint('api', __name__)
github_service = AdvancedGitHubService()

# Helper function to get limiter and cache
def get_limiter():
    try:
        from .. import limiter
        return limiter
    except:
        return None

def get_cache():
    try:
        from .. import cache
        return cache
    except:
        return None


@api_bp.route('/user/<username>', methods=['GET'])
def get_user_stats(username):
    """Get comprehensive user statistics"""
    stats, error = github_service.get_comprehensive_user_stats(username)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(stats), 200


@api_bp.route('/user/<username>/history', methods=['GET'])
def get_user_history(username):
    """Get historical analytics for a user"""
    days = request.args.get('days', default=90, type=int)
    days = min(days, 365)  # Cap at 1 year
    
    history = github_service.get_user_history(username, days)
    
    return jsonify({
        'username': username,
        'days': days,
        'history': history
    }), 200


@api_bp.route('/compare', methods=['POST'])
def compare_users():
    """Compare multiple users"""
    data = request.get_json()
    
    if not data or 'usernames' not in data:
        return jsonify({'error': 'usernames field is required'}), 400
    
    usernames = data['usernames']
    
    if not isinstance(usernames, list) or len(usernames) < 2:
        return jsonify({'error': 'At least 2 usernames required'}), 400
    
    from ..config.config import MAX_COMPARISON_USERS
    if len(usernames) > MAX_COMPARISON_USERS:
        return jsonify({'error': f'Maximum {MAX_COMPARISON_USERS} users can be compared'}), 400
    
    comparisons = github_service.compare_users(usernames)
    
    return jsonify({
        'comparison': comparisons,
        'count': len(comparisons)
    }), 200


@api_bp.route('/rate-limit', methods=['GET'])
def get_rate_limit():
    """Get current GitHub API rate limit"""
    rate_limit = github_service.get_rate_limit()
    return jsonify(rate_limit), 200


@api_bp.route('/search/users', methods=['GET'])
def search_users():
    """Search for GitHub users"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'query parameter q is required'}), 400
    
    try:
        users = github_service.github.search_users(query)
        
        results = []
        for user in users[:20]:  # Limit to 20 results
            results.append({
                'login': user.login,
                'name': user.name,
                'avatar_url': user.avatar_url,
                'bio': user.bio,
                'location': user.location,
                'followers': user.followers,
                'public_repos': user.public_repos,
                'url': user.html_url
            })
        
        return jsonify({
            'query': query,
            'total_count': users.totalCount,
            'results': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/trending', methods=['GET'])
def get_trending():
    """Get trending repositories (mock implementation)"""
    # This is a simplified version. For real trending, you'd use GitHub's trending API
    # or implement custom logic
    
    return jsonify({
        'message': 'Trending feature - implement with GitHub trending API or custom logic',
        'repositories': []
    }), 200


@api_bp.route('/languages', methods=['GET'])
def get_popular_languages():
    """Get popular programming languages"""
    popular_languages = [
        {'name': 'JavaScript', 'color': '#f1e05a'},
        {'name': 'Python', 'color': '#3572A5'},
        {'name': 'Java', 'color': '#b07219'},
        {'name': 'TypeScript', 'color': '#2b7489'},
        {'name': 'C++', 'color': '#f34b7d'},
        {'name': 'C#', 'color': '#178600'},
        {'name': 'PHP', 'color': '#4F5D95'},
        {'name': 'Ruby', 'color': '#701516'},
        {'name': 'Go', 'color': '#00ADD8'},
        {'name': 'Rust', 'color': '#dea584'}
    ]
    
    return jsonify(popular_languages), 200


@api_bp.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429


@api_bp.errorhandler(404)
def not_found_handler(e):
    """Handle not found"""
    return jsonify({
        'error': 'Resource not found',
        'message': str(e.description)
    }), 404


@api_bp.errorhandler(500)
def internal_error_handler(e):
    """Handle internal server error"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500
