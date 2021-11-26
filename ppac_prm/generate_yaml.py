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
        self.ch2ns = []
        for ppac in self.root:
            name = str(ppac.find('NAME').text).lower().replace('-', '')
            xfactor = ppac.find('xfactor').text
            yfactor = ppac.find('yfactor').text
            xoffset = ppac.find('xoffset').text
            yoffset = ppac.find('yoffset').text
            xns_off = ppac.find('xns_off').text
            yns_off = ppac.find('yns_off').text
            xpos_off = ppac.find('xpos_off').text
            ypos_off = ppac.find('ypos_off').text
            xzpos = ppac.find('xzpos').text
            yzpos = ppac.find('yzpos').text
            txsum_min = ppac.find('txsum_min').text
            tysum_min = ppac.find('tysum_min').text
            txsum_max = ppac.find('txsum_max').text
            tysum_max = ppac.find('tysum_max').text
            a_ch2ns = ppac.find('a_ch2ns').text
            x1_ch2ns = ppac.find('x1_ch2ns').text
            x2_ch2ns = ppac.find('x2_ch2ns').text
            y1_ch2ns = ppac.find('y1_ch2ns').text
            y2_ch2ns = ppac.find('y2_ch2ns').text
	    
            ch2ns_list = []
            ch2ns_list.append([0.0, float(x1_ch2ns)])
            ch2ns_list.append([0.0, float(x2_ch2ns)])
            ch2ns_list.append([0.0, float(y1_ch2ns)])
            ch2ns_list.append([0.0, float(y2_ch2ns)])
            ch2ns_list.append([0.0, float(a_ch2ns)])
            self.ch2ns.append({'name': name, 'list': ch2ns_list})

            content = {}
            content['ns2mm'] = [float(xfactor), float(yfactor)]
            content['delayoffset'] = [float(xoffset), float(yoffset)]
            content['linecalib'] = [float(xns_off), float(yns_off)]
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

    def write(self, yaml_name, ch2ns_name):
        with open(yaml_name, 'w') as file:
            yaml.dump(self.yaml_contents, file,
                      sort_keys=False)
        with open(ch2ns_name, 'w') as file:
            for fp in self.ch2ns:
                file.write('# ' + fp['name']+' x1 x2 y1 y2 a\n')
                for prm in fp['list']:
                      file.write(str(prm[0]) + '\t' + str(prm[1]) + '\n')


def generate_yaml(input_file_name):

    parser = PPACXMLParser()

    xml_file = open(input_file_name, 'r')
    parser.feed(xml_file.read())
    xml_file.close()

    parser.parse()
    yaml_name = input_file_name[0:-3]+'yaml'
    ch2ns_name = input_file_name[0:-4] + '_ch2ns.dat'
    parser.write(yaml_name, ch2ns_name)
    return yaml_name
