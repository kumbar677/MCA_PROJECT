import shutil
import os

def create_deployment_zip():
    # Define source directory (current dir)
    source_dir = os.getcwd()
    output_filename = 'project_deploy'
    
    # Create a temporary directory to collect files
    temp_dir = os.path.join(source_dir, 'deploy_temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # List of files/folders to include
    include_files = [
        'app.py', 'config.py', 'create_db.py', 'models.py', 'utils.py', 'requirements.txt',
        'database_schema.sql', 'generate_rules_pdf.py'
    ]
    include_dirs = ['routes', 'templates', 'static', 'migrations']
    
    # Copy files
    for f in include_files:
        if os.path.exists(os.path.join(source_dir, f)):
            shutil.copy2(os.path.join(source_dir, f), os.path.join(temp_dir, f))
            
    # Copy directories
    for d in include_dirs:
        src = os.path.join(source_dir, d)
        dst = os.path.join(temp_dir, d)
        if os.path.exists(src):
            shutil.copytree(src, dst)
            
    # Create zip
    shutil.make_archive(output_filename, 'zip', temp_dir)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    print(f"Created {output_filename}.zip successfully!")

if __name__ == "__main__":
    create_deployment_zip()
