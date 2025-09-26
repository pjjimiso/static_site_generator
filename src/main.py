# main.py

from textnode import TextType, TextNode
from split_nodes import split_nodes_delimiter
from extract_markdown import extract_markdown_title
from markdown_blocks import markdown_to_html_node
from pathlib import Path
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
    html = markdown_to_html_node(markdown_contents).to_html()
    template_contents = read_file_contents(template_path)
    contents = re.sub(r'{{\s*Title\s*}}', title, template_contents)
    contents = re.sub(r'{{\s*Content\s*}}', html, contents)
    #if not os.path.exists(dest_path):
    #    logging.debug(f"Creating directory {dest_path}")
    #    os.mkdir(dest_path)
    file_path = Path(from_path)
    dest_file_name = file_path.stem + ".html"
    dest_file = os.path.join(dest_path, dest_file_name)
    logging.debug(f"Writing contents to {dest_file}")
    write_file_contents(dest_file, contents)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file)
        if os.path.isfile(file_path) and file_path.endswith(".md"):
            print(f"we've found a markdown file to generate: {file_path}")
            generate_page(file_path, template_path, dest_dir_path)
        elif os.path.isdir(file_path):
            print(f"descending into directory {file_path}")
            dest_subdir_path = os.path.join(dest_dir_path, file)
            if not os.path.exists(dest_subdir_path):
                os.mkdir(dest_subdir_path)
            generate_page_recursive(file_path, template_path, dest_subdir_path)


def main(): 
    setup_logging("copy_files.log")
    source = "/home/pjjimiso/Projects/bootdotdev/static_site_generator/static"
    destination = "/home/pjjimiso/Projects/bootdotdev/static_site_generator/public"
    copy_files(src=source, dst=destination)
    generate_page_recursive("content", "template.html", "public")
    #generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")


if __name__ == "__main__": 
    main()

