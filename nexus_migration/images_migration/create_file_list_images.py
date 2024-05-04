import requests, json
from logging import error

def get_all_images_for_registry(
  cert_file='/etc/docker/certs.d/ca.crt',
  smog_resources='http://smog.krakow.xxx:8040/v2/', nexus_repository='smog.krakow.xyz:8040/'
):
  response_repo = requests.get(smog_resources + "_catalog/", verify=cert_file)
  images = []
  if (response_repo.status_code == 200):
    for repository in response_repo.json()['repositories']:
      response_images = requests.get(smog_resources + repository + "/tags/list", verify=cert_file)
      if (response_images.status_code == 200):
          for image_tag in response_images.json()['tags']:
            artifact_name=response_images.json()['name']
            image = nexus_repository + artifact_name + ":" + image_tag
            images.append(image)
      else:
        error(f"there was a problem communicating with the {response_images.status_code} api at the {repository} repository")
  else:
      error(f'there was a problem communicating with the {response_repo.status_code} api in accessing repository directories')
  return images  

def write_all_images_to_file(file_name='images_docker.txt'):
  images = get_all_images_for_registry()
  try:
     with open(file_name, 'w') as file_image:  
       for image in images:
          file_image.write(image + '\n')
  except EnvironmentError:
     print(f'failed to save to file {file_name}')
  print(f'list of images saved to file {file_name}')

  
if __name__ == '__main__' :
  write_all_images_to_file()

