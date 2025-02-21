"""
Convert markdown files to cooklang format using OpenAI API.
"""
import os
from pathlib import Path
from typing import List, Optional
import importlib.resources
import openai
import yaml

class MarkdownToCooklangConverter:
    def __init__(self, api_key: str, spec_path: Optional[Path] = None):
        """Initialize the converter with OpenAI API key and optional spec path."""
        self.client = openai.OpenAI(api_key=api_key)
        
        if spec_path:
            if not spec_path.exists():
                raise FileNotFoundError(f"Cooklang spec file not found: {spec_path}")
            self.spec = spec_path.read_text(encoding='utf-8')
        else:
            # Read spec from package data
            try:
                with importlib.resources.files('md_to_cooklang').joinpath('spec.md').open('r', encoding='utf-8') as f:
                    self.spec = f.read()
            except Exception as e:
                raise FileNotFoundError(f"Could not read package spec file: {str(e)}")

    def convert_text(self, markdown_text: str, custom_instructions: Optional[str] = None) -> str:
        """Convert markdown text to cooklang format using OpenAI."""
        system_prompt = f"""
        Convert the following markdown recipe to cooklang format according to this specification:

        {self.spec}

        Follow the specification exactly when converting the recipe.
        """
        
        if custom_instructions:
            system_prompt += f"\n\nAdditional instructions:\n{custom_instructions}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": markdown_text}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    def convert_file(self, input_path: Path, output_path: Optional[Path] = None, custom_instructions: Optional[str] = None) -> Optional[Path]:
        """Convert a markdown file to cooklang format."""
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if not output_path:
            output_path = input_path.with_suffix('.cook')
            
        # Skip if .cook file already exists
        if output_path.exists():
            print(f"Skipping {input_path} - {output_path} already exists")
            return None
        
        try:
            markdown_text = input_path.read_text(encoding='utf-8')
            cooklang_text = self.convert_text(markdown_text, custom_instructions)
            output_path.write_text(cooklang_text, encoding='utf-8')
            return output_path
        except Exception as e:
            raise RuntimeError(f"Error converting file {input_path}: {str(e)}")

    def convert_directory(self, directory: Path, recursive: bool = True, custom_instructions: Optional[str] = None) -> List[Path]:
        """Convert all markdown files in a directory to cooklang format."""
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        converted_files = []
        pattern = '**/*.md' if recursive else '*.md'
        
        for md_file in directory.glob(pattern):
            try:
                output_path = self.convert_file(md_file, custom_instructions=custom_instructions)
                if output_path:  # Only add to list if file was actually converted
                    converted_files.append(output_path)
            except Exception as e:
                print(f"Warning: Failed to convert {md_file}: {str(e)}")
        
        return converted_files
