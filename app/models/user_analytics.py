from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserAnalytics(db.Model):
    """Store historical user analytics data"""
    __tablename__ = 'user_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, index=True)
    name = db.Column(db.String(200))
    avatar_url = db.Column(db.String(500))
    
    # Stats
    public_repos = db.Column(db.Integer, default=0)
    total_stars = db.Column(db.Integer, default=0)
    total_forks = db.Column(db.Integer, default=0)
    total_issues = db.Column(db.Integer, default=0)
    total_prs = db.Column(db.Integer, default=0)
    followers = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)
    contributions = db.Column(db.Integer, default=0)
    
    # Timestamps
    account_created_at = db.Column(db.DateTime)
    snapshot_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    repositories = db.relationship('RepositorySnapshot', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    language_stats = db.relationship('LanguageStats', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    contributions_history = db.relationship('ContributionHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<UserAnalytics {self.username} - {self.snapshot_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'avatar_url': self.avatar_url,
            'public_repos': self.public_repos,
            'total_stars': self.total_stars,
            'total_forks': self.total_forks,
            'total_issues': self.total_issues,
            'total_prs': self.total_prs,
            'followers': self.followers,
            'following': self.following,
            'contributions': self.contributions,
            'account_created_at': self.account_created_at.isoformat() if self.account_created_at else None,
            'snapshot_date': self.snapshot_date.isoformat()
        }


class RepositorySnapshot(db.Model):
    """Store repository snapshots"""
    __tablename__ = 'repository_snapshots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_analytics_id = db.Column(db.Integer, db.ForeignKey('user_analytics.id'), nullable=False)
    
    repo_name = db.Column(db.String(200), nullable=False)
    repo_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    language = db.Column(db.String(100))
    
    stars = db.Column(db.Integer, default=0)
    forks = db.Column(db.Integer, default=0)
    watchers = db.Column(db.Integer, default=0)
    open_issues = db.Column(db.Integer, default=0)
    size = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    snapshot_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RepositorySnapshot {self.repo_name}>'
    
    def to_dict(self):
        return {
            'repo_name': self.repo_name,
            'repo_url': self.repo_url,
            'description': self.description,
            'language': self.language,
            'stars': self.stars,
            'forks': self.forks,
            'watchers': self.watchers,
            'open_issues': self.open_issues,
            'size': self.size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LanguageStats(db.Model):
    """Store language usage statistics"""
    __tablename__ = 'language_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_analytics_id = db.Column(db.Integer, db.ForeignKey('user_analytics.id'), nullable=False)
    
    language = db.Column(db.String(100), nullable=False)
    repo_count = db.Column(db.Integer, default=0)
    total_stars = db.Column(db.Integer, default=0)
    total_commits = db.Column(db.Integer, default=0)
    bytes_of_code = db.Column(db.BigInteger, default=0)
    
    snapshot_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LanguageStats {self.language}>'
    
    def to_dict(self):
        return {
            'language': self.language,
            'repo_count': self.repo_count,
            'total_stars': self.total_stars,
            'total_commits': self.total_commits,
            'bytes_of_code': self.bytes_of_code
        }


class ContributionHistory(db.Model):
    """Store detailed contribution history"""
    __tablename__ = 'contribution_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_analytics_id = db.Column(db.Integer, db.ForeignKey('user_analytics.id'), nullable=False)
    
    period = db.Column(db.String(50), nullable=False)  # e.g., "2024-Q1", "2024-01"
    period_type = db.Column(db.String(20), nullable=False)  # quarter, month, week, day
    
    commits = db.Column(db.Integer, default=0)
    pull_requests = db.Column(db.Integer, default=0)
    issues = db.Column(db.Integer, default=0)
    code_reviews = db.Column(db.Integer, default=0)
    
    snapshot_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContributionHistory {self.period}>'
    
    def to_dict(self):
        return {
            'period': self.period,
            'period_type': self.period_type,
            'commits': self.commits,
            'pull_requests': self.pull_requests,
            'issues': self.issues,
            'code_reviews': self.code_reviews
        }
