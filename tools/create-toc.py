#!/usr/bin/env python3
"""
This script is used to create a table of contents for the README.md file.
It scans all markdown files in the current directory and its subdirectories,
and creates a table of contents based on the categories and titles of the files.
"""
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


def extract_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            print(frontmatter)
            # Remove frontmatter from content
            content_without_frontmatter = content[match.end():]
            return frontmatter or {}, content_without_frontmatter
        except yaml.YAMLError:
            return {}, content
    return {}, content


def extract_title(content: str) -> str:
    """Extract title from markdown content (first H1 heading)."""
    lines = content.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled"


def get_markdown_files(directory: str) -> List[Path]:
    """Get all markdown files in directory except README.md."""
    md_files = []
    for file_path in Path(directory).glob('*.md'):
        if file_path.name != 'README.md':
            md_files.append(file_path)
    return md_files


def parse_markdown_files(directory: str) -> List[Dict]:
    """Parse all markdown files and extract their metadata."""
    files_data = []
    
    for file_path in get_markdown_files(directory):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, content_without_frontmatter = extract_frontmatter(content)
            title = extract_title(content_without_frontmatter)
            
            # Get categories from frontmatter
            categories = frontmatter.get('categories', [])
            if isinstance(categories, str):
                categories = [categories]
            
            files_data.append({
                'file': file_path.name,
                'title': title,
                'categories': categories,
                'path': str(file_path)
            })
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return files_data


def organize_by_categories(files_data: List[Dict]) -> Dict:
    """Organize files by their categories."""
    organized = {}
    
    for file_data in files_data:
        categories = file_data['categories']
        
        if not categories:
            # If no categories, put in "Other"
            if "Other" not in organized:
                organized["Other"] = []
            organized["Other"].append(file_data)
        else:
            for category in categories:
                if isinstance(category, dict):
                    # Handle nested categories like {'Linux': ['Security']}
                    for main_category, subcategories in category.items():
                        if main_category not in organized:
                            organized[main_category] = {}
                        
                        if isinstance(subcategories, list):
                            for subcategory in subcategories:
                                if subcategory not in organized[main_category]:
                                    organized[main_category][subcategory] = []
                                organized[main_category][subcategory].append(file_data)
                        else:
                            # If subcategories is not a list, treat it as a single subcategory
                            if subcategories not in organized[main_category]:
                                organized[main_category][subcategories] = []
                            organized[main_category][subcategories].append(file_data)
                else:
                    # Handle simple string categories
                    if category not in organized:
                        organized[category] = []
                    organized[category].append(file_data)
    
    return organized


def generate_toc(organized_files: Dict) -> str:
    INDENT = 2
    """Generate table of contents markdown."""
    toc_lines = ["## Table of Contents\n"]
    toc_lines.append("\n") # Markdown linter is happy
    # Sort categories alphabetically
    sorted_categories = sorted(organized_files.keys())
    
    for category in sorted_categories:
        if category == "Other":
            continue  # Skip other for now
        
        toc_lines.append(f"* {category}\n")
        
        # Check if this category has subcategories (nested structure)
        if isinstance(organized_files[category], dict):
            # Handle nested categories
            sorted_subcategories = sorted(organized_files[category].keys())
            for subcategory in sorted_subcategories:
                toc_lines.append(f"{' ' * INDENT}* {subcategory}\n")
                files = sorted(organized_files[category][subcategory], key=lambda x: x['title'])
                for file_data in files:
                    toc_lines.append(f"{' ' * INDENT}*  [{file_data['title']}]({file_data['file']})\n")
                toc_lines.append("")  # Empty line for spacing
        else:
            # Handle simple categories (list of files)
            files = sorted(organized_files[category], key=lambda x: x['title'])
            for file_data in files:
                toc_lines.append(f"{' ' * INDENT}* [{file_data['title']}]({file_data['file']})\n")
            toc_lines.append("")  # Empty line for spacing
    
    # Add other files at the end if any
    if "Other" in organized_files and organized_files["Other"]:
        toc_lines.append("* Other\n")
        files = sorted(organized_files["Other"], key=lambda x: x['title'])
        for file_data in files:
            toc_lines.append(f"{' ' * INDENT}*  [{file_data['title']}]({file_data['file']})\n")
    
    return "".join(toc_lines)


def update_readme_toc(readme_path: str, toc_content: str):
    """Update README.md with the new table of contents."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # Check if Table of Contents section already exists
        toc_pattern = r'(## Table of Contents\n.*?)(?=\n## |\n$|$)'
        match = re.search(toc_pattern, readme_content, re.DOTALL)
        
        if match:
            # Replace existing TOC
            new_content = re.sub(toc_pattern, toc_content, readme_content, flags=re.DOTALL)
        else:
            # Add TOC after the description section
            # Find the end of the description (after "Why?" section)
            desc_end = readme_content.find("## Why?")
            if desc_end == -1:
                new_content = readme_content.rstrip() + "\n\n" + toc_content
            else:
                new_content = readme_content[:desc_end] + "\n\n" + toc_content + "\n" + readme_content[desc_end:]
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Updated {readme_path} with new table of contents")
        
    except Exception as e:
        print(f"Error updating README: {e}")


def main():
    """Main function to generate and update table of contents."""
    # Get the directory where the script is located (should be the project root)
    script_dir = Path(__file__).parent.parent
    readme_path = script_dir / "README.md"
    
    print(f"Scanning directory: {script_dir}")
    
    # Parse all markdown files
    files_data = parse_markdown_files(script_dir)
    
    if not files_data:
        print("No markdown files found (excluding README.md)")
        return
    
    print(f"Found {len(files_data)} markdown files")
    
    organized_files = organize_by_categories(files_data)
    
    # Generate table of contents
    toc_content = generate_toc(organized_files)
    
    update_readme_toc(str(readme_path), toc_content)
    
    print("\nSummary:")
    for category, files in organized_files.items():
        print(f"  {category}: {len(files)} files")
    
    print(f"\n** Table of contents generated successfully! **")


if __name__ == "__main__":
    main()
