#!/usr/bin/env python3
"""
Carrot Sellers Score Calculator

This script analyzes quote fact-check data and calculates carrot scores automatically.
It scans person markdown files and updates scores based on quote accuracy.
"""

import re
import os
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

class CarrotScoreCalculator:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.people_dir = self.docs_dir / "people"
        
    def parse_person_file(self, file_path: Path) -> Dict:
        """Parse a person's markdown file and extract scoring data."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        person_data = {
            'name': self.extract_name(content),
            'quotes': self.extract_quotes(content),
            'manual_scores': self.extract_manual_scores(content),
            'file_path': file_path
        }
        
        return person_data
    
    def extract_name(self, content: str) -> str:
        """Extract person name from content."""
        name_match = re.search(r'<h1>(.*?)</h1>', content)
        return name_match.group(1) if name_match else "Unknown"
    
    def extract_quotes(self, content: str) -> List[Dict]:
        """Extract all quotes and their fact-check status."""
        quotes = []
        
        # Find all quote boxes
        quote_pattern = r'<div class="quote-box">(.*?)</div>\s*</div>'
        quote_matches = re.findall(quote_pattern, content, re.DOTALL)
        
        for quote_match in quote_matches:
            quote_data = {
                'date': self.extract_quote_date(quote_match),
                'source': self.extract_quote_source(quote_match),
                'text': self.extract_quote_text(quote_match),
                'fact_check': self.extract_fact_check(quote_match)
            }
            quotes.append(quote_data)
        
        return quotes
    
    def extract_quote_date(self, quote_content: str) -> str:
        """Extract date from quote content."""
        date_match = re.search(r'<div class="quote-date">(.*?)</div>', quote_content)
        return date_match.group(1) if date_match else ""
    
    def extract_quote_source(self, quote_content: str) -> str:
        """Extract source from quote content."""
        source_match = re.search(r'<div class="quote-source">Source: (.*?)</div>', quote_content)
        return source_match.group(1) if source_match else ""
    
    def extract_quote_text(self, quote_content: str) -> str:
        """Extract quote text."""
        text_match = re.search(r'<div class="quote-text">(.*?)</div>', quote_content, re.DOTALL)
        return text_match.group(1).strip() if text_match else ""
    
    def extract_fact_check(self, quote_content: str) -> Dict:
        """Extract fact-check status and reasoning."""
        # Look for fact-check class and content
        fact_check_match = re.search(r'<div class="fact-check ([^"]+)">', quote_content)
        status = fact_check_match.group(1) if fact_check_match else "unverified"
        
        # Extract the explanation
        explanation_match = re.search(r'<div class="fact-check-label">.*?</div>\s*(.*?)</div>', quote_content, re.DOTALL)
        explanation = explanation_match.group(1).strip() if explanation_match else ""
        
        return {
            'status': status,  # true, false, unverified
            'explanation': explanation
        }
    
    def extract_manual_scores(self, content: str) -> Dict:
        """Extract manually set scores from the scoring breakdown."""
        scores = {}
        
        # Extract individual criterion scores
        criteria_pattern = r'<span>([0-9.]+)/1</span>'
        criteria_matches = re.findall(criteria_pattern, content)
        
        if len(criteria_matches) >= 5:
            scores = {
                'evidence_quality': float(criteria_matches[0]),
                'logical_consistency': float(criteria_matches[1]),
                'transparency': float(criteria_matches[2]),
                'sensationalism': float(criteria_matches[3]),
                'monetization_ethics': float(criteria_matches[4])
            }
        
        return scores
    
    def calculate_auto_scores(self, quotes: List[Dict], manual_scores: Dict) -> Dict:
        """Calculate scores based on quote analysis."""
        if not quotes:
            return manual_scores
        
        # Analyze quotes for automatic scoring hints
        total_quotes = len(quotes)
        false_quotes = sum(1 for q in quotes if q['fact_check']['status'] == 'false')
        true_quotes = sum(1 for q in quotes if q['fact_check']['status'] == 'true')
        unverified_quotes = sum(1 for q in quotes if q['fact_check']['status'] == 'unverified')
        
        # Calculate evidence quality based on quote accuracy
        if total_quotes > 0:
            false_ratio = false_quotes / total_quotes
            evidence_score = min(1.0, false_ratio * 2)  # More false claims = higher carrot score
        else:
            evidence_score = manual_scores.get('evidence_quality', 0.5)
        
        # For now, use manual scores for other criteria
        auto_scores = {
            'evidence_quality': evidence_score,
            'logical_consistency': manual_scores.get('logical_consistency', 0.5),
            'transparency': manual_scores.get('transparency', 0.5),
            'sensationalism': manual_scores.get('sensationalism', 0.5),
            'monetization_ethics': manual_scores.get('monetization_ethics', 0.5)
        }
        
        return auto_scores
    
    def generate_carrot_html(self, score: float) -> str:
        """Generate HTML for carrot meter display."""
        filled_carrots = int(score)
        half_carrot = (score - filled_carrots) >= 0.5
        
        html_parts = []
        
        # Filled carrots
        for i in range(filled_carrots):
            html_parts.append('<span class="carrot filled"></span>')
        
        # Half carrot
        if half_carrot:
            html_parts.append('<span class="carrot half-filled"></span>')
            filled_carrots += 1
        
        # Empty carrots
        for i in range(filled_carrots, 5):
            html_parts.append('<span class="carrot"></span>')
        
        return ''.join(html_parts)
    
    def get_score_category(self, total_score: float) -> Tuple[str, str]:
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
    
    def update_person_file(self, person_data: Dict):
        """Update person file with calculated scores."""
        # For now, just print what we would update
        scores = person_data.get('auto_scores', person_data['manual_scores'])
        total_score = sum(scores.values())
        category, css_class = self.get_score_category(total_score)
        
        print(f"\n=== {person_data['name']} ===")
        print(f"Total quotes: {len(person_data['quotes'])}")
        print(f"Manual scores: {person_data['manual_scores']}")
        print(f"Auto scores: {person_data.get('auto_scores', 'Same as manual')}")
        print(f"Total score: {total_score:.1f}/5.0")
        print(f"Category: {category}")
        print(f"Carrot HTML: {self.generate_carrot_html(total_score)}")
    
    def process_all_people(self):
        """Process all people files and calculate scores."""
        if not self.people_dir.exists():
            print(f"People directory not found: {self.people_dir}")
            return
        
        for md_file in self.people_dir.glob("*.md"):
            if md_file.name == "index.md":
                continue
                
            try:
                person_data = self.parse_person_file(md_file)
                if person_data['manual_scores']:
                    auto_scores = self.calculate_auto_scores(
                        person_data['quotes'], 
                        person_data['manual_scores']
                    )
                    person_data['auto_scores'] = auto_scores
                
                self.update_person_file(person_data)
                
            except Exception as e:
                print(f"Error processing {md_file}: {e}")

def main():
    calculator = CarrotScoreCalculator()
    calculator.process_all_people()

if __name__ == "__main__":
    main()