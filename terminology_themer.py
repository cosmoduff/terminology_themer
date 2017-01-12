#!/usr/bin/env python3
# Program to create terminology terminal emulator themes from json files

from jinja2 import Template
import json
import shutil
import subprocess
import os

# Import json theme. 
# TO DO: Replace json file with arg input later
output_location = os.environ['HOME'] + "/.config/terminology/themes"
json_file = "terminal-sexy.json"
theme = json.loads(open(json_file).read())

if theme["name"] == "":
    theme_name = json_file.rstrip('.json')
else:
    theme_name = theme["name"]

tmp_location = "/tmp/" + theme_name

shutil.copytree("build_template", tmp_location)

colors = theme["color"]
background = theme["background"]

color_template = Template(open("template_files/theme.edc.j2").read())
output_theme = color_template.render(zero=colors[0],one=colors[1],two=colors[2],\
        three=colors[3],four=colors[4],five=colors[5],six=colors[6],\
        seven=colors[7],eight=colors[8],nine=colors[9],ten=colors[10],\
        eleven=colors[11],twelve=colors[12],thirteen=colors[13],\
        fourteen=colors[14],fifteen=colors[15],background=background,theme_name=theme_name)
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

shutil.rmtree(tmp_location)
