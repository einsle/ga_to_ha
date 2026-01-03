from typing import Annotated

import typer
import codecs
from einsle.knx.parser import *

app = typer.Typer(help='Script to convert group address information out of ETS to home assistant.')


@app.command()
def main(
        in_xml_file: Annotated[
            str,
            typer.Option(
                help='Path to XML file exported from ETS'
            )
        ],
        config_file: Annotated[
            str,
            typer.Option(
                help='Path to config file to configure input',
            )
        ] = None):
    """
    Parses ETS generated XML file and generates home assistant knx configuration

    :param in_xml_file: Path to XML file exported from ETS
    :param config_file: Path to config file to configure input
    :return:
    """
    config = configparser.ConfigParser()
    with codecs.open(config_file, 'r', 'utf-8') as cfg_file:
        config.read_file(cfg_file)
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
                CoverParser().parse(config, node, data)
            if config.get('DEFAULT', 'NameClimate') == node.get('Name'):
                ClimateParser().parse(config, node, data)
            if config.get('DEFAULT', 'NameSwitch') == node.get('Name'):
                SwitchParser().parse(config, node, data)
            if config.get('DEFAULT', 'NameSensor') == node.get('Name'):
                SensorParser().parse(config, node, data)
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
    app()
