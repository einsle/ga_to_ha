import configparser

from lxml import etree


class GenericParser:

    def get_prefix(self, name: str):
        """
        get prefix (first parts split by _) of name

        :param name: name to split into array and get first elements of
        :return: first parts of name
        """
        return "_".join(name.split('_')[0:-1])

    def get_suffix(self, name: str):
        """
        get suffix (last part split by _) of name

        :param name: name to split into array and get last element of
        :return: last part of name
        """
        return name.split('_')[-1]


class LightingParser(GenericParser):
    def parse(self, config: configparser.ConfigParser, node: etree.Element, data: dict):
        """
        parse lighting part of XML file and generate structured data

        :param config: pointer to config options
        :param node: parsex etree XML root node
        :param data: data dict to fill parsed data into it
        :return:
        """
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = self.get_prefix(name)
                suffix = self.get_suffix(name)
                address = group_address.get('Address')
                dct = next((item for item in data['light'] if item['name'] == '"{0}"'.format(prefix)), {'name': '"{0}"'.format(prefix)})
                if config.get('light', 'SuffixAddress') == suffix:
                    dct['address'] = '"{0}"'.format(address)
                    data['light'].append(dct)
                if config.get('light', 'SuffixStateAddress') == suffix:
                    dct['state_address'] = '"{0}"'.format(address)
                if config.get('light', 'SuffixBrightnessAddress') == suffix:
                    dct['brightness_address'] = '"{0}"'.format(address)
                if config.get('light', 'SuffixBrightnessStateAddress') == suffix:
                    dct['brightness_state_address'] = '"{0}"'.format(address)
                if config.get('light', 'SuffixProblem') == suffix:
                    b_s = {
                        'name': '"{0}"'.format(name),
                        'device_class': '"problem"',
                        'state_address': '"{0}"'.format(address)
                    }
                    data['binary_sensor'].append(b_s)
                if config.get('light', 'SuffixLightState') == name.split('_')[1]:
                    b_s = {
                        'name': '"{0}"'.format(name),
                        'device_class': '"light"',
                        'state_address': '"{0}"'.format(address)
                    }
                    data['binary_sensor'].append(b_s)


class CoverParser(GenericParser):
    def parse(self, config: configparser.ConfigParser, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = self.get_prefix(name)
                suffix = self.get_suffix(name)
                address = group_address.get('Address')
                dct = next((item for item in data['climate'] if item['name'] == '"{0}"'.format(prefix)), {'name': '"{0}"'.format(prefix)})
                if config.get('cover', 'SuffixMoveLongAddress') == suffix:
                    dct['move_long_address'] = '"{0}"'.format(address)
                    data['cover'].append(dct)
                    if config.has_option('cover', 'CoverDeviceClass_{0}'.format(prefix).replace(' ', '_')):
                        dct['device_class'] = '"{0}"'.format(config.get('cover', 'CoverDeviceClass_{0}'.format(prefix).replace(' ', '_')))
                    else:
                        dct['device_class'] = '"{0}"'.format(config.get('cover', 'CoverDeviceClass'))
                    if config.has_option('cover', 'CoverTravellingTimeUp_{0}'.format(prefix).replace(' ', '_')):
                        dct['travelling_time_up'] = config.get('cover', 'CoverTravellingTimeUp_{0}'.format(prefix).replace(' ', '_'))
                    else:
                        dct['travelling_time_up'] = config.get('cover', 'CoverTravellingTimeUp')
                    if config.has_option('cover', 'CoverTravellingTimeDown_{0}'.format(prefix).replace(' ', '_')):
                        dct['travelling_time_down'] = config.get('cover', 'CoverTravellingTimeDown_{0}'.format(prefix).replace(' ', '_'))
                    else:
                        dct['travelling_time_down'] = config.get('cover', 'CoverTravellingTimeDown')
                if config.get('cover', 'SuffixStopAddress') == suffix:
                    dct['stop_address'] = '"{0}"'.format(address)
                if config.get('cover', 'SuffixPositionAddress') == suffix:
                    dct['position_address'] = '"{0}"'.format(address)
                if config.get('cover', 'SuffixPositionStateAddress') == suffix:
                    dct['position_state_address'] = '"{0}"'.format(address)


class ClimateParser(GenericParser):
    def parse(self, config: configparser.ConfigParser, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = self.get_prefix(name)
                suffix = self.get_suffix(name)
                address = group_address.get('Address')
                dct = next((item for item in data['climate'] if item['name'] == '"{0}"'.format(prefix)), {'name': '"{0}"'.format(prefix)})
                if config.get('climate', 'SuffixTemperatureAddress') == suffix:
                    dct['temperature_address'] = '"{0}"'.format(address)
                    data['climate'].append(dct)
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"temperature"',
                        'device_class': '"temperature"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if config.get('climate', 'SuffixTargetTemperatureAddress') == suffix:
                    dct['target_temperature_address'] = '"{0}"'.format(address)
                if config.get('climate', 'SuffixTargetTemperatureStateAddress') == suffix:
                    dct['target_temperature_state_address'] = '"{0}"'.format(address)
                if config.get('climate', 'SuffixSetpointShiftAddress') == suffix:
                    dct['setpoint_shift_address'] = '"{0}"'.format(address)
                if config.get('climate', 'SuffixSetpointShiftStateAddress') == suffix:
                    dct['setpoint_shift_state_address'] = '"{0}"'.format(address)
                    dct['setpoint_shift_mode'] = '"{0}"'.format(config.get('climate', 'ClimateSetpointShiftMode'))
                    dct['temperature_step'] = config.get('climate', 'ClimateTemperatureStep')
                    dct['setpoint_shift_max'] = config.get('climate', 'ClimateSetpointShiftMax')
                    dct['setpoint_shift_min'] = config.get('climate', 'ClimateSetpointShiftMin')
                if config.get('climate', 'SuffixOperationModeAddress') == suffix:
                    dct['operation_mode_address'] = '"{0}"'.format(address)
                if config.get('climate', 'SuffixOperationModeStateAddress') == suffix:
                    dct['operation_mode_state_address'] = '"{0}"'.format(address)
                if config.get('climate', 'SuffixCommandValueStateAddress') == suffix:
                    dct['command_value_state_address'] = '"{0}"'.format(address)
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"percent"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if config.get('climate', 'SuffixProblem') == suffix:
                    b_s = {
                        'name': '"{}"'.format(name),
                        'device_class': '"problem"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['binary_sensor'].append(b_s)
                if config.get('climate', 'SuffixDiagnostics') == suffix:
                    text = {'name': '"{}"'.format(name),
                            'address': '"{}"'.format(address)}
                    data['text'].append(text)
                if config.get('climate', 'SuffixHumidity') == suffix:
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"humidity"',
                        'device_class': '"humidity"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if config.get('climate', 'SuffixAirQualityVoc') == suffix:
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"pulse_2byte"',
                        'device_class': '"volatile_organic_compounds"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if config.get('climate', 'SuffixAirQualityPpm') == suffix:
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"ppm"',
                        'device_class': '"volatile_organic_compounds"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if config.get('climate', 'SuffixForceState') == suffix:
                    switch = {
                        'name': '"{}"'.format(name),
                        'address': '"{}"'.format(address),
                    }
                    data['switch'].append(switch)


class SwitchParser(GenericParser):
    def parse(self, config: configparser.ConfigParser, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = self.get_prefix(name)
                suffix = self.get_suffix(name)
                address = group_address.get('Address')
                dct = next((item for item in data['switch'] if item['name'] == '"{}"'.format(prefix)), {'name': '"{}"'.format(prefix)})
                if config.get('switch', 'SuffixAddress') == suffix:
                    dct['address'] = '"{}"'.format(address)
                    data['switch'].append(dct)
                if config.get('switch', 'SuffixStateAddress') == suffix:
                    dct['state_address'] = '"{}"'.format(address)
                if suffix.endswith(config.get('switch', 'SuffixCurrent')):
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"current"',
                        'device_class': '"current"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)
                if suffix.endswith(config.get('switch', 'SuffixPower')):
                    sensor = {
                        'name': '"{}"'.format(name),
                        'type': '"power"',
                        'device_class': '"power"',
                        'state_address': '"{}"'.format(address)
                    }
                    data['sensor'].append(sensor)


class SensorParser(GenericParser):
    def parse(self, config: configparser.ConfigParser, node: etree.Element, data: dict):
        for child in node.getchildren():
            for group_address in child.getchildren():
                name = group_address.get('Name')
                prefix = self.get_prefix(name)
                suffix = self.get_suffix(name)
                address = group_address.get('Address')
                b_s = {
                    'name': '"{}"'.format(name),
                    'device_class': '"{0}'.format(config.get('sensor', 'SensorDeviceClass')),
                    'state_address': '"{}"'.format(address)
                }
                if config.has_option('sensor', 'SensorDeviceClass_{0}'.format(prefix).replace(' ', '_')):
                    b_s['device_class'] = config.get('cover', 'SensorDeviceClass_{0}'.format(prefix).replace(' ', '_'))
                data['binary_sensor'].append(b_s)
