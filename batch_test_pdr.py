"""
Comprehensive Test for PlantDoc Dataset Integration
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdr2018_model import process_plantdoc_image, analyze_batch

# Test multiple images from different categories
dataset_path = "C:/Users/uma/OneDrive/Pictures/Screenshots/PlantDoc-Dataset/test"

results = []

# Get all category folders
categories = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

print(f"Found {len(categories)} categories in dataset")
print("=" * 60)

# Test one image from each category
for category in categories[:10]:  # Test first 10 categories
    category_path = os.path.join(dataset_path, category)
    images = [f for f in os.listdir(category_path) if f.endswith('.jpg')]
    
    if images:
        sample_image = os.path.join(category_path, images[0])
        
        try:
            result = process_plantdoc_image(sample_image)
            result['category'] = category
            result['image_file'] = images[0]
            results.append(result)
            
            print(f"\nCategory: {category}")
            print(f"  Image: {images[0]}")
            print(f"  Detected: {result.get('disease', 'Unknown')}")
            print(f"  Confidence: {result.get('confidence', 0):.1f}%")
        except Exception as e:
            print(f"\nError processing {category}: {e}")

# Save results to JSON
output_path = "static/pdr2018_results.json"
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n{'=' * 60}")
print(f"Results saved to: {output_path}")
print(f"Total images tested: {len(results)}")
print("=" * 60)

# Count disease detections
disease_counts = {}
for r in results:
    disease = r.get('disease', 'Unknown')
    disease_counts[disease] = disease_counts.get(disease, 0) + 1

print("\nDisease Detection Summary:")
for disease, count in sorted(disease_counts.items(), key=lambda x: -x[1]):
    print(f"  {disease}: {count}")
