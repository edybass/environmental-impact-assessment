"""
Automated Notification System for Stakeholder Engagement
Email, SMS, and in-app notifications for EIA consultation

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import smtplib
import email.mime.text
import email.mime.multipart
from email.mime.base import MIMEBase
from email import encoders
import requests
import jinja2
import logging
from pathlib import Path
import asyncio
import aiosmtplib
from collections import defaultdict
import re

logger = logging.getLogger(__name__)


class NotificationType(Enum):
    """Types of notifications."""
    EVENT_ANNOUNCEMENT = "event_announcement"
    EVENT_REMINDER = "event_reminder"
    COMMENT_ACKNOWLEDGMENT = "comment_acknowledgment"
    COMMENT_RESPONSE = "comment_response"
    DOCUMENT_AVAILABLE = "document_available"
    CONSULTATION_OPENING = "consultation_opening"
    CONSULTATION_CLOSING = "consultation_closing"
    MEETING_MINUTES = "meeting_minutes"
    PROJECT_UPDATE = "project_update"
    GRIEVANCE_UPDATE = "grievance_update"
    DEADLINE_REMINDER = "deadline_reminder"
    THANK_YOU = "thank_you"


class NotificationChannel(Enum):
    """Notification delivery channels."""
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    IN_APP = "in_app"
    PUSH = "push"


class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class NotificationTemplate:
    """Notification template definition."""
    template_id: str
    notification_type: NotificationType
    channel: NotificationChannel
    languages: Dict[str, Dict[str, str]]  # lang: {subject, body}
    variables: List[str]  # Required template variables
    attachments: List[str] = field(default_factory=list)
    priority: NotificationPriority = NotificationPriority.MEDIUM
    active: bool = True


@dataclass
class NotificationRecipient:
    """Notification recipient."""
    recipient_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    language: str = "en"
    channels: List[NotificationChannel] = field(default_factory=lambda: [NotificationChannel.EMAIL])
    preferences: Dict[str, bool] = field(default_factory=dict)
    timezone: str = "Asia/Dubai"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NotificationJob:
    """Scheduled notification job."""
    job_id: str
    notification_type: NotificationType
    recipients: List[NotificationRecipient]
    template_id: str
    variables: Dict[str, Any]
    scheduled_time: datetime
    channels: List[NotificationChannel]
    status: str = "pending"  # pending, processing, completed, failed
    created_date: datetime = field(default_factory=datetime.now)
    sent_count: int = 0
    failed_count: int = 0
    error_messages: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NotificationLog:
    """Notification delivery log."""
    log_id: str
    job_id: str
    recipient_id: str
    channel: NotificationChannel
    timestamp: datetime
    status: str  # sent, failed, bounced, opened, clicked
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class NotificationSystem:
    """Comprehensive notification management system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        
        # Initialize template engine
        self.jinja_env = jinja2.Environment(
            loader=jinja2.DictLoader({}),
            autoescape=True
        )
        
        # Storage
        self.templates: Dict[str, NotificationTemplate] = {}
        self.jobs: Dict[str, NotificationJob] = {}
        self.logs: List[NotificationLog] = []
        
        # Initialize default templates
        self._initialize_default_templates()
        
        # Channel handlers
        self.channel_handlers = {
            NotificationChannel.EMAIL: self._send_email,
            NotificationChannel.SMS: self._send_sms,
            NotificationChannel.WHATSAPP: self._send_whatsapp,
            NotificationChannel.IN_APP: self._send_in_app,
            NotificationChannel.PUSH: self._send_push
        }
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default notification system configuration."""
        return {
            'email': {
                'smtp_host': 'smtp.gmail.com',
                'smtp_port': 587,
                'smtp_user': 'eia-notifications@example.com',
                'smtp_password': 'password',
                'from_address': 'EIA Consultation <eia-notifications@example.com>',
                'reply_to': 'eia-consultation@example.com',
                'use_tls': True
            },
            'sms': {
                'provider': 'twilio',
                'account_sid': 'your_account_sid',
                'auth_token': 'your_auth_token',
                'from_number': '+1234567890'
            },
            'whatsapp': {
                'provider': 'twilio',
                'account_sid': 'your_account_sid',
                'auth_token': 'your_auth_token',
                'from_number': 'whatsapp:+1234567890'
            },
            'rate_limits': {
                'email_per_hour': 1000,
                'sms_per_hour': 500,
                'whatsapp_per_hour': 500
            },
            'retry_policy': {
                'max_retries': 3,
                'retry_delay': 300  # seconds
            },
            'batch_size': 100,
            'async_enabled': True
        }
    
    def _initialize_default_templates(self):
        """Initialize default notification templates."""
        # Event announcement template
        self.templates['event_announcement'] = NotificationTemplate(
            template_id='event_announcement',
            notification_type=NotificationType.EVENT_ANNOUNCEMENT,
            channel=NotificationChannel.EMAIL,
            languages={
                'en': {
                    'subject': 'New Consultation Event: {{ event_title }}',
                    'body': '''
                    Dear {{ recipient_name }},
                    
                    We are pleased to announce a new consultation event for the {{ project_name }} Environmental Impact Assessment.
                    
                    Event Details:
                    - Title: {{ event_title }}
                    - Date: {{ event_date }}
                    - Time: {{ event_time }}
                    - Location: {{ event_location }}
                    - Language: {{ event_languages }}
                    
                    {{ event_description }}
                    
                    {% if registration_required %}
                    Registration is required. Please register at: {{ registration_link }}
                    {% else %}
                    No registration required. All are welcome!
                    {% endif %}
                    
                    For more information, visit: {{ portal_url }}
                    
                    Best regards,
                    {{ project_name }} EIA Team
                    '''
                },
                'ar': {
                    'subject': 'فعالية استشارية جديدة: {{ event_title }}',
                    'body': '''
                    عزيزي {{ recipient_name }}،
                    
                    يسرنا أن نعلن عن فعالية استشارية جديدة لتقييم الأثر البيئي لمشروع {{ project_name }}.
                    
                    تفاصيل الفعالية:
                    - العنوان: {{ event_title }}
                    - التاريخ: {{ event_date }}
                    - الوقت: {{ event_time }}
                    - المكان: {{ event_location }}
                    - اللغة: {{ event_languages }}
                    
                    {{ event_description }}
                    
                    {% if registration_required %}
                    التسجيل مطلوب. يرجى التسجيل على: {{ registration_link }}
                    {% else %}
                    لا يتطلب التسجيل. الجميع مرحب بهم!
                    {% endif %}
                    
                    لمزيد من المعلومات، تفضل بزيارة: {{ portal_url }}
                    
                    مع أطيب التحيات،
                    فريق تقييم الأثر البيئي لمشروع {{ project_name }}
                    '''
                }
            },
            variables=['recipient_name', 'project_name', 'event_title', 'event_date', 
                      'event_time', 'event_location', 'event_languages', 'event_description',
                      'registration_required', 'registration_link', 'portal_url'],
            priority=NotificationPriority.HIGH
        )
        
        # Comment acknowledgment template
        self.templates['comment_acknowledgment'] = NotificationTemplate(
            template_id='comment_acknowledgment',
            notification_type=NotificationType.COMMENT_ACKNOWLEDGMENT,
            channel=NotificationChannel.EMAIL,
            languages={
                'en': {
                    'subject': 'Thank you for your comment - Reference: {{ comment_id }}',
                    'body': '''
                    Dear {{ recipient_name }},
                    
                    Thank you for submitting your comment on the {{ project_name }} Environmental Impact Assessment.
                    
                    Your comment details:
                    - Reference Number: {{ comment_id }}
                    - Category: {{ comment_category }}
                    - Subject: {{ comment_subject }}
                    - Submitted: {{ submission_date }}
                    
                    We have received your comment and it will be carefully reviewed by our team. 
                    You can expect a response within {{ response_timeframe }} days.
                    
                    You can track the status of your comment at: {{ tracking_link }}
                    
                    If you have any questions, please contact us at {{ contact_email }}
                    
                    Best regards,
                    {{ project_name }} EIA Team
                    '''
                },
                'ar': {
                    'subject': 'شكراً لتعليقك - المرجع: {{ comment_id }}',
                    'body': '''
                    عزيزي {{ recipient_name }}،
                    
                    نشكرك على تقديم تعليقك حول تقييم الأثر البيئي لمشروع {{ project_name }}.
                    
                    تفاصيل تعليقك:
                    - الرقم المرجعي: {{ comment_id }}
                    - الفئة: {{ comment_category }}
                    - الموضوع: {{ comment_subject }}
                    - تاريخ التقديم: {{ submission_date }}
                    
                    لقد استلمنا تعليقك وسيتم مراجعته بعناية من قبل فريقنا.
                    يمكنك توقع الرد خلال {{ response_timeframe }} يوماً.
                    
                    يمكنك تتبع حالة تعليقك على: {{ tracking_link }}
                    
                    إذا كان لديك أي أسئلة، يرجى الاتصال بنا على {{ contact_email }}
                    
                    مع أطيب التحيات،
                    فريق تقييم الأثر البيئي لمشروع {{ project_name }}
                    '''
                }
            },
            variables=['recipient_name', 'project_name', 'comment_id', 'comment_category',
                      'comment_subject', 'submission_date', 'response_timeframe', 
                      'tracking_link', 'contact_email'],
            priority=NotificationPriority.MEDIUM
        )
        
        # Consultation closing reminder
        self.templates['consultation_closing'] = NotificationTemplate(
            template_id='consultation_closing',
            notification_type=NotificationType.CONSULTATION_CLOSING,
            channel=NotificationChannel.EMAIL,
            languages={
                'en': {
                    'subject': 'Final Reminder: {{ days_remaining }} days left to comment',
                    'body': '''
                    Dear {{ recipient_name }},
                    
                    This is a reminder that the public consultation period for the {{ project_name }} 
                    Environmental Impact Assessment will close in {{ days_remaining }} days.
                    
                    Closing Date: {{ closing_date }}
                    
                    If you haven't already, please submit your comments before the deadline:
                    - Online: {{ comment_link }}
                    - Email: {{ contact_email }}
                    - In person: {{ office_address }}
                    
                    Your input is valuable and helps ensure that all environmental and social 
                    considerations are properly addressed.
                    
                    Thank you for your participation.
                    
                    Best regards,
                    {{ project_name }} EIA Team
                    '''
                },
                'ar': {
                    'subject': 'تذكير نهائي: {{ days_remaining }} يوم متبقي للتعليق',
                    'body': '''
                    عزيزي {{ recipient_name }}،
                    
                    هذا تذكير بأن فترة الاستشارة العامة لتقييم الأثر البيئي لمشروع {{ project_name }}
                    ستنتهي خلال {{ days_remaining }} يوم.
                    
                    تاريخ الإغلاق: {{ closing_date }}
                    
                    إذا لم تقم بذلك بعد، يرجى تقديم تعليقاتك قبل الموعد النهائي:
                    - عبر الإنترنت: {{ comment_link }}
                    - البريد الإلكتروني: {{ contact_email }}
                    - شخصياً: {{ office_address }}
                    
                    مساهمتك قيمة وتساعد في ضمان معالجة جميع الاعتبارات البيئية والاجتماعية
                    بشكل صحيح.
                    
                    شكراً لمشاركتك.
                    
                    مع أطيب التحيات،
                    فريق تقييم الأثر البيئي لمشروع {{ project_name }}
                    '''
                }
            },
            variables=['recipient_name', 'project_name', 'days_remaining', 'closing_date',
                      'comment_link', 'contact_email', 'office_address'],
            priority=NotificationPriority.URGENT
        )
    
    def create_template(
        self,
        template_id: str,
        notification_type: NotificationType,
        channel: NotificationChannel,
        languages: Dict[str, Dict[str, str]],
        variables: List[str],
        priority: NotificationPriority = NotificationPriority.MEDIUM
    ) -> NotificationTemplate:
        """
        Create a new notification template.
        
        Args:
            template_id: Unique template identifier
            notification_type: Type of notification
            channel: Delivery channel
            languages: Language versions of template
            variables: Required template variables
            priority: Notification priority
            
        Returns:
            Created template
        """
        template = NotificationTemplate(
            template_id=template_id,
            notification_type=notification_type,
            channel=channel,
            languages=languages,
            variables=variables,
            priority=priority
        )
        
        # Validate and compile templates
        for lang, content in languages.items():
            # Add to Jinja environment
            self.jinja_env.loader.mapping[f"{template_id}_{lang}_subject"] = content['subject']
            self.jinja_env.loader.mapping[f"{template_id}_{lang}_body"] = content['body']
            
            # Test compilation
            try:
                self.jinja_env.get_template(f"{template_id}_{lang}_subject")
                self.jinja_env.get_template(f"{template_id}_{lang}_body")
            except jinja2.TemplateError as e:
                raise ValueError(f"Invalid template syntax in {lang}: {e}")
        
        self.templates[template_id] = template
        return template
    
    def schedule_notification(
        self,
        notification_type: NotificationType,
        recipients: List[NotificationRecipient],
        variables: Dict[str, Any],
        scheduled_time: Optional[datetime] = None,
        channels: Optional[List[NotificationChannel]] = None,
        template_override: Optional[str] = None
    ) -> NotificationJob:
        """
        Schedule a notification job.
        
        Args:
            notification_type: Type of notification
            recipients: List of recipients
            variables: Template variables
            scheduled_time: When to send (None for immediate)
            channels: Delivery channels (None for recipient preferences)
            template_override: Override default template
            
        Returns:
            Scheduled job
        """
        # Find appropriate template
        template_id = template_override or notification_type.value
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates[template_id]
        
        # Validate variables
        missing_vars = set(template.variables) - set(variables.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
        
        # Create job
        job = NotificationJob(
            job_id=f"JOB_{datetime.now().strftime('%Y%m%d%H%M%S')}_{notification_type.value}",
            notification_type=notification_type,
            recipients=recipients,
            template_id=template_id,
            variables=variables,
            scheduled_time=scheduled_time or datetime.now(),
            channels=channels or [template.channel]
        )
        
        self.jobs[job.job_id] = job
        
        # Process immediately if scheduled time is now or past
        if job.scheduled_time <= datetime.now():
            if self.config['async_enabled']:
                asyncio.create_task(self._process_job_async(job))
            else:
                self._process_job(job)
        
        return job
    
    def send_immediate(
        self,
        notification_type: NotificationType,
        recipient: NotificationRecipient,
        variables: Dict[str, Any],
        channel: Optional[NotificationChannel] = None
    ) -> bool:
        """
        Send immediate notification to single recipient.
        
        Args:
            notification_type: Type of notification
            recipient: Recipient
            variables: Template variables
            channel: Delivery channel
            
        Returns:
            Success status
        """
        job = self.schedule_notification(
            notification_type=notification_type,
            recipients=[recipient],
            variables=variables,
            channels=[channel] if channel else None
        )
        
        # Wait for completion
        timeout = 30  # seconds
        start_time = datetime.now()
        
        while job.status == 'processing' and (datetime.now() - start_time).seconds < timeout:
            asyncio.sleep(0.1)
        
        return job.status == 'completed' and job.failed_count == 0
    
    def _process_job(self, job: NotificationJob):
        """Process notification job synchronously."""
        job.status = 'processing'
        
        template = self.templates[job.template_id]
        
        # Process in batches
        batch_size = self.config['batch_size']
        
        for i in range(0, len(job.recipients), batch_size):
            batch = job.recipients[i:i + batch_size]
            
            for recipient in batch:
                for channel in job.channels:
                    try:
                        # Render template
                        subject, body = self._render_template(
                            template, recipient.language, job.variables
                        )
                        
                        # Send via channel
                        handler = self.channel_handlers.get(channel)
                        if handler:
                            success = handler(recipient, subject, body)
                            
                            # Log result
                            self._log_delivery(
                                job.job_id,
                                recipient.recipient_id,
                                channel,
                                'sent' if success else 'failed'
                            )
                            
                            if success:
                                job.sent_count += 1
                            else:
                                job.failed_count += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to send notification: {e}")
                        job.failed_count += 1
                        job.error_messages.append(str(e))
                        
                        self._log_delivery(
                            job.job_id,
                            recipient.recipient_id,
                            channel,
                            'failed',
                            str(e)
                        )
        
        job.status = 'completed'
    
    async def _process_job_async(self, job: NotificationJob):
        """Process notification job asynchronously."""
        job.status = 'processing'
        
        template = self.templates[job.template_id]
        
        # Create tasks for all notifications
        tasks = []
        
        for recipient in job.recipients:
            for channel in job.channels:
                task = self._send_notification_async(
                    job, template, recipient, channel
                )
                tasks.append(task)
        
        # Process in batches
        batch_size = self.config['batch_size']
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            results = await asyncio.gather(*batch, return_exceptions=True)
            
            # Update counters
            for result in results:
                if isinstance(result, Exception):
                    job.failed_count += 1
                    job.error_messages.append(str(result))
                elif result:
                    job.sent_count += 1
                else:
                    job.failed_count += 1
        
        job.status = 'completed'
    
    async def _send_notification_async(
        self,
        job: NotificationJob,
        template: NotificationTemplate,
        recipient: NotificationRecipient,
        channel: NotificationChannel
    ) -> bool:
        """Send single notification asynchronously."""
        try:
            # Render template
            subject, body = self._render_template(
                template, recipient.language, job.variables
            )
            
            # Send via channel
            if channel == NotificationChannel.EMAIL:
                success = await self._send_email_async(recipient, subject, body)
            else:
                # Fall back to sync for other channels
                handler = self.channel_handlers.get(channel)
                success = handler(recipient, subject, body) if handler else False
            
            # Log result
            self._log_delivery(
                job.job_id,
                recipient.recipient_id,
                channel,
                'sent' if success else 'failed'
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            self._log_delivery(
                job.job_id,
                recipient.recipient_id,
                channel,
                'failed',
                str(e)
            )
            raise
    
    def _render_template(
        self,
        template: NotificationTemplate,
        language: str,
        variables: Dict[str, Any]
    ) -> tuple[str, str]:
        """Render notification template."""
        # Get language version
        if language not in template.languages:
            language = 'en'  # Fallback to English
        
        # Render subject and body
        subject_template = self.jinja_env.get_template(f"{template.template_id}_{language}_subject")
        body_template = self.jinja_env.get_template(f"{template.template_id}_{language}_body")
        
        subject = subject_template.render(**variables)
        body = body_template.render(**variables)
        
        return subject, body
    
    def _send_email(
        self,
        recipient: NotificationRecipient,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Send email notification."""
        if not recipient.email:
            return False
        
        try:
            # Create message
            msg = email.mime.multipart.MIMEMultipart()
            msg['From'] = self.config['email']['from_address']
            msg['To'] = recipient.email
            msg['Subject'] = subject
            msg['Reply-To'] = self.config['email']['reply_to']
            
            # Add body
            msg.attach(email.mime.text.MIMEText(body, 'plain', 'utf-8'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        self._attach_file(msg, file_path)
            
            # Send email
            with smtplib.SMTP(self.config['email']['smtp_host'], 
                             self.config['email']['smtp_port']) as server:
                if self.config['email']['use_tls']:
                    server.starttls()
                server.login(self.config['email']['smtp_user'], 
                           self.config['email']['smtp_password'])
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False
    
    async def _send_email_async(
        self,
        recipient: NotificationRecipient,
        subject: str,
        body: str
    ) -> bool:
        """Send email notification asynchronously."""
        if not recipient.email:
            return False
        
        try:
            # Create message
            msg = email.mime.text.MIMEText(body, 'plain', 'utf-8')
            msg['From'] = self.config['email']['from_address']
            msg['To'] = recipient.email
            msg['Subject'] = subject
            msg['Reply-To'] = self.config['email']['reply_to']
            
            # Send asynchronously
            await aiosmtplib.send(
                msg,
                hostname=self.config['email']['smtp_host'],
                port=self.config['email']['smtp_port'],
                username=self.config['email']['smtp_user'],
                password=self.config['email']['smtp_password'],
                use_tls=self.config['email']['use_tls']
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Async email send failed: {e}")
            return False
    
    def _send_sms(
        self,
        recipient: NotificationRecipient,
        subject: str,
        body: str
    ) -> bool:
        """Send SMS notification."""
        if not recipient.phone:
            return False
        
        try:
            # Using Twilio as example
            if self.config['sms']['provider'] == 'twilio':
                # Format message (SMS has character limit)
                message = f"{subject}\n\n{body}"[:160]
                
                # Twilio API call
                auth = (self.config['sms']['account_sid'], 
                       self.config['sms']['auth_token'])
                
                data = {
                    'From': self.config['sms']['from_number'],
                    'To': recipient.phone,
                    'Body': message
                }
                
                response = requests.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{self.config['sms']['account_sid']}/Messages.json",
                    auth=auth,
                    data=data
                )
                
                return response.status_code == 201
            
            return False
            
        except Exception as e:
            logger.error(f"SMS send failed: {e}")
            return False
    
    def _send_whatsapp(
        self,
        recipient: NotificationRecipient,
        subject: str,
        body: str
    ) -> bool:
        """Send WhatsApp notification."""
        if not recipient.phone:
            return False
        
        try:
            # Using Twilio WhatsApp as example
            if self.config['whatsapp']['provider'] == 'twilio':
                message = f"*{subject}*\n\n{body}"
                
                auth = (self.config['whatsapp']['account_sid'], 
                       self.config['whatsapp']['auth_token'])
                
                data = {
                    'From': self.config['whatsapp']['from_number'],
                    'To': f"whatsapp:{recipient.phone}",
                    'Body': message
                }
                
                response = requests.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{self.config['whatsapp']['account_sid']}/Messages.json",
                    auth=auth,
                    data=data
                )
                
                return response.status_code == 201
            
            return False
            
        except Exception as e:
            logger.error(f"WhatsApp send failed: {e}")
            return False
    
    def _send_in_app(
        self,
        recipient: NotificationRecipient,
        subject: str,
        body: str
    ) -> bool:
        """Send in-app notification."""
        # This would integrate with the web application's notification system
        # For now, just log it
        logger.info(f"In-app notification for {recipient.recipient_id}: {subject}")
        return True
    
    def _send_push(
        self,
        recipient: NotificationRecipient,
        subject: str,
        body: str
    ) -> bool:
        """Send push notification."""
        # This would integrate with FCM, APNS, etc.
        # For now, just log it
        logger.info(f"Push notification for {recipient.recipient_id}: {subject}")
        return True
    
    def _attach_file(self, msg: email.mime.multipart.MIMEMultipart, file_path: str):
        """Attach file to email."""
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={Path(file_path).name}'
            )
            msg.attach(part)
    
    def _log_delivery(
        self,
        job_id: str,
        recipient_id: str,
        channel: NotificationChannel,
        status: str,
        error_message: Optional[str] = None
    ):
        """Log notification delivery attempt."""
        log = NotificationLog(
            log_id=f"LOG_{datetime.now().strftime('%Y%m%d%H%M%S')}_{recipient_id}",
            job_id=job_id,
            recipient_id=recipient_id,
            channel=channel,
            timestamp=datetime.now(),
            status=status,
            error_message=error_message
        )
        
        self.logs.append(log)
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get notification job status."""
        job = self.jobs.get(job_id)
        if not job:
            return None
        
        return {
            'job_id': job.job_id,
            'status': job.status,
            'notification_type': job.notification_type.value,
            'total_recipients': len(job.recipients),
            'sent_count': job.sent_count,
            'failed_count': job.failed_count,
            'created_date': job.created_date,
            'scheduled_time': job.scheduled_time,
            'error_messages': job.error_messages
        }
    
    def get_delivery_stats(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get notification delivery statistics."""
        # Filter logs by date range
        period_logs = [log for log in self.logs 
                      if start_date <= log.timestamp <= end_date]
        
        # Calculate statistics
        stats = {
            'total_sent': len(period_logs),
            'by_channel': defaultdict(int),
            'by_status': defaultdict(int),
            'by_type': defaultdict(int),
            'success_rate': 0.0,
            'average_per_day': 0.0
        }
        
        # Count by channel and status
        for log in period_logs:
            stats['by_channel'][log.channel.value] += 1
            stats['by_status'][log.status] += 1
        
        # Count by notification type
        for job in self.jobs.values():
            if start_date <= job.created_date <= end_date:
                stats['by_type'][job.notification_type.value] += job.sent_count
        
        # Calculate rates
        if stats['total_sent'] > 0:
            sent_success = stats['by_status'].get('sent', 0)
            stats['success_rate'] = (sent_success / stats['total_sent']) * 100
        
        days = max((end_date - start_date).days, 1)
        stats['average_per_day'] = stats['total_sent'] / days
        
        return dict(stats)
    
    def create_notification_campaign(
        self,
        name: str,
        notification_type: NotificationType,
        recipient_criteria: Dict[str, Any],
        variables: Dict[str, Any],
        schedule: Dict[str, Any]
    ) -> str:
        """
        Create a notification campaign.
        
        Args:
            name: Campaign name
            notification_type: Type of notifications
            recipient_criteria: Criteria for selecting recipients
            variables: Template variables
            schedule: Campaign schedule
            
        Returns:
            Campaign ID
        """
        campaign_id = f"CAMPAIGN_{datetime.now().strftime('%Y%m%d%H%M%S')}_{name}"
        
        # This would typically:
        # 1. Query recipient database based on criteria
        # 2. Create scheduled jobs for each notification
        # 3. Handle recurring notifications
        # 4. Track campaign performance
        
        logger.info(f"Created campaign {campaign_id}")
        
        return campaign_id
    
    def bulk_import_recipients(
        self,
        file_path: str,
        default_preferences: Optional[Dict[str, bool]] = None
    ) -> int:
        """
        Bulk import recipients from file.
        
        Args:
            file_path: Path to CSV/Excel file
            default_preferences: Default notification preferences
            
        Returns:
            Number of recipients imported
        """
        import pandas as pd
        
        # Read file
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        # Process recipients
        recipients = []
        
        for _, row in df.iterrows():
            recipient = NotificationRecipient(
                recipient_id=f"REC_{row.get('id', '')}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                name=row.get('name', ''),
                email=row.get('email'),
                phone=row.get('phone'),
                language=row.get('language', 'en'),
                preferences=default_preferences or {}
            )
            recipients.append(recipient)
        
        # Store recipients (in real system, would save to database)
        logger.info(f"Imported {len(recipients)} recipients")
        
        return len(recipients)