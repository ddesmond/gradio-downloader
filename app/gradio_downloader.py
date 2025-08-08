import gradio as gr
import yaml
import os
from urllib.parse import urlparse
import requests

def load_yaml_config(yaml_file_path):
    """Load file URLs from a YAML file."""
    try:
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config.get('files', [])
    except Exception as e:
        return f"Error loading YAML file: {str(e)}"

def download_file(url):
    """Download a file from the given URL."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return f"Error: Unable to download file (Status code: {response.status_code})"
        
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_file"
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return f"File downloaded successfully: {filename}"
    except Exception as e:
        return f"Error downloading file: {str(e)}"

def create_download_interface():
    """Create a Gradio interface with download buttons from YAML config."""
    yaml_file_path = "files.yaml"  # Path to your YAML file
    files = load_yaml_config(yaml_file_path)
    
    if isinstance(files, str):
        return files  # Return error message if YAML loading failed
    
    with gr.Blocks() as demo:
        gr.Markdown("## File Downloader")
        gr.Markdown("Click the buttons below to download files specified in the YAML configuration.")
        
        with gr.Column():
            for file_info in files:
                url = file_info.get('url')
                label = file_info.get('label', os.path.basename(urlparse(url).path) or "Download File")
                if url:
                    gr.DownloadButton(label=label, value=url)
        
        gr.Markdown("### Download Status")
        status = gr.Textbox(label="Status", interactive=False)
    
    return demo

# Launch the app
if __name__ == "__main__":
    interface = create_download_interface()
    if isinstance(interface, str):
        print(interface)  # Print error if YAML loading failed
    else:
        interface.launch()