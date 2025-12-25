"""
MkDocs macros for automated carrot score calculation.

This module provides template functions that can be called from markdown files
to automatically calculate and display carrot scores based on quote data.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

def define_env(env):
    """Define the macro environment for MkDocs."""
    
    @env.macro
    def carrot_meter(evidence=0.5, consistency=0.5, transparency=0.5, sensationalism=0.5, monetization=0.5):
        """
        Generate a carrot meter display based on individual scores.
        
        Args:
            evidence: Evidence quality score (0-1)
            consistency: Logical consistency score (0-1) 
            transparency: Transparency score (0-1)
            sensationalism: Sensationalism score (0-1)
            monetization: Monetization ethics score (0-1)
        
        Returns:
            HTML string for carrot meter display
        """
        total_score = evidence + consistency + transparency + sensationalism + monetization
        
        # Generate carrot HTML
        filled_carrots = int(total_score)
        has_half = (total_score - filled_carrots) >= 0.5
        
        carrots_html = []
        
        # Add filled carrots
        for i in range(filled_carrots):
            carrots_html.append('<span class="carrot filled"></span>')
        
        # Add half carrot if needed
        if has_half:
            carrots_html.append('<span class="carrot half-filled"></span>')
            filled_carrots += 1
        
        # Add empty carrots
        for i in range(filled_carrots, 5):
            carrots_html.append('<span class="carrot"></span>')
        
        # Get category
        category, css_class = get_score_category(total_score)
        
        return f'''<div class="carrot-meter">
            <span class="carrot-meter-label">Carrot Seller Level:</span>
            {' '.join(carrots_html)}
            <span class="carrot-meter-score">({total_score:.1f}/5 🥕)</span>
            <span class="score-category {css_class}">{category}</span>
        </div>'''
    
    @env.macro
    def score_breakdown(evidence=0.5, consistency=0.5, transparency=0.5, sensationalism=0.5, monetization=0.5,
                        evidence_note="", consistency_note="", transparency_note="", sensationalism_note="", monetization_note=""):
        """
        Generate a compact score bar with collapsible details including notes.

        Returns:
            HTML string for compact score bar display
        """
        total_score = evidence + consistency + transparency + sensationalism + monetization
        category, css_class = get_score_category(total_score)

        # Short labels for the compact bar
        bar_items = [
            ("Evid", evidence),
            ("Cons", consistency),
            ("Trans", transparency),
            ("Sens", sensationalism),
            ("Ethics", monetization)
        ]

        # Full labels with notes for the details section
        detail_items = [
            ("Evidence", evidence, evidence_note or "Source credibility"),
            ("Consistency", consistency, consistency_note or "Position consistency"),
            ("Transparency", transparency, transparency_note or "Source citation"),
            ("Sensationalism", sensationalism, sensationalism_note or "Presentation tone"),
            ("Ethics", monetization, monetization_note or "Conflict disclosure")
        ]

        # Build compact bar items
        bar_html = []
        for label, score in bar_items:
            bar_html.append(f'''<div class="score-bar-item"><span class="label">{label}</span><span class="value">{score:.1f}</span></div>''')

        # Build detail rows with notes
        detail_html = []
        for name, score, note in detail_items:
            detail_html.append(f'''<div class="score-detail-row"><span class="detail-name">{name}</span><span class="detail-value">{score:.1f}</span><span class="detail-note">{note}</span></div>''')

        return f'''<div class="score-breakdown">
<div class="score-bar">
{''.join(bar_html)}
<div class="score-bar-total"><span class="total-value">{total_score:.1f}/5</span><span class="score-category {css_class}">{category}</span></div>
</div>
<details class="score-details-toggle">
<summary>Scoring rationale</summary>
<div class="score-details-content">
<div class="score-details-grid">
{''.join(detail_html)}
</div>
</div>
</details>
</div>'''
    
    @env.macro 
    def analyze_quotes(quotes_text=""):
        """
        Analyze quotes in the current page and suggest scores.
        This is a simplified version - in practice you'd parse the actual quotes.
        
        Returns:
            Dictionary with suggested scores
        """
        # This is a placeholder - would need to parse actual quote data
        # For now, return default scores
        return {
            'evidence': 0.5,
            'consistency': 0.5, 
            'transparency': 0.5,
            'sensationalism': 0.5,
            'monetization': 0.5
        }
    
    @env.macro
    def last_updated():
        """
        Get the last git commit date for the current file.
        Returns a formatted date string.
        """
        try:
            # Get the current page's source file path
            page = env.variables.get('page')
            if not page or not hasattr(page, 'file') or not page.file:
                return "Unknown"
            
            file_path = page.file.src_path
            
            # Get last commit date for this file using git
            cmd = ['git', 'log', '-1', '--format=%cd', '--date=format:%B %d, %Y', '--', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=env.conf['docs_dir'])
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                # Fallback to current date if git fails
                return datetime.now().strftime("%B %d, %Y")
                
        except Exception as e:
            # Fallback to current date if anything fails
            return datetime.now().strftime("%B %d, %Y")

def get_score_category(total_score: float) -> Tuple[str, str]:
    """Get score category and CSS class."""
    if total_score <= 0.5:
        return "Highly Credible", "highly-credible"
    elif total_score <= 1.5:
        return "Generally Reliable", "generally-reliable"
    elif total_score <= 2.5:
        return "Mixed Record", "mixed-record"
    elif total_score <= 3.5:
        return "Questionable", "questionable"
    elif total_score <= 4.5:
        return "Major Carrot Seller", "major-carrot-seller"
    else:
        return "Maximum Carrot Seller", "maximum-carrot-seller"

def on_post_build(env):
    """Run after the site is built to generate data exports.

    Skips export during 'mkdocs serve' to prevent infinite rebuild loops,
    since exports write to docs/data/ which triggers file change detection.
    """
    import os

    # Skip during mkdocs serve - check environment variable
    if os.environ.get('MKDOCS_SERVE'):
        return

    try:
        # Get the script directory
        script_dir = Path(__file__).parent
        export_script = script_dir / 'export_data.py'

        # Run the export script
        result = subprocess.run([sys.executable, str(export_script)],
                              capture_output=True, text=True, check=True)

        print("Data export completed successfully")
        if result.stdout:
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Data export failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error during data export: {e}")