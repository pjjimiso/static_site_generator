# main.py

from textnode import TextType, TextNode
from split_nodes import split_nodes_delimiter
from extract_markdown import extract_markdown_title
from markdown_blocks import markdown_to_html_node
import logging
import os
import shutil
import re


def setup_logging(file):
    logging.basicConfig(
        filename=file,
        level=logging.DEBUG,
        filemode='w',
        format='%(asctime)s %(levelname)s: %(message)s'
    )

def copy_files(src, dst, level=1):
    if os.path.exists(dst) and level == 1: 
        logging.debug(f"Removing existing root directory {dst}")
        shutil.rmtree(dst)
    logging.debug(f"Creating directory {dst}")
    os.mkdir(dst)
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        if os.path.isfile(file_path):
            logging.debug(f"Copying file {file_path}")
            shutil.copy(file_path, dst)
        else:
            subdir = os.path.join(dst, file)
            copy_files(src=file_path, dst=subdir, level=level+1)

def read_file_contents(file): 
    try:
        with open(file, 'r') as f: 
            contents = f.read()
    except FileNotFoundError: 
        print(f"Error: the file {file} was not found")
    except Exception as e: 
        print(f"An error occured {e}")
    return  contents

def write_file_contents(file, contents): 
    try:
        with open(file, 'w') as f: 
            f.write(contents)
    except FileNotFoundError: 
        print(f"Error: the file {file} was not found")
    except Exception as e: 
        print(f"An error occured {e}")

def generate_page(from_path, template_path, dest_path): 
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_contents = read_file_contents(from_path)
    title = extract_markdown_title(markdown_contents)
    logging.debug(f"Page title: {title}")
    logging.debug(f"printing contents of markdown file:\n{markdown_contents}")
    html = markdown_to_html_node(markdown_contents).to_html()
    template_contents = read_file_contents(template_path)
    contents = re.sub(r'{{\s*Title\s*}}', title, template_contents)
    logging.debug(f"Replace Title with {title}:\n{contents}")
    contents = re.sub(r'{{\s*Content\s*}}', html, contents)
    logging.debug(f"Replace Contents:\n{contents}")
    write_file_contents(dest_path, contents)
    logging.debug(f"printing contents to index.html:\n{dest_path}")


def main(): 
    setup_logging("copy_files.log")
    source = "/home/pjjimiso/Projects/bootdotdev/static_site_generator/static"
    destination = "/home/pjjimiso/Projects/bootdotdev/static_site_generator/public"
    copy_files(src=source, dst=destination)
    generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")


if __name__ == "__main__": 
    main()

