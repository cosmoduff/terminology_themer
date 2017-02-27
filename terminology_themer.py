#!/usr/bin/env python3
# Program to create terminology terminal emulator themes from json files

from jinja2 import Template
import json
import shutil
import subprocess
import os
import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description='Create them from json file')

    parser.add_argument('path',
                        metavar='json_file',
                        type=str,
                        help='path to the json file containing the theme.')
    
    args = parser.parse_args()

    return args

def cleanup(remove_dir):
    shutil.rmtree(remove_dir)

def configure_tmp(name):
    # Takes a directory name creates the directory under /tmp and returns its
    # path.
    # Feel like this should just create the dir and take the full path as the
    # arg.

    tmp_location = "/tmp/" + theme_name
    
    shutil.copytree("build_template", tmp_location)

    return tmp_location

def set_theme_name(json_file):
    # Set the theme name as filename if the name var is empty
    if theme["name"] == "":
        theme_name = json_file.rstrip('.json')
    else:
        theme_name = theme["name"]

    return theme_name


def main():

    args = get_args()

    # Import json theme. 
    output_location = os.environ['HOME'] + "/.config/terminology/themes"
    file_path = args.path
    json_file = os.path.basename(args.path)
    theme = json.loads(open(file_path).read())
    theme_name = set_theme_name(theme)

    # Set the output location and exit if it exists
    # Would like to add a force option later
    output_file = output_location + "/" + theme_name + ".edj"
    if os.path.isfile(output_file):
            print("The theme " + theme_name + " already exists.")
            sys.exit(0)
    
    tmp_location = configure_tmp(theme_name)
    
    # Set color vars
    colors = theme["color"]
    background = theme["background"]
    foreground = theme["foreground"]
    
    # Change color15 to match foreground for random gen themes
    if foreground != colors[15]:
        colors[15] = foreground
    
    color_template = Template(open("template_files/theme.edc.j2").read())
    output_theme = color_template.render(zero=colors[0],one=colors[1],two=colors[2],\
            three=colors[3],four=colors[4],five=colors[5],six=colors[6],\
            seven=colors[7],eight=colors[8],nine=colors[9],ten=colors[10],\
            eleven=colors[11],twelve=colors[12],thirteen=colors[13],\
            fourteen=colors[14],fifteen=colors[15],background=background,\
            foreground=foreground,theme_name=theme_name)
    build_template = Template(open("template_files/build.sh.j2").read())
    output_build = build_template.render(theme_name=theme_name)
    
    build_file = open(tmp_location+"/build.sh", "w")
    color_file = open(tmp_location+"/"+theme_name+".edc", "w")
    
    build_file.write(output_build)
    build_file.close()
    
    os.chmod(tmp_location+"/build.sh", 0o700)
    
    color_file.write(output_theme)
    color_file.close()
    
    os.chdir(tmp_location)
    subprocess.call([tmp_location+"/build.sh"])
    
    shutil.move(tmp_location+"/"+theme_name+".edj", output_location)
    
    cleanup(tmp_location)

# Execute
if __name__=="__main__":
    main()
