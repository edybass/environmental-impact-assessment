"""
Public Consultation Portal
Web-based interface for stakeholder participation in EIA process

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import hashlib
import secrets
from pathlib import Path
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class PortalSection(Enum):
    """Sections of the consultation portal."""
    HOME = "home"
    PROJECT_INFO = "project_info"
    DOCUMENTS = "documents"
    COMMENT_FORM = "comment_form"
    EVENTS = "events"
    FAQ = "faq"
    CONTACT = "contact"
    GRIEVANCE = "grievance"
    UPDATES = "updates"


@dataclass
class PortalUser:
    """Portal user registration."""
    user_id: str
    email: str
    name: str
    organization: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: str = "en"
    location: Optional[str] = None
    stakeholder_type: str = "public"
    registration_date: datetime = field(default_factory=datetime.now)
    verified: bool = False
    notification_preferences: Dict[str, bool] = field(default_factory=lambda: {
        'email': True,
        'sms': False,
        'project_updates': True,
        'event_reminders': True,
        'comment_responses': True
    })


@dataclass
class Document:
    """Consultation document."""
    document_id: str
    title: str
    description: str
    document_type: str  # eia_summary, fact_sheet, presentation, report
    file_path: str
    file_size: int  # bytes
    language: str
    upload_date: datetime
    download_count: int = 0
    categories: List[str] = field(default_factory=list)
    access_level: str = "public"  # public, registered, restricted


@dataclass
class OnlineComment:
    """Online comment submission."""
    submission_id: str
    user_id: Optional[str]
    timestamp: datetime
    name: str
    email: str
    phone: Optional[str]
    organization: Optional[str]
    comment_category: str
    comment_subject: str
    comment_text: str
    location_reference: Optional[str]
    attachments: List[str] = field(default_factory=list)
    language: str = "en"
    ip_address: str = ""
    user_agent: str = ""
    consent_given: bool = False
    newsletter_signup: bool = False


@dataclass
class Event:
    """Consultation event."""
    event_id: str
    event_type: str  # public_meeting, workshop, site_visit, webinar
    title: str
    description: str
    date: datetime
    duration_hours: float
    location: str
    venue_details: Dict[str, str]
    capacity: Optional[int]
    registration_required: bool
    registration_link: Optional[str]
    languages: List[str]
    facilitators: List[str]
    materials_available: List[str]
    accessibility_info: str
    contact_info: Dict[str, str]
    registrations: List[str] = field(default_factory=list)
    status: str = "upcoming"  # upcoming, ongoing, completed, cancelled


@dataclass
class Notification:
    """System notification."""
    notification_id: str
    user_id: str
    notification_type: str  # comment_response, event_reminder, update, announcement
    subject: str
    message: str
    created_date: datetime
    send_date: Optional[datetime]
    sent: bool = False
    read: bool = False
    channel: str = "email"  # email, sms, in_app
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConsultationPortal:
    """Public consultation portal system."""
    
    def __init__(self, project_id: int, base_url: str = "https://eia-consultation.example.com"):
        self.project_id = project_id
        self.base_url = base_url
        
        # Portal configuration
        self.config = {
            'languages': ['en', 'ar'],
            'comment_categories': [
                'Air Quality',
                'Water Resources', 
                'Noise and Vibration',
                'Traffic and Transportation',
                'Visual Impact',
                'Flora and Fauna',
                'Social Impact',
                'Economic Impact',
                'Health and Safety',
                'Cultural Heritage',
                'Other'
            ],
            'file_upload_limit': 10 * 1024 * 1024,  # 10MB
            'allowed_file_types': ['pdf', 'doc', 'docx', 'jpg', 'png', 'xlsx'],
            'session_timeout': 3600,  # 1 hour
            'max_comment_length': 5000,
            'require_registration': False,
            'enable_notifications': True,
            'moderation_enabled': True
        }
        
        # Portal content templates
        self.content_templates = {
            'welcome_message': {
                'en': """Welcome to the Environmental Impact Assessment Public Consultation Portal. 
                       Your participation helps ensure that environmental and social considerations 
                       are properly addressed in project planning.""",
                'ar': """مرحباً بكم في بوابة الاستشارة العامة لتقييم الأثر البيئي.
                       مشاركتكم تساعد في ضمان معالجة الاعتبارات البيئية والاجتماعية
                       بشكل صحيح في تخطيط المشروع."""
            },
            'comment_guidelines': {
                'en': """Please provide specific, constructive feedback related to environmental 
                       and social impacts. All comments will be reviewed and responded to.""",
                'ar': """يرجى تقديم ملاحظات محددة وبناءة تتعلق بالآثار البيئية
                       والاجتماعية. سيتم مراجعة جميع التعليقات والرد عليها."""
            }
        }
        
        # Initialize storage
        self.users: Dict[str, PortalUser] = {}
        self.documents: Dict[str, Document] = {}
        self.comments: List[OnlineComment] = []
        self.events: Dict[str, Event] = {}
        self.notifications: List[Notification] = []
    
    def create_portal_structure(self) -> Dict[str, Any]:
        """
        Create portal page structure and navigation.
        
        Returns:
            Portal structure definition
        """
        structure = {
            'navigation': {
                'primary': [
                    {'id': 'home', 'label': {'en': 'Home', 'ar': 'الرئيسية'}, 'url': '/'},
                    {'id': 'project', 'label': {'en': 'Project Information', 'ar': 'معلومات المشروع'}, 'url': '/project'},
                    {'id': 'documents', 'label': {'en': 'Documents', 'ar': 'المستندات'}, 'url': '/documents'},
                    {'id': 'participate', 'label': {'en': 'Participate', 'ar': 'المشاركة'}, 'url': '/participate'},
                    {'id': 'events', 'label': {'en': 'Events', 'ar': 'الفعاليات'}, 'url': '/events'},
                    {'id': 'contact', 'label': {'en': 'Contact', 'ar': 'اتصل بنا'}, 'url': '/contact'}
                ],
                'footer': [
                    {'id': 'privacy', 'label': {'en': 'Privacy Policy', 'ar': 'سياسة الخصوصية'}, 'url': '/privacy'},
                    {'id': 'terms', 'label': {'en': 'Terms of Use', 'ar': 'شروط الاستخدام'}, 'url': '/terms'},
                    {'id': 'accessibility', 'label': {'en': 'Accessibility', 'ar': 'إمكانية الوصول'}, 'url': '/accessibility'}
                ]
            },
            'pages': {
                'home': {
                    'sections': [
                        {'type': 'hero', 'content': 'welcome_message'},
                        {'type': 'project_summary', 'content': 'dynamic'},
                        {'type': 'consultation_timeline', 'content': 'dynamic'},
                        {'type': 'how_to_participate', 'content': 'static'},
                        {'type': 'latest_updates', 'content': 'dynamic', 'limit': 5}
                    ]
                },
                'project': {
                    'sections': [
                        {'type': 'project_overview', 'content': 'dynamic'},
                        {'type': 'location_map', 'content': 'interactive'},
                        {'type': 'key_features', 'content': 'static'},
                        {'type': 'timeline', 'content': 'dynamic'},
                        {'type': 'benefits', 'content': 'static'}
                    ]
                },
                'documents': {
                    'sections': [
                        {'type': 'document_categories', 'content': 'dynamic'},
                        {'type': 'document_search', 'content': 'interactive'},
                        {'type': 'document_list', 'content': 'dynamic'},
                        {'type': 'download_help', 'content': 'static'}
                    ]
                },
                'participate': {
                    'sections': [
                        {'type': 'participation_options', 'content': 'static'},
                        {'type': 'comment_form', 'content': 'interactive'},
                        {'type': 'comment_guidelines', 'content': 'static'},
                        {'type': 'previous_comments', 'content': 'dynamic', 'moderated': True}
                    ]
                },
                'events': {
                    'sections': [
                        {'type': 'upcoming_events', 'content': 'dynamic'},
                        {'type': 'event_calendar', 'content': 'interactive'},
                        {'type': 'past_events', 'content': 'dynamic'},
                        {'type': 'event_materials', 'content': 'dynamic'}
                    ]
                },
                'contact': {
                    'sections': [
                        {'type': 'contact_info', 'content': 'static'},
                        {'type': 'office_locations', 'content': 'static'},
                        {'type': 'contact_form', 'content': 'interactive'},
                        {'type': 'response_time', 'content': 'static'}
                    ]
                }
            },
            'features': {
                'multilingual': True,
                'responsive': True,
                'accessible': True,
                'search': True,
                'user_accounts': True,
                'notifications': True,
                'social_sharing': True,
                'analytics': True,
                'feedback': True
            }
        }
        
        return structure
    
    def register_user(
        self,
        email: str,
        name: str,
        organization: Optional[str] = None,
        phone: Optional[str] = None,
        preferred_language: str = "en"
    ) -> PortalUser:
        """
        Register a new portal user.
        
        Args:
            email: User email
            name: User name
            organization: Organization name
            phone: Phone number
            preferred_language: Language preference
            
        Returns:
            Registered user
        """
        # Generate user ID
        user_id = f"USR_{hashlib.md5(email.encode()).hexdigest()[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create user
        user = PortalUser(
            user_id=user_id,
            email=email,
            name=name,
            organization=organization,
            phone=phone,
            preferred_language=preferred_language
        )
        
        # Store user
        self.users[user_id] = user
        
        # Send verification email
        if self.config['enable_notifications']:
            self._send_verification_email(user)
        
        return user
    
    def upload_document(
        self,
        title: str,
        description: str,
        document_type: str,
        file_path: str,
        file_size: int,
        language: str = "en",
        categories: Optional[List[str]] = None
    ) -> Document:
        """
        Upload a consultation document.
        
        Args:
            title: Document title
            description: Document description
            document_type: Type of document
            file_path: Path to file
            file_size: File size in bytes
            language: Document language
            categories: Document categories
            
        Returns:
            Document record
        """
        # Generate document ID
        document_id = f"DOC_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(4)}"
        
        # Create document record
        document = Document(
            document_id=document_id,
            title=title,
            description=description,
            document_type=document_type,
            file_path=file_path,
            file_size=file_size,
            language=language,
            upload_date=datetime.now(),
            categories=categories or []
        )
        
        # Store document
        self.documents[document_id] = document
        
        # Notify registered users
        if self.config['enable_notifications']:
            self._notify_document_upload(document)
        
        return document
    
    def submit_comment(
        self,
        name: str,
        email: str,
        comment_category: str,
        comment_subject: str,
        comment_text: str,
        user_id: Optional[str] = None,
        phone: Optional[str] = None,
        organization: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        consent_given: bool = True
    ) -> OnlineComment:
        """
        Submit public comment.
        
        Args:
            name: Commenter name
            email: Commenter email
            comment_category: Comment category
            comment_subject: Comment subject
            comment_text: Comment text
            user_id: Registered user ID
            phone: Phone number
            organization: Organization
            attachments: Attached files
            consent_given: Privacy consent
            
        Returns:
            Comment submission
        """
        # Validate comment
        if len(comment_text) > self.config['max_comment_length']:
            raise ValueError(f"Comment exceeds maximum length of {self.config['max_comment_length']} characters")
        
        if comment_category not in self.config['comment_categories']:
            raise ValueError(f"Invalid comment category: {comment_category}")
        
        # Generate submission ID
        submission_id = f"SUBM_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(4)}"
        
        # Create comment
        comment = OnlineComment(
            submission_id=submission_id,
            user_id=user_id,
            timestamp=datetime.now(),
            name=name,
            email=email,
            phone=phone,
            organization=organization,
            comment_category=comment_category,
            comment_subject=comment_subject,
            comment_text=comment_text,
            attachments=attachments or [],
            consent_given=consent_given
        )
        
        # Store comment
        self.comments.append(comment)
        
        # Send confirmation
        if self.config['enable_notifications']:
            self._send_comment_confirmation(comment)
        
        # Trigger moderation if enabled
        if self.config['moderation_enabled']:
            self._moderate_comment(comment)
        
        return comment
    
    def create_event(
        self,
        event_type: str,
        title: str,
        description: str,
        date: datetime,
        duration_hours: float,
        location: str,
        venue_details: Dict[str, str],
        capacity: Optional[int] = None,
        registration_required: bool = False,
        languages: Optional[List[str]] = None
    ) -> Event:
        """
        Create consultation event.
        
        Args:
            event_type: Type of event
            title: Event title
            description: Event description
            date: Event date and time
            duration_hours: Duration in hours
            location: Event location
            venue_details: Venue information
            capacity: Maximum capacity
            registration_required: Registration required flag
            languages: Event languages
            
        Returns:
            Event record
        """
        # Generate event ID
        event_id = f"EVT_{datetime.now().strftime('%Y%m%d')}_{secrets.token_hex(4)}"
        
        # Create event
        event = Event(
            event_id=event_id,
            event_type=event_type,
            title=title,
            description=description,
            date=date,
            duration_hours=duration_hours,
            location=location,
            venue_details=venue_details,
            capacity=capacity,
            registration_required=registration_required,
            registration_link=f"{self.base_url}/events/{event_id}/register" if registration_required else None,
            languages=languages or ['en', 'ar'],
            facilitators=[],
            materials_available=[],
            accessibility_info="Venue is wheelchair accessible. Sign language interpretation available upon request.",
            contact_info={}
        )
        
        # Store event
        self.events[event_id] = event
        
        # Notify users
        if self.config['enable_notifications']:
            self._notify_new_event(event)
        
        return event
    
    def register_for_event(
        self,
        event_id: str,
        user_id: str,
        special_requirements: Optional[str] = None
    ) -> bool:
        """
        Register user for event.
        
        Args:
            event_id: Event ID
            user_id: User ID
            special_requirements: Any special requirements
            
        Returns:
            Success status
        """
        if event_id not in self.events:
            raise ValueError(f"Event {event_id} not found")
        
        event = self.events[event_id]
        
        # Check capacity
        if event.capacity and len(event.registrations) >= event.capacity:
            return False
        
        # Check if already registered
        if user_id in event.registrations:
            return True
        
        # Register user
        event.registrations.append(user_id)
        
        # Send confirmation
        if self.config['enable_notifications']:
            self._send_event_confirmation(event_id, user_id)
        
        # Store special requirements
        if special_requirements:
            if 'special_requirements' not in event.metadata:
                event.metadata['special_requirements'] = {}
            event.metadata['special_requirements'][user_id] = special_requirements
        
        return True
    
    def generate_portal_content(
        self,
        section: PortalSection,
        language: str = "en",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate dynamic portal content.
        
        Args:
            section: Portal section
            language: Content language
            user_id: Current user ID
            
        Returns:
            Section content
        """
        content = {
            'section': section.value,
            'language': language,
            'generated_at': datetime.now().isoformat()
        }
        
        if section == PortalSection.HOME:
            content['data'] = {
                'welcome_message': self.content_templates['welcome_message'][language],
                'active_consultation': self._get_active_consultation_info(),
                'latest_updates': self._get_latest_updates(5),
                'upcoming_events': self._get_upcoming_events(3),
                'quick_links': self._get_quick_links(language)
            }
        
        elif section == PortalSection.DOCUMENTS:
            content['data'] = {
                'categories': self._get_document_categories(),
                'documents': self._get_documents_by_language(language),
                'featured_documents': self._get_featured_documents(),
                'download_stats': self._get_download_statistics()
            }
        
        elif section == PortalSection.COMMENT_FORM:
            content['data'] = {
                'form_fields': self._get_comment_form_fields(language),
                'categories': self.config['comment_categories'],
                'guidelines': self.content_templates['comment_guidelines'][language],
                'user_info': self._get_user_info(user_id) if user_id else None
            }
        
        elif section == PortalSection.EVENTS:
            content['data'] = {
                'upcoming': self._get_upcoming_events(),
                'past': self._get_past_events(),
                'user_registrations': self._get_user_events(user_id) if user_id else []
            }
        
        elif section == PortalSection.FAQ:
            content['data'] = {
                'faqs': self._get_faqs(language),
                'categories': self._get_faq_categories(),
                'contact_for_more': self._get_contact_info(language)
            }
        
        return content
    
    def get_portal_analytics(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get portal usage analytics.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Analytics data
        """
        # Filter data by date range
        period_comments = [c for c in self.comments 
                          if start_date <= c.timestamp <= end_date]
        
        period_users = [u for u in self.users.values() 
                       if start_date <= u.registration_date <= end_date]
        
        # Calculate metrics
        analytics = {
            'overview': {
                'total_users': len(self.users),
                'new_users_period': len(period_users),
                'total_comments': len(self.comments),
                'comments_period': len(period_comments),
                'total_documents': len(self.documents),
                'total_events': len(self.events)
            },
            'engagement': {
                'active_users': self._count_active_users(start_date, end_date),
                'comments_per_day': len(period_comments) / max((end_date - start_date).days, 1),
                'popular_categories': self._get_popular_categories(period_comments),
                'response_rate': self._calculate_response_rate()
            },
            'documents': {
                'total_downloads': sum(d.download_count for d in self.documents.values()),
                'popular_documents': self._get_popular_documents(),
                'by_language': self._get_documents_by_language_stats()
            },
            'events': {
                'total_registrations': sum(len(e.registrations) for e in self.events.values()),
                'attendance_rate': self._calculate_attendance_rate(),
                'popular_event_types': self._get_popular_event_types()
            },
            'geographic': {
                'user_locations': self._get_user_locations(),
                'comment_locations': self._get_comment_locations()
            },
            'technical': {
                'page_views': "Integration required with web analytics",
                'bounce_rate': "Integration required with web analytics",
                'session_duration': "Integration required with web analytics"
            }
        }
        
        return analytics
    
    def export_comments_report(
        self,
        format: str = "xlsx",
        include_personal_info: bool = False
    ) -> str:
        """
        Export comments for analysis.
        
        Args:
            format: Export format (xlsx, csv, json)
            include_personal_info: Include personal information
            
        Returns:
            File path
        """
        import pandas as pd
        
        # Prepare data
        data = []
        for comment in self.comments:
            record = {
                'Submission ID': comment.submission_id,
                'Date': comment.timestamp.strftime('%Y-%m-%d %H:%M'),
                'Category': comment.comment_category,
                'Subject': comment.comment_subject,
                'Comment': comment.comment_text,
                'Language': comment.language,
                'Attachments': len(comment.attachments)
            }
            
            if include_personal_info:
                record.update({
                    'Name': comment.name,
                    'Email': comment.email,
                    'Organization': comment.organization or '',
                    'Phone': comment.phone or ''
                })
            
            data.append(record)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Export based on format
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == "xlsx":
            filename = f"comments_export_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
        elif format == "csv":
            filename = f"comments_export_{timestamp}.csv"
            df.to_csv(filename, index=False)
        elif format == "json":
            filename = f"comments_export_{timestamp}.json"
            df.to_json(filename, orient='records', indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filename
    
    def _send_verification_email(self, user: PortalUser):
        """Send email verification."""
        verification_token = secrets.token_urlsafe(32)
        verification_link = f"{self.base_url}/verify?token={verification_token}&user={user.user_id}"
        
        notification = Notification(
            notification_id=f"NOTIF_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_id=user.user_id,
            notification_type="verification",
            subject="Verify your email for EIA Consultation Portal",
            message=f"""
            Dear {user.name},
            
            Thank you for registering. Please verify your email by clicking:
            {verification_link}
            
            This link expires in 24 hours.
            
            Best regards,
            EIA Consultation Team
            """,
            created_date=datetime.now(),
            send_date=datetime.now(),
            channel="email"
        )
        
        self.notifications.append(notification)
    
    def _notify_document_upload(self, document: Document):
        """Notify users of new document."""
        for user in self.users.values():
            if user.notification_preferences.get('project_updates', True):
                notification = Notification(
                    notification_id=f"NOTIF_{datetime.now().strftime('%Y%m%d%H%M%S')}_{user.user_id}",
                    user_id=user.user_id,
                    notification_type="document",
                    subject=f"New document available: {document.title}",
                    message=f"""
                    A new document has been uploaded to the consultation portal:
                    
                    Title: {document.title}
                    Type: {document.document_type}
                    Language: {document.language}
                    
                    View at: {self.base_url}/documents/{document.document_id}
                    """,
                    created_date=datetime.now(),
                    send_date=datetime.now(),
                    channel="email"
                )
                self.notifications.append(notification)
    
    def _send_comment_confirmation(self, comment: OnlineComment):
        """Send comment submission confirmation."""
        notification = Notification(
            notification_id=f"NOTIF_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_id=comment.user_id or f"ANON_{comment.email}",
            notification_type="comment_confirmation",
            subject="Your comment has been received",
            message=f"""
            Dear {comment.name},
            
            Thank you for your comment on the EIA consultation.
            
            Reference: {comment.submission_id}
            Category: {comment.comment_category}
            Subject: {comment.comment_subject}
            
            We will review your comment and respond within 30 days.
            
            Best regards,
            EIA Consultation Team
            """,
            created_date=datetime.now(),
            send_date=datetime.now(),
            channel="email"
        )
        
        self.notifications.append(notification)
    
    def _moderate_comment(self, comment: OnlineComment):
        """Basic comment moderation."""
        # Check for spam indicators
        spam_keywords = ['viagra', 'casino', 'lottery', 'prize', 'click here']
        comment_lower = comment.comment_text.lower()
        
        if any(keyword in comment_lower for keyword in spam_keywords):
            comment.metadata['moderation_status'] = 'spam'
            comment.metadata['moderation_date'] = datetime.now().isoformat()
            return
        
        # Check for inappropriate content
        inappropriate_keywords = ['profanity_list']  # Would have actual list
        
        if any(keyword in comment_lower for keyword in inappropriate_keywords):
            comment.metadata['moderation_status'] = 'flagged'
            comment.metadata['moderation_reason'] = 'inappropriate_content'
        else:
            comment.metadata['moderation_status'] = 'approved'
        
        comment.metadata['moderation_date'] = datetime.now().isoformat()
    
    def _notify_new_event(self, event: Event):
        """Notify users of new event."""
        for user in self.users.values():
            if user.notification_preferences.get('event_reminders', True):
                notification = Notification(
                    notification_id=f"NOTIF_{datetime.now().strftime('%Y%m%d%H%M%S')}_{user.user_id}",
                    user_id=user.user_id,
                    notification_type="event",
                    subject=f"New consultation event: {event.title}",
                    message=f"""
                    A new consultation event has been scheduled:
                    
                    {event.title}
                    Date: {event.date.strftime('%B %d, %Y at %H:%M')}
                    Location: {event.location}
                    
                    {event.description}
                    
                    {'Registration required' if event.registration_required else 'No registration needed'}
                    
                    More info: {self.base_url}/events/{event.event_id}
                    """,
                    created_date=datetime.now(),
                    send_date=datetime.now(),
                    channel="email"
                )
                self.notifications.append(notification)
    
    def _send_event_confirmation(self, event_id: str, user_id: str):
        """Send event registration confirmation."""
        event = self.events[event_id]
        user = self.users.get(user_id)
        
        if user:
            notification = Notification(
                notification_id=f"NOTIF_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                user_id=user_id,
                notification_type="event_confirmation",
                subject=f"Registration confirmed: {event.title}",
                message=f"""
                Dear {user.name},
                
                Your registration is confirmed for:
                
                {event.title}
                Date: {event.date.strftime('%B %d, %Y at %H:%M')}
                Location: {event.location}
                
                Please arrive 15 minutes early for registration.
                
                Best regards,
                EIA Consultation Team
                """,
                created_date=datetime.now(),
                send_date=datetime.now(),
                channel="email"
            )
            self.notifications.append(notification)
    
    def _get_active_consultation_info(self) -> Dict[str, Any]:
        """Get active consultation information."""
        return {
            'status': 'active',
            'phase': 'Draft EIA Review',
            'start_date': datetime.now() - timedelta(days=7),
            'end_date': datetime.now() + timedelta(days=23),
            'days_remaining': 23,
            'comments_received': len(self.comments),
            'events_scheduled': len([e for e in self.events.values() if e.status == 'upcoming'])
        }
    
    def _get_latest_updates(self, limit: int) -> List[Dict[str, Any]]:
        """Get latest portal updates."""
        updates = []
        
        # Recent documents
        recent_docs = sorted(self.documents.values(), 
                           key=lambda d: d.upload_date, 
                           reverse=True)[:limit]
        
        for doc in recent_docs:
            updates.append({
                'type': 'document',
                'date': doc.upload_date,
                'title': f"New document: {doc.title}",
                'link': f"/documents/{doc.document_id}"
            })
        
        # Recent events
        recent_events = sorted([e for e in self.events.values() if e.status == 'upcoming'],
                             key=lambda e: e.date)[:limit]
        
        for event in recent_events:
            updates.append({
                'type': 'event',
                'date': event.date,
                'title': f"Upcoming: {event.title}",
                'link': f"/events/{event.event_id}"
            })
        
        # Sort by date
        updates.sort(key=lambda u: u['date'], reverse=True)
        
        return updates[:limit]
    
    def _get_upcoming_events(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get upcoming events."""
        upcoming = [e for e in self.events.values() 
                   if e.date > datetime.now() and e.status == 'upcoming']
        upcoming.sort(key=lambda e: e.date)
        
        if limit:
            upcoming = upcoming[:limit]
        
        return [{
            'id': e.event_id,
            'title': e.title,
            'date': e.date,
            'location': e.location,
            'type': e.event_type,
            'registration_required': e.registration_required,
            'spaces_available': (e.capacity - len(e.registrations)) if e.capacity else None
        } for e in upcoming]
    
    def _get_quick_links(self, language: str) -> List[Dict[str, str]]:
        """Get quick access links."""
        links = [
            {'label': {'en': 'Submit Comment', 'ar': 'إرسال تعليق'}, 
             'url': '/participate#comment-form', 'icon': 'comment'},
            {'label': {'en': 'Download EIA Summary', 'ar': 'تحميل ملخص التقييم'}, 
             'url': '/documents/eia-summary', 'icon': 'download'},
            {'label': {'en': 'View Project Map', 'ar': 'عرض خريطة المشروع'}, 
             'url': '/project#map', 'icon': 'map'},
            {'label': {'en': 'Upcoming Events', 'ar': 'الفعاليات القادمة'}, 
             'url': '/events', 'icon': 'calendar'}
        ]
        
        return [{'label': link['label'][language], 
                'url': link['url'], 
                'icon': link['icon']} for link in links]
    
    def _get_document_categories(self) -> List[Dict[str, Any]]:
        """Get document categories with counts."""
        categories = defaultdict(int)
        
        for doc in self.documents.values():
            for cat in doc.categories:
                categories[cat] += 1
        
        return [{'name': cat, 'count': count, 'slug': cat.lower().replace(' ', '-')} 
                for cat, count in categories.items()]
    
    def _get_documents_by_language(self, language: str) -> List[Dict[str, Any]]:
        """Get documents filtered by language."""
        docs = [d for d in self.documents.values() if d.language == language]
        
        return [{
            'id': d.document_id,
            'title': d.title,
            'description': d.description,
            'type': d.document_type,
            'size': self._format_file_size(d.file_size),
            'date': d.upload_date,
            'downloads': d.download_count,
            'url': f"/documents/{d.document_id}/download"
        } for d in docs]
    
    def _get_featured_documents(self) -> List[Dict[str, Any]]:
        """Get featured/important documents."""
        featured_types = ['eia_summary', 'fact_sheet', 'presentation']
        featured = [d for d in self.documents.values() if d.document_type in featured_types]
        
        return [{
            'id': d.document_id,
            'title': d.title,
            'type': d.document_type,
            'languages': [d.language]  # In real system, might have multiple versions
        } for d in featured[:5]]
    
    def _get_download_statistics(self) -> Dict[str, Any]:
        """Get document download statistics."""
        total_downloads = sum(d.download_count for d in self.documents.values())
        
        if self.documents:
            most_downloaded = max(self.documents.values(), key=lambda d: d.download_count)
            return {
                'total': total_downloads,
                'most_popular': most_downloaded.title,
                'most_popular_count': most_downloaded.download_count
            }
        
        return {'total': 0, 'most_popular': None, 'most_popular_count': 0}
    
    def _get_comment_form_fields(self, language: str) -> List[Dict[str, Any]]:
        """Get comment form field definitions."""
        fields = [
            {
                'name': 'name',
                'type': 'text',
                'label': {'en': 'Full Name', 'ar': 'الاسم الكامل'},
                'required': True,
                'placeholder': {'en': 'Enter your full name', 'ar': 'أدخل اسمك الكامل'}
            },
            {
                'name': 'email',
                'type': 'email',
                'label': {'en': 'Email Address', 'ar': 'البريد الإلكتروني'},
                'required': True,
                'placeholder': {'en': 'your.email@example.com', 'ar': 'بريدك@example.com'}
            },
            {
                'name': 'phone',
                'type': 'tel',
                'label': {'en': 'Phone Number', 'ar': 'رقم الهاتف'},
                'required': False,
                'placeholder': {'en': '+971 XX XXX XXXX', 'ar': '+971 XX XXX XXXX'}
            },
            {
                'name': 'organization',
                'type': 'text',
                'label': {'en': 'Organization', 'ar': 'المنظمة'},
                'required': False,
                'placeholder': {'en': 'Your organization (optional)', 'ar': 'منظمتك (اختياري)'}
            },
            {
                'name': 'category',
                'type': 'select',
                'label': {'en': 'Comment Category', 'ar': 'فئة التعليق'},
                'required': True,
                'options': self.config['comment_categories']
            },
            {
                'name': 'subject',
                'type': 'text',
                'label': {'en': 'Subject', 'ar': 'الموضوع'},
                'required': True,
                'placeholder': {'en': 'Brief subject of your comment', 'ar': 'موضوع تعليقك باختصار'}
            },
            {
                'name': 'comment',
                'type': 'textarea',
                'label': {'en': 'Your Comment', 'ar': 'تعليقك'},
                'required': True,
                'placeholder': {'en': 'Please provide your detailed comment here...', 
                               'ar': 'يرجى تقديم تعليقك المفصل هنا...'},
                'maxlength': self.config['max_comment_length']
            },
            {
                'name': 'attachments',
                'type': 'file',
                'label': {'en': 'Attachments', 'ar': 'المرفقات'},
                'required': False,
                'multiple': True,
                'accept': ','.join([f'.{ext}' for ext in self.config['allowed_file_types']])
            },
            {
                'name': 'consent',
                'type': 'checkbox',
                'label': {'en': 'I consent to the processing of my personal data', 
                         'ar': 'أوافق على معالجة بياناتي الشخصية'},
                'required': True
            },
            {
                'name': 'newsletter',
                'type': 'checkbox',
                'label': {'en': 'Subscribe to project updates', 'ar': 'الاشتراك في تحديثات المشروع'},
                'required': False
            }
        ]
        
        # Return with translated labels
        return [{
            'name': f['name'],
            'type': f['type'],
            'label': f['label'][language],
            'required': f['required'],
            'placeholder': f.get('placeholder', {}).get(language, ''),
            'options': f.get('options', []),
            'maxlength': f.get('maxlength'),
            'multiple': f.get('multiple', False),
            'accept': f.get('accept', '')
        } for f in fields]
    
    def _get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information for pre-filling forms."""
        user = self.users.get(user_id)
        if user:
            return {
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'organization': user.organization
            }
        return None
    
    def _get_past_events(self) -> List[Dict[str, Any]]:
        """Get past events."""
        past = [e for e in self.events.values() 
               if e.date < datetime.now() or e.status == 'completed']
        past.sort(key=lambda e: e.date, reverse=True)
        
        return [{
            'id': e.event_id,
            'title': e.title,
            'date': e.date,
            'type': e.event_type,
            'attendance': len(e.registrations),
            'materials_available': len(e.materials_available) > 0
        } for e in past]
    
    def _get_user_events(self, user_id: str) -> List[str]:
        """Get events user is registered for."""
        if not user_id:
            return []
        
        return [e.event_id for e in self.events.values() if user_id in e.registrations]
    
    def _get_faqs(self, language: str) -> List[Dict[str, str]]:
        """Get frequently asked questions."""
        # This would be loaded from content management
        # Simplified example
        faqs = [
            {
                'question': {
                    'en': 'How can I submit a comment?',
                    'ar': 'كيف يمكنني تقديم تعليق؟'
                },
                'answer': {
                    'en': 'You can submit comments through our online form, by email, or at public meetings.',
                    'ar': 'يمكنك تقديم التعليقات من خلال النموذج الإلكتروني أو البريد الإلكتروني أو في الاجتماعات العامة.'
                },
                'category': 'participation'
            }
        ]
        
        return [{
            'question': faq['question'][language],
            'answer': faq['answer'][language],
            'category': faq['category']
        } for faq in faqs]
    
    def _get_faq_categories(self) -> List[str]:
        """Get FAQ categories."""
        return ['participation', 'project', 'environmental', 'process', 'contact']
    
    def _get_contact_info(self, language: str) -> Dict[str, Any]:
        """Get contact information."""
        return {
            'hotline': '+971-X-XXX-XXXX',
            'email': 'consultation@project.ae',
            'office_hours': {'en': 'Sunday-Thursday 8:00-17:00', 
                           'ar': 'الأحد-الخميس 8:00-17:00'},
            'address': {'en': 'Project Information Center, Dubai, UAE',
                       'ar': 'مركز معلومات المشروع، دبي، الإمارات'}
        }
    
    def _count_active_users(self, start_date: datetime, end_date: datetime) -> int:
        """Count active users in period."""
        active_users = set()
        
        # Users who submitted comments
        for comment in self.comments:
            if start_date <= comment.timestamp <= end_date and comment.user_id:
                active_users.add(comment.user_id)
        
        # Users who registered for events
        for event in self.events.values():
            if start_date <= event.date <= end_date:
                active_users.update(event.registrations)
        
        return len(active_users)
    
    def _get_popular_categories(self, comments: List[OnlineComment]) -> List[Tuple[str, int]]:
        """Get popular comment categories."""
        category_counts = defaultdict(int)
        
        for comment in comments:
            category_counts[comment.comment_category] += 1
        
        # Sort by count
        popular = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        return popular[:5]
    
    def _calculate_response_rate(self) -> float:
        """Calculate comment response rate."""
        if not self.comments:
            return 0.0
        
        # Count comments with responses (would check actual response field)
        responded = sum(1 for c in self.comments if c.metadata.get('response_sent', False))
        
        return (responded / len(self.comments)) * 100
    
    def _get_popular_documents(self) -> List[Tuple[str, int]]:
        """Get most downloaded documents."""
        docs = sorted(self.documents.values(), 
                     key=lambda d: d.download_count, 
                     reverse=True)[:5]
        
        return [(d.title, d.download_count) for d in docs]
    
    def _get_documents_by_language_stats(self) -> Dict[str, int]:
        """Get document count by language."""
        lang_counts = defaultdict(int)
        
        for doc in self.documents.values():
            lang_counts[doc.language] += 1
        
        return dict(lang_counts)
    
    def _calculate_attendance_rate(self) -> float:
        """Calculate event attendance rate."""
        completed_events = [e for e in self.events.values() if e.status == 'completed']
        
        if not completed_events:
            return 0.0
        
        total_registered = sum(len(e.registrations) for e in completed_events)
        total_attended = sum(e.metadata.get('actual_attendance', len(e.registrations)) 
                           for e in completed_events)
        
        return (total_attended / total_registered * 100) if total_registered > 0 else 0.0
    
    def _get_popular_event_types(self) -> List[Tuple[str, int]]:
        """Get popular event types by registration."""
        type_registrations = defaultdict(int)
        
        for event in self.events.values():
            type_registrations[event.event_type] += len(event.registrations)
        
        popular = sorted(type_registrations.items(), key=lambda x: x[1], reverse=True)
        
        return popular
    
    def _get_user_locations(self) -> Dict[str, int]:
        """Get user location distribution."""
        location_counts = defaultdict(int)
        
        for user in self.users.values():
            location = user.location or 'Unknown'
            location_counts[location] += 1
        
        return dict(location_counts)
    
    def _get_comment_locations(self) -> Dict[str, int]:
        """Get comment location references."""
        location_counts = defaultdict(int)
        
        for comment in self.comments:
            location = comment.location_reference or 'General'
            location_counts[location] += 1
        
        return dict(location_counts)
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size for display."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"