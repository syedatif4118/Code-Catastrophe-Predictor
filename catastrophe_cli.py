#!/usr/bin/env python3
"""
Code Catastrophe Predictor - Command Line Interface

Usage:
    python catastrophe_cli.py <file_or_directory>
    python catastrophe_cli.py --url <github_url>
    python catastrophe_cli.py --stdin

Examples:
    python catastrophe_cli.py src/api/authentication.py
    python catastrophe_cli.py ./src
    python catastrophe_cli.py --url https://github.com/user/repo/blob/main/server.py
    cat mycode.py | python catastrophe_cli.py --stdin
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict
from code_catastrophe_predictor import CodeCatastrophePredictor
from datetime import datetime


class CodeAnalyzer:
    """Analyzes real code files and directories"""

    SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.c', '.cpp', '.rs'}

    def __init__(self):
        self.predictor = CodeCatastrophePredictor()

    def analyze_file(self, file_path: str) -> str:
        """Read and analyze a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # Build context description
            file_name = os.path.basename(file_path)
            lines = code.count('\n') + 1

            # Check for architecture description file
            arch_description = ""
            arch_file = file_path.replace('.py', '.architecture.md')
            if os.path.exists(arch_file):
                try:
                    with open(arch_file, 'r', encoding='utf-8') as f:
                        arch_description = f.read()
                    print(f"   📚 Found architecture description: {os.path.basename(arch_file)}")
                except:
                    pass

            # Build architecture section
            arch_section = ""
            if arch_description:
                arch_section = f"\n\nDETAILED ARCHITECTURE & DEPLOYMENT INFO:\n{arch_description}"

            description = f"""
FILE: {file_name}
LANGUAGE: {self._detect_language(file_path)}
SIZE: {lines} lines
PATH: {file_path}

CODE CONTENT:
```
{code[:2000]}  {'... (truncated)' if len(code) > 2000 else ''}
```

ARCHITECTURAL CONTEXT:
- This is actual production code from: {file_path}
- Please analyze this REAL code, not hypothetical examples
- Focus on realistic failures based on what you see in the code
{arch_section}
"""
            return description

        except Exception as e:
            return f"Error reading file {file_path}: {e}"

    def analyze_directory(self, dir_path: str) -> str:
        """Analyze all supported files in directory"""
        code_files = []

        for root, dirs, files in os.walk(dir_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', 'venv', '.venv'}]

            for file in files:
                if Path(file).suffix in self.SUPPORTED_EXTENSIONS:
                    code_files.append(os.path.join(root, file))

        if not code_files:
            return f"No supported code files found in {dir_path}"

        # Build architecture description
        file_list = '\n'.join([f"  - {f}" for f in code_files[:20]])
        if len(code_files) > 20:
            file_list += f"\n  ... and {len(code_files) - 20} more files"

        # Sample first file for code context
        sample_code = ""
        if code_files:
            try:
                with open(code_files[0], 'r', encoding='utf-8') as f:
                    sample_code = f.read()[:1500]
            except:
                pass

        description = f"""
PROJECT DIRECTORY: {dir_path}
TOTAL FILES: {len(code_files)} code files

FILE STRUCTURE:
{file_list}

SAMPLE CODE (from {os.path.basename(code_files[0]) if code_files else 'N/A'}):
```
{sample_code}
```

ARCHITECTURAL CONTEXT:
- This is a real codebase with {len(code_files)} files
- Multiple components may interact
- Focus on system-level failures and integration issues
- Consider how different files/modules might fail together
"""
        return description

    def analyze_stdin(self) -> str:
        """Analyze code from stdin"""
        code = sys.stdin.read()

        description = f"""
CODE FROM STDIN:
```
{code}
```

ARCHITECTURAL CONTEXT:
- This is user-provided code for analysis
- Analyze as a standalone component
- Consider production deployment scenarios
"""
        return description

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.c': 'C',
            '.cpp': 'C++',
            '.rs': 'Rust'
        }
        return lang_map.get(ext, 'Unknown')


def print_results(results: Dict, output_file: str = None):
    """Pretty print or save results"""

    if output_file:
        # Save to JSON
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Results saved to: {output_file}")
        return

    # Print to terminal
    print("\n" + "="*80)
    print("💀 CODE CATASTROPHE PREDICTION RESULTS")
    print("="*80)

    catastrophes = results.get('catastrophes', [])

    if not catastrophes:
        print("\n❌ No catastrophes generated")
        return

    print(f"\n📊 Generated {len(catastrophes)} production failure scenarios:\n")

    for i, cat in enumerate(catastrophes, 1):
        print(f"\n{'─'*80}")
        print(f"💀 CATASTROPHE #{i}: {cat['name']}")
        print(f"{'─'*80}")
        print(f"🎯 Probability: {cat['probability'].upper()}")
        print(f"💥 Blast Radius: {cat['blast_radius']}")
        print(f"🔍 Detection: {cat['detection_difficulty']}")

        if cat.get('impact_metrics'):
            metrics = cat['impact_metrics']
            print(f"💰 Revenue Impact: {metrics.get('revenue_impact', 'Unknown')}")
            print(f"⏱️  Downtime: {metrics.get('downtime_hours', 'Unknown')} hours")

        print(f"\n📝 DESCRIPTION:")
        print(f"   {cat['description'][:300]}...")

        print(f"\n🔓 VULNERABILITY:")
        print(f"   {cat.get('vulnerability', 'N/A')[:200]}...")

        if cat.get('historical_precedent'):
            print(f"\n📚 HISTORICAL PRECEDENT:")
            print(f"   {cat['historical_precedent'][:200]}...")

        if cat.get('warning_signs'):
            print(f"\n⚠️  WARNING SIGNS:")
            for sign in cat['warning_signs'][:3]:
                print(f"   • {sign}")

    # Show top catastrophe analysis if available
    if results.get('top_catastrophe_analysis'):
        analysis = results['top_catastrophe_analysis']
        print(f"\n\n{'='*80}")
        print("🔬 MULTI-AGENT ANALYSIS (Top Catastrophe)")
        print(f"{'='*80}")

        if analysis.get('paranoid'):
            print(f"\n😰 PARANOID ENGINEER:")
            print(f"   {analysis['paranoid'][:200]}...")

        if analysis.get('debugger'):
            print(f"\n🔧 OPTIMISTIC DEBUGGER:")
            print(f"   {analysis['debugger'][:200]}...")

        if analysis.get('veteran'):
            veteran = analysis['veteran']
            print(f"\n⚡ PRODUCTION VETERAN:")
            print(f"   Realism Score: {veteran.get('realism_score', 'N/A')}/10")
            print(f"   {veteran.get('analysis', '')[:200]}...")

    print(f"\n{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Predict production failures for real code using Opus 4.6",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s src/api/auth.py
  %(prog)s ./backend --output results.json
  %(prog)s --stdin < mycode.py
  %(prog)s src/ --scenarios 5
        """
    )

    parser.add_argument('path', nargs='?', help='File or directory to analyze')
    parser.add_argument('--stdin', action='store_true', help='Read code from stdin')
    parser.add_argument('--output', '-o', help='Save results to JSON file')
    parser.add_argument('--scenarios', '-n', type=int, default=3, help='Number of scenarios to generate (default: 3)')

    args = parser.parse_args()

    # Validate input
    if not args.stdin and not args.path:
        parser.print_help()
        sys.exit(1)

    print("="*80)
    print("💀 CODE CATASTROPHE PREDICTOR - CLI")
    print("   Powered by Claude Opus 4.6 Adaptive Thinking")
    print("="*80)

    analyzer = CodeAnalyzer()

    # Analyze code
    if args.stdin:
        print("\n📖 Reading code from stdin...")
        code_description = analyzer.analyze_stdin()
    elif os.path.isfile(args.path):
        print(f"\n📖 Analyzing file: {args.path}")
        code_description = analyzer.analyze_file(args.path)
    elif os.path.isdir(args.path):
        print(f"\n📖 Analyzing directory: {args.path}")
        code_description = analyzer.analyze_directory(args.path)
    else:
        print(f"\n❌ Error: '{args.path}' is not a valid file or directory")
        sys.exit(1)

    # Run prediction
    print(f"\n🤖 Running catastrophe prediction with {args.scenarios} scenarios...")
    print("   (This may take 30-60 seconds with Opus 4.6 adaptive thinking)\n")

    predictor = CodeCatastrophePredictor()
    results = predictor.predict(code_description)

    # Output results
    print_results(results, args.output)

    print("✅ Analysis complete!")
    print("\n💡 TIP: Use --output results.json to save full details")


if __name__ == "__main__":
    main()
