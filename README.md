# Universal Documentation to llms.txt Generator

Generate `llms.txt` and `llms-full.txt` from **any** markdown-based documentation repository on GitHub. Works with Laravel, .NET, Vue.js, React, and any other project that uses markdown files for documentation.

## Features

✨ **Fully Agnostic** - Works with any GitHub repository containing markdown files  
🔍 **Auto-Detection** - Automatically fetches project info, homepage URL, and description from GitHub  
📁 **Flexible Paths** - Specify any subfolder as the documentation root  
🌿 **Branch Support** - Clone from any branch (main, master, version branches)  
🏷️ **Version Tagging** - Add version strings to output filenames  
🔗 **Smart URLs** - Generates proper documentation URLs with file-based routing  
📦 **Two Outputs** - Creates both index (llms.txt) and complete docs (llms-full.txt)

## Quick Start

### Python Script (Recommended)

```bash
# Basic usage - auto-detects everything from GitHub
python3 generate_docs.py https://github.com/owner/repo

# With branch specification
python3 generate_docs.py https://github.com/laravel/docs --branch 12.x

# Documentation in subfolder
python3 generate_docs.py https://github.com/vercel/next.js --root docs

# Full options
python3 generate_docs.py https://github.com/vuejs/docs \
    --name "Vue.js" \
    --version "3.x" \
    --branch main \
    --base-url https://vuejs.org \
    --description "The Progressive JavaScript Framework"
```

### Bash Script

```bash
# Basic usage
./generate_docs.sh https://github.com/owner/repo

# With options
./generate_docs.sh https://github.com/laravel/docs \
    --branch 12.x \
    --name Laravel \
    --version 12
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

## Real-World Examples

### Laravel Documentation

```bash
# Latest version
python3 generate_docs.py https://github.com/laravel/docs \
    --branch master \
    --name Laravel

# Specific version
python3 generate_docs.py https://github.com/laravel/docs \
    --branch 12.x \
    --name Laravel \
    --version 12
```

Output: `llms-12.txt` and `llms-full-12.txt`

### Next.js Documentation

```bash
# Next.js keeps docs in 'docs' subfolder
python3 generate_docs.py https://github.com/vercel/next.js \
    --root docs \
    --name "Next.js" \
    --branch canary
```

### Vue.js Documentation

```bash
python3 generate_docs.py https://github.com/vuejs/docs \
    --name "Vue.js" \
    --version 3
```

### React Documentation

```bash
python3 generate_docs.py https://github.com/reactjs/react.dev \
    --root src/content \
    --name React
```

### Tailwind CSS Documentation

```bash
python3 generate_docs.py https://github.com/tailwindlabs/tailwindcss.com \
    --root src/pages/docs \
    --name "Tailwind CSS"
```

### Your Custom Project

```bash
python3 generate_docs.py https://github.com/username/my-project \
    --root documentation \
    --name "My Awesome Project" \
    --version "2.0" \
    --base-url https://docs.myproject.com \
    --description "Documentation for My Awesome Project"
```

## How It Works

1. **Clones** the repository (shallow clone with depth=1 for speed)
2. **Discovers** markdown files in the specified root folder
3. **Fetches** project metadata from GitHub API (name, homepage, description)
4. **Extracts** titles and descriptions from each markdown file
5. **Generates** two files:
   - **llms.txt** - Lightweight index with titles and descriptions (~50-100 KB)
   - **llms-full.txt** - Complete documentation content (~5-20 MB)
6. **Cleans up** temporary files (unless `--keep-repo` is used)

## Output Format

### llms.txt (Index)

```markdown
# Project Name Documentation - Version

> Project description from GitHub

Website: https://project.com

## Documentation Index

### [Getting Started](https://project.com/getting-started)

Introduction to the project and how to get started quickly...

### [API Reference](https://project.com/api-reference)

Complete API reference for all available methods and classes...

---

## Notes

- For complete documentation content, see `llms-full.txt`
- Total sections: 42
```

### llms-full.txt (Complete Documentation)

```markdown
# Project Name Documentation - Complete - Version

> Project description from GitHub

Website: https://project.com

---

## Getting Started

**Path:** `getting-started.md`
**URL:** https://project.com/getting-started

[Full markdown content from getting-started.md]

---

## API Reference

**Path:** `api/reference.md`
**URL:** https://project.com/api/reference

[Full markdown content from api/reference.md]

---

...
```

## File-Based Routing

The script assumes file-based routing, converting file paths to URLs:

- `getting-started.md` → `https://base-url/getting-started`
- `api/reference.md` → `https://base-url/api/reference`
- `guides/advanced.md` → `https://base-url/guides/advanced`

## Batch Processing

Generate documentation for multiple versions:

```bash
# Multiple Laravel versions
for version in 12.x 11.x 10.x; do
    python3 generate_docs.py https://github.com/laravel/docs \
        --branch $version \
        --name Laravel \
        --version $version
done

# Result: llms-12.x.txt, llms-11.x.txt, llms-10.x.txt, etc.
```

Generate for multiple projects:

```bash
# Create a list of projects
cat > projects.txt << EOF
https://github.com/laravel/docs,Laravel,12.x
https://github.com/vuejs/docs,Vue.js,main
https://github.com/vercel/next.js/docs,Next.js,canary
EOF

# Process each project
while IFS=, read -r repo name branch; do
    python3 generate_docs.py "$repo" \
        --name "$name" \
        --branch "$branch" \
        --version "$branch"
done < projects.txt
```

## Use Cases

### For AI/LLM Training
- Generate comprehensive training data from documentation
- Create context for fine-tuning models on specific frameworks
- Build RAG (Retrieval Augmented Generation) knowledge bases

### For Developers
- Offline documentation access in a single file
- Quick reference without internet connection
- Documentation archival and version comparison

### For Documentation Teams
- Generate documentation snapshots for releases
- Create distributable documentation packages
- Monitor documentation completeness and structure

## Requirements

### Python Script
- Python 3.6 or higher
- `git` command-line tool
- Internet connection (for cloning and GitHub API)

### Bash Script
- Bash 4.0 or higher
- `git` command-line tool
- Standard Unix utilities (`grep`, `sed`, `find`)

## File Sizes

Typical file sizes vary by project:

| Project | llms.txt | llms-full.txt |
|---------|----------|---------------|
| Laravel | ~80 KB | ~7 MB |
| Next.js | ~50 KB | ~4 MB |
| Vue.js | ~60 KB | ~5 MB |
| React | ~70 KB | ~6 MB |

## Auto-Detection Details

The script automatically detects from GitHub:

1. **Project Name** - From repository name or `name` field
2. **Homepage URL** - From repository `homepage` field (used as `base-url`)
3. **Description** - From repository description

You can override any of these with command-line options.

## Troubleshooting

### Branch Not Found
If the branch doesn't exist, the script automatically tries:
1. Your specified branch
2. `master` branch
3. Default branch

### GitHub API Rate Limiting
The script uses anonymous GitHub API calls. If you hit rate limits:
- Wait an hour for the limit to reset
- Manually specify `--base-url` and `--description` to skip API calls

### No Markdown Files Found
- Check the `--root` path is correct
- Ensure the repository contains `.md` files
- Use `--keep-repo` to inspect the cloned repository

### Permission Denied
Make scripts executable:
```bash
chmod +x generate_docs.py generate_docs.sh
```

## Advanced Usage

### Skip GitHub API (Faster, No Rate Limits)

```bash
python3 generate_docs.py https://github.com/owner/repo \
    --name "Project Name" \
    --base-url https://docs.example.com \
    --description "Your description here"
```

### Generate Only Index (Lightweight)

```bash
python3 generate_docs.py https://github.com/owner/repo --index-only
```

### Keep Repository for Inspection

```bash
python3 generate_docs.py https://github.com/owner/repo --keep-repo
# Repository kept in /tmp/docs-repo
```

### Custom Output Directory

```bash
python3 generate_docs.py https://github.com/owner/repo \
    --output-dir ./docs-output \
    --version v2.0
```

## Contributing

This script is designed to be repository-agnostic. If you find edge cases or have suggestions:

1. Test with various documentation structures
2. Check file-based routing assumptions
3. Verify URL generation
4. Report any issues or improvements

## License

These scripts are provided as-is for generating documentation files. Generated documentation content is subject to its original repository's license.

## Credits

Created to solve the problem of accessing documentation in LLM-friendly formats across any project that uses markdown documentation.
