import typer
from lxml import etree
from einsle.knx.parser import BeleuchtungParser, BeschattungParser, KontakteParser


def main(file: str):
    tree = etree.parse(file)
    root = tree.getroot()
    print('knx:')
    if len(root):
        for node in root.getchildren():
#             print(node.get('Name'))

            if "Beleuchtung" == node.get('Name'):
                BeleuchtungParser().parse(node)
            if "Beschattung" == node.get('Name'):
                BeschattungParser().parse(node)
            if "Kontakte" == node.get('Name'):
                KontakteParser().parse(node)


if __name__ == '__main__':
    typer.run(main)
