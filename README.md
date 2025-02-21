# md-to-cooklang

I keep my recipes in Markdown in an Obsidian vault, but I wanted to convert them to [Cooklang](https://github.com/cooklang/spec) to make them easier to follow on mobile.

This tool is a simple wrapper around OpenAI's gpt-4o-mini to convert Markdown recipes to Cooklang format. It can be used as a command line tool or as a Python library.

## Installation

```bash
pip install .
```

## Usage

### OpenAI API Key

You can provide your OpenAI API key in one of three ways:

1. Environment variable:
```bash
export OPENAI_API_KEY=your-api-key
```

2. Command line option:
```bash
md-to-cooklang recipe.md --api-key your-api-key
```

3. .env file in your working directory:
```
OPENAI_API_KEY=your-api-key
```

### Command Line

```bash

# Convert a single file
md-to-cooklang recipe.md

# Convert all markdown files in a directory
md-to-cooklang recipe_dir/

# Convert without recursion
md-to-cooklang recipe_dir/ --no-recursive

# Use custom cooklang specification file
md-to-cooklang recipe.md --spec-path /path/to/spec.md

# Add custom instructions for conversion
md-to-cooklang recipe.md -i "convert to English"
md-to-cooklang recipe_dir/ --instructions "use metric units"
```

Note: The converter will skip any markdown files that already have a corresponding .cook file in the same directory.

### Python API

```python
from md_to_cooklang import MarkdownToCooklangConverter
from pathlib import Path

# Initialize converter
converter = MarkdownToCooklangConverter(
    api_key="your-api-key",
    spec_path=Path("/path/to/spec.md")  # Optional, defaults to package's spec.md
)

# Convert a single file
converter.convert_file(
    Path("recipe.md"),
    custom_instructions="convert to English"  # Optional
)

# Convert all markdown files in a directory (skips existing .cook files)
converted_files = converter.convert_directory(
    Path("recipe_dir/"),
    recursive=True,  # Optional, defaults to True
    custom_instructions="use metric units"  # Optional
)
```

## Features

- Converts markdown recipe files to cooklang format using OpenAI's GPT-4
- Handles ingredients, cookware, timers, and metadata
- Supports both single file and directory conversion
- Preserves recipe structure and formatting
- CLI and Python API interfaces

## Requirements

- Python 3.8 or higher
- OpenAI API key
- Required packages: openai, click, pyyaml

## License

MIT License
