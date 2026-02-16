#!/usr/bin/env python3
"""
Aithon entry point - enables: aithon --input x.py --output y.ai
"""

from aithon import convert_file, convert_directory
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Aithon - AI-First Structured Python Converter (with numbered block terminators!)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aithon --input input.py
  aithon --input input.py --output output.ai
  aithon --directory ./src/
  aithon --directory ./src/ --output-dir ./ai/
  aithon --directory ./src/ --dry-run

Each block gets a unique number: #/1, #/2, #/3, etc.
        """
    )
    
    parser.add_argument('--input', dest='input_file', 
                        help='Input Python file')
    parser.add_argument('--output', dest='output_file', 
                        help='Output .ai file')
    parser.add_argument('--directory', dest='directory',
                        help='Input directory to convert recursively')
    parser.add_argument('--output-dir', dest='output_dir',
                        help='Output directory (for directory mode)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be converted without converting')
    
    args = parser.parse_args()
    
    # Directory mode
    if args.directory:
        result = convert_directory(args.directory, args.output_dir, args.dry_run)
        print(result)
    # Single file mode
    elif args.input_file:
        if args.output_file:
            convert_file(args.input_file, args.output_file)
        else:
            convert_file(args.input_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
