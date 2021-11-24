import yaml
import xml.etree.ElementTree as ElementTree

# Parser to generate yaml parameter file for artemis from BigRIPSPPAC.xml


class PPACXMLParser():

    def __init__(self):
        self.elements = []
        self.param_dict = dict()

    def feed(self, xml):
        self.root = ElementTree.fromstring(xml)

    def parse(self):
        contents = {}
        for ppac in self.root:
            name = str(ppac.find('NAME').text).lower().replace('-', '')
            xfactor = ppac.find('xfactor').text
            yfactor = ppac.find('yfactor').text
            xoffset = ppac.find('xoffset').text
            yoffset = ppac.find('yoffset').text
            xpos_off = ppac.find('xpos_off').text
            ypos_off = ppac.find('ypos_off').text
            xzpos = ppac.find('xzpos').text
            yzpos = ppac.find('yzpos').text
            txsum_min = ppac.find('txsum_min').text
            tysum_min = ppac.find('tysum_min').text
            txsum_max = ppac.find('txsum_max').text
            tysum_max = ppac.find('tysum_max').text

            content = {}
            content['ns2mm'] = [float(xfactor), float(yfactor)]
            content['delayoffset'] = [float(xoffset), float(yoffset)]
            content['linecalib'] = [0.0, 1.0]
            content['exchange'] = 0
            content['reflectx'] = 0
            content['geometry'] = [float(xpos_off), float(
                ypos_off), 0.5*(float(xzpos)+float(yzpos))]
            content['TXSumLimit'] = [float(txsum_min), float(txsum_max)]
            content['TYSumLimit'] = [float(tysum_min), float(tysum_max)]

            contents[name] = content

        self.yaml_contents = {}
        self.yaml_contents['Type'] = 'art::TPPACParameter'
        self.yaml_contents['Contents'] = contents

    def write(self, yaml_name):
        with open(yaml_name, 'w') as file:
            yaml.dump(self.yaml_contents, file,
                      sort_keys=False)


def generate_yaml(input_file_name):

    parser = PPACXMLParser()

    xml_file = open(input_file_name, 'r')
    parser.feed(xml_file.read())
    xml_file.close()

    parser.parse()
    yaml_name = input_file_name[0:-3]+'yaml'
    parser.write(yaml_name)
    return yaml_name
