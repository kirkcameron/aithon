"""aithon: AI + python. Injects #/<line> markers for AI-assisted editing."""

import ast
import os
from pathlib import Path
import argparse


HELP = """
aithon: AI + python. Injects #/<line> markers into Python code for AI-assisted editing.

WHAT:
  Injects AI-readable #/<line> markers at Python block boundaries.
  Output can be fed to AI agents for targeted code edits.

NOT A FORMATTER:
  Does NOT fix broken code. Does NOT fix indentation. Does NOT reformat.
  Only adds #/<line> markers to existing code structure.
  For broken Python, markers go BEFORE blocks (heuristic). For valid Python, markers go AFTER (AST).

WHEN TO USE:
  - When preparing Python files for multi-turn AI editing sessions
  - When you need stable block references that survive reformatting
  - Before asking AI to "edit block at #/X" in complex files
  - When code will be pasted through repeated AI conversation turns

TAGS: code-editing, markers, anchors, python, block-references, whitespace-safe

DEPENDENCIES: Python 3.8+, .py files only
LIMITATIONS: Non-Python files ignored. Extremely malformed Python may fail.

WHY:
  When code is pasted through repeated AI conversation turns, whitespace
  gets corrupted: tabs become spaces, indentation drifts, structure breaks.
  #/<line> markers survive this corruption and let AI reference exact
  block boundaries: "edit the block after #/5" works even when the code
  has been reformatted 10 times.

HOW TO EDIT:
  Reference blocks by their marker, then describe the change.

    "Rewrite the function after #/3 to use pathlib instead of os.path"
    "Add error handling to the block after #/7"
    "Replace the if-statement at #/5 with a match/case"

  The marker pins the exact code section. The prompt does the rest.

BEFORE:
  def foo(x):
      if x > 0:
          return x
      return 0

AFTER:
  def foo(x):
  #/3
      if x > 0:
      #/5
          return x
      #/6
      return 0
  #/7

USAGE:
  aithon --source <file> --target <file>
  aithon --srcdir <dir> --tgtdir <dir> [--action replica|replace|restore]

FLAGS:
  --source        Input file
  --target        Output file
  --srcdir        Input directory
  --tgtdir        Output directory
  --action        replica (create _ai files), replace (overwrite existing files), or restore (remove markers)
  --dryrun       Show what would be converted

EXAMPLES:
  aithon --source app.py --target app_ai.py
  aithon --srcdir src/ --tgtdir ai/
  aithon --srcdir src/ --tgtdir src/ --action replace
  aithon --action restore --source app_ai.py --target app.py
  aithon --action restore --srcdir ai/ --tgtdir clean/
"""


def get_terminators_ast(tree, source_lines):
    """Find line numbers where blocks END using AST."""
    block_markers = {}
    
    def process_node(node):
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            if node.lineno == node.end_lineno:
                return
        
        if hasattr(node, 'body') and node.body:
            last_stmt = node.body[-1]
            if hasattr(last_stmt, 'end_lineno'):
                block_markers[last_stmt.end_lineno] = last_stmt.end_lineno
        
        if hasattr(node, 'handlers') and node.handlers:
            for handler in node.handlers:
                if handler.body and handler.body[-1]:
                    if hasattr(handler.body[-1], 'end_lineno'):
                        block_markers[handler.body[-1].end_lineno] = handler.body[-1].end_lineno
        
        if hasattr(node, 'orelse') and node.orelse:
            if node.orelse[-1] and hasattr(node.orelse[-1], 'end_lineno'):
                block_markers[node.orelse[-1].end_lineno] = node.orelse[-1].end_lineno
        
        if hasattr(node, 'finalbody') and node.finalbody:
            if node.finalbody[-1] and hasattr(node.finalbody[-1], 'end_lineno'):
                block_markers[node.finalbody[-1].end_lineno] = node.finalbody[-1].end_lineno
    
    for node in ast.walk(tree):
        process_node(node)
    
    return block_markers


def get_terminators_heuristic(source_code):
    """Heuristic for broken Python - find block starts."""
    lines = source_code.split('\n')
    block_markers = {}
    
    block_starts = {'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 
                    'except', 'finally', 'with', 'match', 'case', 'async'}
    
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            continue
        
        first_word = stripped.split()[0] if stripped.split() else ''
        
        if first_word == 'async' and len(stripped.split()) > 1:
            second_word = stripped.split()[1]
            if second_word in ('def', 'for', 'with'):
                first_word = 'async ' + second_word
        
        if first_word in block_starts or stripped.startswith(('async ',)):
            block_markers[i] = i
    
    return block_markers


def convert_aithon(source_code):
    """Convert Python to Aithon format."""
    import re
    
    lines = source_code.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == '#/' or re.match(r'^#/\d+$', stripped):
            continue
        if re.match(r'^#/\d*\s*$', line):
            continue
        cleaned_lines.append(line)
    
    source_code = '\n'.join(cleaned_lines)
    source_lines = source_code.split('\n')
    
    try:
        tree = ast.parse(source_code)
        markers = get_terminators_ast(tree, source_lines)
        new_lines = []
        for i, line in enumerate(source_lines, 1):
            new_lines.append(line)
            if i in markers:
                new_lines.append(f'#/{markers[i]}')
    except SyntaxError:
        markers = get_terminators_heuristic(source_code)
        new_lines = []
        for i, line in enumerate(source_lines, 1):
            if i in markers:
                new_lines.append(f'#/{markers[i]}')
            new_lines.append(line)
    
    return '\n'.join(new_lines)


def convert_file(input_path, output_path):
    """Convert a single Python file."""
    with open(input_path, 'r') as f:
        source = f.read()
    
    aithon_code = convert_aithon(source)
    
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(aithon_code)
        return f"Converted: {input_path} -> {output_path}"
    else:
        print(aithon_code)
        return None


def convert_directory(source_dir, target_dir, dry_run=False, process='replica'):
    """Convert all .py files in a directory."""
    input_path = Path(source_dir)
    py_files = list(input_path.rglob("*.py"))
    
    if not py_files:
        return f"No .py files found in {source_dir}"
    
    results = []
    for py_file in py_files:
        rel_path = py_file.relative_to(input_path)
        
        if process == 'inplace':
            out_file = py_file
        else:
            if target_dir:
                output_path = Path(target_dir)
                stem = rel_path.stem
                if not stem.endswith('_ai'):
                    stem = stem + '_ai'
                out_file = output_path / (stem + '.py')
            else:
                stem = rel_path.stem
                if not stem.endswith('_ai'):
                    stem = stem + '_ai'
                out_file = py_file.parent / (stem + '.py')
        
        if dry_run:
            results.append(f"DRY RUN: {py_file} -> {out_file}")
        else:
            if out_file.parent != py_file.parent:
                os.makedirs(out_file.parent, exist_ok=True)
            msg = convert_file(py_file, out_file)
            results.append(msg)
    
    return "\n".join(results)


def revert_aithon(source_code):
    """Remove #/<line> markers from code."""
    import re
    lines = source_code.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == '#/' or re.match(r'^#/\d+$', stripped):
            continue
        if re.match(r'^#/\d*\s*$', line):
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def revert_file(input_path, output_path):
    """Remove markers from a single file."""
    with open(input_path, 'r') as f:
        source = f.read()
    
    clean_code = revert_aithon(source)
    
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(clean_code)
        return f"Reverted: {input_path} -> {output_path}"
    else:
        print(clean_code)
        return None


def main():
    parser = argparse.ArgumentParser(
        prog="aithon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP
    )
    
    parser.add_argument('--source', help='Input file')
    parser.add_argument('--target', help='Output file')
    parser.add_argument('--srcdir', help='Input directory')
    parser.add_argument('--tgtdir', help='Output directory')
    parser.add_argument('--action', default='replica', choices=['replica', 'replace', 'restore'],
                        help='replica (create _ai files), replace (overwrite existing files), or restore (remove markers)')
    parser.add_argument('--dryrun', action='store_true',
                        help='Show what would be converted')
    
    args = parser.parse_args()
    
    if args.action == 'restore':
        # Remove markers
        if args.source:
            if not args.target:
                parser.error("--target required")
            print(revert_file(args.source, args.target))
        elif args.srcdir:
            if not args.tgtdir:
                parser.error("--tgtdir required")
            input_path = Path(args.srcdir)
            output_path = Path(args.tgtdir)
            py_files = list(input_path.rglob("*.py"))
            for py_file in py_files:
                rel_path = py_file.relative_to(input_path)
                out_file = output_path / rel_path.name
                out_file.parent.mkdir(parents=True, exist_ok=True)
                revert_file(py_file, out_file)
            print(f"Restored {len(py_files)} files")
        else:
            parser.print_help()
    elif args.srcdir:
        if not args.tgtdir:
            parser.error("--tgtdir required")
        process = 'inplace' if args.action == 'replace' else 'replica'
        print(convert_directory(args.srcdir, args.tgtdir, args.dryrun, process))
    elif args.source:
        if not args.target:
            parser.error("--target required")
        convert_file(args.source, args.target)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
