import xml.etree.ElementTree as ET

def get_pom_info(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    with open(output_file, "w") as f:
        for child in root.iter():
            text = 'mvn -s deploy.xml deploy:deploy-file '
            if child.tag in ['artifactId']:
                text +=  ' -DartifactId=' + child.text
            if child.tag in ['groupId']:
                text += ' -DgroupId=' + child.text 
            if child.tag in ['version']:
                text += ' -Dversion=' + child.text
            text +=  ' -Dpackaging=jar' 
            # if child.tag in ['pomFile']:
            #     text += child.text
            # if child.tag in ['url']:      
            #     text += child.text
            f.write(f"{text}\n")
            text=''


if __name__ == "__main__":
    xml_file_path = "pom.xml"
    output_file_path = "test_data.txt"
    get_pom_info(xml_file_path, output_file_path)
