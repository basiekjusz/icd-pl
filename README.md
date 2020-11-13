# icd-pl

Collection of Polish ICD-9 and ICD-10 dictionaries parsed to JSON and parsers. The files has been originally obtained and parsed
from files from [CSIOZ coding systems register](https://rsk.rejestrymedyczne.csioz.gov.pl/_layouts/15/rsk/default.aspx).

Current version of ICD-10 JSON file includes COVID-19 infections.

## Parsers usage

Both parsers require `python3` and `xmltodict` which you can install using following command:
```
apt-get install python3
pip install xmltodict
```

When running any of two parsers you must specify input file path. For example:
```
python icd10_xml_to_json.py icd10_source.xml
```

You can also specify output file path using `-o` or `--output` flag. For example:
```
python icd10_xml_to_json.py icd10_source.xml -o icd_out.json
```
