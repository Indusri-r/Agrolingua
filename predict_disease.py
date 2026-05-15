import argparse
import json
import sys

from model_stub import process_image


def main():
    parser = argparse.ArgumentParser(
        description='Predict plant disease from an image using the trained deep learning model.'
    )
    parser.add_argument('image_path', help='Path to the leaf or crop image file')
    parser.add_argument('--lang', default='en', help='Fallback language code for heuristic output')
    parser.add_argument('--pretty', action='store_true', help='Pretty-print JSON output')
    args = parser.parse_args()

    result = process_image(args.image_path, args.lang)

    if args.pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))

    if result.get('status') == 'error':
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
