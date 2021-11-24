# shscripts
scripts for OEDO/SHARAQ

## ppac_prm
A script for downloading BigRIPS ppac parameters and generating a yaml file for artemis

To use:
```
python3 download_xml.py
```
It will tell you to input the url to the bripscnt server where you download ppac xml files then the local path to save xml and yaml files for the first run. It will generate config.yaml file that contains those information so you will not be asked to enter them again. config.yaml will be generated in the same directory as download_xml.py located. modify or delete this file to change the url or path.
