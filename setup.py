#!/usr/bin/env python3
"""
Setup script for Google Product Categories
Downloads the latest taxonomy from Google and processes it into nested set model format.
"""

import requests
import json
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class GoogleProductTaxonomyProcessor:
    """Processes Google Product Taxonomy data into nested set model format."""
    
    def __init__(self):
        self.taxonomy_url = "https://www.google.com/basepages/producttype/taxonomy.en-US.txt"
        self.categories = []
        self.next_id = 1
        self.next_position = 1
        
    def download_taxonomy(self) -> str:
        """Download the latest taxonomy from Google."""
        print(f"Downloading taxonomy from: {self.taxonomy_url}")
        
        try:
            response = requests.get(self.taxonomy_url, timeout=30)
            response.raise_for_status()
            
            # Save raw taxonomy
            with open("taxonomy.en-US.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(f"Downloaded {len(response.text)} characters")
            return response.text
            
        except requests.RequestException as e:
            print(f"Error downloading taxonomy: {e}")
            raise
    
    def parse_taxonomy(self, raw_taxonomy: str) -> List[Dict]:
        """Parse the raw taxonomy into a structured format."""
        print("Parsing taxonomy...")
        
        lines = raw_taxonomy.strip().split('\n')
        categories = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Split by ' > ' to get hierarchy
            parts = line.split(' > ')
            
            # Process each level
            for i, part in enumerate(parts):
                category_name = part  # Just the individual category name
                category_path = ' > '.join(parts[:i+1])  # Full path for parent lookup
                
                # Check if we already have this category by name
                existing = next((cat for cat in categories if cat['title'] == category_name), None)
                if existing:
                    continue
                
                # Find parent
                parent_id = None
                if i > 0:
                    parent_name = parts[i-1]  # Parent's individual name
                    parent = next((cat for cat in categories if cat['title'] == parent_name), None)
                    if parent:
                        parent_id = parent['id']
                
                category = {
                    'id': self.next_id,
                    'parent_id': parent_id,
                    'title': category_name,  # Just the name, not the full path
                    'depth': i + 1
                }
                
                categories.append(category)
                self.next_id += 1
        
        self.categories = categories
        print(f"Parsed {len(categories)} categories")
        return categories
    
    def build_nested_set(self) -> List[Dict]:
        """Convert parent-child model to nested set model."""
        print("Building nested set model...")
        
        # Initialize nested set values
        for cat in self.categories:
            cat['left'] = None
            cat['right'] = None
        
        # Build nested set using depth-first traversal
        def assign_positions(category_id: int, current_position: int) -> int:
            """Recursively assign left and right positions."""
            category = next(cat for cat in self.categories if cat['id'] == category_id)
            category['left'] = current_position
            current_position += 1
            
            # Process children
            children = [cat for cat in self.categories if cat['parent_id'] == category_id]
            for child in children:
                current_position = assign_positions(child['id'], current_position)
            
            category['right'] = current_position
            current_position += 1
            return current_position
        
        # Start with root categories
        root_categories = [cat for cat in self.categories if cat['parent_id'] is None]
        current_position = 1
        
        for root in root_categories:
            current_position = assign_positions(root['id'], current_position)
        
        # Verify all categories have positions
        for cat in self.categories:
            if cat['left'] is None or cat['right'] is None:
                print(f"Warning: Category {cat['id']} ({cat['title']}) missing nested set values")
        
        print(f"Built nested set model with positions 1 to {current_position - 1}")
        return self.categories
    
    def save_json(self, filename: str = "google_products_categories.json"):
        """Save categories to JSON file with nested set model."""
        print(f"Saving to {filename}...")
        
        # Prepare output with nested set values
        output_categories = []
        for cat in self.categories:
            output_cat = {
                'id': cat['id'],
                'parent_id': cat['parent_id'],
                'title': cat['title'],
                'left': cat['left'],
                'right': cat['right'],
                'depth': cat['depth']
            }
            output_categories.append(output_cat)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_categories, f, indent=4, ensure_ascii=False)
        
        print(f"Saved {len(output_categories)} categories to {filename}")
    
    def save_sql(self, filename: str = "google_product_categories.sql"):
        """Save categories to SQL file with nested set model."""
        print(f"Saving to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("-- Google Product Categories (Nested Set Model)\n")
            f.write(f"-- Generated on: {datetime.now().isoformat()}\n")
            f.write("-- Source: https://www.google.com/basepages/producttype/taxonomy.en-US.txt\n\n")
            
            f.write("CREATE TABLE IF NOT EXISTS google_product_categories (\n")
            f.write("    id INTEGER PRIMARY KEY,\n")
            f.write("    parent_id INTEGER,\n")
            f.write("    title TEXT NOT NULL,\n")
            f.write("    left INTEGER NOT NULL,\n")
            f.write("    right INTEGER NOT NULL,\n")
            f.write("    depth INTEGER NOT NULL,\n")
            f.write("    FOREIGN KEY (parent_id) REFERENCES google_product_categories(id)\n")
            f.write(");\n\n")
            
            f.write("-- Insert categories\n")
            for cat in self.categories:
                parent_id = cat['parent_id'] if cat['parent_id'] is not None else 'NULL'
                title = cat['title'].replace("'", "''")  # Escape single quotes
                
                f.write(f"INSERT INTO google_product_categories (id, parent_id, title, left, right, depth) VALUES ({cat['id']}, {parent_id}, '{title}', {cat['left']}, {cat['right']}, {cat['depth']});\n")
        
        print(f"Saved SQL schema and data to {filename}")
    
    def create_sqlite_database(self, filename: str = "google_product_categories.db"):
        """Create SQLite database with nested set model."""
        print(f"Creating SQLite database: {filename}...")
        
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        # Drop existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS google_product_categories")
        
        # Create table
        cursor.execute("""
            CREATE TABLE google_product_categories (
                id INTEGER PRIMARY KEY,
                parent_id INTEGER,
                title TEXT NOT NULL,
                left INTEGER NOT NULL,
                right INTEGER NOT NULL,
                depth INTEGER NOT NULL,
                FOREIGN KEY (parent_id) REFERENCES google_product_categories(id)
            )
        """)
        
        # Insert data
        for cat in self.categories:
            cursor.execute("""
                INSERT INTO google_product_categories (id, parent_id, title, left, right, depth)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cat['id'], cat['parent_id'], cat['title'], cat['left'], cat['right'], cat['depth']))
        
        # Create indexes for nested set model
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_left ON google_product_categories(left)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_right ON google_product_categories(right)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_parent_id ON google_product_categories(parent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_depth ON google_product_categories(depth)")
        
        conn.commit()
        conn.close()
        
        print(f"Created SQLite database with {len(self.categories)} categories")
    
    def generate_statistics(self):
        """Generate and display statistics about the taxonomy."""
        print("\n=== Taxonomy Statistics ===")
        print(f"Total categories: {len(self.categories)}")
        
        levels = {}
        root_count = 0
        
        for cat in self.categories:
            depth = cat['depth']
            levels[depth] = levels.get(depth, 0) + 1
            
            if cat['parent_id'] is None:
                root_count += 1
        
        print(f"Root categories: {root_count}")
        print(f"Maximum depth: {max(levels.keys()) if levels else 0}")
        
        # Nested set specific statistics
        if self.categories:
            min_left = min(cat['left'] for cat in self.categories)
            max_right = max(cat['right'] for cat in self.categories)
            print(f"Nested set range: {min_left} to {max_right}")
            print(f"Total positions used: {max_right}")
        
        print("\nCategories by depth:")
        for depth in sorted(levels.keys()):
            print(f"  Depth {depth}: {levels[depth]} categories")
    
    def run(self):
        """Run the complete setup process."""
        print("=== Google Product Categories Setup (Nested Set Model) ===")
        print(f"Started at: {datetime.now().isoformat()}")
        
        try:
            # Download latest taxonomy
            raw_taxonomy = self.download_taxonomy()
            
            # Parse into structured format
            self.parse_taxonomy(raw_taxonomy)
            
            # Build nested set model
            self.build_nested_set()
            
            # Generate all output formats
            self.save_json()
            self.save_sql()
            self.create_sqlite_database()
            
            # Show statistics
            self.generate_statistics()
            
            print(f"\nSetup completed successfully at: {datetime.now().isoformat()}")
            
        except Exception as e:
            print(f"Setup failed: {e}")
            raise


def main():
    """Main entry point."""
    processor = GoogleProductTaxonomyProcessor()
    processor.run()


if __name__ == "__main__":
    main()
