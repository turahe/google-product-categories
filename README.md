# Google Product Categories

[![CI](https://github.com/turahe/google-product-categories/workflows/CI/badge.svg)](https://github.com/turahe/google-product-categories/actions)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive repository containing Google Product Taxonomy data in multiple formats, with an automated setup script to download and process the latest taxonomy from Google's official source.

## What is Google Product Taxonomy?

The Google Product Taxonomy is a hierarchical classification system used by Google Shopping and other Google services to categorize products. It helps ensure products are properly classified for better search results and advertising performance.

## Features

- **Automated Download**: Downloads the latest taxonomy directly from Google's official source
- **Multiple Formats**: Generates JSON, SQL, text, and SQLite database formats
- **Hierarchical Structure**: Maintains parent-child relationships with proper IDs
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Statistics**: Provides detailed analysis of the taxonomy structure

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection to download the taxonomy

### Windows Users

1. **Using Batch File (Recommended)**:
   ```
   setup.bat
   ```

2. **Using PowerShell**:
   ```
   .\setup.ps1
   ```

### macOS/Linux Users

1. Make the script executable:
   ```bash
   chmod +x setup.sh
   ```

2. Run the setup:
   ```bash
   ./setup.sh
   ```

### Manual Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Python script:
   ```bash
   python setup.py
   ```

## What the Setup Script Does

1. **Downloads** the latest taxonomy from [Google's official source](https://www.google.com/basepages/producttype/taxonomy.en-US.txt)
2. **Parses** the hierarchical structure into a structured format
3. **Builds** a nested set model for efficient tree traversal
4. **Generates** multiple output formats:
   - `google_products_categories.json` - JSON format with nested set model (left/right positions)
   - `google_product_categories.sql` - SQL schema with nested set columns and insert statements
   - `taxonomy-with-ids.en-US.txt` - Human-readable text format with nested set positions
   - `google_product_categories.db` - SQLite database with nested set indexes
5. **Provides** detailed statistics about the taxonomy structure including nested set ranges

## Output Files

### JSON Format (`google_products_categories.json`)
```json
[
    {
        "id": 1,
        "parent_id": null,
        "title": "Animals & Pet Supplies",
        "left": 1,
        "right": 100,
        "depth": 1
    },
    {
        "id": 2,
        "parent_id": 1,
        "title": "Live Animals",
        "left": 2,
        "right": 15,
        "depth": 2
    }
]
```

### SQL Format (`google_product_categories.sql`)
- Complete table schema with nested set model (left, right)
- Foreign key constraints for parent relationships
- All category data as INSERT statements with nested set positions
- Optimized for database import and tree traversal queries

### Text Format (`taxonomy-with-ids.en-US.txt`)
```
# Google Product Taxonomy with Nested Set Model
# Generated on: 2024-01-XX
# Source: https://www.google.com/basepages/producttype/taxonomy.en-US.txt

   1 | [   1-100] | Animals & Pet Supplies
     2 | [   2- 15] | Animals & Pet Supplies > Live Animals
     4 | [  16- 99] | Animals & Pet Supplies > Pet Supplies
       5 | [  17- 25] | Animals & Pet Supplies > Pet Supplies > Bird Supplies
```

### SQLite Database (`google_product_categories.db`)
- Full relational database with nested set model columns
- Foreign key constraints for data integrity
- Optimized indexes for nested set queries (left, right)
- Efficient tree traversal and hierarchical queries

## Project Structure

```
google-product-categories/
├── setup.py                 # Main Python setup script (Nested Set Model)
├── requirements.txt         # Python dependencies
├── setup.bat               # Windows batch script
├── setup.ps1               # Windows PowerShell script
├── setup.sh                # Unix/Linux/macOS shell script
├── google_products_categories.json  # JSON output with nested set
├── google_product_categories.sql    # SQL output with nested set schema (left, right, depth)
├── taxonomy-with-ids.en-US.txt     # Text output with nested set positions
├── google_product_categories.db     # SQLite database with nested set
├── taxonomy.en-US.txt              # Raw downloaded taxonomy
└── README.md                       # This file
```

## Nested Set Model Benefits

The nested set model provides several advantages over simple parent-child relationships:

- **Efficient Tree Traversal**: Find all descendants or ancestors with simple range queries
- **Fast Hierarchical Queries**: Get entire subtrees without recursive joins
- **Easy Level Calculations**: Determine depth and relationships quickly
- **Performance**: Optimized for read-heavy operations on hierarchical data

## Usage Examples

### Query the Database (Nested Set Model)
```python
import sqlite3

conn = sqlite3.connect('google_product_categories.db')
cursor = conn.cursor()

# Find all root categories
cursor.execute("SELECT * FROM google_product_categories WHERE parent_id IS NULL")
root_categories = cursor.fetchall()

# Find all descendants of "Animals & Pet Supplies" using nested set
cursor.execute("""
    SELECT * FROM google_product_categories 
    WHERE left > (SELECT left FROM google_product_categories WHERE title = 'Animals & Pet Supplies')
    AND right < (SELECT right FROM google_product_categories WHERE title = 'Animals & Pet Supplies')
    ORDER BY left
""")
pet_categories = cursor.fetchall()

# Find all ancestors of a category
cursor.execute("""
    SELECT * FROM google_product_categories 
    WHERE left < (SELECT left FROM google_product_categories WHERE title = 'Bird Food')
    AND right > (SELECT right FROM google_product_categories WHERE title = 'Bird Food')
    ORDER BY left
""")
ancestors = cursor.fetchall()

# Get categories at a specific depth
cursor.execute("SELECT * FROM google_product_categories WHERE depth = 3 ORDER BY left")
depth3_categories = cursor.fetchall()

conn.close()
```

### Load JSON Data (Nested Set Model)
```python
import json

with open('google_products_categories.json', 'r') as f:
    categories = json.load(f)

# Find category by title
def find_category(title):
    return next((cat for cat in categories if cat['title'] == title), None)

# Get all descendants using nested set model
def get_descendants(category_title):
    category = find_category(category_title)
    if not category:
        return []
    
    return [cat for cat in categories 
            if cat['left'] > category['left'] and cat['right'] < category['right']]

# Get all ancestors using nested set model
def get_ancestors(category_title):
    category = find_category(category_title)
    if not category:
        return []
    
    return [cat for cat in categories 
            if cat['left'] < category['left'] and cat['right'] > category['right']]

# Get siblings (same parent)
def get_siblings(category_title):
    category = find_category(category_title)
    if not category or not category['parent_id']:
        return []
    
    parent = find_category_by_id(category['parent_id'])
    if not parent:
        return []
    
    return [cat for cat in categories 
            if cat['parent_id'] == category['parent_id'] and cat['id'] != category['id']]

# Find category by ID
def find_category_by_id(category_id):
    return next((cat for cat in categories if cat['id'] == category_id), None)
```

## Updating the Taxonomy

To get the latest taxonomy data, simply run the setup script again:

```bash
python setup.py
```

The script will:
- Download the latest version from Google
- Regenerate all output formats
- Preserve the same ID structure for consistency

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Data Source

The taxonomy data is sourced from Google's official Product Taxonomy:
- **URL**: https://www.google.com/basepages/producttype/taxonomy.en-US.txt
- **Format**: Hierarchical text with ` > ` separators
- **Updated**: Periodically by Google

## Disclaimer

This project is not affiliated with Google. The taxonomy data is sourced from Google's public taxonomy file and is used for educational and development purposes.