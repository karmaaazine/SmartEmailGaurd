#!/usr/bin/env python3
"""
Smart Email Guardian CLI Tool
Analyzes email content for spam, phishing, and security threats.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Add the ai directory to the path
sys.path.append(str(Path(__file__).parent / "ai"))

from ai.email_guard import analyze_email

def read_input(input_source: Optional[str] = None) -> str:
    """
    Read email content from file or stdin.
    
    Args:
        input_source: Path to file or None for stdin
        
    Returns:
        str: Email content
    """
    if input_source:
        try:
            with open(input_source, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File '{input_source}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        print("Enter email content (Ctrl+D or Ctrl+Z when finished):", file=sys.stderr)
        return sys.stdin.read()

def format_output(result: dict, output_format: str = "json") -> str:
    """
    Format the analysis result for output.
    
    Args:
        result: Analysis result dictionary
        output_format: Output format ('json', 'text', 'table')
        
    Returns:
        str: Formatted output
    """
    if output_format == "json":
        return json.dumps(result, indent=2)
    
    elif output_format == "text":
        lines = [
            f"📧 Email Analysis Results",
            f"{'='*50}",
            f"Classification: {result['classification'].upper()}",
            f"Confidence: {result['confidence']:.2%}",
            f"Explanation: {result['explanation']}",
            f"",
            f"📊 Features:",
            f"  - Text length: {result['features'].get('length', 0)} characters",
            f"  - Word count: {result['features'].get('word_count', 0)}",
            f"  - URLs found: {result['features'].get('url_count', 0)}",
            f"  - Emails found: {result['features'].get('email_count', 0)}",
            f"  - Urgent words: {result['features'].get('urgent_words', 0)}",
        ]
        
        if result['indicators']:
            lines.append(f"")
            lines.append(f"⚠️  Detected Indicators:")
            for indicator in result['indicators']:
                lines.append(f"  - {indicator}")
        
        return "\n".join(lines)
    
    elif output_format == "table":
        # Simple table format
        return f"{result['classification']}\t{result['confidence']:.2%}\t{result['explanation']}"
    
    else:
        return json.dumps(result, indent=2)

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Smart Email Guardian - AI-powered spam and phishing detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze email from file
  python email_guard.py -f suspicious_email.txt
  
  # Analyze email from stdin
  echo "Your email content here" | python email_guard.py
  
  # Output in text format
  python email_guard.py -f email.txt -o text
  
  # Output in table format
  python email_guard.py -f email.txt -o table
        """
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Input file containing email content (default: stdin)'
    )
    
    parser.add_argument(
        '-o', '--output-format',
        choices=['json', 'text', 'table'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Smart Email Guardian v1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        # Read input
        email_content = read_input(args.file)
        
        if not email_content.strip():
            print("Error: No email content provided.", file=sys.stderr)
            sys.exit(1)
        
        # Analyze email
        print("🔍 Analyzing email content...", file=sys.stderr)
        result = analyze_email(email_content)
        
        # Output result
        output = format_output(result, args.output_format)
        print(output)
        
        # Exit with appropriate code based on classification
        if result['classification'] in ['phishing', 'spam']:
            sys.exit(2)  # Exit code 2 for suspicious content
        elif result['classification'] == 'invalid':
            sys.exit(1)  # Exit code 1 for invalid input
        else:
            sys.exit(0)  # Exit code 0 for legitimate content
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 