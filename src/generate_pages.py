# generate_pages.py


from pathlib import Path
from extract_markdown import extract_markdown_title
from markdown_blocks import markdown_to_html_node
import os
import shutil
import re
import logging

logger = logging.getLogger(__name__)


def copy_files(src, dst, level=1):
    logger.debug(f"Copying files from {src} to {dst}")
    logger.debug(f"Current level = {level}")
    if os.path.exists(dst) and level == 1: 
        logger.debug(f"Root directory already exists, removing {dst}")
        shutil.rmtree(dst)
    logger.debug(f"Creating new directory {dst}")
    os.mkdir(dst)
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        if os.path.isfile(file_path):
            logger.debug(f"Copying file {file_path} to {dst}")
            shutil.copy(file_path, dst)
        else:
            subdir = os.path.join(dst, file)
            logger.debug(f"Copying files in subdirectory {subdir}")
            copy_files(src=file_path, dst=subdir, level=level+1)


def read_file_contents(file): 
    logger.debug(f"Reading from file {file}")
    try:
        with open(file, 'r') as f: 
            contents = f.read()
    except FileNotFoundError: 
        logger.error(f"the file {file} was not found")
        print(f"Error: the file {file} was not found")
    except Exception as e:
        logger.error(f"An error occured while reading the file {e}")
        print(f"An error occured while reading the file {e}")
    return  contents


def write_file_contents(file, contents): 
    logger.debug(f"Writing to file {file}")
    try:
        with open(file, 'w') as f: 
            f.write(contents)
    except FileNotFoundError: 
        logger.error(f"the file {file} was not found")
        print(f"Error: the file {file} was not found")
    except Exception as e: 
        logger.error(f"An error occured while writing the file {e}")
        print(f"An error occured while writing the file {e}")


def replace_template_contents(markdown_contents, template_contents):
    title = extract_markdown_title(markdown_contents)
    logger.debug(f"Page title: {title}")
    html = markdown_to_html_node(markdown_contents).to_html()
    contents = re.sub(r'{{\s*Title\s*}}', title, template_contents)
    contents = re.sub(r'{{\s*Content\s*}}', html, contents)
    return contents


def replace_basepath_links(contents, basepath): 
    logger.info(f"Replacing href and src urls with {basepath}")
    contents = re.sub(r'(href|src)="\/', r'\1' + f'="{basepath}', contents)
    return contents


def generate_page(basepath, from_path, template_path, dest_path): 
    logger.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_contents = read_file_contents(from_path)
    template_contents = read_file_contents(template_path)
    html_contents = replace_template_contents(markdown_contents, template_contents)
    # Required for hosting on Github pages 
    if basepath != "/":
        html_contents = replace_basepath_links(html_contents, basepath)
    file_path = Path(from_path)
    dest_file_name = file_path.stem + ".html"
    dest_file = os.path.join(dest_path, dest_file_name)
    logger.info(f"Writing page contents to {dest_file}")
    write_file_contents(dest_file, html_contents)


def generate_page_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    logger.info(f"Generating pages from {dir_path_content} to {dest_dir_path} using template file {template_path} and basepath {basepath}")
    for file in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file)
        if os.path.isfile(file_path) and file_path.endswith(".md"):
            generate_page(basepath, file_path, template_path, dest_dir_path)
        elif os.path.isdir(file_path):
            dest_subdir_path = os.path.join(dest_dir_path, file)
            if not os.path.exists(dest_subdir_path):
                os.mkdir(dest_subdir_path)
            generate_page_recursive(basepath, file_path, template_path, dest_subdir_path)
