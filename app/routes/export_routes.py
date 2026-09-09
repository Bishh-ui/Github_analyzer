from flask import Blueprint, send_file, request, jsonify
from ..services.advanced_github_service import AdvancedGitHubService
import json
import csv
import io
from datetime import datetime

export_bp = Blueprint('export', __name__)
github_service = AdvancedGitHubService()


@export_bp.route('/json/<username>', methods=['GET'])
def export_json(username):
    """Export user statistics as JSON"""
    stats, error = github_service.get_comprehensive_user_stats(username)
    
    if error:
        return jsonify({'error': error}), 404
    
    # Create JSON file
    json_data = json.dumps(stats, indent=2, default=str)
    
    # Create in-memory file
    buffer = io.BytesIO()
    buffer.write(json_data.encode('utf-8'))
    buffer.seek(0)
    
    filename = f"github_analytics_{username}_{datetime.now().strftime('%Y%m%d')}.json"
    
    return send_file(
        buffer,
        mimetype='application/json',
        as_attachment=True,
        download_name=filename
    )


@export_bp.route('/csv/<username>', methods=['GET'])
def export_csv(username):
    """Export user statistics as CSV"""
    stats, error = github_service.get_comprehensive_user_stats(username)
    
    if error:
        return jsonify({'error': error}), 404
    
    # Create CSV file
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    # Write basic stats
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Username', stats['user']['login']])
    writer.writerow(['Name', stats['user']['name']])
    writer.writerow(['Followers', stats['stats']['followers']])
    writer.writerow(['Following', stats['stats']['following']])
    writer.writerow(['Public Repos', stats['stats']['public_repos']])
    writer.writerow(['Total Stars', stats['stats']['total_stars']])
    writer.writerow(['Total Forks', stats['stats']['total_forks']])
    writer.writerow(['Total Contributions', stats['stats']['contributions']])
    
    # Write language stats
    writer.writerow([])
    writer.writerow(['Language Statistics'])
    writer.writerow(['Language', 'Repos', 'Stars', 'Commits'])
    for lang, count in stats['languages']['by_repos'].items():
        writer.writerow([
            lang,
            count,
            stats['languages']['by_stars'].get(lang, 0),
            stats['languages']['by_commits'].get(lang, 0)
        ])
    
    # Write top repos
    writer.writerow([])
    writer.writerow(['Top Repositories'])
    writer.writerow(['Name', 'Stars', 'Forks', 'Language', 'URL'])
    for repo in stats['repos']['top_repos_by_stars'][:10]:
        writer.writerow([
            repo['name'],
            repo['stars'],
            repo['forks'],
            repo['language'],
            repo['url']
        ])
    
    # Prepare file for download
    buffer.seek(0)
    bytes_buffer = io.BytesIO()
    bytes_buffer.write(buffer.getvalue().encode('utf-8'))
    bytes_buffer.seek(0)
    
    filename = f"github_analytics_{username}_{datetime.now().strftime('%Y%m%d')}.csv"
    
    return send_file(
        bytes_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )


@export_bp.route('/markdown/<username>', methods=['GET'])
def export_markdown(username):
    """Export user statistics as Markdown"""
    stats, error = github_service.get_comprehensive_user_stats(username)
    
    if error:
        return jsonify({'error': error}), 404
    
    # Create Markdown content
    md_content = f"""# GitHub Analytics Report for {stats['user']['login']}

## User Profile

- **Name**: {stats['user']['name'] or 'N/A'}
- **Username**: {stats['user']['login']}
- **Bio**: {stats['user']['bio'] or 'N/A'}
- **Location**: {stats['user']['location'] or 'N/A'}
- **Company**: {stats['user']['company'] or 'N/A'}
- **Profile URL**: {stats['user']['profile_url']}
- **Account Age**: {stats['user']['account_age_years']} years

## Statistics Overview

| Metric | Value |
|--------|-------|
| Public Repositories | {stats['stats']['public_repos']} |
| Total Stars | {stats['stats']['total_stars']} |
| Total Forks | {stats['stats']['total_forks']} |
| Total Issues | {stats['stats']['total_issues']} |
| Followers | {stats['stats']['followers']} |
| Following | {stats['stats']['following']} |
| Total Contributions | {stats['stats']['contributions']} |
| Avg Stars per Repo | {stats['stats']['avg_stars_per_repo']} |

## Advanced Metrics

| Metric | Score |
|--------|-------|
| Impact Score | {stats['advanced_metrics']['impact_score']} |
| Consistency Score | {stats['advanced_metrics']['consistency_score']} |
| Diversity Score | {stats['advanced_metrics']['diversity_score']} |

## Language Distribution

### By Number of Repositories

| Language | Repos | Stars | Commits |
|----------|-------|-------|---------|
"""
    
    for lang, count in list(stats['languages']['by_repos'].items())[:10]:
        stars = stats['languages']['by_stars'].get(lang, 0)
        commits = stats['languages']['by_commits'].get(lang, 0)
        md_content += f"| {lang} | {count} | {stars} | {commits} |\n"
    
    md_content += f"""
## Top Repositories by Stars

| Repository | Stars | Forks | Language |
|------------|-------|-------|----------|
"""
    
    for repo in stats['repos']['top_repos_by_stars'][:10]:
        md_content += f"| [{repo['name']}]({repo['url']}) | {repo['stars']} | {repo['forks']} | {repo['language']} |\n"
    
    md_content += f"""
---
*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # Create in-memory file
    buffer = io.BytesIO()
    buffer.write(md_content.encode('utf-8'))
    buffer.seek(0)
    
    filename = f"github_analytics_{username}_{datetime.now().strftime('%Y%m%d')}.md"
    
    return send_file(
        buffer,
        mimetype='text/markdown',
        as_attachment=True,
        download_name=filename
    )


@export_bp.route('/pdf/<username>', methods=['GET'])
def export_pdf(username):
    """Export user statistics as PDF (requires additional library)"""
    # Note: PDF generation would require reportlab or similar
    # This is a placeholder implementation
    return jsonify({
        'message': 'PDF export requires reportlab library',
        'implementation': 'Install reportlab and implement PDF generation'
    }), 501
