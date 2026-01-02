import configparser

import typer

from einsle.knx.parser import *


def main(config_file: str, in_xml_file: str):
    config = configparser.ConfigParser()
    config.read(config_file)
    tree = etree.parse(in_xml_file)
    root = tree.getroot()
    if len(root):
        data = dict()
        data['binary_sensor'] = []
        data['climate'] = []
        data['cover'] = []
        data['light'] = []
        data['sensor'] = []
        data['switch'] = []
        data['text'] = []
        for node in root.getchildren():
            if config.get('DEFAULT', 'NameLight') == node.get('Name'):
                LightingParser().parse(config, node, data)
            if config.get('DEFAULT', 'NameCover') == node.get('Name'):
                CoverParser().parse(node, data)
            if config.get('DEFAULT', 'NameClimate') == node.get('Name'):
                ClimateParser().parse(node, data)
            if config.get('DEFAULT', 'NameSwitch') == node.get('Name'):
                SwitchParser().parse(node, data)
            if config.get('DEFAULT', 'NameSensor') == node.get('Name'):
                SensorParser().parse(node, data)
        keys_list = list(data.keys())
        for key in keys_list:
            print('{0}:'.format(key))
            l_data = data[key]
            for d in l_data:
                print('  - name: {0}'.format(d['name']))
                for k, value in d.items():
                    if 'name' not in k:
                        print('    {0}: {1}'.format(k, value))


if __name__ == '__main__':
    typer.run(main)
