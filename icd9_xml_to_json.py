import json
import xmltodict
import re
import argparse
import os

# List of parsed ICD9 items
icd_list = []


def parse_node(node):
    """

    This method takes a node and checks whether it is a leaf. 
    If so, it puts it to icd_list.

    """
    if("nodes" not in node.keys()):
        icd_list.append({"code": node['@code'], "desc": node['name']})
    else:
        parse_item(node)


def parse_item(item):
    """

    This method takes an item and process it's nodes. 
    As xmltodict returns inconsistently list or just one
    item it has to be handled.

    """

    if 'nodes' not in item.keys():
        return

    # Handling node appearing as list
    if(isinstance(item['nodes']['node'], list)):
        for node in item['nodes']['node']:
            parse_node(node)
    # Handling node appearing as one item
    else:
        parse_node(item['nodes']['node'])


parser = argparse.ArgumentParser()

parser.add_argument("path", help="Input file path")
parser.add_argument("-o", "--output", help="Output file path")

args = parser.parse_args()

with open(args.path, "r") as ICD9_xml:
    data_dict = xmltodict.parse(ICD9_xml.read())

    ICD9_xml.close()

parse_item(data_dict['hcd'])

if args.output:
    out_path = args.output
else:
    out_path = os.path.splitext(args.path)[0] + ".json"

with open(out_path, "w") as ICD9_json:
    json.dump(icd_list, ICD9_json, ensure_ascii=False)
    ICD9_json.close()
