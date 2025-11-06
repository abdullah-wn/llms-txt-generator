# llms.txt Generator - Universal Documentation Converter

Convert any GitHub documentation repository into `llms.txt` and `llms-full.txt` formats for LLM consumption.

## Features

✨ **Universal** - Works with any markdown documentation repository  
🔍 **Auto-Detection** - Fetches project info from GitHub automatically  
📁 **Flexible** - Supports custom root folders and branches  
🏷️ **Version Support** - Tag outputs with version numbers  
📦 **Dual Output** - Creates both index and full documentation files

## Installation

### Option 1: Direct Download

```bash
# Download the script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/generate_docs.py

# Make it executable
chmod +x generate_docs.py
```

### Option 2: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
chmod +x generate_docs.py
```

## Quick Start

```bash
# Basic usage - auto-detects everything from GitHub
python3 generate_docs.py https://github.com/owner/repo

# With branch specification
python3 generate_docs.py https://github.com/laravel/docs --branch 12.x

# Documentation in subfolder
python3 generate_docs.py https://github.com/vercel/next.js --root docs

# With version tag
python3 generate_docs.py https://github.com/vuejs/docs --version 3.x
```

## Usage

```bash
python3 generate_docs.py REPO_URL [OPTIONS]
```

## Command Line Options

### Required
- **`repo_url`** - GitHub repository URL (e.g., `https://github.com/owner/repo`)

### Optional
- **`--root FOLDER`** - Root folder within repo containing markdown files (default: repository root)
- **`--branch BRANCH`** - Branch to clone (default: `main`, falls back to `master` if not found)
- **`--name NAME`** - Project name (default: auto-detected from GitHub)
- **`--version VERSION`** - Version string to include in output (adds suffix to filenames)
- **`--base-url URL`** - Base URL for documentation links (default: auto-detected from GitHub About)
- **`--description TEXT`** - Project description (default: auto-detected from GitHub About)
- **`--output-dir DIR`** - Output directory for generated files (default: current directory)
- **`--keep-repo`** - Keep the cloned repository after generation (useful for debugging)
- **`--index-only`** - Generate only llms.txt (index)
- **`--full-only`** - Generate only llms-full.txt (complete docs)

## Examples

### Laravel Documentation

```bash
# Latest version
python3 generate_docs.py https://github.com/laravel/docs

# Specific version with tagging
python3 generate_docs.py https://github.com/laravel/docs \
    --branch 12.x \
    --version 12
```

**Output:** `llms-12.txt` and `llms-full-12.txt`

### Next.js Documentation

```bash
python3 generate_docs.py https://github.com/vercel/next.js \
    --root docs \
    --name "Next.js"
```

### Vue.js Documentation

```bash
python3 generate_docs.py https://github.com/vuejs/docs \
    --version 3
```

### Your Own Project

```bash
python3 generate_docs.py https://github.com/username/my-project \
    --root documentation \
    --name "My Project" \
    --version "2.0" \
    --base-url https://docs.myproject.com
```

### Batch Processing Multiple Versions

```bash
for version in 12.x 11.x 10.x; do
    python3 generate_docs.py https://github.com/laravel/docs \
        --branch $version \
        --version $version
done
```

**Result:** `llms-12.x.txt`, `llms-11.x.txt`, `llms-10.x.txt`, etc.

## Output Files

### llms.txt (Index)
Lightweight index file (~50-100 KB) containing:
- Document titles and descriptions
- Links to full documentation
- Table of contents

### llms-full.txt (Complete Documentation)
Complete documentation file (~5-10 MB) containing:
- All markdown content
- Full text of every documentation page
- Perfect for LLM training and RAG systems

## How It Works

1. **Clones** the repository (shallow clone for speed)
2. **Discovers** all markdown files in the specified root folder
3. **Fetches** project metadata from GitHub API (name, homepage, description)
4. **Extracts** titles and descriptions from markdown files
5. **Generates** two output files with proper formatting
6. **Cleans up** temporary files automatically

## Requirements

- Python 3.6+
- Git command-line tool
- Internet connection (for cloning repos and GitHub API)

## Auto-Detection

The script automatically detects from GitHub:
- **Project name** - From repository name
- **Homepage URL** - From repository settings (used as base URL)
- **Description** - From repository description
- **Default branch** - Falls back from main → master → default

You can override any of these with command-line options.

## Use Cases

- **AI/LLM Training** - Generate training data from documentation
- **RAG Systems** - Create knowledge bases for retrieval
- **Offline Access** - Have complete docs in a single file
- **Documentation Archival** - Create version snapshots
- **Multi-framework Development** - Process docs from multiple frameworks

## Troubleshooting

### Branch not found
The script automatically tries main → master → default branch.

### No markdown files found
Use `--root` to specify the correct folder containing .md files.

### GitHub API rate limit
Manually specify `--base-url` and `--description` to skip API calls:
```bash
python3 generate_docs.py https://github.com/owner/repo \
    --base-url https://docs.example.com \
    --description "Your description"
```

## Advanced Usage

### Skip GitHub API (No Rate Limits)

```bash
python3 generate_docs.py https://github.com/owner/repo \
    --name "Project Name" \
    --base-url https://docs.example.com \
    --description "Your description here"
```

### Keep Repository for Inspection

```bash
python3 generate_docs.py https://github.com/owner/repo --keep-repo
# Repository kept in /tmp/docs-repo
```

### Generate Only Index (Fast Preview)

```bash
python3 generate_docs.py https://github.com/owner/repo --index-only
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this script for any purpose.

## Credits

Created to make documentation accessible in LLM-friendly formats across any project.

---

**Need help?** Run `python3 generate_docs.py --help` for more information.
