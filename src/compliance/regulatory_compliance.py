"""
Regulatory Compliance Module
UAE and KSA environmental regulation compliance checking

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance status categories."""
    COMPLIANT = "Compliant"
    NON_COMPLIANT = "Non-Compliant"
    CONDITIONAL = "Conditional"
    PENDING = "Pending Review"


class Jurisdiction(Enum):
    """Supported jurisdictions."""
    UAE_FEDERAL = "UAE Federal"
    DUBAI = "Dubai"
    ABU_DHABI = "Abu Dhabi"
    SHARJAH = "Sharjah"
    KSA_NATIONAL = "KSA National"
    RIYADH = "Riyadh"
    JEDDAH = "Jeddah"
    NEOM = "NEOM"


@dataclass
class Regulation:
    """Environmental regulation definition."""
    id: str
    name: str
    jurisdiction: Jurisdiction
    category: str
    requirement: str
    threshold: Optional[Dict] = None
    penalty: Optional[str] = None
    reference: Optional[str] = None


@dataclass
class ComplianceCheck:
    """Compliance check result."""
    regulation_id: str
    regulation_name: str
    status: ComplianceStatus
    actual_value: Optional[float] = None
    required_value: Optional[float] = None
    deviation: Optional[float] = None
    recommendation: Optional[str] = None
    evidence_required: Optional[List[str]] = None


@dataclass
class ComplianceReport:
    """Overall compliance assessment report."""
    project_name: str
    jurisdiction: Jurisdiction
    assessment_date: datetime
    overall_status: ComplianceStatus
    compliance_percentage: float
    checks: List[ComplianceCheck]
    required_permits: List[str]
    action_items: List[str]


class RegulatoryCompliance:
    """
    Comprehensive regulatory compliance checker for UAE and KSA.
    Covers environmental regulations for construction projects.
    """

    def __init__(self):
        """Initialize compliance checker with regulations database."""
        self.regulations = self._load_regulations()
        self.permit_requirements = self._load_permit_requirements()

    def _load_regulations(self) -> Dict[str, List[Regulation]]:
        """Load environmental regulations for each jurisdiction."""
        regulations = {
            # UAE Federal Regulations
            Jurisdiction.UAE_FEDERAL: [
                Regulation(
                    id="UAE-FED-001",
                    name="Federal Law No. 24 - Environmental Protection",
                    jurisdiction=Jurisdiction.UAE_FEDERAL,
                    category="General",
                    requirement="Conduct EIA for projects likely to affect environment",
                    reference="Federal Law No. 24 of 1999"
                ),
                Regulation(
                    id="UAE-FED-002",
                    name="Air Quality Standards",
                    jurisdiction=Jurisdiction.UAE_FEDERAL,
                    category="Air Quality",
                    requirement="PM10 24-hour average not to exceed 150 μg/m³",
                    threshold={"pm10_24hr": 150, "pm25_24hr": 65},
                    penalty="Fine up to AED 500,000",
                    reference="Cabinet Decision No. 37 of 2006"
                ),
                Regulation(
                    id="UAE-FED-003",
                    name="Noise Level Limits",
                    jurisdiction=Jurisdiction.UAE_FEDERAL,
                    category="Noise",
                    requirement="Construction noise limit 65 dB(A) in residential areas (day)",
                    threshold={"noise_residential_day": 65, "noise_residential_night": 55},
                    penalty="Stop work order possible"
                ),
                Regulation(
                    id="UAE-FED-004",
                    name="Waste Management",
                    jurisdiction=Jurisdiction.UAE_FEDERAL,
                    category="Waste",
                    requirement="Proper segregation and disposal of construction waste",
                    reference="Federal Law No. 12 of 2018"
                ),
            ],
            
            # Dubai Specific Regulations
            Jurisdiction.DUBAI: [
                Regulation(
                    id="DXB-001",
                    name="Dubai Municipality Environmental Regulations",
                    jurisdiction=Jurisdiction.DUBAI,
                    category="General",
                    requirement="Environmental permit required for all construction projects",
                    reference="Local Order No. 61 of 1991"
                ),
                Regulation(
                    id="DXB-002",
                    name="Green Building Regulations",
                    jurisdiction=Jurisdiction.DUBAI,
                    category="Sustainability",
                    requirement="Comply with Al Sa'fat green building rating system",
                    reference="Dubai Municipality Circular No. 198"
                ),
                Regulation(
                    id="DXB-003",
                    name="Construction Site Management",
                    jurisdiction=Jurisdiction.DUBAI,
                    category="Site Management",
                    requirement="Site hoarding, dust control, and waste management plan required",
                    reference="TRAKHEES Guidelines"
                ),
            ],
            
            # Abu Dhabi Specific Regulations
            Jurisdiction.ABU_DHABI: [
                Regulation(
                    id="AUH-001",
                    name="EAD Environmental Regulations",
                    jurisdiction=Jurisdiction.ABU_DHABI,
                    category="General",
                    requirement="EIA required for projects as per EAD guidelines",
                    reference="EAD Technical Guidance Document"
                ),
                Regulation(
                    id="AUH-002",
                    name="Estidama Pearl Rating",
                    jurisdiction=Jurisdiction.ABU_DHABI,
                    category="Sustainability",
                    requirement="Minimum 1 Pearl rating for all new buildings",
                    reference="Estidama PBRS"
                ),
                Regulation(
                    id="AUH-003",
                    name="Construction Environmental Management Plan",
                    jurisdiction=Jurisdiction.ABU_DHABI,
                    category="Management",
                    requirement="CEMP required and must be approved by EAD",
                    reference="EAD CEMP Guidelines"
                ),
            ],
            
            # KSA National Regulations
            Jurisdiction.KSA_NATIONAL: [
                Regulation(
                    id="KSA-001",
                    name="General Environmental Regulations",
                    jurisdiction=Jurisdiction.KSA_NATIONAL,
                    category="General",
                    requirement="Environmental permit from NCEC required",
                    reference="Royal Decree No. M/165"
                ),
                Regulation(
                    id="KSA-002",
                    name="Air Quality Standards",
                    jurisdiction=Jurisdiction.KSA_NATIONAL,
                    category="Air Quality",
                    requirement="PM10 24-hour average not to exceed 340 μg/m³",
                    threshold={"pm10_24hr": 340, "pm25_24hr": 75},
                    reference="NCEC Air Quality Standards"
                ),
                Regulation(
                    id="KSA-003",
                    name="Noise Regulations",
                    jurisdiction=Jurisdiction.KSA_NATIONAL,
                    category="Noise",
                    requirement="Construction noise limit 70 dB(A) during day",
                    threshold={"noise_day": 70, "noise_night": 60},
                    reference="NCEC Noise Standards"
                ),
                Regulation(
                    id="KSA-004",
                    name="Water Conservation",
                    jurisdiction=Jurisdiction.KSA_NATIONAL,
                    category="Water",
                    requirement="Water conservation plan required for all projects",
                    reference="National Water Strategy 2030"
                ),
            ],
            
            # NEOM Specific Regulations
            Jurisdiction.NEOM: [
                Regulation(
                    id="NEOM-001",
                    name="NEOM Environmental Standards",
                    jurisdiction=Jurisdiction.NEOM,
                    category="General",
                    requirement="Zero single-use plastic policy",
                    reference="NEOM Environmental Policy"
                ),
                Regulation(
                    id="NEOM-002",
                    name="Renewable Energy Requirement",
                    jurisdiction=Jurisdiction.NEOM,
                    category="Energy",
                    requirement="100% renewable energy for construction sites",
                    reference="NEOM Sustainability Guidelines"
                ),
                Regulation(
                    id="NEOM-003",
                    name="Biodiversity Protection",
                    jurisdiction=Jurisdiction.NEOM,
                    category="Biodiversity",
                    requirement="Zero net loss of biodiversity",
                    reference="NEOM Conservation Policy"
                ),
            ],
        }
        
        return regulations

    def _load_permit_requirements(self) -> Dict[Jurisdiction, List[str]]:
        """Load permit requirements by jurisdiction."""
        return {
            Jurisdiction.UAE_FEDERAL: [
                "Environmental Impact Assessment (if required)",
                "Environmental Permit",
                "No Objection Certificate (NOC)",
            ],
            Jurisdiction.DUBAI: [
                "Dubai Municipality Environmental Permit",
                "Construction Environmental Management Plan",
                "Waste Management Plan",
                "Air Quality Monitoring Plan (for large projects)",
            ],
            Jurisdiction.ABU_DHABI: [
                "EAD Environmental Permit",
                "Approved CEMP",
                "Estidama Pearl Rating Certificate",
                "Environmental Monitoring Plan",
            ],
            Jurisdiction.KSA_NATIONAL: [
                "NCEC Environmental License",
                "Environmental Compliance Certificate",
                "Construction Permit with Environmental Conditions",
                "Water Conservation Plan",
            ],
            Jurisdiction.NEOM: [
                "NEOM Environmental Authorization",
                "Biodiversity Management Plan",
                "Zero Waste Plan",
                "Renewable Energy Compliance Certificate",
            ],
        }

    def check_compliance(self, 
                        project_data: Dict,
                        jurisdiction: Jurisdiction) -> ComplianceReport:
        """
        Check project compliance with regulations.
        
        Args:
            project_data: Dictionary containing project parameters and measurements
            jurisdiction: Jurisdiction to check compliance against
            
        Returns:
            ComplianceReport with detailed compliance assessment
        """
        checks = []
        applicable_regulations = self.regulations.get(jurisdiction, [])
        
        # Also include federal regulations for UAE emirates
        if jurisdiction in [Jurisdiction.DUBAI, Jurisdiction.ABU_DHABI, Jurisdiction.SHARJAH]:
            applicable_regulations.extend(self.regulations[Jurisdiction.UAE_FEDERAL])
        
        for regulation in applicable_regulations:
            check = self._check_regulation(regulation, project_data)
            checks.append(check)
        
        # Calculate overall compliance
        compliant_count = sum(1 for c in checks if c.status == ComplianceStatus.COMPLIANT)
        total_count = len(checks)
        compliance_percentage = (compliant_count / total_count * 100) if total_count > 0 else 0
        
        # Determine overall status
        if compliance_percentage == 100:
            overall_status = ComplianceStatus.COMPLIANT
        elif compliance_percentage >= 80:
            overall_status = ComplianceStatus.CONDITIONAL
        else:
            overall_status = ComplianceStatus.NON_COMPLIANT
        
        # Generate action items
        action_items = self._generate_action_items(checks)
        
        # Get required permits
        required_permits = self.permit_requirements.get(jurisdiction, [])
        
        return ComplianceReport(
            project_name=project_data.get('project_name', 'Unknown Project'),
            jurisdiction=jurisdiction,
            assessment_date=datetime.now(),
            overall_status=overall_status,
            compliance_percentage=compliance_percentage,
            checks=checks,
            required_permits=required_permits,
            action_items=action_items
        )

    def _check_regulation(self, regulation: Regulation, project_data: Dict) -> ComplianceCheck:
        """Check compliance with a specific regulation."""
        check = ComplianceCheck(
            regulation_id=regulation.id,
            regulation_name=regulation.name,
            status=ComplianceStatus.PENDING
        )
        
        # Check based on regulation category
        if regulation.category == "Air Quality" and regulation.threshold:
            pm10_actual = project_data.get('pm10_concentration', 0)
            pm10_limit = regulation.threshold.get('pm10_24hr', float('inf'))
            
            check.actual_value = pm10_actual
            check.required_value = pm10_limit
            check.deviation = ((pm10_actual - pm10_limit) / pm10_limit * 100) if pm10_limit > 0 else 0
            
            if pm10_actual <= pm10_limit:
                check.status = ComplianceStatus.COMPLIANT
            else:
                check.status = ComplianceStatus.NON_COMPLIANT
                check.recommendation = f"Reduce PM10 levels by {check.deviation:.1f}% to meet standards"
        
        elif regulation.category == "Noise" and regulation.threshold:
            noise_actual = project_data.get('noise_level', 0)
            noise_limit = regulation.threshold.get('noise_residential_day', 
                                                 regulation.threshold.get('noise_day', float('inf')))
            
            check.actual_value = noise_actual
            check.required_value = noise_limit
            check.deviation = ((noise_actual - noise_limit) / noise_limit * 100) if noise_limit > 0 else 0
            
            if noise_actual <= noise_limit:
                check.status = ComplianceStatus.COMPLIANT
            else:
                check.status = ComplianceStatus.NON_COMPLIANT
                check.recommendation = f"Reduce noise levels by {check.deviation:.1f}% to meet standards"
        
        elif regulation.category == "Waste":
            has_waste_plan = project_data.get('waste_management_plan', False)
            waste_segregation = project_data.get('waste_segregation', False)
            
            if has_waste_plan and waste_segregation:
                check.status = ComplianceStatus.COMPLIANT
            else:
                check.status = ComplianceStatus.NON_COMPLIANT
                check.recommendation = "Implement comprehensive waste management plan with segregation"
                check.evidence_required = ["Waste Management Plan", "Waste Tracking Records"]
        
        elif regulation.category == "General":
            # For general requirements, check if EIA is provided
            has_eia = project_data.get('eia_completed', False)
            if regulation.requirement.lower().find('eia') != -1:
                check.status = ComplianceStatus.COMPLIANT if has_eia else ComplianceStatus.NON_COMPLIANT
                if not has_eia:
                    check.recommendation = "Complete Environmental Impact Assessment"
                    check.evidence_required = ["EIA Report", "Authority Approval"]
            else:
                # Assume compliant for other general requirements
                check.status = ComplianceStatus.CONDITIONAL
                check.recommendation = "Verify compliance with authority"
        
        elif regulation.category == "Sustainability":
            # Check green building compliance
            has_green_cert = project_data.get('green_building_cert', False)
            if has_green_cert:
                check.status = ComplianceStatus.COMPLIANT
            else:
                check.status = ComplianceStatus.NON_COMPLIANT
                check.recommendation = "Obtain required green building certification"
                check.evidence_required = ["Green Building Design Documents", "Certification Application"]
        
        elif regulation.category == "Water":
            water_usage = project_data.get('water_consumption', 0)
            has_conservation_plan = project_data.get('water_conservation_plan', False)
            
            if has_conservation_plan:
                check.status = ComplianceStatus.COMPLIANT
            else:
                check.status = ComplianceStatus.NON_COMPLIANT
                check.recommendation = "Develop water conservation plan"
                check.evidence_required = ["Water Conservation Plan", "Water Usage Projections"]
        
        else:
            # Default to conditional for unimplemented checks
            check.status = ComplianceStatus.CONDITIONAL
            check.recommendation = f"Manual verification required for {regulation.category}"
        
        return check

    def _generate_action_items(self, checks: List[ComplianceCheck]) -> List[str]:
        """Generate prioritized action items based on compliance checks."""
        action_items = []
        
        # Priority 1: Non-compliant items
        non_compliant = [c for c in checks if c.status == ComplianceStatus.NON_COMPLIANT]
        for check in non_compliant:
            if check.recommendation:
                action_items.append(f"[HIGH] {check.recommendation}")
        
        # Priority 2: Conditional items
        conditional = [c for c in checks if c.status == ComplianceStatus.CONDITIONAL]
        for check in conditional:
            if check.recommendation:
                action_items.append(f"[MEDIUM] {check.recommendation}")
        
        # Priority 3: Evidence requirements
        evidence_needed = [c for c in checks if c.evidence_required]
        for check in evidence_needed:
            for evidence in check.evidence_required:
                action_items.append(f"[MEDIUM] Submit {evidence}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_items = []
        for item in action_items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)
        
        return unique_items

    def get_jurisdiction_summary(self, jurisdiction: Jurisdiction) -> Dict:
        """
        Get summary of regulations for a jurisdiction.
        
        Args:
            jurisdiction: Jurisdiction to summarize
            
        Returns:
            Dictionary with jurisdiction information
        """
        regulations = self.regulations.get(jurisdiction, [])
        permits = self.permit_requirements.get(jurisdiction, [])
        
        summary = {
            'jurisdiction': jurisdiction.value,
            'total_regulations': len(regulations),
            'categories': list(set(r.category for r in regulations)),
            'required_permits': permits,
            'key_thresholds': {},
            'penalties': []
        }
        
        # Extract key thresholds
        for reg in regulations:
            if reg.threshold:
                summary['key_thresholds'].update(reg.threshold)
            if reg.penalty:
                summary['penalties'].append(reg.penalty)
        
        return summary

    def compare_jurisdictions(self, jurisdictions: List[Jurisdiction]) -> pd.DataFrame:
        """
        Compare regulations across multiple jurisdictions.
        
        Args:
            jurisdictions: List of jurisdictions to compare
            
        Returns:
            DataFrame with comparison
        """
        import pandas as pd
        
        comparison_data = []
        categories = set()
        
        # Collect all categories
        for jurisdiction in jurisdictions:
            regs = self.regulations.get(jurisdiction, [])
            categories.update(r.category for r in regs)
        
        # Build comparison matrix
        for category in sorted(categories):
            row = {'Category': category}
            
            for jurisdiction in jurisdictions:
                regs = self.regulations.get(jurisdiction, [])
                cat_regs = [r for r in regs if r.category == category]
                
                if cat_regs:
                    # Summarize requirements for this category
                    if category == "Air Quality":
                        pm10_limits = [r.threshold.get('pm10_24hr', 'N/A') 
                                     for r in cat_regs if r.threshold]
                        row[jurisdiction.value] = f"PM10: {min(pm10_limits) if pm10_limits else 'N/A'} μg/m³"
                    elif category == "Noise":
                        noise_limits = []
                        for r in cat_regs:
                            if r.threshold:
                                noise_limits.extend([
                                    r.threshold.get('noise_residential_day', 
                                                  r.threshold.get('noise_day', 'N/A'))
                                ])
                        row[jurisdiction.value] = f"{min(noise_limits) if noise_limits else 'N/A'} dB(A)"
                    else:
                        row[jurisdiction.value] = f"{len(cat_regs)} regulation(s)"
                else:
                    row[jurisdiction.value] = "Not specified"
            
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)

    def generate_compliance_certificate(self, report: ComplianceReport) -> str:
        """
        Generate compliance certificate text.
        
        Args:
            report: Compliance report
            
        Returns:
            Certificate text
        """
        if report.overall_status != ComplianceStatus.COMPLIANT:
            return "Certificate cannot be issued - project is not fully compliant"
        
        certificate = f"""
ENVIRONMENTAL COMPLIANCE CERTIFICATE
=====================================

Project: {report.project_name}
Jurisdiction: {report.jurisdiction.value}
Assessment Date: {report.assessment_date.strftime('%Y-%m-%d')}

This is to certify that the above project has been assessed and found to be in 
FULL COMPLIANCE with applicable environmental regulations.

Compliance Score: {report.compliance_percentage:.1f}%
Total Regulations Checked: {len(report.checks)}

This certificate is valid for 12 months from the assessment date, subject to:
- Continued compliance with all regulations
- Implementation of any recommended improvements
- Regular monitoring and reporting as required

Issued by: EIA Compliance System
Authorized by: Regulatory Compliance Module
        """
        
        return certificate


def main():
    """Example usage of RegulatoryCompliance."""
    # Initialize compliance checker
    compliance_checker = RegulatoryCompliance()
    
    # Example project data
    project_data = {
        'project_name': 'Dubai Marina Tower',
        'pm10_concentration': 120,  # μg/m³
        'pm25_concentration': 55,   # μg/m³
        'noise_level': 68,          # dB(A)
        'water_consumption': 2500,  # m³
        'eia_completed': True,
        'waste_management_plan': True,
        'waste_segregation': True,
        'green_building_cert': False,
        'water_conservation_plan': True
    }
    
    # Check compliance for Dubai
    report = compliance_checker.check_compliance(project_data, Jurisdiction.DUBAI)
    
    # Display results
    print(f"Compliance Assessment for {report.project_name}")
    print("=" * 50)
    print(f"Jurisdiction: {report.jurisdiction.value}")
    print(f"Overall Status: {report.overall_status.value}")
    print(f"Compliance Score: {report.compliance_percentage:.1f}%")
    
    print("\nNon-Compliant Items:")
    for check in report.checks:
        if check.status == ComplianceStatus.NON_COMPLIANT:
            print(f"- {check.regulation_name}")
            if check.actual_value and check.required_value:
                print(f"  Actual: {check.actual_value}, Required: {check.required_value}")
            if check.recommendation:
                print(f"  Action: {check.recommendation}")
    
    print("\nRequired Permits:")
    for permit in report.required_permits:
        print(f"- {permit}")
    
    print("\nAction Items:")
    for i, action in enumerate(report.action_items[:5], 1):
        print(f"{i}. {action}")
    
    # Compare jurisdictions
    print("\n\nJurisdiction Comparison:")
    comparison = compliance_checker.compare_jurisdictions([
        Jurisdiction.DUBAI, 
        Jurisdiction.ABU_DHABI, 
        Jurisdiction.KSA_NATIONAL
    ])
    print(comparison.to_string())


if __name__ == "__main__":
    main()