#!/usr/bin/env python3
"""
Generate llms.txt and llms-full.txt from any markdown documentation repository.
Agnostic script that works with any GitHub repo containing markdown files.
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
import argparse
from urllib.parse import urlparse


def run_command(cmd, cwd=None, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        return None


def extract_repo_info(repo_url):
    """Extract owner and repo name from GitHub URL."""
    # Handle both git and https URLs
    patterns = [
        r'github\.com[:/]([^/]+)/([^/.]+)',
        r'([^/]+)/([^/.]+?)(?:\.git)?$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, repo_url)
        if match:
            owner = match.group(1)
            repo = match.group(2).replace('.git', '')
            return owner, repo
    
    return None, None


def fetch_github_about(owner, repo):
    """Fetch the About/Description from GitHub repository."""
    try:
        import urllib.request
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        req = urllib.request.Request(api_url)
        req.add_header('User-Agent', 'llms-txt-generator')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            homepage = data.get('homepage', '').strip()
            description = data.get('description', '').strip()
            
            return {
                'homepage': homepage if homepage else None,
                'description': description if description else None,
                'name': data.get('name', repo)
            }
    except Exception as e:
        print(f"  ⚠ Could not fetch GitHub metadata: {e}")
        return {'homepage': None, 'description': None, 'name': repo}


def clone_repo(repo_url, target_dir, branch="main"):
    """Clone the GitHub repository."""
    print(f"Cloning repository from {repo_url}...")
    print(f"Branch: {branch}")
    
    # First try to clone with specified branch
    cmd = ["git", "clone", "--depth", "1", "--branch", branch, repo_url, target_dir]
    result = run_command(cmd)
    
    if result is None:
        # If branch doesn't exist, try master
        print(f"  ⚠ Branch '{branch}' not found, trying 'master'...")
        cmd = ["git", "clone", "--depth", "1", "--branch", "master", repo_url, target_dir]
        result = run_command(cmd)
        
        if result is None:
            # If still fails, try default branch
            print(f"  ⚠ Trying default branch...")
            cmd = ["git", "clone", "--depth", "1", repo_url, target_dir]
            result = run_command(cmd)
            
            if result is None:
                print(f"✗ Failed to clone repository")
                return False
    
    print(f"✓ Repository cloned to {target_dir}")
    return True


def collect_markdown_files(docs_dir, root_folder="."):
    """Collect all markdown files from the specified directory."""
    docs_path = Path(docs_dir) / root_folder
    
    if not docs_path.exists():
        print(f"✗ Directory not found: {docs_path}")
        return []
    
    # Collect all .md files recursively
    md_files = []
    for md_file in sorted(docs_path.rglob("*.md")):
        # Skip common non-documentation files
        if any(skip in md_file.parts for skip in ['.github', 'node_modules', '.git']):
            continue
        md_files.append(md_file)
    
    print(f"✓ Found {len(md_files)} markdown files in {root_folder}")
    return md_files, docs_path


def extract_first_paragraph(content):
    """Extract the first meaningful paragraph from markdown content."""
    lines = content.strip().split('\n')
    paragraph = []
    
    for line in lines:
        line = line.strip()
        # Skip title lines, empty lines, and special markers
        if line.startswith('#') or not line or line.startswith('---') or line.startswith('<!--'):
            continue
        
        # Start collecting paragraph
        if line and not paragraph:
            paragraph.append(line)
        elif line and paragraph:
            paragraph.append(line)
        elif not line and paragraph:
            break  # End of first paragraph
    
    result = ' '.join(paragraph)
    # Limit length
    if len(result) > 300:
        result = result[:297] + "..."
    return result if result else "Documentation section."


def extract_title(content):
    """Extract the first H1 title from the markdown."""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return None


def get_relative_path(file_path, root_path):
    """Get the relative path from root for URL generation."""
    try:
        rel_path = file_path.relative_to(root_path)
        # Convert to URL path (forward slashes, no extension)
        url_path = str(rel_path.with_suffix('')).replace(os.sep, '/')
        return url_path
    except ValueError:
        return file_path.stem


def generate_llms_txt(md_files, root_path, output_file, project_name, base_url=None, version=None, description=None):
    """Generate concise llms.txt index file."""
    print(f"\nGenerating {output_file} (index)...")
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # Write header
        title = f"{project_name} Documentation"
        if version:
            title += f" - {version}"
        
        out.write(f"# {title}\n\n")
        
        if description:
            out.write(f"> {description}\n\n")
        
        if base_url:
            out.write(f"Website: {base_url}\n")
        
        out.write("\n")
        
        # Write index of all documents
        out.write("## Documentation Index\n\n")
        
        # Process each markdown file to create index
        file_info = []
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                url_path = get_relative_path(md_file, root_path)
                title = extract_title(content) or url_path.replace('/', ' > ').replace('-', ' ').title()
                desc = extract_first_paragraph(content)
                
                # Generate full URL if base_url provided
                if base_url:
                    full_url = f"{base_url.rstrip('/')}/{url_path}"
                else:
                    full_url = url_path
                
                file_info.append({
                    'path': url_path,
                    'title': title,
                    'description': desc,
                    'url': full_url
                })
            except Exception as e:
                print(f"  ✗ Error processing {md_file.name}: {e}")
                continue
        
        # Write the index
        for info in file_info:
            out.write(f"### [{info['title']}]({info['url']})\n\n")
            out.write(f"{info['description']}\n\n")
        
        out.write("\n---\n\n")
        out.write("## Notes\n\n")
        out.write("- For complete documentation content, see `llms-full.txt`\n")
        out.write(f"- Total sections: {len(file_info)}\n")
    
    print(f"✓ llms.txt generated successfully")
    size_kb = os.path.getsize(output_file) / 1024
    print(f"  File size: {size_kb:.2f} KB")


def generate_llms_full_txt(md_files, root_path, output_file, project_name, base_url=None, version=None, description=None):
    """Generate complete llms-full.txt with all documentation."""
    print(f"\nGenerating {output_file} (full documentation)...")
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # Write header
        title = f"{project_name} Documentation - Complete"
        if version:
            title += f" - {version}"
        
        out.write(f"# {title}\n\n")
        
        if description:
            out.write(f"> {description}\n\n")
        
        if base_url:
            out.write(f"Website: {base_url}\n")
        
        out.write("\n---\n\n")
        
        # Process each markdown file
        for idx, md_file in enumerate(md_files, 1):
            print(f"  [{idx}/{len(md_files)}] Processing {md_file.name}...")
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                url_path = get_relative_path(md_file, root_path)
                title = extract_title(content) or url_path.replace('/', ' > ').replace('-', ' ').title()
                
                # Generate full URL if base_url provided
                if base_url:
                    full_url = f"{base_url.rstrip('/')}/{url_path}"
                else:
                    full_url = url_path
                
                # Write section header
                out.write(f"## {title}\n\n")
                out.write(f"**Path:** `{url_path}.md`  \n")
                if base_url:
                    out.write(f"**URL:** {full_url}\n\n")
                else:
                    out.write(f"**File:** `{url_path}.md`\n\n")
                out.write(content)
                out.write("\n\n")
                out.write("---\n\n")
                
            except Exception as e:
                print(f"  ✗ Error reading {md_file.name}: {e}")
                continue
    
    print(f"✓ llms-full.txt generated successfully")
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"  File size: {size_mb:.2f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Generate llms.txt and llms-full.txt from any markdown documentation repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Laravel docs
  python3 generate_docs.py https://github.com/laravel/docs --branch 12.x --name Laravel
  
  # Next.js docs (in 'docs' folder)
  python3 generate_docs.py https://github.com/vercel/next.js --root docs --name Next.js
  
  # Vue.js docs with custom base URL
  python3 generate_docs.py https://github.com/vuejs/docs \\
      --name Vue.js --base-url https://vuejs.org --version 3.x
  
  # Custom project
  python3 generate_docs.py https://github.com/user/project \\
      --root documentation --name "My Project" --version 2.0
        """
    )
    
    # Required arguments
    parser.add_argument(
        "repo_url",
        help="GitHub repository URL (e.g., https://github.com/owner/repo)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--root",
        default=".",
        help="Root folder within repo containing markdown files (default: repository root)"
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to clone (default: main)"
    )
    parser.add_argument(
        "--name",
        help="Project name (default: extracted from repo)"
    )
    parser.add_argument(
        "--version",
        help="Version string to include in output (optional)"
    )
    parser.add_argument(
        "--base-url",
        help="Base URL for documentation links (default: auto-detected from GitHub About)"
    )
    parser.add_argument(
        "--description",
        help="Project description (default: auto-detected from GitHub About)"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory for generated files (default: current directory)"
    )
    parser.add_argument(
        "--keep-repo",
        action="store_true",
        help="Keep the cloned repository after generation"
    )
    parser.add_argument(
        "--full-only",
        action="store_true",
        help="Generate only llms-full.txt"
    )
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Generate only llms.txt (index)"
    )
    
    args = parser.parse_args()
    
    # Extract repo info
    owner, repo = extract_repo_info(args.repo_url)
    if not owner or not repo:
        print(f"✗ Could not parse repository URL: {args.repo_url}")
        sys.exit(1)
    
    print(f"Repository: {owner}/{repo}")
    
    # Fetch GitHub metadata if not provided
    github_info = fetch_github_about(owner, repo)
    
    # Set project name
    project_name = args.name or github_info['name'] or repo
    
    # Set base URL
    base_url = args.base_url or github_info['homepage']
    
    # Set description
    description = args.description or github_info['description']
    
    print(f"Project: {project_name}")
    if base_url:
        print(f"Base URL: {base_url}")
    if description:
        print(f"Description: {description}")
    print()
    
    # Setup paths
    repo_dir = "/tmp/docs-repo"
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate output filenames
    version_suffix = f"-{args.version}" if args.version else ""
    llms_file = output_dir / f"llms{version_suffix}.txt"
    llms_full_file = output_dir / f"llms-full{version_suffix}.txt"
    
    # Clean up existing repo if present
    if os.path.exists(repo_dir):
        print(f"Removing existing directory: {repo_dir}")
        subprocess.run(["rm", "-rf", repo_dir], check=True)
    
    # Clone repository
    if not clone_repo(args.repo_url, repo_dir, args.branch):
        sys.exit(1)
    
    print()
    
    # Collect markdown files
    md_files, root_path = collect_markdown_files(repo_dir, args.root)
    if not md_files:
        print("✗ No markdown files found")
        sys.exit(1)
    
    # Generate files based on options
    if not args.full_only:
        generate_llms_txt(
            md_files, root_path, llms_file, 
            project_name, base_url, args.version, description
        )
    
    if not args.index_only:
        generate_llms_full_txt(
            md_files, root_path, llms_full_file,
            project_name, base_url, args.version, description
        )
    
    # Cleanup
    if not args.keep_repo:
        print(f"\nCleaning up: removing {repo_dir}")
        subprocess.run(["rm", "-rf", repo_dir], check=True)
    
    print(f"\n✅ Done! Generated files:")
    if not args.full_only and llms_file.exists():
        size_kb = llms_file.stat().st_size / 1024
        print(f"   • {llms_file} ({size_kb:.1f} KB) - index")
    if not args.index_only and llms_full_file.exists():
        size_mb = llms_full_file.stat().st_size / (1024 * 1024)
        print(f"   • {llms_full_file} ({size_mb:.1f} MB) - complete documentation")


if __name__ == "__main__":
    main()
