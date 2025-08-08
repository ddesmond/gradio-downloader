import os
import yaml
import argparse

def parse_shell_scripts(directory):
    # Initialize list to store shell script details
    sh_files = []

    # Walk through directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.sh'):
                # Store file name and full path
                sh_files.append({
                    'label': file,
                    'script': os.path.join(root, file)
                })

    return sh_files


def write_yaml_file(sh_files, output_file):
    # Create dictionary for YAML structure
    data = {'downloads': sh_files}

    # Write to YAML file
    with open(output_file, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)


def main():
    # Specify directory to scan (current directory in this case)

    output_file = 'links.yaml'
    directory = 'scripts'

    parser = argparse.ArgumentParser(description='Parse a folder for .sh files and generate a YAML file.')
    parser.add_argument('directory', type=str, help='Directory to scan for .sh files')
    args = parser.parse_args()
    if not args.directory:
        directory = directory
    else:
        directory = args.directory
    print(directory)
    # Parse shell scripts and write to YAML
    sh_files = parse_shell_scripts(directory)
    write_yaml_file(sh_files, output_file)
    print(f"YAML file '{output_file}' generated successfully with {len(sh_files)} shell scripts.")


if __name__ == '__main__':
    main()