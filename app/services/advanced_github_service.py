from github import Github
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import concurrent.futures
from functools import lru_cache
import re
import ssl
import certifi
from ..config.config import GITHUB_TOKEN, MAX_WORKERS
from ..models.user_analytics import db, UserAnalytics, RepositorySnapshot, LanguageStats, ContributionHistory


class AdvancedGitHubService:
    """Enhanced GitHub service with advanced analytics"""
    
    def __init__(self):
        # Disable SSL verification for Windows compatibility
        # This is safe for local development
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Initialize GitHub client without SSL verification
        # Handle case where token is not set or is placeholder
        token = GITHUB_TOKEN if GITHUB_TOKEN and GITHUB_TOKEN != 'your_github_token_here' else None
        
        if token:
            self.github = Github(token, per_page=100, verify=False)
        else:
            # Anonymous access (60 requests/hour)
            self.github = Github(verify=False)
        
        try:
            self.authenticated_user = self.github.get_user() if token else None
        except:
            self.authenticated_user = None
    
    def get_rate_limit(self):
        """Get detailed rate limit information"""
        rate_limit = self.github.get_rate_limit()
        return {
            'core': {
                'remaining': rate_limit.core.remaining,
                'limit': rate_limit.core.limit,
                'used': rate_limit.core.limit - rate_limit.core.remaining,
                'reset_time': rate_limit.core.reset.strftime('%H:%M:%S'),
                'reset_datetime': rate_limit.core.reset.isoformat(),
                'percentage_used': round((rate_limit.core.limit - rate_limit.core.remaining) / rate_limit.core.limit * 100, 2)
            },
            'search': {
                'remaining': rate_limit.search.remaining,
                'limit': rate_limit.search.limit,
                'used': rate_limit.search.limit - rate_limit.search.remaining,
                'reset_time': rate_limit.search.reset.strftime('%H:%M:%S'),
                'reset_datetime': rate_limit.search.reset.isoformat()
            },
            'graphql': {
                'remaining': rate_limit.graphql.remaining,
                'limit': rate_limit.graphql.limit,
                'used': rate_limit.graphql.limit - rate_limit.graphql.remaining,
                'reset_time': rate_limit.graphql.reset.strftime('%H:%M:%S'),
                'reset_datetime': rate_limit.graphql.reset.isoformat()
            }
        }
    
    def get_comprehensive_user_stats(self, username):
        """Get comprehensive user statistics with advanced metrics"""
        try:
            user = self.github.get_user(username)
            repos = list(user.get_repos())
            
            # Fetch repository stats in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                repo_stats = list(filter(None, executor.map(self._fetch_advanced_repo_stats, repos)))
            
            # Process all statistics
            stats = self._process_comprehensive_stats(repo_stats, user)
            
            # Add advanced metrics
            stats['advanced_metrics'] = self._calculate_advanced_metrics(user, repo_stats)
            stats['contribution_patterns'] = self._analyze_contribution_patterns(repo_stats)
            stats['code_quality_metrics'] = self._calculate_code_quality_metrics(repo_stats)
            stats['collaboration_metrics'] = self._calculate_collaboration_metrics(user, repos)
            stats['trending_analysis'] = self._analyze_trending_repos(repo_stats)
            stats['rate_limit'] = self.get_rate_limit()
            
            # Save to database if enabled
            self._save_analytics_snapshot(username, stats)
            
            return stats, None
        except Exception as e:
            return None, str(e)
    
    def _fetch_advanced_repo_stats(self, repo):
        """Fetch advanced repository statistics"""
        try:
            commit_dates = defaultdict(int)
            commit_authors = set()
            recent_activity = []
            
            # Get commits
            try:
                commits = list(repo.get_commits()[:100])  # Limit to recent 100 commits
                for commit in commits:
                    date = commit.commit.author.date
                    quarter = f"{date.year} Q{(date.month-1)//3 + 1}"
                    month = date.strftime("%Y-%m")
                    week = date.strftime("%Y-W%U")
                    
                    commit_dates[quarter] += 1
                    commit_dates[f"month_{month}"] = commit_dates.get(f"month_{month}", 0) + 1
                    commit_dates[f"week_{week}"] = commit_dates.get(f"week_{week}", 0) + 1
                    
                    if commit.author:
                        commit_authors.add(commit.author.login)
                    
                    # Track recent activity (last 30 days)
                    if (datetime.now(timezone.utc) - date).days <= 30:
                        recent_activity.append({
                            'date': date.isoformat(),
                            'message': commit.commit.message[:100]
                        })
            except:
                commits = []
            
            # Get languages
            try:
                languages = repo.get_languages()
            except:
                languages = {}
            
            # Get contributors count
            try:
                contributors_count = repo.get_contributors().totalCount
            except:
                contributors_count = 0
            
            # Calculate activity score
            now = datetime.now(timezone.utc)
            days_since_update = (now - repo.updated_at).days
            activity_score = self._calculate_activity_score(
                repo.stargazers_count, 
                repo.forks_count, 
                len(commits),
                days_since_update
            )
            
            return {
                'name': repo.name,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'watchers': repo.watchers_count,
                'language': repo.language or 'Unknown',
                'languages': languages,
                'created_at': repo.created_at,
                'updated_at': repo.updated_at,
                'description': repo.description,
                'size': repo.size,
                'commits': len(commits),
                'commit_history': dict(commit_dates),
                'unique_contributors': len(commit_authors),
                'contributors_count': contributors_count,
                'url': repo.html_url,
                'issues': repo.open_issues_count,
                'has_wiki': repo.has_wiki,
                'has_pages': repo.has_pages,
                'is_fork': repo.fork,
                'is_archived': repo.archived,
                'default_branch': repo.default_branch,
                'license': repo.license.name if repo.license else None,
                'topics': repo.get_topics(),
                'recent_activity': recent_activity,
                'activity_score': activity_score,
                'days_since_update': days_since_update
            }
        except Exception as e:
            print(f"Error fetching repo {repo.name}: {str(e)}")
            return None
    
    def _calculate_activity_score(self, stars, forks, commits, days_since_update):
        """Calculate a normalized activity score"""
        # Weight factors
        star_weight = 0.3
        fork_weight = 0.2
        commit_weight = 0.3
        recency_weight = 0.2
        
        # Normalize values (logarithmic scale for stars and forks)
        import math
        star_score = math.log10(stars + 1) * 10
        fork_score = math.log10(forks + 1) * 10
        commit_score = min(commits / 10, 100)  # Cap at 100
        recency_score = max(0, 100 - days_since_update)  # Recent is better
        
        total_score = (
            star_score * star_weight +
            fork_score * fork_weight +
            commit_score * commit_weight +
            recency_score * recency_weight
        )
        
        return round(total_score, 2)
    
    def _process_comprehensive_stats(self, repo_stats, user):
        """Process comprehensive statistics"""
        total_commit_history = defaultdict(int)
        languages_bytes = defaultdict(int)
        repos_by_language = defaultdict(int)
        stars_by_language = defaultdict(int)
        commits_by_language = defaultdict(int)
        
        for repo in repo_stats:
            # Aggregate commit history
            for period, count in repo.get('commit_history', {}).items():
                total_commit_history[period] += count
            
            # Aggregate language stats
            lang = repo['language'] or 'Unknown'
            repos_by_language[lang] += 1
            stars_by_language[lang] += repo['stars']
            commits_by_language[lang] += repo['commits']
            
            # Language bytes
            for language, bytes_count in repo.get('languages', {}).items():
                languages_bytes[language] += bytes_count
        
        # Calculate totals
        total_stars = sum(repo['stars'] for repo in repo_stats)
        total_forks = sum(repo['forks'] for repo in repo_stats)
        total_watchers = sum(repo.get('watchers', 0) for repo in repo_stats)
        total_issues = sum(repo.get('issues', 0) for repo in repo_stats)
        total_commits = sum(repo['commits'] for repo in repo_stats)
        
        # Get top repositories by different metrics
        top_repos_by_stars = sorted(repo_stats, key=lambda x: x['stars'], reverse=True)[:10]
        top_repos_by_forks = sorted(repo_stats, key=lambda x: x['forks'], reverse=True)[:10]
        top_repos_by_activity = sorted(repo_stats, key=lambda x: x['activity_score'], reverse=True)[:10]
        
        # Calculate account metrics
        now = datetime.now(timezone.utc)
        account_age = (now - user.created_at).days
        
        return {
            'user': {
                'name': user.name,
                'login': user.login,
                'bio': user.bio,
                'avatar_url': user.avatar_url,
                'location': user.location,
                'email': user.email,
                'company': user.company,
                'blog': user.blog,
                'twitter_username': user.twitter_username,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
                'account_age_days': account_age,
                'account_age_years': round(account_age / 365, 2),
                'hireable': user.hireable,
                'profile_url': user.html_url
            },
            'stats': {
                'public_repos': user.public_repos,
                'total_stars': total_stars,
                'total_forks': total_forks,
                'total_watchers': total_watchers,
                'total_issues': total_issues,
                'followers': user.followers,
                'following': user.following,
                'contributions': total_commits,
                'public_gists': user.public_gists,
                'avg_stars_per_repo': round(total_stars / len(repo_stats), 2) if repo_stats else 0,
                'avg_forks_per_repo': round(total_forks / len(repo_stats), 2) if repo_stats else 0,
                'commit_history': dict(sorted(total_commit_history.items(), reverse=True))
            },
            'languages': {
                'by_repos': dict(repos_by_language),
                'by_stars': dict(stars_by_language),
                'by_commits': dict(commits_by_language),
                'by_bytes': dict(languages_bytes),
                'total_languages': len(repos_by_language)
            },
            'repos': {
                'all_repos': repo_stats,
                'top_repos_by_stars': self._format_repos(top_repos_by_stars),
                'top_repos_by_forks': self._format_repos(top_repos_by_forks),
                'top_repos_by_activity': self._format_repos(top_repos_by_activity)
            }
        }
    
    def _format_repos(self, repos):
        """Format repository data for output"""
        return [{
            **repo,
            'created_at': repo['created_at'].isoformat(),
            'updated_at': repo['updated_at'].isoformat()
        } for repo in repos]
    
    def _calculate_advanced_metrics(self, user, repo_stats):
        """Calculate advanced developer metrics"""
        if not repo_stats:
            return {}
        
        total_stars = sum(repo['stars'] for repo in repo_stats)
        total_forks = sum(repo['forks'] for repo in repo_stats)
        total_commits = sum(repo['commits'] for repo in repo_stats)
        
        # Calculate impact score
        impact_score = self._calculate_impact_score(
            total_stars, total_forks, total_commits,
            user.followers, len(repo_stats)
        )
        
        # Calculate consistency score (based on commit distribution)
        consistency_score = self._calculate_consistency_score(repo_stats)
        
        # Calculate diversity score (based on languages used)
        diversity_score = self._calculate_diversity_score(repo_stats)
        
        return {
            'impact_score': impact_score,
            'consistency_score': consistency_score,
            'diversity_score': diversity_score,
            'repos_with_stars': len([r for r in repo_stats if r['stars'] > 0]),
            'repos_with_forks': len([r for r in repo_stats if r['forks'] > 0]),
            'archived_repos': len([r for r in repo_stats if r.get('is_archived', False)]),
            'forked_repos': len([r for r in repo_stats if r.get('is_fork', False)]),
            'original_repos': len([r for r in repo_stats if not r.get('is_fork', False)]),
            'repos_with_license': len([r for r in repo_stats if r.get('license')]),
            'repos_with_wiki': len([r for r in repo_stats if r.get('has_wiki', False)]),
            'repos_with_pages': len([r for r in repo_stats if r.get('has_pages', False)])
        }
    
    def _calculate_impact_score(self, stars, forks, commits, followers, repo_count):
        """Calculate developer impact score"""
        import math
        
        # Logarithmic scale to prevent domination by single factor
        star_impact = math.log10(stars + 1) * 20
        fork_impact = math.log10(forks + 1) * 15
        commit_impact = math.log10(commits + 1) * 10
        follower_impact = math.log10(followers + 1) * 25
        repo_impact = math.log10(repo_count + 1) * 10
        
        total_impact = star_impact + fork_impact + commit_impact + follower_impact + repo_impact
        
        return round(min(total_impact, 100), 2)  # Cap at 100
    
    def _calculate_consistency_score(self, repo_stats):
        """Calculate consistency based on commit patterns"""
        if not repo_stats:
            return 0
        
        # Get all monthly commits
        monthly_commits = defaultdict(int)
        for repo in repo_stats:
            for period, count in repo.get('commit_history', {}).items():
                if period.startswith('month_'):
                    monthly_commits[period] += count
        
        if not monthly_commits:
            return 0
        
        # Calculate coefficient of variation (lower is more consistent)
        commits = list(monthly_commits.values())
        if not commits:
            return 0
        
        mean = sum(commits) / len(commits)
        if mean == 0:
            return 0
        
        variance = sum((x - mean) ** 2 for x in commits) / len(commits)
        std_dev = variance ** 0.5
        cv = std_dev / mean
        
        # Convert to score (inverse of cv, normalized to 0-100)
        consistency = max(0, 100 - (cv * 100))
        
        return round(consistency, 2)
    
    def _calculate_diversity_score(self, repo_stats):
        """Calculate language diversity score"""
        languages = set()
        for repo in repo_stats:
            if repo.get('language'):
                languages.add(repo['language'])
            # Add additional languages from repo
            for lang in repo.get('languages', {}).keys():
                languages.add(lang)
        
        # More languages = higher diversity, with diminishing returns
        import math
        diversity = min(math.log10(len(languages) + 1) * 40, 100)
        
        return round(diversity, 2)
    
    def _analyze_contribution_patterns(self, repo_stats):
        """Analyze contribution patterns over time"""
        daily_commits = defaultdict(int)
        weekly_commits = defaultdict(int)
        monthly_commits = defaultdict(int)
        quarterly_commits = defaultdict(int)
        
        for repo in repo_stats:
            for period, count in repo.get('commit_history', {}).items():
                if period.startswith('week_'):
                    weekly_commits[period.replace('week_', '')] += count
                elif period.startswith('month_'):
                    monthly_commits[period.replace('month_', '')] += count
                elif 'Q' in period:
                    quarterly_commits[period] += count
        
        # Get most active periods
        top_weeks = dict(sorted(weekly_commits.items(), key=lambda x: x[1], reverse=True)[:10])
        top_months = dict(sorted(monthly_commits.items(), key=lambda x: x[1], reverse=True)[:12])
        
        return {
            'weekly_commits': dict(weekly_commits),
            'monthly_commits': dict(monthly_commits),
            'quarterly_commits': dict(quarterly_commits),
            'most_active_weeks': top_weeks,
            'most_active_months': top_months,
            'total_active_weeks': len(weekly_commits),
            'total_active_months': len(monthly_commits)
        }
    
    def _calculate_code_quality_metrics(self, repo_stats):
        """Calculate code quality indicators"""
        repos_with_readme = 0
        repos_with_tests = 0
        repos_with_ci = 0
        total_documentation_score = 0
        
        for repo in repo_stats:
            # Check for documentation indicators
            if repo.get('description'):
                total_documentation_score += 1
            if repo.get('has_wiki'):
                total_documentation_score += 0.5
            
            # Estimate based on common patterns
            # (In a real implementation, you'd check actual files)
            if repo.get('size', 0) > 0:
                repos_with_readme += 1  # Assume repos have README
        
        return {
            'avg_documentation_score': round(total_documentation_score / len(repo_stats), 2) if repo_stats else 0,
            'repos_with_description': len([r for r in repo_stats if r.get('description')]),
            'repos_with_topics': len([r for r in repo_stats if r.get('topics')]),
            'avg_topics_per_repo': round(sum(len(r.get('topics', [])) for r in repo_stats) / len(repo_stats), 2) if repo_stats else 0
        }
    
    def _calculate_collaboration_metrics(self, user, repos):
        """Calculate collaboration and community metrics"""
        total_contributors = 0
        
        for repo in repos[:20]:  # Limit to prevent rate limiting
            try:
                contributors_count = repo.get('unique_contributors', 0)
                total_contributors += contributors_count
            except:
                pass
        
        return {
            'followers': user.followers,
            'following': user.following,
            'follower_following_ratio': round(user.followers / max(user.following, 1), 2),
            'avg_contributors_per_repo': round(total_contributors / min(len(repos), 20), 2) if repos else 0,
            'social_reach_score': min(user.followers * 0.1, 100)
        }
    
    def _analyze_trending_repos(self, repo_stats):
        """Analyze trending repositories"""
        # Get repos updated in last 30 days
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        recently_active = [
            repo for repo in repo_stats 
            if repo['updated_at'] > thirty_days_ago
        ]
        
        # Get repos with recent activity
        hot_repos = sorted(
            recently_active,
            key=lambda x: x['activity_score'],
            reverse=True
        )[:5]
        
        return {
            'recently_active_count': len(recently_active),
            'hot_repos': self._format_repos(hot_repos),
            'repos_updated_last_week': len([
                r for r in repo_stats 
                if (datetime.now(timezone.utc) - r['updated_at']).days <= 7
            ]),
            'repos_updated_last_month': len(recently_active)
        }
    
    def _save_analytics_snapshot(self, username, stats):
        """Save analytics snapshot to database"""
        try:
            user_analytics = UserAnalytics(
                username=username,
                name=stats['user']['name'],
                avatar_url=stats['user']['avatar_url'],
                public_repos=stats['stats']['public_repos'],
                total_stars=stats['stats']['total_stars'],
                total_forks=stats['stats']['total_forks'],
                total_issues=stats['stats']['total_issues'],
                total_prs=0,  # Would need additional API calls
                followers=stats['stats']['followers'],
                following=stats['stats']['following'],
                contributions=stats['stats']['contributions'],
                account_created_at=datetime.fromisoformat(stats['user']['created_at'].replace('Z', '+00:00'))
            )
            
            db.session.add(user_analytics)
            db.session.commit()
            
            return user_analytics.id
        except Exception as e:
            print(f"Error saving analytics snapshot: {str(e)}")
            db.session.rollback()
            return None
    
    def get_user_history(self, username, days=90):
        """Get historical analytics for a user"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        history = UserAnalytics.query.filter(
            UserAnalytics.username == username,
            UserAnalytics.snapshot_date >= cutoff_date
        ).order_by(UserAnalytics.snapshot_date.asc()).all()
        
        return [record.to_dict() for record in history]
    
    def compare_users(self, usernames):
        """Compare multiple users"""
        comparisons = []
        
        for username in usernames:
            stats, error = self.get_comprehensive_user_stats(username)
            if stats:
                comparisons.append({
                    'username': username,
                    'stats': stats
                })
        
        return comparisons
