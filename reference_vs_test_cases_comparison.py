#!/usr/bin/env python3
"""
Reference Algorithm vs Your 6 Test Cases Comparison
Detailed comparison to find the closest match
"""

def compare_reference_with_test_cases():
    """Compare reference parameters with your 6 test cases"""
    
    print("🔍 REFERENCE ALGORITHM vs YOUR 6 TEST CASES")
    print("=" * 60)
    
    # Reference algorithm parameters (from attached file)
    reference = {
        "name": "Reference Algorithms",
        "area_width": 100,
        "area_height": 100,
        "sensing_range": 20,
        "num_nodes": 20,  # (PSO uses 30)
        "target_coverage": 95,  # Average of 90-99%
        "total_area": 10000,
        "sensor_coverage_area": 3.14159 * 20**2,  # ~1257 unit²
        "max_possible_coverage": 251.3,  # 20 sensors * 1257 / 10000 * 100
        "theoretical_sensors_needed": 7.96,  # 10000 / 1257
        "sensor_redundancy": 2.51  # 20 / 7.96
    }
    
    # Your 6 test cases
    test_cases = {
        "small_area_few_drones": {
            "area_width": 25, "area_height": 25, 
            "num_drones": 5, "sensing_range": 8,
            "target_coverage": 85
        },
        "medium_area_standard": {
            "area_width": 50, "area_height": 50,
            "num_drones": 15, "sensing_range": 8,
            "target_coverage": 90
        },
        "large_area_many_drones": {
            "area_width": 100, "area_height": 100,
            "num_drones": 30, "sensing_range": 12,
            "target_coverage": 95
        },
        "challenging_small_radius": {
            "area_width": 60, "area_height": 60,
            "num_drones": 20, "sensing_range": 6,
            "target_coverage": 88
        },
        "efficiency_test": {
            "area_width": 40, "area_height": 40,
            "num_drones": 12, "sensing_range": 10,
            "target_coverage": 92
        },
        "parallel_processing_test": {
            "area_width": 80, "area_height": 80,
            "num_drones": 25, "sensing_range": 10,
            "target_coverage": 90
        }
    }
    
    print("📐 REFERENCE ALGORITHM PARAMETERS:")
    print(f"   Area: {reference['area_width']}×{reference['area_height']} = {reference['total_area']:,} unit²")
    print(f"   Sensing Range: {reference['sensing_range']} units")
    print(f"   Number of Sensors: {reference['num_nodes']}")
    print(f"   Target Coverage: ~{reference['target_coverage']}%")
    print(f"   Sensor Coverage Area: {reference['sensor_coverage_area']:.0f} unit²")
    print(f"   Theoretical Sensors Needed: {reference['theoretical_sensors_needed']:.1f}")
    print(f"   Sensor Redundancy: {reference['sensor_redundancy']:.1f}x")
    
    print(f"\n📊 DETAILED COMPARISON WITH YOUR 6 TEST CASES:")
    print("-" * 55)
    
    similarity_scores = []
    
    for case_name, case_params in test_cases.items():
        total_area = case_params["area_width"] * case_params["area_height"]
        sensor_area = 3.14159 * case_params["sensing_range"]**2
        theoretical_sensors = total_area / sensor_area
        redundancy = case_params["num_drones"] / theoretical_sensors
        max_coverage = min((case_params["num_drones"] * sensor_area) / total_area * 100, 100)
        
        # Calculate similarity score (lower = more similar)
        area_similarity = abs(total_area - reference["total_area"]) / reference["total_area"]
        range_similarity = abs(case_params["sensing_range"] - reference["sensing_range"]) / reference["sensing_range"]
        nodes_similarity = abs(case_params["num_drones"] - reference["num_nodes"]) / reference["num_nodes"]
        coverage_similarity = abs(case_params["target_coverage"] - reference["target_coverage"]) / reference["target_coverage"]
        
        # Weighted similarity score (area and range are most important)
        total_similarity = (area_similarity * 0.4 + range_similarity * 0.4 + 
                          nodes_similarity * 0.15 + coverage_similarity * 0.05)
        
        similarity_scores.append((case_name, total_similarity, case_params, {
            'total_area': total_area,
            'sensor_area': sensor_area,
            'theoretical_sensors': theoretical_sensors,
            'redundancy': redundancy,
            'max_coverage': max_coverage
        }))
        
        print(f"\n🔹 {case_name.replace('_', ' ').upper()}")
        print(f"   Area: {case_params['area_width']}×{case_params['area_height']} = {total_area:,} unit²")
        print(f"   Drones: {case_params['num_drones']}, Range: {case_params['sensing_range']} units")
        print(f"   Target Coverage: {case_params['target_coverage']}%")
        print(f"   Theoretical Sensors Needed: {theoretical_sensors:.1f}")
        print(f"   Sensor Redundancy: {redundancy:.1f}x")
        print(f"   Max Possible Coverage: {max_coverage:.1f}%")
        
        # Direct comparisons
        area_diff = ((total_area - reference["total_area"]) / reference["total_area"]) * 100
        range_diff = ((case_params["sensing_range"] - reference["sensing_range"]) / reference["sensing_range"]) * 100
        nodes_diff = ((case_params["num_drones"] - reference["num_nodes"]) / reference["num_nodes"]) * 100
        coverage_diff = case_params["target_coverage"] - reference["target_coverage"]
        
        print(f"   📊 vs Reference:")
        print(f"      Area: {area_diff:+.1f}% ({'✅' if abs(area_diff) < 10 else '❌'})")
        print(f"      Range: {range_diff:+.1f}% ({'✅' if abs(range_diff) < 20 else '❌'})")
        print(f"      Nodes: {nodes_diff:+.1f}% ({'✅' if abs(nodes_diff) < 30 else '❌'})")
        print(f"      Coverage: {coverage_diff:+.0f}% ({'✅' if abs(coverage_diff) < 10 else '❌'})")
        print(f"   🎯 Similarity Score: {total_similarity:.3f} ({'✅ GOOD' if total_similarity < 0.3 else '⚠️ FAIR' if total_similarity < 0.6 else '❌ POOR'})")
    
    # Sort by similarity (best match first)
    similarity_scores.sort(key=lambda x: x[1])
    
    print(f"\n🏆 RANKING BY SIMILARITY TO REFERENCE:")
    print("-" * 45)
    
    for i, (case_name, score, params, calcs) in enumerate(similarity_scores, 1):
        status = "🥇 BEST" if i == 1 else "🥈 GOOD" if i == 2 else "🥉 OK" if i == 3 else "📊"
        print(f"{i}. {status} {case_name.replace('_', ' ').title()}")
        print(f"   Similarity Score: {score:.3f}")
        if i == 1:
            print(f"   ⭐ This is your CLOSEST match to the reference!")
    
    # Best match analysis
    best_match = similarity_scores[0]
    case_name, score, params, calcs = best_match
    
    print(f"\n🎯 BEST MATCH ANALYSIS: {case_name.replace('_', ' ').title()}")
    print("-" * 50)
    print("Parameter Comparison:")
    print(f"   Area: Reference {reference['area_width']}×{reference['area_height']} vs Your {params['area_width']}×{params['area_height']}")
    print(f"   Range: Reference {reference['sensing_range']} vs Your {params['sensing_range']} units")
    print(f"   Sensors: Reference {reference['num_nodes']} vs Your {params['num_drones']}")
    print(f"   Target: Reference ~{reference['target_coverage']}% vs Your {params['target_coverage']}%")
    
    if score < 0.2:
        print("   ✅ EXCELLENT match - Very similar parameters")
    elif score < 0.4:
        print("   ✅ GOOD match - Close enough for comparison") 
    elif score < 0.6:
        print("   ⚠️ FAIR match - Some significant differences")
    else:
        print("   ❌ POOR match - Major parameter differences")
    
    print(f"\n💡 RECOMMENDATIONS:")
    print("-" * 20)
    
    if case_name == "large_area_many_drones":
        print("✅ Your 'Large Area Many Drones' case is the closest match!")
        print("   Consider adjusting for even better comparison:")
        print(f"   • Reduce sensing range from {params['sensing_range']} to 20 units")
        print(f"   • Reduce drones from {params['num_drones']} to 20")
        print("   • This would match the reference exactly!")
    else:
        print(f"✅ Use '{case_name.replace('_', ' ').title()}' for comparison with reference")
        print("   This is your most similar test case.")
        
    print(f"\n📈 ALTERNATIVE: Create Perfect Match")
    print("-" * 35)
    print("For exact comparison with reference algorithms:")
    print("   • Area: 100×100 units")
    print("   • Sensing Range: 20 units") 
    print("   • Number of Drones: 20")
    print("   • Target Coverage: 95%")
    print("   • This would be identical to the reference!")
    
    return {
        "best_match": best_match,
        "all_scores": similarity_scores,
        "reference": reference
    }

if __name__ == "__main__":
    results = compare_reference_with_test_cases()
