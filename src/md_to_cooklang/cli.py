"""
Command-line interface for markdown to cooklang converter.
"""
import os
from pathlib import Path
from typing import Optional
import click
from dotenv import load_dotenv

from .converter import MarkdownToCooklangConverter

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--recursive/--no-recursive', '-r', default=True,
              help='Recursively process directories')
@click.option('--api-key', envvar='OPENAI_API_KEY',
              help='OpenAI API key (can also be set via OPENAI_API_KEY environment variable)')
@click.option('--spec-path', type=click.Path(exists=True),
              help='Path to cooklang specification file (defaults to spec.md in package directory)')
@click.option('--instructions', '-i', help='Custom instructions for the conversion (e.g., "convert to English")')
def main(input_path: str, recursive: bool, api_key: Optional[str], spec_path: Optional[str], instructions: Optional[str]):
    """Convert markdown files to cooklang format.
    
    INPUT_PATH can be a single markdown file or a directory containing markdown files.
    """
    # Try to load API key from .env file if not provided
    load_dotenv()
    
    api_key = api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise click.UsageError(
            "OpenAI API key not provided. Either:\n"
            "1. Use --api-key option\n"
            "2. Set OPENAI_API_KEY environment variable\n"
            "3. Create a .env file with OPENAI_API_KEY=your-key"
        )

    try:
        converter = MarkdownToCooklangConverter(
            api_key,
            spec_path=Path(spec_path) if spec_path else None
        )
        input_path = Path(input_path)
        
        if input_path.is_file():
            if not input_path.suffix == '.md':
                raise click.UsageError("Input file must be a markdown file (.md)")
            output_path = converter.convert_file(input_path, custom_instructions=instructions)
            click.echo(f"Converted {input_path} -> {output_path}")
        
        elif input_path.is_dir():
            converted = converter.convert_directory(input_path, recursive=recursive, custom_instructions=instructions)
            click.echo(f"Converted {len(converted)} files:")
            for path in converted:
                click.echo(f"  {path}")
        
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main()
