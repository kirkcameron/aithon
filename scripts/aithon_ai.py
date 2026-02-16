#!/usr/bin/env python3
"""
Aithon Converter - Adds numbered block terminators to Python code
Handles both valid Python AND broken Python with whitespace issues!
Each block gets a unique number: #/1, #/2, #/3, etc.
Usage: python aithon.ai <input.py> [output.ai]
       python aithon.ai --dir <directory> [-o <output_dir>]
"""

import sys
import ast
import os
import tokenize
import io
from pathlib import Path
import argparse


def get_terminators_ast(tree, source_lines):
    """Find all line numbers where we need to add terminators (for valid Python)"""
    terminators = {}  # line_number -> block_id
    
    block_counter = [0]  # Use list to allow mutation in nested function
    
    def process_node(node):
        # Skip one-liners
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            if node.lineno == node.end_lineno:
                return
#/52
        
        # Find the last line of this block
        if hasattr(node, 'body') and node.body:
            last_stmt = node.body[-1]
            if hasattr(last_stmt, 'end_lineno'):
                block_counter[0] += 1
                if isinstance(last_stmt, (ast.Pass, ast.Return, ast.Raise)):
                    terminators[last_stmt.end_lineno] = block_counter[0]
#/63
                else:
                    terminators[last_stmt.end_lineno] = block_counter[0]
#/64
        
        # Handle except handlers
        if hasattr(node, 'handlers') and node.handlers:
            for handler in node.handlers:
                if handler.body and handler.body[-1]:
                    block_counter[0] += 1
                    terminators[handler.body[-1].end_lineno] = block_counter[0]
#/65
        
        # Handle else blocks (if/while/for)
        if hasattr(node, 'orelse') and node.orelse:
            if node.orelse[-1]:
                block_counter[0] += 1
                terminators[node.orelse[-1].end_lineno] = block_counter[0]
#/55
        
        # Handle finally blocks
        if hasattr(node, 'finalbody') and node.finalbody:
            if node.finalbody[-1]:
                block_counter[0] += 1
                terminators[node.finalbody[-1].end_lineno] = block_counter[0]
#/56
    
    for node in ast.walk(tree):
        process_node(node)
#/10
    
    return terminators
#/2


def get_terminators_tokenize(source_code):
    """Find terminators using tokenize - works even with broken whitespace!"""
    terminators = {}  # line_number -> block_id
    lines = source_code.split('\n')
    
    # Track indentation stack: [(indent_level, line_number), ...]
    indent_stack = [(0, 0)]  # (indent_level, line_number_where_this_level_started)
    
    # Block keywords that increase indentation
    block_keywords = {'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 
                      'with', 'def', 'class', 'except_handler', 'match', 'case'}
    
    # Counter for unique block IDs
    block_counter = [0]
    
    # Track previous token
    prev_token = None
    
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source_code).readline))
#/11
    except:
        # If tokenize completely fails, fall back to simple approach
        return simple_terminator_finder(source_code)
#/33
    
    for token in tokens:
        tok_type, tok_string, (start_row, start_col), (end_row, end_col), _ = token
        
        # Calculate indent level for this line (based on leading whitespace)
        if start_row <= len(lines):
            line = lines[start_row - 1]
            indent = len(line) - len(line.lstrip())
#/34
        else:
            indent = 0
#/35
        
        # NEWLINE or NL tokens indicate end of logical line
        if tok_type in (tokenize.NEWLINE, tokenize.NL):
            # Check if we're dedenting
            while indent_stack and indent < indent_stack[-1][0]:
                # We're leaving a block - add terminator with unique ID
                dedent_from_line = indent_stack[-1][1]
                block_counter[0] += 1
                terminators[dedent_from_line] = block_counter[0]
                indent_stack.pop()
#/57
        
        # Check for block-starting keywords at the beginning of a line
        if tok_type == tokenize.NAME and tok_string in block_keywords:
            # Check if this is at the start of a logical line
            if start_col == 0 or (prev_token and prev_token[0] in (tokenize.NEWLINE, tokenize.NL)):
                # First, handle any dedents
                while indent_stack and indent < indent_stack[-1][0]:
                    dedent_from_line = indent_stack[-1][1]
                    block_counter[0] += 1
                    terminators[dedent_from_line] = block_counter[0]
                    indent_stack.pop()
#/66
                
                # Push new indent level (but only if not elif/else)
                if tok_string not in ('elif', 'else', 'except', 'finally', 'case'):
                    indent_stack.append((indent, start_row))
#/67
        
        # Handle 'else', 'elif', 'except', 'finally' - they reset to previous level
        if tok_type == tokenize.NAME and tok_string in ('else', 'elif', 'except', 'finally', 'case'):
            # Pop to previous block level
            while indent_stack and indent < indent_stack[-1][0]:
                dedent_from_line = indent_stack[-1][1]
                block_counter[0] += 1
                terminators[dedent_from_line] = block_counter[0]
                indent_stack.pop()
#/59
        
        prev_token = (tok_type, tok_string, start_row)
#/13
    
    return terminators
#/3


def simple_terminator_finder(source_code):
    """Fallback: use regex to find block ends"""
    import re
    terminators = {}
    lines = source_code.split('\n')
    block_counter = [0]
    
    # Keywords that start blocks
    block_starts = ['if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 
                    'finally:', 'with ', 'def ', 'class ', 'match ', 'case ']
    
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        
        # If line dedents (less indent than previous), add terminator to previous line
        if stripped and not stripped.startswith('#'):
            if any(stripped.startswith(kw) for kw in ['elif ', 'else:', 'except', 'finally:']):
                if i > 1:
                    block_counter[0] += 1
                    terminators[i - 1] = block_counter[0]
#/68
    
    return terminators
#/4


def convert_aithon(source_code):
    """Convert Python source to Aithon format - handles broken code too!"""
    import re
    
    # Strip existing #/ or #/n terminators to ensure idempotency
    # Remove any line that is JUST #/ or #/number
    lines = source_code.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are exactly #/ or #/ followed by digits
        if stripped == '#/' or re.match(r'^#/\d+$', stripped):
            continue
#/40
        # Also skip if the line ONLY contains #/ followed by optional digits and whitespace
        if re.match(r'^#/\d*\s*$', line):
            continue
#/41
        cleaned_lines.append(line)
#/15
    
    source_code = '\n'.join(cleaned_lines)
    source_lines = source_code.split('\n')
    
    # First try AST (works for valid Python)
    try:
        tree = ast.parse(source_code)
        terminators = get_terminators_ast(tree, source_lines)
#/16
    except SyntaxError:
        # Fall back to tokenize-based approach for broken code
        terminators = get_terminators_tokenize(source_code)
#/42
    
    # Build new source with numbered terminators
    new_lines = []
    for i, line in enumerate(source_lines, 1):
        new_lines.append(line)
        if i in terminators and line.strip():
            new_lines.append(f'#/{terminators[i]}')
#/43
    
    return '\n'.join(new_lines)
#/5


def convert_file(input_path, output_path=None):
    """Convert a single Python file"""
    with open(input_path, 'r') as f:
        source = f.read()
#/19
    
    aithon_code = convert_aithon(source)
    
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
#/44
        with open(output_path, 'w') as f:
            f.write(aithon_code)
#/45
        return f"Converted: {input_path} -> {output_path}"
#/20
    else:
        print(aithon_code)
        return None
#/21


def convert_directory(input_dir, output_dir=None, dry_run=False):
    """Convert all .py files in a directory recursively"""
    input_path = Path(input_dir)
    
    if output_dir:
        output_path = Path(output_dir)
#/22
    else:
        output_path = input_path
#/23
    
    # Find all .py files
    py_files = list(input_path.rglob("*.py"))
    
    if not py_files:
        return f"No .py files found in {input_dir}"
#/24
    
    results = []
    for py_file in py_files:
        # Calculate relative path
        rel_path = py_file.relative_to(input_path)
        
        # Check if already _ai file - keep name as-is
        if rel_path.stem.endswith('_ai'):
            stem = rel_path.stem
        else:
            stem = rel_path.stem + '_ai'
        
        # Determine output file path
        if output_dir:
            out_file = output_path / (stem + '.py')
        else:
            # In-place: keep same directory
            out_file = py_file.parent / (stem + '.py')
#/47
        
        if dry_run:
            results.append(f"DRY RUN: {py_file} -> {out_file}")
#/48
        else:
            msg = convert_file(py_file, out_file)
            results.append(msg)
#/49
    
    return "\n".join(results)
#/7


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aithon - AI-First Structured Python Converter (with numbered block terminators!)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python aithon.ai --input input.py
  python aithon.ai --input input.py --output output.ai
  python aithon.ai --directory ./src/
  python aithon.ai --directory ./src/ --output-dir ./ai/
  python aithon.ai --directory ./src/ --dry-run

Each block gets a unique number: #/1, #/2, #/3, etc.
This makes editing easier - each terminator is uniquely identifiable!
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
#/26
    # Single file mode
    elif args.input_file:
        if args.output_file:
            convert_file(args.input_file, args.output_file)
#/61
        else:
            convert_file(args.input_file)
#/62
    else:
        parser.print_help()
#/51
