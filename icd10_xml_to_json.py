import json
import xmltodict
import re
import argparse
import os

# Regex pattern to find whether the icd code is the leaf, not a subcategory
icd_pattern = re.compile("[A-Z][0-9][0-9].[0-9]$")

# List of parsed ICD10 items
icd_list = []


def parse_node(node):
    """

    This method takes a node and reads code attribute. If it is a leaf,
    then it is put in icd_list.

    """

    code_match = icd_pattern.match(node["@code"])
    if(code_match):
        icd_list.append({"code": code_match.group(), "name": node['name']})
    else:
        parse_item(node)


def parse_item(item):
    """

    This method takes an item and process it's nodes. Unfortunately
    polish ICD10 XML file are very inconsistent, as many <nodes/> attributes
    sometimes appear in one <node/> item. Also, xmltodict returns erratically
    list or just one item, so this case has to be handled too.

    """

    if 'nodes' not in item.keys():
        return

    nodes = []

    # Handling many <nodes/> attributes in one item
    if(isinstance(item['nodes'], list)):
        for nodes_item in item['nodes']:
            nodes.append(nodes_item['node'])
    else:
        # Handling node appearing as list
        if(isinstance(item['nodes']['node'], list)):
            nodes = item['nodes']['node']
        # Handling node appearing as one item
        else:
            nodes.append(item['nodes']['node'])

    for node in nodes:
        parse_node(node)


parser = argparse.ArgumentParser()

parser.add_argument("path", help="Input file path")
parser.add_argument("-o", "--output", help="Output file path")
parser.add_argument("-n", "--number", action="store_true", help="Display number of parsed items")

args = parser.parse_args()

with open(args.path, "r") as ICD10_xml:
    data_dict = xmltodict.parse(ICD10_xml.read())

    ICD10_xml.close()

parse_item(data_dict['hcd'])

if args.output:
    out_path = args.output
else:
    out_path = os.path.splitext(args.path)[0] + ".json"

with open(out_path, "w") as ICD10_json:
    json.dump(icd_list, ICD10_json, ensure_ascii=False)
    ICD10_json.close()

if(args.number):
    print("Total number of parsed items:", len(icd_list))
