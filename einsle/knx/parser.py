from lxml import etree


class LightingParser:
    def parse(self, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = "_".join(name.split('_')[0:2])
                suffix = "_".join(name.split('_')[2:])
                address = group_address.get('Address')
                dct = next((item for item in data['light'] if item['name'] == prefix), {'name': prefix})
                if 'Schalten' == suffix:
                    dct['address'] = address
                    data['light'].append(dct)
                if 'Schalten Status' == suffix:
                    dct['state_address'] = address
                if 'Dimmen absolut' == suffix:
                    dct['brightness_address'] = address
                if 'Dimmen Status' == suffix:
                    dct['brightness_state_address'] = address
                if 'Alarm' == suffix:
                    b_s = {
                        'name': '"{}"'.format(name),
                        'state_address': '"{}"'.format(address)
                    }
                    data['binary_sensor'].append(b_s)
                if 'Licht Status' == name.split('_')[1]:
                    b_s = {
                        'name': '"{}"'.format(name),
                        'state_address': '"{}"'.format(address)
                    }
                    data['binary_sensor'].append(b_s)


class CoverParser:
    def parse(self, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = "_".join(name.split('_')[0:2])
                suffix = "_".join(name.split('_')[2:])
                address = group_address.get('Address')
                dct = next((item for item in data['cover'] if item['name'] == prefix), {'name': prefix})
                if 'Fahren Auf/Ab' == suffix:
                    dct['move_long_address'] = address
                    data['cover'].append(dct)
                    if name.endswith('Oberlicht kippen_Fahren Auf/Ab'):
                        dct['device_class'] = '"window"'
                    else:
                        dct['device_class'] = '"shutter"'
                    if name.startswith('Büro_Rollladen Nord'):
                        dct['travelling_time_down'] = '36'
                        dct['travelling_time_up'] = '36'
                    if name.startswith('Büro_Rollladen Süd'):
                        dct['travelling_time_down'] = '36'
                        dct['travelling_time_up'] = '36'
                    if name.startswith('Schlafen_Rollladen'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                    if name.startswith('WC_Rollladen'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                    if name.startswith('Bad_Rollladen'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                    if name.startswith('Speiß_Rollladen'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                    if name.startswith('Küche_Rollladen'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                    if name.startswith('Küche_Oberlicht_'):
                        dct['travelling_time_down'] = '14'
                        dct['travelling_time_up'] = '14'
                    if name.startswith('Küche_Oberlicht kippen_'):
                        dct['travelling_time_down'] = '15'
                        dct['travelling_time_up'] = '15'
                    if name.startswith('Essen_Rollladen Balkon'):
                        dct['travelling_time_down'] = '26'
                        dct['travelling_time_up'] = '28'
                    if name.startswith('Essen_Rollladen Süd'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                    if name.startswith('Essen_Rollladen Mitte'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                    if name.startswith('Wohnen_Rollladen Nord'):
                        dct['travelling_time_down'] = '17'
                        dct['travelling_time_up'] = '17'
                if 'Stopp' == suffix:
                    dct['stop_address'] = address
                if 'Absolute Position' == suffix:
                    dct['position_address'] = address
                if 'Absolute Position Status' == suffix:
                    dct['position_state_address'] = address


class ClimateParser:
    def parse(self, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = "_".join(name.split('_')[0:2])
                suffix = "_".join(name.split('_')[2:])
                address = group_address.get('Address')
                dct = next((item for item in data['climate'] if item['name'] == prefix), {'name': prefix})
                if 'Ist-Temperatur' == suffix:
                    dct['temperature_address'] = address
                    data['climate'].append(dct)
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"temperature"',
                        'device_class': '"temperature"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if 'Sollwert' == suffix:
                    dct['target_temperature_address'] = address
                if 'Sollwert Status' == suffix:
                    dct['target_temperature_state_address'] = address
                if 'Sollwertverschiebung' == suffix:
                    dct['setpoint_shift_address'] = address
                if 'Sollwertverschiebung Status' == suffix:
                    dct['setpoint_shift_state_address'] = address
                    dct['setpoint_shift_mode'] = '"DPT9002"'
                    dct['temperature_step'] = '0.5'
                    dct['setpoint_shift_max'] = '5'
                    dct['setpoint_shift_min'] = '-5'
                if 'Betriebsart' == suffix:
                    dct['operation_mode_address'] = address
                if 'Betriebsart Status' == suffix:
                    dct['operation_mode_state_address'] = address
                if 'Status Stellwert %' == suffix:
                    dct['command_value_state_address'] = address
                if 'Störung' == suffix:
                    b_s = {
                        'name': '"{}"'.format(name),
                        'device_class': '"problem"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['binary_sensor'].append(b_s)
                if 'Diagnose' == suffix:
                    text = {'name': '"{}"'.format(name),
                            'address': '"{}"'.format(address)}
                    data['text'].append(text)
                if 'Humidity' == suffix:
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"humidity"',
                        'device_class': '"humidity"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if 'Air Quality voc' == suffix:
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"pulse_2byte"',
                        'device_class': '"volatile_organic_compounds"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if 'Air Quality ppm' == suffix:
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"ppm"',
                        'device_class': '"volatile_organic_compounds"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)


class SwitchParser:
    def parse(self, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = "_".join(name.split('_')[0:2])
                suffix = "_".join(name.split('_')[2:])
                address = group_address.get('Address')
                dct = next((item for item in data['switch'] if item['name'] == prefix), {'name': prefix})
                if 'Schalten' == suffix:
                    dct['address'] = address
                    data['switch'].append(dct)
                if 'Schalten Status' == suffix:
                    dct['state_address'] = address
                if suffix.endswith('Stromwert'):
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"current"',
                        'device_class': '"current"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)


class SensorParser:
    def parse(self, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                address = group_address.get('Address')
                b_s = {
                    'name': '"{}"'.format(name),
                    'device_class': '"window"',
                    'state_address': '"{}"'.format(address)
                }
                data['binary_sensor'].append(b_s)
