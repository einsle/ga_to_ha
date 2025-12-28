import typer
from lxml import etree
from einsle.knx.parser import *


def main(file: str):
    tree = etree.parse(file)
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
            if "Beleuchtung" == node.get('Name'):
                LightingParser().parse(node, data)
            if "Beschattung" == node.get('Name'):
                CoverParser().parse(node, data)
            if "Heizung" == node.get('Name'):
                ClimateParser().parse(node, data)
            if "Verbraucher" == node.get('Name'):
                SwitchParser().parse(node, data)
            if "Kontakte" == node.get('Name'):
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
