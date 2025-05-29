"""
Stakeholder Engagement Management System
Professional stakeholder consultation and management for EIA

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import pandas as pd
from collections import defaultdict
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class StakeholderType(Enum):
    """Types of stakeholders in EIA process."""
    GOVERNMENT = "government"
    COMMUNITY = "community"
    NGO = "ngo"
    BUSINESS = "business"
    ACADEMIC = "academic"
    MEDIA = "media"
    AFFECTED_PARTY = "affected_party"
    INDIGENOUS = "indigenous"
    TECHNICAL_EXPERT = "technical_expert"


class EngagementLevel(Enum):
    """Levels of stakeholder engagement."""
    INFORM = "inform"  # One-way communication
    CONSULT = "consult"  # Two-way communication
    INVOLVE = "involve"  # Work directly throughout
    COLLABORATE = "collaborate"  # Partner in decisions
    EMPOWER = "empower"  # Final decision making


class CommentStatus(Enum):
    """Status of stakeholder comments."""
    RECEIVED = "received"
    UNDER_REVIEW = "under_review"
    ADDRESSED = "addressed"
    INCORPORATED = "incorporated"
    NOT_APPLICABLE = "not_applicable"
    CLARIFICATION_NEEDED = "clarification_needed"


class MeetingType(Enum):
    """Types of stakeholder meetings."""
    PUBLIC_HEARING = "public_hearing"
    FOCUS_GROUP = "focus_group"
    ONE_ON_ONE = "one_on_one"
    WORKSHOP = "workshop"
    SITE_VISIT = "site_visit"
    ONLINE_CONSULTATION = "online_consultation"
    INFORMATION_SESSION = "information_session"


@dataclass
class Stakeholder:
    """Individual or organization stakeholder."""
    stakeholder_id: str
    name: str
    stakeholder_type: StakeholderType
    organization: Optional[str] = None
    position: Optional[str] = None
    contact_info: Dict[str, str] = field(default_factory=dict)
    location: Optional[Tuple[float, float]] = None  # (lat, lon)
    language_preference: str = "en"
    engagement_level: EngagementLevel = EngagementLevel.INFORM
    influence_level: str = "medium"  # low, medium, high
    interest_level: str = "medium"  # low, medium, high
    concerns: List[str] = field(default_factory=list)
    preferred_contact_method: str = "email"
    special_requirements: List[str] = field(default_factory=list)
    engagement_history: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    created_date: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Comment:
    """Stakeholder comment or feedback."""
    comment_id: str
    stakeholder_id: str
    submission_date: datetime
    comment_text: str
    topic_category: str
    impact_area: str  # air, water, noise, social, etc.
    sentiment: str  # positive, negative, neutral
    priority: str  # low, medium, high, critical
    status: CommentStatus
    assigned_to: Optional[str] = None
    response_text: Optional[str] = None
    response_date: Optional[datetime] = None
    actions_taken: List[str] = field(default_factory=list)
    eia_section_reference: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    follow_up_required: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Meeting:
    """Stakeholder meeting record."""
    meeting_id: str
    meeting_type: MeetingType
    title: str
    date: datetime
    location: str
    duration_hours: float
    facilitator: str
    attendees: List[str]  # stakeholder_ids
    agenda: List[str]
    minutes: str
    decisions: List[str]
    action_items: List[Dict[str, Any]]
    materials_presented: List[str]
    issues_raised: List[Dict[str, Any]]
    commitments_made: List[str]
    follow_up_required: bool
    recording_available: bool = False
    language_used: str = "en"
    interpreter_present: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsultationPlan:
    """Public consultation plan."""
    plan_id: str
    project_id: int
    phases: List[Dict[str, Any]]
    timeline: Dict[str, datetime]
    objectives: List[str]
    target_stakeholders: List[str]
    methods: List[str]
    resources_required: Dict[str, Any]
    success_metrics: List[str]
    risk_mitigation: Dict[str, str]
    budget: float
    regulatory_requirements: List[str]
    cultural_considerations: List[str]
    created_date: datetime
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None


class StakeholderEngagementSystem:
    """Comprehensive stakeholder engagement management system."""
    
    def __init__(self):
        # UAE/KSA specific regulatory requirements
        self.regulatory_requirements = {
            'UAE': {
                'public_consultation_period': 30,  # days
                'notice_period': 14,  # days before meeting
                'languages': ['ar', 'en'],
                'public_hearing_required': True,
                'online_consultation_allowed': True,
                'response_timeframe': 30  # days
            },
            'KSA': {
                'public_consultation_period': 45,  # days
                'notice_period': 21,  # days before meeting
                'languages': ['ar', 'en'],
                'public_hearing_required': True,
                'online_consultation_allowed': True,
                'response_timeframe': 45  # days
            }
        }
        
        # Comment categories
        self.comment_categories = [
            'Air Quality',
            'Water Resources',
            'Noise and Vibration',
            'Traffic and Transportation',
            'Visual Impact',
            'Ecological Impact',
            'Social Impact',
            'Economic Impact',
            'Cultural Heritage',
            'Health and Safety',
            'Cumulative Effects',
            'Alternatives',
            'Mitigation Measures',
            'Monitoring',
            'General Concern'
        ]
        
        # Engagement methods by stakeholder type
        self.engagement_methods = {
            StakeholderType.GOVERNMENT: ['formal_letters', 'meetings', 'reports'],
            StakeholderType.COMMUNITY: ['public_meetings', 'surveys', 'focus_groups', 'social_media'],
            StakeholderType.NGO: ['workshops', 'meetings', 'written_submissions'],
            StakeholderType.BUSINESS: ['meetings', 'presentations', 'written_communication'],
            StakeholderType.ACADEMIC: ['technical_workshops', 'peer_review', 'written_submissions'],
            StakeholderType.MEDIA: ['press_releases', 'briefings', 'fact_sheets'],
            StakeholderType.AFFECTED_PARTY: ['one_on_one', 'site_visits', 'compensation_discussions'],
            StakeholderType.INDIGENOUS: ['traditional_meetings', 'cultural_protocols', 'translators']
        }
    
    def identify_stakeholders(
        self,
        project_data: Dict[str, Any],
        impact_radius_km: float = 5.0
    ) -> List[Stakeholder]:
        """
        Identify project stakeholders systematically.
        
        Args:
            project_data: Project information
            impact_radius_km: Radius for affected parties
            
        Returns:
            List of identified stakeholders
        """
        stakeholders = []
        
        # 1. Government stakeholders
        gov_stakeholders = self._identify_government_stakeholders(
            project_data.get('location', 'UAE')
        )
        stakeholders.extend(gov_stakeholders)
        
        # 2. Affected communities
        if 'sensitive_receptors' in project_data:
            community_stakeholders = self._identify_community_stakeholders(
                project_data['sensitive_receptors'],
                project_data.get('project_boundary')
            )
            stakeholders.extend(community_stakeholders)
        
        # 3. NGOs and civil society
        ngo_stakeholders = self._identify_ngo_stakeholders(
            project_data.get('impact_types', []),
            project_data.get('location', 'UAE')
        )
        stakeholders.extend(ngo_stakeholders)
        
        # 4. Business stakeholders
        business_stakeholders = self._identify_business_stakeholders(
            project_data.get('project_type'),
            project_data.get('location', 'UAE')
        )
        stakeholders.extend(business_stakeholders)
        
        # 5. Technical experts
        expert_stakeholders = self._identify_technical_experts(
            project_data.get('impact_types', [])
        )
        stakeholders.extend(expert_stakeholders)
        
        # Assign IDs and analyze influence/interest
        for i, stakeholder in enumerate(stakeholders):
            stakeholder.stakeholder_id = f"SH_{i+1:04d}"
            # Analyze influence and interest
            influence, interest = self._analyze_stakeholder_power(stakeholder)
            stakeholder.influence_level = influence
            stakeholder.interest_level = interest
            stakeholder.engagement_level = self._determine_engagement_level(
                influence, interest
            )
        
        return stakeholders
    
    def create_consultation_plan(
        self,
        project_data: Dict[str, Any],
        stakeholders: List[Stakeholder],
        project_duration_months: int
    ) -> ConsultationPlan:
        """
        Create comprehensive consultation plan.
        
        Args:
            project_data: Project information
            stakeholders: Identified stakeholders
            project_duration_months: Project duration
            
        Returns:
            Consultation plan
        """
        location = project_data.get('location', 'UAE')
        requirements = self.regulatory_requirements.get(location, self.regulatory_requirements['UAE'])
        
        # Define consultation phases
        phases = [
            {
                'phase': 'Scoping',
                'duration_days': 30,
                'objectives': [
                    'Introduce project to stakeholders',
                    'Identify key concerns and issues',
                    'Define scope of assessment'
                ],
                'activities': [
                    'Stakeholder mapping workshop',
                    'Initial public meeting',
                    'Online survey launch',
                    'One-on-one meetings with key stakeholders'
                ]
            },
            {
                'phase': 'Impact Assessment',
                'duration_days': 60,
                'objectives': [
                    'Share preliminary findings',
                    'Gather feedback on impacts',
                    'Discuss mitigation options'
                ],
                'activities': [
                    'Technical workshops',
                    'Focus group discussions',
                    'Site visits with community',
                    'Online consultation portal'
                ]
            },
            {
                'phase': 'Draft EIA Review',
                'duration_days': requirements['public_consultation_period'],
                'objectives': [
                    'Present draft EIA',
                    'Collect formal comments',
                    'Address concerns'
                ],
                'activities': [
                    'Public hearing',
                    'Written comment period',
                    'Response preparation',
                    'Final stakeholder meetings'
                ]
            },
            {
                'phase': 'Implementation',
                'duration_days': project_duration_months * 30,
                'objectives': [
                    'Ongoing engagement',
                    'Monitor compliance',
                    'Address emerging issues'
                ],
                'activities': [
                    'Regular update meetings',
                    'Grievance mechanism operation',
                    'Performance reporting',
                    'Adaptive management'
                ]
            }
        ]
        
        # Create timeline
        start_date = datetime.now()
        timeline = {}
        current_date = start_date
        
        for phase in phases:
            phase_name = phase['phase']
            timeline[f"{phase_name}_start"] = current_date
            current_date += timedelta(days=phase['duration_days'])
            timeline[f"{phase_name}_end"] = current_date
        
        # Determine methods based on stakeholder types
        methods = set()
        for stakeholder in stakeholders:
            methods.update(self.engagement_methods.get(
                stakeholder.stakeholder_type,
                ['meetings', 'written_communication']
            ))
        
        # Calculate resources
        resources = {
            'personnel': {
                'consultation_manager': 1,
                'facilitators': 2,
                'translators': 2,
                'administrative_support': 1
            },
            'venues': [
                'Community center for public meetings',
                'Meeting rooms for focus groups',
                'Online platform for virtual consultations'
            ],
            'materials': [
                'Project fact sheets (AR/EN)',
                'EIA summary documents',
                'Comment forms',
                'Presentation materials',
                'Website/portal'
            ],
            'equipment': [
                'Audio/video recording',
                'Projection equipment',
                'Translation equipment',
                'Online meeting platform'
            ]
        }
        
        # Success metrics
        metrics = [
            f"Minimum {requirements['public_consultation_period']} days public review",
            "80% of identified stakeholders engaged",
            "All comments responded to within timeframe",
            "Zero legitimate grievances unresolved",
            "Positive media coverage",
            "Regulatory approval obtained"
        ]
        
        # Risk mitigation
        risks = {
            'Low participation': 'Multiple engagement channels, convenient timing',
            'Language barriers': 'Professional translation, visual materials',
            'Misinformation': 'Proactive communication, fact sheets',
            'Opposition groups': 'Early engagement, transparent process',
            'COVID restrictions': 'Online alternatives, safety protocols',
            'Cultural sensitivities': 'Local facilitators, appropriate venues'
        }
        
        plan = ConsultationPlan(
            plan_id=f"CP_{project_data.get('project_id', 0)}_{datetime.now().strftime('%Y%m%d')}",
            project_id=project_data.get('project_id', 0),
            phases=phases,
            timeline=timeline,
            objectives=[
                'Ensure regulatory compliance',
                'Build stakeholder trust and support',
                'Identify and address all concerns',
                'Improve project design through feedback',
                'Establish ongoing engagement framework'
            ],
            target_stakeholders=[s.stakeholder_id for s in stakeholders],
            methods=list(methods),
            resources_required=resources,
            success_metrics=metrics,
            risk_mitigation=risks,
            budget=self._estimate_consultation_budget(len(stakeholders), project_duration_months),
            regulatory_requirements=[
                f"{location} Federal EIA requirements",
                f"Minimum {requirements['public_consultation_period']} days public review",
                f"{requirements['notice_period']} days advance notice for meetings",
                "Arabic and English documentation required"
            ],
            cultural_considerations=[
                'Prayer time considerations for meetings',
                'Gender-separated sessions if requested',
                'Ramadan timing adjustments',
                'Weekend is Friday-Saturday',
                'Respect for local customs and hierarchy'
            ],
            created_date=datetime.now()
        )
        
        return plan
    
    def record_comment(
        self,
        stakeholder_id: str,
        comment_text: str,
        submission_method: str = "online",
        attachments: Optional[List[str]] = None
    ) -> Comment:
        """
        Record stakeholder comment or feedback.
        
        Args:
            stakeholder_id: ID of stakeholder
            comment_text: Comment text
            submission_method: How comment was submitted
            attachments: Any attached files
            
        Returns:
            Comment record
        """
        # Analyze comment
        category = self._categorize_comment(comment_text)
        impact_area = self._identify_impact_area(comment_text)
        sentiment = self._analyze_sentiment(comment_text)
        priority = self._assess_priority(comment_text, sentiment)
        
        comment = Comment(
            comment_id=f"COM_{datetime.now().strftime('%Y%m%d%H%M%S')}_{stakeholder_id[-4:]}",
            stakeholder_id=stakeholder_id,
            submission_date=datetime.now(),
            comment_text=comment_text,
            topic_category=category,
            impact_area=impact_area,
            sentiment=sentiment,
            priority=priority,
            status=CommentStatus.RECEIVED,
            attachments=attachments or [],
            metadata={
                'submission_method': submission_method,
                'word_count': len(comment_text.split()),
                'language_detected': self._detect_language(comment_text)
            }
        )
        
        return comment
    
    def process_comments(
        self,
        comments: List[Comment],
        eia_sections: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Process and analyze all comments.
        
        Args:
            comments: List of comments
            eia_sections: EIA document sections
            
        Returns:
            Analysis dataframe
        """
        # Group comments by category and impact area
        analysis = defaultdict(lambda: {
            'count': 0,
            'sentiments': {'positive': 0, 'negative': 0, 'neutral': 0},
            'priorities': {'low': 0, 'medium': 0, 'high': 0, 'critical': 0},
            'key_concerns': [],
            'suggested_responses': []
        })
        
        for comment in comments:
            key = f"{comment.topic_category}_{comment.impact_area}"
            analysis[key]['count'] += 1
            analysis[key]['sentiments'][comment.sentiment] += 1
            analysis[key]['priorities'][comment.priority] += 1
            
            # Extract key concerns
            if comment.priority in ['high', 'critical']:
                analysis[key]['key_concerns'].append(comment.comment_text[:200])
            
            # Generate suggested response
            response = self._generate_response_template(comment)
            analysis[key]['suggested_responses'].append(response)
        
        # Convert to dataframe
        rows = []
        for key, data in analysis.items():
            category, impact = key.split('_', 1)
            rows.append({
                'Category': category,
                'Impact Area': impact,
                'Total Comments': data['count'],
                'Positive': data['sentiments']['positive'],
                'Negative': data['sentiments']['negative'],
                'Neutral': data['sentiments']['neutral'],
                'Critical Priority': data['priorities']['critical'],
                'High Priority': data['priorities']['high'],
                'Response Rate Required': 'Immediate' if data['priorities']['critical'] > 0 else 'Standard'
            })
        
        df = pd.DataFrame(rows)
        
        # Sort by priority
        df['Priority Score'] = df['Critical Priority'] * 4 + df['High Priority'] * 2 + df['Negative']
        df = df.sort_values('Priority Score', ascending=False)
        
        return df
    
    def generate_response_matrix(
        self,
        comments: List[Comment],
        project_data: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        Generate comment-response matrix.
        
        Args:
            comments: List of comments
            project_data: Project information
            
        Returns:
            Response matrix dataframe
        """
        matrix_data = []
        
        for comment in comments:
            # Generate response
            if comment.response_text:
                response = comment.response_text
            else:
                response = self._generate_response_template(comment)
            
            # Determine actions
            actions = self._determine_required_actions(comment, project_data)
            
            # EIA section reference
            section = self._find_relevant_eia_section(comment.comment_text)
            
            matrix_data.append({
                'Comment ID': comment.comment_id,
                'Stakeholder': comment.stakeholder_id,
                'Date': comment.submission_date.strftime('%Y-%m-%d'),
                'Category': comment.topic_category,
                'Comment Summary': comment.comment_text[:200] + '...' if len(comment.comment_text) > 200 else comment.comment_text,
                'Response': response,
                'Actions Required': ', '.join(actions),
                'EIA Section': section,
                'Status': comment.status.value,
                'Priority': comment.priority
            })
        
        df = pd.DataFrame(matrix_data)
        
        # Sort by priority and date
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        df['Priority_Rank'] = df['Priority'].map(priority_order)
        df = df.sort_values(['Priority_Rank', 'Date'])
        df = df.drop('Priority_Rank', axis=1)
        
        return df
    
    def record_meeting(
        self,
        meeting_type: MeetingType,
        title: str,
        attendee_ids: List[str],
        agenda: List[str],
        minutes: str,
        decisions: List[str],
        action_items: List[Dict[str, Any]]
    ) -> Meeting:
        """
        Record stakeholder meeting.
        
        Args:
            meeting_type: Type of meeting
            title: Meeting title
            attendee_ids: List of attendee stakeholder IDs
            agenda: Meeting agenda items
            minutes: Meeting minutes
            decisions: Decisions made
            action_items: Action items with assignees and deadlines
            
        Returns:
            Meeting record
        """
        meeting = Meeting(
            meeting_id=f"MTG_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            meeting_type=meeting_type,
            title=title,
            date=datetime.now(),
            location="To be specified",
            duration_hours=2.0,  # Default
            facilitator="To be specified",
            attendees=attendee_ids,
            agenda=agenda,
            minutes=minutes,
            decisions=decisions,
            action_items=action_items,
            materials_presented=[],
            issues_raised=[],
            commitments_made=[],
            follow_up_required=len(action_items) > 0
        )
        
        return meeting
    
    def generate_engagement_report(
        self,
        stakeholders: List[Stakeholder],
        comments: List[Comment],
        meetings: List[Meeting],
        consultation_plan: ConsultationPlan
    ) -> Dict[str, Any]:
        """
        Generate comprehensive engagement report.
        
        Args:
            stakeholders: List of stakeholders
            comments: List of comments
            meetings: List of meetings
            consultation_plan: Consultation plan
            
        Returns:
            Engagement report
        """
        # Analyze engagement metrics
        total_stakeholders = len(stakeholders)
        engaged_stakeholders = len(set(
            [c.stakeholder_id for c in comments] +
            [a for m in meetings for a in m.attendees]
        ))
        
        # Comment analysis
        comment_stats = {
            'total': len(comments),
            'by_status': {},
            'by_priority': {},
            'by_category': {},
            'response_rate': 0
        }
        
        for comment in comments:
            # Status
            status = comment.status.value
            comment_stats['by_status'][status] = comment_stats['by_status'].get(status, 0) + 1
            
            # Priority
            priority = comment.priority
            comment_stats['by_priority'][priority] = comment_stats['by_priority'].get(priority, 0) + 1
            
            # Category
            category = comment.topic_category
            comment_stats['by_category'][category] = comment_stats['by_category'].get(category, 0) + 1
        
        # Calculate response rate
        addressed = comment_stats['by_status'].get('addressed', 0) + comment_stats['by_status'].get('incorporated', 0)
        if comment_stats['total'] > 0:
            comment_stats['response_rate'] = (addressed / comment_stats['total']) * 100
        
        # Meeting analysis
        meeting_stats = {
            'total': len(meetings),
            'by_type': {},
            'total_attendees': 0,
            'average_attendance': 0,
            'total_decisions': 0,
            'total_action_items': 0
        }
        
        for meeting in meetings:
            # Type
            mtype = meeting.meeting_type.value
            meeting_stats['by_type'][mtype] = meeting_stats['by_type'].get(mtype, 0) + 1
            
            # Attendance
            meeting_stats['total_attendees'] += len(meeting.attendees)
            
            # Decisions and actions
            meeting_stats['total_decisions'] += len(meeting.decisions)
            meeting_stats['total_action_items'] += len(meeting.action_items)
        
        if meeting_stats['total'] > 0:
            meeting_stats['average_attendance'] = meeting_stats['total_attendees'] / meeting_stats['total']
        
        # Stakeholder analysis
        stakeholder_stats = {
            'by_type': {},
            'by_engagement_level': {},
            'high_influence': 0,
            'high_interest': 0
        }
        
        for stakeholder in stakeholders:
            # Type
            stype = stakeholder.stakeholder_type.value
            stakeholder_stats['by_type'][stype] = stakeholder_stats['by_type'].get(stype, 0) + 1
            
            # Engagement level
            level = stakeholder.engagement_level.value
            stakeholder_stats['by_engagement_level'][level] = stakeholder_stats['by_engagement_level'].get(level, 0) + 1
            
            # Influence/interest
            if stakeholder.influence_level == 'high':
                stakeholder_stats['high_influence'] += 1
            if stakeholder.interest_level == 'high':
                stakeholder_stats['high_interest'] += 1
        
        # Generate report
        report = {
            'executive_summary': {
                'total_stakeholders_identified': total_stakeholders,
                'stakeholders_engaged': engaged_stakeholders,
                'engagement_rate': (engaged_stakeholders / total_stakeholders * 100) if total_stakeholders > 0 else 0,
                'total_comments_received': comment_stats['total'],
                'comment_response_rate': comment_stats['response_rate'],
                'total_meetings_held': meeting_stats['total'],
                'key_concerns_addressed': comment_stats['by_status'].get('addressed', 0) + comment_stats['by_status'].get('incorporated', 0)
            },
            'stakeholder_analysis': stakeholder_stats,
            'comment_analysis': comment_stats,
            'meeting_analysis': meeting_stats,
            'consultation_phases': {
                'completed': self._get_completed_phases(consultation_plan),
                'current': self._get_current_phase(consultation_plan),
                'upcoming': self._get_upcoming_phases(consultation_plan)
            },
            'key_issues': self._identify_key_issues(comments),
            'recommendations': self._generate_recommendations(stakeholders, comments, meetings),
            'compliance_status': {
                'regulatory_requirements_met': True,  # Simplified
                'public_consultation_period': 'Compliant',
                'notification_requirements': 'Compliant',
                'language_requirements': 'Compliant'
            },
            'next_steps': self._identify_next_steps(consultation_plan, comments, meetings),
            'appendices': [
                'Stakeholder Register',
                'Comment-Response Matrix',
                'Meeting Minutes',
                'Consultation Materials'
            ]
        }
        
        return report
    
    def create_public_disclosure_package(
        self,
        project_data: Dict[str, Any],
        eia_summary: str,
        consultation_plan: ConsultationPlan,
        languages: List[str] = ['en', 'ar']
    ) -> Dict[str, Any]:
        """
        Create public disclosure package.
        
        Args:
            project_data: Project information
            eia_summary: Non-technical EIA summary
            consultation_plan: Consultation plan
            languages: Languages for materials
            
        Returns:
            Disclosure package contents
        """
        package = {
            'project_fact_sheet': {
                'title': project_data.get('name', 'Project'),
                'location': project_data.get('location', ''),
                'developer': project_data.get('developer', ''),
                'project_type': project_data.get('type', ''),
                'key_benefits': [
                    'Economic development',
                    'Job creation',
                    'Infrastructure improvement'
                ],
                'potential_impacts': [
                    'Temporary construction impacts',
                    'Traffic changes',
                    'Environmental considerations'
                ],
                'mitigation_commitment': 'All impacts will be managed according to international best practices',
                'timeline': project_data.get('timeline', {}),
                'contact_information': {
                    'project_hotline': '+971-X-XXX-XXXX',
                    'email': 'project@example.com',
                    'website': 'www.projecteia.com',
                    'office_address': 'Project Information Center'
                }
            },
            'eia_summary': {
                'executive_summary': eia_summary,
                'key_findings': [],
                'proposed_mitigation': [],
                'monitoring_commitments': []
            },
            'consultation_information': {
                'how_to_participate': [
                    'Attend public meetings',
                    'Submit written comments',
                    'Visit project website',
                    'Call project hotline',
                    'Visit information center'
                ],
                'upcoming_events': self._format_upcoming_events(consultation_plan),
                'comment_period': {
                    'start_date': consultation_plan.timeline.get('Draft EIA Review_start', datetime.now()),
                    'end_date': consultation_plan.timeline.get('Draft EIA Review_end', datetime.now() + timedelta(days=30)),
                    'submission_methods': [
                        'Online form at website',
                        'Email to project@example.com',
                        'Written letter to project office',
                        'Comment box at public locations',
                        'Verbal comments at public meetings'
                    ]
                },
                'languages_available': languages,
                'special_accommodations': 'Translation services and accessibility support available upon request'
            },
            'frequently_asked_questions': self._generate_faqs(project_data),
            'grievance_mechanism': {
                'how_to_submit': [
                    'Online grievance form',
                    'Grievance boxes at public locations',
                    'Direct submission to CLO',
                    'Through community representatives'
                ],
                'process': [
                    'Receipt and registration within 24 hours',
                    'Initial response within 7 days',
                    'Investigation and resolution within 30 days',
                    'Appeal process available'
                ],
                'contact': {
                    'community_liaison_officer': 'Name TBD',
                    'phone': '+971-X-XXX-XXXX',
                    'email': 'grievance@project.com'
                }
            },
            'visual_materials': [
                'Project location map',
                'Project layout diagram',
                'Environmental management flowchart',
                'Consultation process timeline'
            ],
            'distribution_plan': {
                'locations': [
                    'Municipality offices',
                    'Community centers',
                    'Public libraries',
                    'Mosques',
                    'Schools',
                    'Healthcare facilities',
                    'Local businesses'
                ],
                'digital_channels': [
                    'Project website',
                    'Social media',
                    'WhatsApp broadcast',
                    'Email newsletters'
                ],
                'media_outlets': [
                    'Local newspapers',
                    'Radio stations',
                    'Community bulletins'
                ]
            }
        }
        
        return package
    
    def _identify_government_stakeholders(self, location: str) -> List[Stakeholder]:
        """Identify government stakeholders based on location."""
        stakeholders = []
        
        # Common government stakeholders
        if location == 'UAE':
            agencies = [
                ('Ministry of Climate Change and Environment', 'Federal environmental regulator'),
                ('Environment Agency - Abu Dhabi', 'Local environmental regulator'),
                ('Dubai Municipality', 'Local planning authority'),
                ('Roads and Transport Authority', 'Transport infrastructure'),
                ('DEWA/ADWEA', 'Utilities provider'),
                ('Civil Defence', 'Safety and emergency response')
            ]
        else:  # KSA
            agencies = [
                ('Ministry of Environment, Water and Agriculture', 'Federal environmental regulator'),
                ('National Center for Environmental Compliance', 'Compliance monitoring'),
                ('Saudi Authority for Industrial Cities', 'Industrial development'),
                ('Ministry of Municipal and Rural Affairs', 'Local planning'),
                ('Saudi Electricity Company', 'Utilities provider'),
                ('General Directorate of Civil Defense', 'Safety and emergency response')
            ]
        
        for name, position in agencies:
            stakeholder = Stakeholder(
                stakeholder_id='',  # Will be assigned later
                name=name,
                stakeholder_type=StakeholderType.GOVERNMENT,
                organization=name,
                position=position,
                engagement_level=EngagementLevel.COLLABORATE,
                influence_level='high',
                interest_level='high',
                preferred_contact_method='formal_letter'
            )
            stakeholders.append(stakeholder)
        
        return stakeholders
    
    def _identify_community_stakeholders(
        self,
        sensitive_receptors: List[Any],
        project_boundary: Any
    ) -> List[Stakeholder]:
        """Identify community stakeholders from sensitive receptors."""
        stakeholders = []
        
        # Group receptors by type
        receptor_groups = defaultdict(list)
        for receptor in sensitive_receptors:
            receptor_groups[receptor.receptor_type].append(receptor)
        
        # Create community representatives
        for receptor_type, receptors in receptor_groups.items():
            if receptor_type in ['residential', 'school', 'mosque']:
                # Create representative for each major cluster
                stakeholder = Stakeholder(
                    stakeholder_id='',
                    name=f"{receptor_type.title()} Community Representative",
                    stakeholder_type=StakeholderType.COMMUNITY,
                    organization=f"Local {receptor_type} community",
                    concerns=[
                        'Noise during construction',
                        'Air quality impacts',
                        'Traffic disruption',
                        'Property values'
                    ],
                    engagement_level=EngagementLevel.INVOLVE,
                    influence_level='medium',
                    interest_level='high'
                )
                stakeholders.append(stakeholder)
        
        return stakeholders
    
    def _identify_ngo_stakeholders(
        self,
        impact_types: List[str],
        location: str
    ) -> List[Stakeholder]:
        """Identify relevant NGOs based on impact types."""
        stakeholders = []
        
        # Environmental NGOs
        if any(impact in impact_types for impact in ['air', 'water', 'ecology', 'climate']):
            stakeholder = Stakeholder(
                stakeholder_id='',
                name='Emirates Environmental Group' if location == 'UAE' else 'Saudi Environmental Society',
                stakeholder_type=StakeholderType.NGO,
                organization='Environmental NGO',
                concerns=['Environmental protection', 'Sustainability', 'Compliance'],
                engagement_level=EngagementLevel.CONSULT,
                influence_level='medium',
                interest_level='high'
            )
            stakeholders.append(stakeholder)
        
        # Social/community NGOs
        if any(impact in impact_types for impact in ['social', 'displacement', 'livelihood']):
            stakeholder = Stakeholder(
                stakeholder_id='',
                name='Community Development Organization',
                stakeholder_type=StakeholderType.NGO,
                organization='Social NGO',
                concerns=['Community welfare', 'Social impacts', 'Vulnerable groups'],
                engagement_level=EngagementLevel.INVOLVE,
                influence_level='medium',
                interest_level='medium'
            )
            stakeholders.append(stakeholder)
        
        return stakeholders
    
    def _identify_business_stakeholders(
        self,
        project_type: str,
        location: str
    ) -> List[Stakeholder]:
        """Identify business stakeholders."""
        stakeholders = []
        
        # Local business associations
        stakeholder = Stakeholder(
            stakeholder_id='',
            name=f"{location} Chamber of Commerce",
            stakeholder_type=StakeholderType.BUSINESS,
            organization='Business Association',
            concerns=['Economic impacts', 'Business opportunities', 'Supply chain'],
            engagement_level=EngagementLevel.CONSULT,
            influence_level='medium',
            interest_level='medium'
        )
        stakeholders.append(stakeholder)
        
        return stakeholders
    
    def _identify_technical_experts(self, impact_types: List[str]) -> List[Stakeholder]:
        """Identify technical experts needed."""
        stakeholders = []
        
        expert_areas = {
            'air': 'Air Quality Expert',
            'water': 'Hydrologist',
            'noise': 'Acoustic Consultant',
            'ecology': 'Ecologist',
            'social': 'Social Impact Specialist',
            'heritage': 'Cultural Heritage Expert',
            'traffic': 'Traffic Engineer'
        }
        
        for impact in impact_types:
            if impact in expert_areas:
                stakeholder = Stakeholder(
                    stakeholder_id='',
                    name=expert_areas[impact],
                    stakeholder_type=StakeholderType.TECHNICAL_EXPERT,
                    position='Independent Expert',
                    engagement_level=EngagementLevel.CONSULT,
                    influence_level='low',
                    interest_level='medium'
                )
                stakeholders.append(stakeholder)
        
        return stakeholders
    
    def _analyze_stakeholder_power(
        self,
        stakeholder: Stakeholder
    ) -> Tuple[str, str]:
        """Analyze stakeholder influence and interest levels."""
        # Influence based on type and position
        if stakeholder.stakeholder_type == StakeholderType.GOVERNMENT:
            influence = 'high'
        elif stakeholder.stakeholder_type in [StakeholderType.AFFECTED_PARTY, StakeholderType.INDIGENOUS]:
            influence = 'high'  # Legal rights
        elif stakeholder.stakeholder_type == StakeholderType.MEDIA:
            influence = 'medium'
        else:
            influence = 'low'
        
        # Interest based on proximity and impacts
        if stakeholder.stakeholder_type in [StakeholderType.AFFECTED_PARTY, StakeholderType.COMMUNITY]:
            interest = 'high'
        elif stakeholder.stakeholder_type == StakeholderType.GOVERNMENT:
            interest = 'high'
        else:
            interest = 'medium'
        
        return influence, interest
    
    def _determine_engagement_level(
        self,
        influence: str,
        interest: str
    ) -> EngagementLevel:
        """Determine appropriate engagement level."""
        # Power-interest matrix
        if influence == 'high' and interest == 'high':
            return EngagementLevel.COLLABORATE
        elif influence == 'high' and interest in ['medium', 'low']:
            return EngagementLevel.CONSULT
        elif influence in ['medium', 'low'] and interest == 'high':
            return EngagementLevel.INVOLVE
        else:
            return EngagementLevel.INFORM
    
    def _estimate_consultation_budget(
        self,
        num_stakeholders: int,
        duration_months: int
    ) -> float:
        """Estimate consultation budget."""
        # Base costs
        personnel_cost = 25000 * duration_months  # Monthly team cost
        
        # Meeting costs
        public_meetings = 5000 * 4  # 4 major public meetings
        focus_groups = 2000 * 8  # 8 focus groups
        
        # Materials and translation
        materials_cost = 15000  # Design, printing, translation
        
        # Online platform
        digital_cost = 10000  # Website, portal, maintenance
        
        # Venue and logistics
        venue_cost = 3000 * duration_months
        
        # Contingency (20%)
        subtotal = personnel_cost + public_meetings + focus_groups + materials_cost + digital_cost + venue_cost
        total = subtotal * 1.2
        
        return total
    
    def _categorize_comment(self, comment_text: str) -> str:
        """Categorize comment based on content."""
        comment_lower = comment_text.lower()
        
        # Keywords for each category
        category_keywords = {
            'Air Quality': ['air', 'dust', 'emission', 'pollution', 'smell', 'odor'],
            'Water Resources': ['water', 'groundwater', 'drainage', 'flood', 'contamination'],
            'Noise and Vibration': ['noise', 'sound', 'vibration', 'quiet', 'loud'],
            'Traffic and Transportation': ['traffic', 'road', 'congestion', 'parking', 'access'],
            'Visual Impact': ['view', 'landscape', 'visual', 'aesthetic', 'ugly'],
            'Ecological Impact': ['wildlife', 'habitat', 'trees', 'vegetation', 'ecosystem'],
            'Social Impact': ['community', 'job', 'employment', 'displacement', 'culture'],
            'Economic Impact': ['cost', 'property', 'business', 'economy', 'value'],
            'Health and Safety': ['health', 'safety', 'accident', 'emergency', 'disease'],
            'Alternatives': ['alternative', 'option', 'instead', 'better way', 'different']
        }
        
        # Find best matching category
        max_score = 0
        best_category = 'General Concern'
        
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in comment_lower)
            if score > max_score:
                max_score = score
                best_category = category
        
        return best_category
    
    def _identify_impact_area(self, comment_text: str) -> str:
        """Identify primary impact area from comment."""
        comment_lower = comment_text.lower()
        
        impact_keywords = {
            'air': ['air', 'dust', 'emission', 'breathe'],
            'water': ['water', 'drain', 'flood', 'contaminate'],
            'noise': ['noise', 'sound', 'loud', 'quiet'],
            'traffic': ['traffic', 'road', 'drive', 'congestion'],
            'visual': ['view', 'look', 'ugly', 'aesthetic'],
            'ecology': ['animal', 'plant', 'tree', 'habitat'],
            'social': ['community', 'people', 'neighbor', 'family'],
            'economic': ['money', 'cost', 'job', 'business']
        }
        
        # Count keywords
        impact_scores = {}
        for impact, keywords in impact_keywords.items():
            impact_scores[impact] = sum(1 for keyword in keywords if keyword in comment_lower)
        
        # Return highest scoring impact
        if max(impact_scores.values()) > 0:
            return max(impact_scores, key=impact_scores.get)
        return 'general'
    
    def _analyze_sentiment(self, comment_text: str) -> str:
        """Analyze comment sentiment."""
        comment_lower = comment_text.lower()
        
        # Sentiment indicators
        positive_words = ['support', 'good', 'benefit', 'approve', 'positive', 'help', 'improve', 'excellent']
        negative_words = ['oppose', 'bad', 'concern', 'worry', 'negative', 'damage', 'destroy', 'terrible']
        
        positive_score = sum(1 for word in positive_words if word in comment_lower)
        negative_score = sum(1 for word in negative_words if word in comment_lower)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def _assess_priority(self, comment_text: str, sentiment: str) -> str:
        """Assess comment priority."""
        comment_lower = comment_text.lower()
        
        # Critical indicators
        critical_words = ['illegal', 'violation', 'death', 'catastrophe', 'court', 'sue', 'emergency']
        high_words = ['serious', 'major', 'significant', 'urgent', 'important', 'critical']
        
        if any(word in comment_lower for word in critical_words):
            return 'critical'
        elif any(word in comment_lower for word in high_words) or sentiment == 'negative':
            return 'high'
        elif sentiment == 'positive':
            return 'low'
        else:
            return 'medium'
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text (simplified)."""
        # Check for Arabic characters
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        
        if arabic_chars > len(text) * 0.3:
            return 'ar'
        else:
            return 'en'
    
    def _generate_response_template(self, comment: Comment) -> str:
        """Generate template response for comment."""
        templates = {
            'positive': "Thank you for your support of the project. {specific_response}",
            'negative': "We appreciate your concerns regarding {topic}. {specific_response} We are committed to addressing these issues through {mitigation}.",
            'neutral': "Thank you for your feedback on {topic}. {specific_response}"
        }
        
        base_template = templates.get(comment.sentiment, templates['neutral'])
        
        # Customize based on category
        specific_responses = {
            'Air Quality': "Air quality monitoring will be conducted throughout the project",
            'Noise and Vibration': "Noise levels will be controlled within regulatory limits",
            'Traffic and Transportation': "A traffic management plan will be implemented",
            'Social Impact': "Community concerns are a priority in our planning",
            'Environmental Impact': "Environmental protection measures will be strictly enforced"
        }
        
        specific = specific_responses.get(comment.topic_category, "Your input is valuable for project planning")
        
        mitigation_options = {
            'Air Quality': "dust suppression and emission controls",
            'Noise and Vibration': "noise barriers and time restrictions",
            'Traffic and Transportation': "alternative routes and peak hour management",
            'Social Impact': "community programs and local hiring",
            'Environmental Impact': "best practice environmental management"
        }
        
        mitigation = mitigation_options.get(comment.topic_category, "appropriate mitigation measures")
        
        response = base_template.format(
            topic=comment.topic_category.lower(),
            specific_response=specific,
            mitigation=mitigation
        )
        
        return response
    
    def _determine_required_actions(
        self,
        comment: Comment,
        project_data: Dict[str, Any]
    ) -> List[str]:
        """Determine actions required for comment."""
        actions = []
        
        # Priority-based actions
        if comment.priority == 'critical':
            actions.append("Immediate management review")
            actions.append("Legal consultation if needed")
        elif comment.priority == 'high':
            actions.append("Detailed technical response required")
            actions.append("Consider design modifications")
        
        # Category-based actions
        category_actions = {
            'Air Quality': ["Review air quality modeling", "Enhance dust control measures"],
            'Noise and Vibration': ["Update noise assessment", "Review construction schedule"],
            'Traffic and Transportation': ["Review traffic impact study", "Coordinate with authorities"],
            'Social Impact': ["Schedule community meeting", "Review social management plan"],
            'Alternatives': ["Document alternatives analysis", "Provide justification"]
        }
        
        if comment.topic_category in category_actions:
            actions.extend(category_actions[comment.topic_category])
        
        # Follow-up actions
        if comment.follow_up_required:
            actions.append("Schedule follow-up communication")
        
        return actions[:3]  # Limit to top 3 actions
    
    def _find_relevant_eia_section(self, comment_text: str) -> str:
        """Find relevant EIA section for comment."""
        # EIA section mapping
        section_keywords = {
            'Executive Summary': ['summary', 'overview', 'general'],
            'Project Description': ['project', 'construction', 'design', 'location'],
            'Legal Framework': ['law', 'regulation', 'permit', 'compliance'],
            'Baseline Conditions': ['existing', 'current', 'baseline', 'present'],
            'Impact Assessment': ['impact', 'effect', 'change', 'consequence'],
            'Mitigation Measures': ['mitigation', 'reduce', 'prevent', 'control'],
            'Environmental Management Plan': ['management', 'monitoring', 'plan'],
            'Alternatives Analysis': ['alternative', 'option', 'comparison'],
            'Stakeholder Engagement': ['consultation', 'community', 'public']
        }
        
        comment_lower = comment_text.lower()
        
        # Find best matching section
        best_section = 'General'
        max_score = 0
        
        for section, keywords in section_keywords.items():
            score = sum(1 for keyword in keywords if keyword in comment_lower)
            if score > max_score:
                max_score = score
                best_section = section
        
        return best_section
    
    def _get_completed_phases(self, plan: ConsultationPlan) -> List[str]:
        """Get completed consultation phases."""
        completed = []
        current_date = datetime.now()
        
        for phase in plan.phases:
            phase_name = phase['phase']
            end_date = plan.timeline.get(f"{phase_name}_end")
            if end_date and end_date < current_date:
                completed.append(phase_name)
        
        return completed
    
    def _get_current_phase(self, plan: ConsultationPlan) -> Optional[str]:
        """Get current consultation phase."""
        current_date = datetime.now()
        
        for phase in plan.phases:
            phase_name = phase['phase']
            start_date = plan.timeline.get(f"{phase_name}_start")
            end_date = plan.timeline.get(f"{phase_name}_end")
            
            if start_date and end_date:
                if start_date <= current_date <= end_date:
                    return phase_name
        
        return None
    
    def _get_upcoming_phases(self, plan: ConsultationPlan) -> List[str]:
        """Get upcoming consultation phases."""
        upcoming = []
        current_date = datetime.now()
        
        for phase in plan.phases:
            phase_name = phase['phase']
            start_date = plan.timeline.get(f"{phase_name}_start")
            if start_date and start_date > current_date:
                upcoming.append(phase_name)
        
        return upcoming
    
    def _identify_key_issues(self, comments: List[Comment]) -> List[Dict[str, Any]]:
        """Identify key issues from comments."""
        # Group by category and priority
        issue_groups = defaultdict(lambda: {'count': 0, 'examples': []})
        
        for comment in comments:
            if comment.priority in ['high', 'critical']:
                key = f"{comment.topic_category}_{comment.impact_area}"
                issue_groups[key]['count'] += 1
                if len(issue_groups[key]['examples']) < 3:
                    issue_groups[key]['examples'].append(comment.comment_text[:100])
        
        # Convert to list of key issues
        key_issues = []
        for key, data in issue_groups.items():
            if data['count'] >= 3:  # Threshold for key issue
                category, impact = key.split('_', 1)
                key_issues.append({
                    'category': category,
                    'impact_area': impact,
                    'frequency': data['count'],
                    'examples': data['examples'],
                    'significance': 'High' if data['count'] > 10 else 'Medium'
                })
        
        # Sort by frequency
        key_issues.sort(key=lambda x: x['frequency'], reverse=True)
        
        return key_issues[:10]  # Top 10 issues
    
    def _generate_recommendations(
        self,
        stakeholders: List[Stakeholder],
        comments: List[Comment],
        meetings: List[Meeting]
    ) -> List[str]:
        """Generate recommendations for improving engagement."""
        recommendations = []
        
        # Analyze engagement gaps
        engaged_ids = set([c.stakeholder_id for c in comments] + 
                         [a for m in meetings for a in m.attendees])
        
        # Check for unengaged high-priority stakeholders
        unengaged_high = [s for s in stakeholders 
                         if s.stakeholder_id not in engaged_ids 
                         and s.influence_level == 'high']
        
        if unengaged_high:
            recommendations.append(
                f"Priority engagement needed with {len(unengaged_high)} high-influence stakeholders"
            )
        
        # Check response rate
        unaddressed = [c for c in comments if c.status == CommentStatus.RECEIVED]
        if len(unaddressed) > 0:
            recommendations.append(
                f"Address {len(unaddressed)} pending comments to improve response rate"
            )
        
        # Check for critical issues
        critical_comments = [c for c in comments if c.priority == 'critical']
        if critical_comments:
            recommendations.append(
                "Immediate action required on critical stakeholder concerns"
            )
        
        # Engagement method recommendations
        low_attendance = [m for m in meetings if len(m.attendees) < 10]
        if len(low_attendance) > len(meetings) * 0.3:
            recommendations.append(
                "Consider alternative engagement methods to improve participation"
            )
        
        # Language considerations
        ar_comments = [c for c in comments if c.metadata.get('language_detected') == 'ar']
        if len(ar_comments) < len(comments) * 0.3:
            recommendations.append(
                "Increase Arabic language outreach to ensure inclusive engagement"
            )
        
        # Follow-up recommendations
        pending_actions = sum(len(m.action_items) for m in meetings)
        if pending_actions > 20:
            recommendations.append(
                f"Prioritize completion of {pending_actions} pending action items"
            )
        
        return recommendations
    
    def _identify_next_steps(
        self,
        plan: ConsultationPlan,
        comments: List[Comment],
        meetings: List[Meeting]
    ) -> List[str]:
        """Identify immediate next steps."""
        next_steps = []
        
        # Current phase actions
        current_phase = self._get_current_phase(plan)
        if current_phase:
            phase_data = next((p for p in plan.phases if p['phase'] == current_phase), None)
            if phase_data:
                remaining_activities = [a for a in phase_data['activities'] 
                                      if not self._is_activity_complete(a, meetings)]
                if remaining_activities:
                    next_steps.append(f"Complete {current_phase} phase activities: {', '.join(remaining_activities[:2])}")
        
        # Comment responses
        pending_responses = [c for c in comments if not c.response_text]
        if pending_responses:
            next_steps.append(f"Prepare responses for {len(pending_responses)} comments")
        
        # Upcoming meetings
        next_steps.append("Schedule next round of stakeholder meetings")
        
        # Reporting
        next_steps.append("Update stakeholder engagement tracking system")
        
        # Regulatory submissions
        next_steps.append("Prepare regulatory compliance documentation")
        
        return next_steps[:5]  # Top 5 next steps
    
    def _is_activity_complete(self, activity: str, meetings: List[Meeting]) -> bool:
        """Check if consultation activity is complete."""
        # Simplified check based on meeting titles
        activity_lower = activity.lower()
        for meeting in meetings:
            if any(word in meeting.title.lower() for word in activity_lower.split()):
                return True
        return False
    
    def _format_upcoming_events(self, plan: ConsultationPlan) -> List[Dict[str, Any]]:
        """Format upcoming consultation events."""
        events = []
        current_phase = self._get_current_phase(plan)
        
        if current_phase:
            # Mock upcoming events based on phase
            if current_phase == 'Draft EIA Review':
                events.extend([
                    {
                        'event': 'Public Hearing',
                        'date': datetime.now() + timedelta(days=7),
                        'time': '18:00-20:00',
                        'location': 'Community Center, Main Hall',
                        'language': 'Arabic/English with translation',
                        'registration': 'Not required'
                    },
                    {
                        'event': 'Focus Group - Residential Communities',
                        'date': datetime.now() + timedelta(days=10),
                        'time': '10:00-12:00',
                        'location': 'Project Information Center',
                        'language': 'Arabic/English',
                        'registration': 'Required - call hotline'
                    }
                ])
        
        return events
    
    def _generate_faqs(self, project_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate frequently asked questions."""
        faqs = [
            {
                'question': 'What is an Environmental Impact Assessment (EIA)?',
                'answer': 'An EIA is a study to identify and evaluate potential environmental impacts of a proposed project and develop measures to avoid or minimize negative effects.'
            },
            {
                'question': 'How can I participate in the consultation process?',
                'answer': 'You can participate by attending public meetings, submitting written comments, visiting our website, or contacting the project team directly.'
            },
            {
                'question': 'Will my comments make a difference?',
                'answer': 'Yes! All comments are carefully reviewed and considered. Many project improvements come from stakeholder feedback.'
            },
            {
                'question': 'What languages are available for consultation?',
                'answer': 'All materials and meetings are available in Arabic and English. Translation services are provided.'
            },
            {
                'question': 'How will construction affect my daily life?',
                'answer': 'Temporary impacts may include noise and traffic. We will implement strict controls and inform you in advance of any disruptions.'
            },
            {
                'question': 'What environmental protection measures will be implemented?',
                'answer': 'Comprehensive measures include dust control, noise barriers, water protection, and ecological monitoring throughout the project.'
            },
            {
                'question': 'How can I report a concern during construction?',
                'answer': 'Use our 24/7 hotline, submit through the grievance system, or contact the Community Liaison Officer directly.'
            },
            {
                'question': 'Where can I see the full EIA report?',
                'answer': 'The full report is available at public locations listed on our website and can be downloaded from our project portal.'
            }
        ]
        
        return faqs