from flask import Blueprint, render_template, request, jsonify
from ..services.advanced_github_service import AdvancedGitHubService

github_bp = Blueprint('github', __name__)
github_service = AdvancedGitHubService()

# Import cache and limiter after blueprint creation to avoid circular imports
def init_limiter():
    from .. import limiter
    return limiter

def apply_rate_limit(route_func):
    """Decorator to apply rate limiting"""
    try:
        limiter_instance = init_limiter()
        return limiter_instance.limit("30 per minute")(route_func)
    except:
        return route_func

@github_bp.route('/', methods=['GET', 'POST'])
def index():
    """Handle the main page and user analysis requests"""
    username = request.form.get('username') or request.args.get('username')
    mode = request.form.get('mode') or request.args.get('mode', 'single')
    
    if mode == 'compare':
        raw_users = request.form.get('usernames') or request.args.get('usernames', '')
        usernames = [u.strip() for u in raw_users.split(',') if u.strip()]
        
        if len(usernames) < 2:
            return render_template('index.html', error='Please provide at least 2 usernames for comparison')
        
        comparisons = github_service.compare_users(usernames[:5])
        return render_template('compare.html', comparisons=comparisons)
    
    elif username:
        username = username.strip()
        stats, error = github_service.get_comprehensive_user_stats(username)
        return render_template('index.html', user_stats=stats, error=error)

    return render_template('index.html')


@github_bp.route('/compare')
def compare_page():
    """Render comparison page"""
    return render_template('compare.html')


@github_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@github_bp.route('/docs')
def documentation():
    """API documentation page"""
    return render_template('docs.html') 