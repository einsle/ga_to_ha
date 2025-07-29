from lxml import etree


class BeleuchtungParser:
    def parse(self, node: etree.Element):
        print('  light:')
        for child in node.getchildren():
            for address in child.getchildren():
                if address.get('Name').endswith('_Schalten'):
                    print('    - name: "{}"'.format(address.get('Name').removesuffix('_Schalten')))
                    print('      address: "{}"'.format(address.get('Address')))
                if address.get('Name').endswith('_Status Schalten'):
                    print('      state_address: "{}"'.format(address.get('Address')))
                if address.get('Name').endswith('_Dimmen absolut'):
                    print('      brightness_address: "{}"'.format(address.get('Address')))
                if address.get('Name').endswith('_Status Dimmen'):
                    print('      brightness_state_address: "{}"'.format(address.get('Address')))


class BeschattungParser:
    def parse(self, node: etree.Element):
        print('  cover:')
        for child in node.getchildren():
            for address in child.getchildren():
                if address.get('Name').endswith('_Fahren Auf/Ab'):
                    print('    - name: "{}"'.format(address.get('Name').removesuffix('_Fahren Auf/Ab')))
                    if address.get('Name').endswith('Oberlicht kippen_Fahren Auf/Ab'):
                        print('      device_class: "window"')
                    else:
                        print('      device_class: "shutter"')
                    print('      travelling_time_down: 17')
                    print('      travelling_time_up: 17')
                    print('      move_long_address: "{}"'.format(address.get('Address')))
                if address.get('Name').endswith('_Stopp'):
                    print('      stop_address: "{}"'.format(address.get('Address')))
                if address.get('Name').endswith('_Absolute Position'):
                    print('      position_address: "{}"'.format(address.get('Address')))
                if address.get('Name').endswith('_Status Absolute Position'):
                    print('      position_state_address: "{}"'.format(address.get('Address')))


class KontakteParser:
    def parse(self, node: etree.Element):
        print('  binary_sensor:')
        for child in node.getchildren():
            for address in child.getchildren():
                print('    - name: "{}"'.format(address.get('Name').removesuffix('_Status')))
                print('      device_class: "window"')
                print('      state_address: "{}"'.format(address.get('Address')))
