"""
Authentication and Authorization Service
User management, authentication, and access control

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_
import bcrypt
import jwt
import secrets
import logging
from enum import Enum

from src.services.base_service import BaseService, ValidationError, ServiceException, UnauthorizedError
from src.models import User, Project
from src.config import get_config

logger = logging.getLogger(__name__)
config = get_config()


class UserRole(Enum):
    """User roles with permissions."""
    ADMIN = "admin"  # Full access
    ASSESSOR = "assessor"  # Can perform assessments
    CLIENT = "client"  # Can view own projects
    REGULATOR = "regulator"  # Can view compliance data
    VIEWER = "viewer"  # Read-only access


class Permission(Enum):
    """System permissions."""
    # Project permissions
    PROJECT_CREATE = "project.create"
    PROJECT_READ = "project.read"
    PROJECT_UPDATE = "project.update"
    PROJECT_DELETE = "project.delete"
    
    # Assessment permissions
    ASSESSMENT_CREATE = "assessment.create"
    ASSESSMENT_READ = "assessment.read"
    ASSESSMENT_UPDATE = "assessment.update"
    
    # Compliance permissions
    COMPLIANCE_CREATE = "compliance.create"
    COMPLIANCE_READ = "compliance.read"
    COMPLIANCE_APPROVE = "compliance.approve"
    
    # Monitoring permissions
    MONITORING_CREATE = "monitoring.create"
    MONITORING_READ = "monitoring.read"
    
    # Report permissions
    REPORT_GENERATE = "report.generate"
    REPORT_EXPORT = "report.export"
    
    # Admin permissions
    USER_MANAGE = "user.manage"
    SYSTEM_CONFIG = "system.config"


# Role-Permission mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [p for p in Permission],  # All permissions
    UserRole.ASSESSOR: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.ASSESSMENT_CREATE,
        Permission.ASSESSMENT_READ,
        Permission.ASSESSMENT_UPDATE,
        Permission.COMPLIANCE_CREATE,
        Permission.COMPLIANCE_READ,
        Permission.MONITORING_CREATE,
        Permission.MONITORING_READ,
        Permission.REPORT_GENERATE,
        Permission.REPORT_EXPORT
    ],
    UserRole.CLIENT: [
        Permission.PROJECT_READ,
        Permission.ASSESSMENT_READ,
        Permission.COMPLIANCE_READ,
        Permission.MONITORING_READ,
        Permission.REPORT_GENERATE
    ],
    UserRole.REGULATOR: [
        Permission.PROJECT_READ,
        Permission.ASSESSMENT_READ,
        Permission.COMPLIANCE_READ,
        Permission.COMPLIANCE_APPROVE,
        Permission.MONITORING_READ,
        Permission.REPORT_GENERATE
    ],
    UserRole.VIEWER: [
        Permission.PROJECT_READ,
        Permission.ASSESSMENT_READ,
        Permission.MONITORING_READ
    ]
}


class AuthService(BaseService[User]):
    """
    Authentication and authorization service.
    Handles user management, login, and access control.
    """
    
    def __init__(self, session: Session):
        super().__init__(User, session)
        self.token_expiry = timedelta(minutes=config.security.access_token_expire_minutes)
    
    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate user creation data."""
        required_fields = ['username', 'email', 'password']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(f"{field} is required", field)
        
        # Validate username
        if len(data['username']) < 3:
            raise ValidationError("Username must be at least 3 characters", 'username')
        
        if not data['username'].replace('_', '').replace('-', '').isalnum():
            raise ValidationError("Username can only contain letters, numbers, underscores, and hyphens", 'username')
        
        # Check username uniqueness
        if self.exists({'username': data['username']}):
            raise ValidationError("Username already exists", 'username')
        
        # Validate email
        if '@' not in data['email'] or '.' not in data['email']:
            raise ValidationError("Invalid email format", 'email')
        
        # Check email uniqueness
        if self.exists({'email': data['email']}):
            raise ValidationError("Email already registered", 'email')
        
        # Validate password
        self._validate_password(data['password'])
        
        # Validate role
        if 'role' in data:
            valid_roles = [role.value for role in UserRole]
            if data['role'] not in valid_roles:
                raise ValidationError(f"Invalid role. Must be one of: {valid_roles}", 'role')
    
    def _validate_update_data(self, data: Dict[str, Any], entity: User) -> None:
        """Validate user update data."""
        # Can't change username
        if 'username' in data and data['username'] != entity.username:
            raise ValidationError("Username cannot be changed", 'username')
        
        # Validate email if changing
        if 'email' in data and data['email'] != entity.email:
            if '@' not in data['email'] or '.' not in data['email']:
                raise ValidationError("Invalid email format", 'email')
            
            # Check uniqueness
            existing = self.session.query(User).filter(
                User.email == data['email'],
                User.id != entity.id
            ).first()
            
            if existing:
                raise ValidationError("Email already registered", 'email')
        
        # Validate password if changing
        if 'password' in data:
            self._validate_password(data['password'])
    
    def _validate_password(self, password: str) -> None:
        """Validate password strength."""
        if len(password) < config.security.password_min_length:
            raise ValidationError(
                f"Password must be at least {config.security.password_min_length} characters",
                'password'
            )
        
        if config.security.password_require_special:
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(not c.isalnum() for c in password)
            
            if not (has_upper and has_lower and has_digit and has_special):
                raise ValidationError(
                    "Password must contain uppercase, lowercase, digit, and special character",
                    'password'
                )
    
    def register_user(self, 
                     username: str,
                     email: str,
                     password: str,
                     full_name: str = None,
                     organization: str = None,
                     role: str = UserRole.CLIENT.value) -> User:
        """
        Register new user.
        
        Args:
            username: Unique username
            email: User email
            password: Plain text password
            full_name: Full name
            organization: Organization name
            role: User role
            
        Returns:
            Created user
        """
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'full_name': full_name,
            'organization': organization,
            'role': role,
            'active': True
        }
        
        # Validate before creating
        self._validate_create_data({**user_data, 'password': password})
        
        # Create user (without password in data)
        user_data.pop('password', None)
        user = self.model_class(**user_data)
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        logger.info(f"Registered new user: {username} with role {role}")
        return user
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password.
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            User if authenticated, None otherwise
        """
        # Find user by username or email
        user = self.session.query(User).filter(
            or_(
                User.username == username,
                User.email == username
            )
        ).first()
        
        if not user:
            logger.warning(f"Authentication failed: User not found - {username}")
            return None
        
        if not user.active:
            logger.warning(f"Authentication failed: User inactive - {username}")
            return None
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            logger.warning(f"Authentication failed: Invalid password - {username}")
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.session.commit()
        
        logger.info(f"User authenticated: {username}")
        return user
    
    def generate_token(self, user: User) -> str:
        """
        Generate JWT token for user.
        
        Args:
            user: User object
            
        Returns:
            JWT token string
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + self.token_expiry,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            config.security.secret_key,
            algorithm=config.security.algorithm
        )
        
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                config.security.secret_key,
                algorithms=[config.security.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def get_current_user(self, token: str) -> Optional[User]:
        """
        Get current user from token.
        
        Args:
            token: JWT token
            
        Returns:
            User if valid token, None otherwise
        """
        payload = self.verify_token(token)
        if not payload:
            return None
        
        user = self.get_by_id(payload['user_id'], raise_on_not_found=False)
        
        if not user or not user.active:
            return None
        
        return user
    
    def check_permission(self, user: User, permission: Permission) -> bool:
        """
        Check if user has specific permission.
        
        Args:
            user: User object
            permission: Permission to check
            
        Returns:
            True if user has permission
        """
        try:
            role = UserRole(user.role)
            role_permissions = ROLE_PERMISSIONS.get(role, [])
            return permission in role_permissions
        except ValueError:
            logger.error(f"Invalid user role: {user.role}")
            return False
    
    def check_project_access(self, user: User, project_id: int) -> bool:
        """
        Check if user has access to specific project.
        
        Args:
            user: User object
            project_id: Project ID
            
        Returns:
            True if user has access
        """
        # Admins and regulators have access to all projects
        if user.role in [UserRole.ADMIN.value, UserRole.REGULATOR.value]:
            return True
        
        # Assessors have access to all projects they can work on
        if user.role == UserRole.ASSESSOR.value:
            return True
        
        # Clients only have access to their own projects
        if user.role == UserRole.CLIENT.value:
            project = self.session.query(Project).filter_by(id=project_id).first()
            if project and (
                project.client_name == user.organization or
                project.client_contact == user.email
            ):
                return True
        
        return False
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if successful
        """
        user = self.get_by_id(user_id)
        
        # Verify old password
        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise UnauthorizedError("Invalid current password")
        
        # Validate new password
        self._validate_password(new_password)
        
        # Update password
        user.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.session.commit()
        
        logger.info(f"Password changed for user: {user.username}")
        return True
    
    def reset_password(self, email: str) -> str:
        """
        Generate password reset token.
        
        Args:
            email: User email
            
        Returns:
            Reset token
        """
        user = self.session.query(User).filter_by(email=email).first()
        
        if not user:
            raise ServiceException("User not found")
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # In production, store token with expiry
        # For now, just return it
        logger.info(f"Password reset requested for: {email}")
        
        return reset_token
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful
        """
        user = self.get_by_id(user_id)
        user.active = False
        self.session.commit()
        
        logger.info(f"User deactivated: {user.username}")
        return True
    
    def get_user_permissions(self, user: User) -> List[str]:
        """
        Get list of user permissions.
        
        Args:
            user: User object
            
        Returns:
            List of permission strings
        """
        try:
            role = UserRole(user.role)
            permissions = ROLE_PERMISSIONS.get(role, [])
            return [p.value for p in permissions]
        except ValueError:
            return []
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """
        Get user activity statistics.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with user statistics
        """
        user = self.get_by_id(user_id)
        
        # Get project count if client
        project_count = 0
        if user.role == UserRole.CLIENT.value:
            project_count = self.session.query(Project).filter(
                or_(
                    Project.client_name == user.organization,
                    Project.client_contact == user.email
                )
            ).count()
        
        stats = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'active': user.active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'project_count': project_count,
            'permissions': self.get_user_permissions(user)
        }
        
        return stats