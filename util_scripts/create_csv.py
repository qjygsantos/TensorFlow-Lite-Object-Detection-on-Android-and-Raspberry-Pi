import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            filename = root.find('filename').text
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)
            name = member.find('name').text
            
            xmin = int(member.find('bndboxxmin').text) if member.find('bndboxxmin') is not None else None
            ymin = int(member.find('bndboxymin').text) if member.find('bndboxymin') is not None else None
            xmax = int(member.find('bndboxxmax').text) if member.find('bndboxxmax') is not None else None
            ymax = int(member.find('bndboxymax').text) if member.find('bndboxymax') is not None else None
            
            xml_list.append((filename, width, height, name, xmin, ymin, xmax, ymax))

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    for folder in ['train','validation']:
        image_path = os.path.join(os.getcwd(), ('images' + folder))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(('images' + folder + '_labels.csv'), index=None)
        print('Successfully converted xml to csv.')

main()
