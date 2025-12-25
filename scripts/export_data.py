#!/usr/bin/env python3
"""
Export all tracked data to CSV and JSON formats.
This script runs during the build process to generate downloadable datasets.
"""

import csv
import json
import os
from pathlib import Path
from datetime import datetime
import re

def extract_person_data(file_path):
    """Extract structured data from a person's markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract person name from filename
        name = file_path.stem.replace('-', ' ').title()
        if name == 'Example Person':
            name = 'Dr. Alex Thompson'
        
        # Extract carrot meter scores using regex
        carrot_pattern = r'carrot_meter\(evidence=([\d.]+),\s*consistency=([\d.]+),\s*transparency=([\d.]+),\s*sensationalism=([\d.]+),\s*monetization=([\d.]+)\)'
        carrot_match = re.search(carrot_pattern, content)
        
        if not carrot_match:
            return None
            
        evidence = float(carrot_match.group(1))
        consistency = float(carrot_match.group(2))
        transparency = float(carrot_match.group(3))
        sensationalism = float(carrot_match.group(4))
        monetization = float(carrot_match.group(5))
        total_score = evidence + consistency + transparency + sensationalism + monetization
        
        # Determine category
        if total_score <= 0.5:
            category = "Highly Credible"
        elif total_score <= 1.5:
            category = "Generally Reliable"
        elif total_score <= 2.5:
            category = "Mixed Record"
        elif total_score <= 3.5:
            category = "Questionable"
        elif total_score <= 4.5:
            category = "Major Carrot Seller"
        else:
            category = "Maximum Carrot Seller"
        
        # Extract basic info
        info_pattern = r'<span class="info-label">([^:]+):</span>\s*<span>([^<]+)</span>'
        info_matches = re.findall(info_pattern, content)
        info_dict = {match[0]: match[1] for match in info_matches}
        
        # Extract quotes
        quotes = []
        quote_pattern = r'<div class="quote-box">(.*?)</div>\s*(?=<div class="quote-box">|</div>|$)'
        quote_matches = re.findall(quote_pattern, content, re.DOTALL)
        
        for quote_content in quote_matches:
            date_match = re.search(r'<div class="quote-date">([^<]+)</div>', quote_content)
            source_match = re.search(r'<div class="quote-source">Source: ([^<]+)</div>', quote_content)
            text_match = re.search(r'<div class="quote-text">\s*"?([^<]+)"?\s*</div>', quote_content)
            fact_check_match = re.search(r'<div class="fact-check ([^"]+)">.*?<div class="fact-check-label">Fact Check: ([^<]+)</div>', quote_content, re.DOTALL)
            
            if date_match and source_match and text_match:
                quote_data = {
                    'date': date_match.group(1).strip(),
                    'source': source_match.group(1).strip(),
                    'text': text_match.group(1).strip().strip('"'),
                    'fact_check_status': fact_check_match.group(2).strip() if fact_check_match else 'UNKNOWN',
                    'fact_check_class': fact_check_match.group(1).strip() if fact_check_match else 'unknown'
                }
                quotes.append(quote_data)
        
        return {
            'name': name,
            'title': info_dict.get('Title', ''),
            'known_for': info_dict.get('Known For', ''),
            'active_since': info_dict.get('Active Since', ''),
            'platform': info_dict.get('Primary Platform', ''),
            'affiliations': info_dict.get('Affiliations', ''),
            'evidence_score': evidence,
            'consistency_score': consistency,
            'transparency_score': transparency,
            'sensationalism_score': sensationalism,
            'monetization_score': monetization,
            'total_score': round(total_score, 1),
            'category': category,
            'quotes': quotes,
            'profile_url': f"people/{file_path.stem}/"
        }
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def export_to_csv(data, output_path):
    """Export data to CSV format."""
    # Person-level CSV
    person_csv_path = output_path / 'carrot-sellers-people.csv'
    with open(person_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name', 'Title', 'Known For', 'Active Since', 'Primary Platform', 'Affiliations',
            'Evidence Score', 'Consistency Score', 'Transparency Score', 'Sensationalism Score', 'Monetization Score',
            'Total Score', 'Category', 'Profile URL', 'Total Quotes'
        ])
        
        for person in data:
            writer.writerow([
                person['name'], person['title'], person['known_for'], person['active_since'],
                person['platform'], person['affiliations'], person['evidence_score'],
                person['consistency_score'], person['transparency_score'], person['sensationalism_score'],
                person['monetization_score'], person['total_score'], person['category'],
                person['profile_url'], len(person['quotes'])
            ])
    
    # Quotes-level CSV
    quotes_csv_path = output_path / 'carrot-sellers-quotes.csv'
    with open(quotes_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Person Name', 'Quote Date', 'Source', 'Quote Text', 'Fact Check Status', 'Person Total Score', 'Person Category'
        ])
        
        for person in data:
            for quote in person['quotes']:
                writer.writerow([
                    person['name'], quote['date'], quote['source'], quote['text'],
                    quote['fact_check_status'], person['total_score'], person['category']
                ])
    
    # Combined CSV
    combined_csv_path = output_path / 'carrot-sellers-data.csv'
    with open(combined_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Person Name', 'Title', 'Total Score', 'Category', 'Quote Date', 'Source', 'Quote Text', 'Fact Check Status'
        ])
        
        for person in data:
            if person['quotes']:
                for quote in person['quotes']:
                    writer.writerow([
                        person['name'], person['title'], person['total_score'], person['category'],
                        quote['date'], quote['source'], quote['text'], quote['fact_check_status']
                    ])
            else:
                # Include person even if no quotes
                writer.writerow([
                    person['name'], person['title'], person['total_score'], person['category'],
                    '', '', '', ''
                ])

def export_to_json(data, output_path):
    """Export data to JSON format."""
    json_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_people': len(data),
            'total_quotes': sum(len(person['quotes']) for person in data),
            'source': 'Carrot Sellers - UFO/UAP Claims Tracker'
        },
        'people': data
    }
    
    json_path = output_path / 'carrot-sellers-data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

def main():
    """Main export function."""
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / 'docs'
    people_dir = docs_dir / 'people'
    
    # Create data output directory
    data_dir = docs_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Find all person markdown files
    person_files = list(people_dir.glob('*.md'))
    person_files = [f for f in person_files if f.name not in ['index.md', 'TEMPLATE.md']]
    
    # Extract data from all person files
    all_data = []
    for file_path in person_files:
        person_data = extract_person_data(file_path)
        if person_data:
            all_data.append(person_data)
    
    # Sort by total score (ascending - least carrots first)
    all_data.sort(key=lambda x: x['total_score'])
    
    # Export to both formats
    export_to_csv(all_data, data_dir)
    export_to_json(all_data, data_dir)
    
    print(f"✅ Exported data for {len(all_data)} people")
    print(f"📊 CSV files: {data_dir}/carrot-sellers-*.csv")
    print(f"💾 JSON file: {data_dir}/carrot-sellers-data.json")

if __name__ == '__main__':
    main()