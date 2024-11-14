import os
import sys
from pathlib import Path
import time

# Try to import tkinter for folder picker
try:
    import tkinter as tk
    from tkinter import filedialog
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

# Define what to ignore
IGNORED_DIRS = {
    'node_modules',
    '.git',
    'dist',
    'build',
    '.next',
    '__pycache__',
    '.vscode',
    '.idea',
    'coverage',
    '.husky',
    '.github',
    'public',
    'out',
    'logs',
    '.turbo',
    '.vercel',
    'vendor',
    'temp',
    'tmp',
    '.svn',
    '.hg',
    'node_modules.cache'
}

IGNORED_FILES = {
    # Next.js files
    'next-env.d.ts',
    'next.config.mjs',
    'next.config.js',
    
    # Package manager files
    'package.json',
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    
    # Config files
    '.gitignore',
    '.eslintrc.json',
    '.eslintrc.js',
    '.prettierrc',
    'tsconfig.json',
    'postcss.config.js',
    'postcss.config.mjs',
    'tailwind.config.js',
    'tailwind.config.ts',
    'jest.config.js',
    'babel.config.js',
    'vite.config.ts',
    'components.json',
    
    # Environment files
    '.env',
    '.env.local',
    '.env.development',
    '.env.production',
    
    # Other
    '.DS_Store',
    '.npmrc',
    '.nvmrc',
    '.cursorignore',
    'README.md',
    'LICENSE',
    'global.d.ts',
    'CHANGELOG.md',
    'CONTRIBUTING.md'
}

IGNORED_EXTENSIONS = {
    # Images
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp', 
    # Documents
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv',
    # Archives
    '.zip', '.tar', '.gz', '.rar', '.7z',
    # Media
    '.mp3', '.mp4', '.wav', '.avi', '.mov', '.webm',
    # Fonts
    '.ttf', '.woff', '.woff2', '.eot', '.otf',
    # Compiled
    '.pyc', '.pyo', '.pyd', '.dll', '.exe', '.so',
    # Other
    '.lock', '.map', '.min.js', '.min.css',
    # Binary
    '.bin', '.dat', '.db', '.sqlite',
    # Backup
    '.bak', '.backup', '.tmp'
}

# Known text file extensions
TEXT_FILE_EXTENSIONS = {
    '.ts', '.tsx', '.js', '.jsx', '.mjs',
    '.css', '.scss', '.less', '.sass',
    '.html', '.htm', '.xml',
    '.json', '.yaml', '.yml',
    '.md', '.mdx', '.txt',
    '.sh', '.bash', '.zsh',
    '.env',
    '.vue', '.svelte', 
    '.astro',
    '.php',
    '.rs',
    '.go'
}

def select_directory():
    """Select directory using GUI or fallback to command line"""
    if HAS_TKINTER:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        print("Please select a folder to process...")
        directory = filedialog.askdirectory(
            title='Select Folder to Process',
            initialdir=os.getcwd()
        )
        
        if not directory:  # If user cancels selection
            print("No folder selected. Exiting...")
            sys.exit(0)
            
        return directory
    else:
        # Fallback to command line selection
        print("Tkinter not available. Please install python-tk package for GUI folder selection.")
        print("Falling back to command line selection.")
        
        if len(sys.argv) > 1:
            directory = sys.argv[1]
            if os.path.isdir(directory):
                return directory
            else:
                print(f"Error: '{directory}' is not a valid directory")
                sys.exit(1)
        else:
            return os.getcwd()

def is_binary_file(file_path):
    """Improved binary file detection"""
    try:
        # Skip binary check for known text file extensions
        ext = os.path.splitext(file_path)[1].lower()
        if ext in TEXT_FILE_EXTENSIONS:
            return False
            
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            # Count null bytes and control characters
            null_count = chunk.count(b'\x00')
            control_count = sum(1 for b in chunk if b < 32 and b not in {9, 10, 13})  # Tab, LF, CR
            
            # Consider binary if there are null bytes or too many control characters
            return null_count > 0 or (control_count / len(chunk) if chunk else 0) > 0.3
    except Exception:
        return True

def should_process_file(filename, filepath):
    """Determine if a file should be processed"""
    # Check for backup files first
    if filename.endswith(('.bak', '.backup', '.tmp')):
        return False
        
    # Check if file should be ignored
    if filename in IGNORED_FILES:
        return False
    
    # Check file extension
    _, ext = os.path.splitext(filename)
    if ext.lower() in IGNORED_EXTENSIONS:
        return False
    
    # Check file size (skip files larger than 10MB)
    try:
        if os.path.getsize(filepath) > 10 * 1024 * 1024:
            print(f'Skipping large file: {filepath}')
            return False
    except OSError:
        return False
    
    return True

def create_backup(file_path):
    """Create a backup of the file before modifying"""
    try:
        backup_path = f"{file_path}.bak"
        # Remove existing backup if it exists
        if os.path.exists(backup_path):
            os.remove(backup_path)
        with open(file_path, 'rb') as source:
            with open(backup_path, 'wb') as target:
                target.write(source.read())
        return True
    except Exception as e:
        print(f"Failed to create backup for {file_path}: {str(e)}")
        return False

def cleanup_backup(file_path):
    """Clean up backup file if it exists"""
    backup_path = f"{file_path}.bak"
    try:
        if os.path.exists(backup_path):
            os.remove(backup_path)
        return True
    except Exception as e:
        print(f"Warning: Failed to clean up backup for {file_path}: {str(e)}")
        return False

def add_file_path_comment(file_path, base_dir):
    """Add file path comment to the beginning of a file"""
    try:
        # Create backup first
        if not create_backup(file_path):
            return False

        # Check if it's a binary file
        if is_binary_file(file_path):
            cleanup_backup(file_path)
            print(f'Skipping binary file: {file_path}')
            return False

        # Try different encodings
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            cleanup_backup(file_path)
            print(f'Unable to read file with supported encodings: {file_path}')
            return False

        # Skip empty files
        if not content.strip():
            cleanup_backup(file_path)
            print(f'Skipping empty file: {file_path}')
            return False
        
        # Convert path to relative path from the selected directory
        rel_path = os.path.relpath(file_path, base_dir)
        normalized_path = str(Path(rel_path)).replace('\\', '/')
        
        # Check for existing file path comment
        first_line = content.split('\n')[0].strip() if content else ''
        
        # Check various comment formats
        existing_comments = [
            f'// {normalized_path}',
            f'# {normalized_path}',
            '// File:',  # Partial match
            '# File:',   # Partial match
        ]
        
        if any(first_line.startswith(comment) for comment in existing_comments):
            cleanup_backup(file_path)
            print(f'File already has path comment: {normalized_path}')
            return False

        # Choose comment style based on file extension
        ext = os.path.splitext(file_path)[1].lower()
        comment_char = '#' if ext in {
            '.py', '.rb', '.sh', '.yml', '.yaml', '.conf',
            '.toml', '.ini'  # Additional config file types
        } else '//'

        # Consider adding a blank line after the comment for better readability
        new_content = f'{comment_char} {normalized_path}\n\n{content}'
        
        # Write with detected encoding
        with open(file_path, 'w', encoding=encoding, newline='') as file:
            file.write(new_content)
        
        # Clean up backup after successful write
        cleanup_backup(file_path)
            
        return True

    except PermissionError:
        print(f'Permission denied: {file_path}')
        return False
    except Exception as e:
        print(f'Error processing {file_path}: {str(e)}')
        # Restore from backup if exists
        backup_path = f"{file_path}.bak"
        if os.path.exists(backup_path):
            try:
                os.replace(backup_path, file_path)
                print(f'Restored backup for {file_path}')
                cleanup_backup(file_path)
            except Exception as restore_error:
                print(f'Failed to restore backup for {file_path}: {str(restore_error)}')
        return False

def process_directory(directory):
    """Process all files in the directory"""
    files_processed = 0
    files_skipped = 0
    start_time = time.time()

    try:
        for root, dirs, files in os.walk(directory):
            # Remove ignored directories in-place
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in files:
                file_path = os.path.join(root, file)
                if should_process_file(file, file_path):
                    try:
                        if add_file_path_comment(file_path, directory):
                            print(f'Added path comment to: {file_path}')
                            files_processed += 1
                        else:
                            files_skipped += 1
                    except Exception as e:
                        print(f'Error processing {file_path}: {str(e)}')
                        files_skipped += 1

    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        return files_processed, files_skipped, time.time() - start_time
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return files_processed, files_skipped, time.time() - start_time

    return files_processed, files_skipped, time.time() - start_time

if __name__ == '__main__':
    try:
        print("Starting file path comment adder...")
        
        # Select directory using GUI or command line
        directory = select_directory()

        print(f"\nProcessing files in: {directory}")
        print("=" * 50)
        
        processed, skipped, duration = process_directory(directory)
        
        print("\nSummary:")
        print("=" * 50)
        print(f'Directory processed: {directory}')
        print(f'Files processed: {processed}')
        print(f'Files skipped: {skipped}')
        print(f'Duration: {duration:.2f} seconds')
        
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        sys.exit(1)