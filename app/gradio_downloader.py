import gradio as gr
import yaml
import subprocess
import os
import pathlib

def load_yaml_config(file_path):
    """Load YAML configuration from the specified file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def run_bash_script(script_path):
    """Execute a bash script and return its output."""
    try:
        result = subprocess.run(['bash', script_path], capture_output=True, text=True, check=True)
        return f"Script executed successfully:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Error executing script:\n{e.stderr}"


def create_page(page_name, pages_config, links_config):
    """Create a Gradio page based on the provided configuration."""
    page_config = pages_config.get(page_name, {})
    title = page_config.get("title", page_name)
    content = page_config.get("content", f"Welcome to {page_name}")

    with gr.Blocks() as page:
        gr.Markdown(f"# {title}")
        gr.Markdown(content)

        # Add download buttons for this page if specified in links.yaml
        if page_name in links_config:
            gr.Markdown("## Downloads")
            for download in links_config[page_name]:
                button_label = download.get("label", "Download")
                script_path = pathlib.Path(download.get("script")).as_posix()
                if script_path and os.path.exists(script_path):

                    gr.Button(button_label).click(
                        fn=run_bash_script,
                        inputs=gr.Textbox(value=script_path, visible=False),
                        outputs=gr.Textbox(label="Script Output"),
                        api_name=f"download_{button_label.lower().replace(' ', '_')}"
                    )


    return page


def create_gradio_app(pages_yaml="./pages.yaml", links_yaml="./links.yaml", server_name="0.0.0.0", server_port=None):
    """Create and launch a Gradio app with pages and download buttons."""
    # Load configurations
    pages_config = load_yaml_config(pages_yaml)
    links_config = load_yaml_config(links_yaml)

    # Create the Gradio app with Blocks
    with gr.Blocks() as download_app:
        with gr.Tabs() as tabs:
            for page_name in pages_config.keys():
                with gr.Tab(page_name, id=page_name.lower()):
                    create_page(page_name, pages_config, links_config)

    # Launch the app
    download_app.launch(server_name=server_name, server_port=server_port, root_path="")
    return download_app


if __name__ == "__main__":
    create_gradio_app(server_port=8105)  # Default port