# add-file-paths

A Python utility that automatically adds file path comments to the beginning of source files in a project. This tool helps developers maintain better code organization by clearly identifying file locations within a codebase and enhances AI tools' understanding of your project structure.

## Features

- 📝 Adds file path comments to the beginning of source files
- 🤖 Improves AI code assistance by providing clear file context
- 🎯 Smart detection of appropriate comment style (`//` or `#`) based on file type
- 🚫 Comprehensive ignore lists for directories, files, and extensions
- 💾 Automatic backup creation before modifying files
- 🔍 Binary file detection and skipping
- 📊 Processing summary with statistics
- 🖥️ GUI folder selection (if tkinter is available) with CLI fallback

## Why Use File Path Comments?

### For Developers
- Quickly identify file locations when viewing code snippets
- Easier navigation in large codebases
- Better context when reviewing pull requests
- Helpful for documentation and code reviews

### For AI Tools
- Provides crucial context for AI code assistants
- Helps AI better understand project structure
- Improves AI's ability to:
  - Generate relevant code suggestions
  - Understand file relationships
  - Provide more accurate recommendations
  - Navigate and reference project files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/add-file-paths.git
cd add-file-paths
```

2. Install dependencies (optional - only needed for GUI support):
```bash
pip install tkinter
```

## Usage

Run the script directly:
```bash
python add_file_paths.py
```

Or specify a directory via command line:
```bash
python add_file_paths.py /path/to/your/project
```

### Example Output

Before:
```javascript
function hello() {
    console.log("Hello, world!");
}
```

After:
```javascript
// File: src/utils/hello.js
function hello() {
    console.log("Hello, world!");
}
```

## Configuration

The script includes several configuration sets that can be modified:

- `IGNORED_DIRS`: Directories to skip (e.g., node_modules, .git)
- `IGNORED_FILES`: Specific files to skip (e.g., package.json, .env)
- `IGNORED_EXTENSIONS`: File extensions to skip (e.g., .jpg, .pdf)
- `TEXT_FILE_EXTENSIONS`: Known text file extensions to process

## Safety Features

- Creates backups before modifying files
- Skips binary files automatically
- Checks for existing file path comments
- Handles multiple file encodings
- Size limit checks (skips files > 10MB)
- Restores from backup if any errors occur

## AI Integration Tips

When using this tool with AI assistants:

1. Run the tool before sharing code with AI
2. Include file path comments when pasting code snippets
3. The path context helps AI:
   - Understand the file's role in your project
   - Make more relevant suggestions
   - Reference related files accurately
   - Maintain proper import paths

## Limitations

- Maximum file size: 10MB
- Requires Python 3.x
- GUI folder picker requires tkinter (optional)
- Does not process binary files
- Skips empty files

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
