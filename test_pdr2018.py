"""
Test script for PlantDoc Dataset Integration
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdr2018_model import process_plantdoc_image, get_dataset_statistics, analyze_batch

# Print dataset statistics
print("=" * 60)
print("PlantDoc Dataset Integration - Statistics")
print("=" * 60)
stats = get_dataset_statistics()
print(f"Total Disease Classes: {stats['total_classes']}")
print(f"\nCategories:")
print(f"  Fruits: {', '.join(stats['categories']['fruits'])}")
print(f"  Vegetables: {', '.join(stats['categories']['vegetables'])}")
print(f"  Disease Types: {', '.join(stats['categories']['disease_types'])}")

# Test with a sample image from PlantDoc dataset
dataset_path = "C:/Users/uma/OneDrive/Pictures/Screenshots/PlantDoc-Dataset/test"

# Try to find and analyze an image
try:
    # Find first image in test folder
    test_images = []
    for root, dirs, files in os.walk(dataset_path):
        for f in files:
            if f.endswith('.jpg'):
                test_images.append(os.path.join(root, f))
    
    if test_images:
        sample_image = test_images[0]
        print(f"\n{'=' * 60}")
        print(f"Testing with image: {sample_image}")
        print("=" * 60)
        
        result = process_plantdoc_image(sample_image)
        
        print(f"\nResults:")
        print(f"  Status: {result.get('status')}")
        print(f"  Plant Name: {result.get('plant_name')}")
        print(f"  Disease: {result.get('disease')}")
        print(f"  Confidence: {result.get('confidence', 0):.1f}%")
        print(f"  Treatment: {result.get('treatment', 'N/A')}")
        
        if 'recommendations' in result:
            print(f"\n  Recommendations:")
            for rec in result['recommendations']:
                print(f"    - {rec}")
    else:
        print("\nNo test images found in dataset")

except Exception as e:
    print(f"\nError during testing: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
