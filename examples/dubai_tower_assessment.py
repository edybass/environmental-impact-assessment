"""
Example Usage of EIA Tool
Demonstrates screening and impact assessment for a Dubai construction project
"""

from src.assessment import EIAScreening
from src.analysis import ConstructionImpact


def main():
    print("=== Environmental Impact Assessment Tool ===")
    print("Project: Dubai Marina Tower Development\n")

    # Step 1: EIA Screening
    print("1. EIA SCREENING")
    print("-" * 40)

    screening = EIAScreening("commercial", "Dubai")

    project_data = {
        "project_size": 25000,  # m²
        "duration": 24,  # months
        "sensitive_receptors": ["residential_area", "school"],
        "water_usage": 1200,  # m³/day
        "near_protected_area": False
    }

    result = screening.assess(project_data)

    print(f"EIA Required: {'Yes' if result.eia_required else 'No'}")
    print(f"EIA Level: {result.eia_level}")
    print(f"Estimated Duration: {result.estimated_duration} days")
    print(f"\nKey Concerns:")
    for concern in result.key_concerns:
        print(f"  • {concern}")

    print(f"\nRequired Studies:")
    for study in result.specialist_studies:
        print(f"  • {study}")

    # Step 2: Construction Impact Assessment
    print(f"\n\n2. CONSTRUCTION IMPACT ASSESSMENT")
    print("-" * 40)

    analyzer = ConstructionImpact()

    # Noise Assessment
    print("\nNoise Impact:")
    noise = analyzer.assess_noise(
        equipment=["pile_driver", "excavator", "concrete_mixer", "crane"],
        working_hours="07:00-18:00",
        nearest_receptor_distance=100,
        receptor_type="residential",
        barriers=False
    )

    print(f"  Peak Noise Level: {noise.peak_noise_level:.1f} dB(A)")
    print(f"  Average Noise Level: {noise.average_noise_level:.1f} dB(A)")
    print(f"  Exceeds Limit: {'Yes' if noise.exceeds_limit else 'No'}")

    if noise.mitigation_required:
        print("  Mitigation Measures:")
        for measure in noise.mitigation_measures[:3]:
            print(f"    • {measure}")

    # Dust Assessment
    print("\nDust Impact:")
    dust = analyzer.assess_dust(
        soil_type="sandy",
        moisture_content=3,  # Low moisture (typical for UAE)
        wind_speed=20,  # km/h (moderate wind)
        area_disturbed=10000,  # m²
        mitigation_measures=["water_spraying", "barriers", "covering"]
    )

    print(f"  PM10 Concentration: {dust.pm10_concentration:.1f} μg/m³")
    print(f"  PM2.5 Concentration: {dust.pm25_concentration:.1f} μg/m³")
    print(f"  Exceeds Limit: {'Yes' if dust.exceeds_limit else 'No'}")
    print(f"  Mitigation Effectiveness: {dust.mitigation_effectiveness:.0f}%")
    print(f"  Affected Area: {dust.affected_area_radius:.0f}m radius")

    # Generate mitigation plan
    print("\n\n3. MITIGATION PLAN")
    print("-" * 40)

    mitigation = analyzer.generate_mitigation_plan(noise, dust)

    print("General Environmental Measures:")
    for measure in mitigation["general_measures"][:5]:
        print(f"  • {measure}")

    print("\n✅ Assessment Complete!")
    print("\nNext Steps:")
    print("1. Submit EIA to Dubai Municipality")
    print("2. Implement Construction Environmental Management Plan")
    print("3. Establish monitoring program")
    print("4. Conduct regular audits")


if __name__ == "__main__":
    main()
