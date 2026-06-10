import os

def generate_codebase_summary(start_dir, output_file="project_summary.md"):
    # Folders to ignore to keep the output clean
    ignore_dirs = {'.git', '__pycache__', 'venv', '.idea', '.vscode', 'node_modules'}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Project Architecture Map\n\n")
        
        for root, dirs, files in os.walk(start_dir):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            level = root.replace(start_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            sub_indent = ' ' * 4 * (level + 1)
            
            # Write folder name
            f.write(f"{indent}- 📁 **{os.path.basename(root)}/**\n")
            
            for file in files:
                if file.endswith(('.py', '.js', '.json', '.html', '.css', '.md')): # Add extensions you care about
                    f.write(f"{sub_indent}- 📄 {file}\n")
                    
    print(f"✅ Project map successfully generated in {output_file}")

if __name__ == "__main__":
    # Runs from the current directory of the script
    generate_codebase_summary(os.getcwd())