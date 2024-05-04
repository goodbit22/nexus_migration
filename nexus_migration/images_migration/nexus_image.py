#!/usr/bin/env python3
import json, requests, docker
from os import path
from datetime import date, datetime

def get_last_processed_image(current_tag_file_name='current_tag.txt') -> str:
	current_tag = ''
	if path.isfile(current_tag_file_name):
		print(f'file {current_tag_file_name} exists')	
		with open(current_tag_file_name, 'r+') as current_tag_file:
			current_tag = current_tag_file.readline().replace('\n', '')
	else:	
		print(f'file {current_tag_file_name} does not exist')	
		with open(current_tag_file_name, 'w') as current_tag_file:
			pass
		print(f'file {current_tag_file_name} has been created')	
	return current_tag

def read_file_image_docker(image_tags_file_name='images_docker.txt'): 
	with open(image_tags_file_name, 'r') as image_tags_file:
		image_tags = [image_tag.replace('\n', '') for image_tag in image_tags_file.readlines()] 	
	return image_tags

def check_file_correct_entry(image_tags): 
	current_tag = get_last_processed_image()
	if current_tag == "":
		return 0
	elif current_tag.find(',') == -1:
		raise Exception("Clean the file with the last line or insert the line you want to start with")	
	else: 
		current_name_tag, current_index = current_tag.split(',')
		if image_tags[int(current_index)] == current_name_tag:
			return int(current_index)
		else:
			raise Exception("Clean the file with the last line or insert the line you want to start with.")	
		
def push_images_from_smog_to_nexus(
	current_tag_file_name='current_tag.txt', 
	cert_file='/etc/docker/certs.d/ca.crt',
	smog_resources='https://repo.krakow.xyz:5001/v2/',
	smog_repository='repo.krakow.xyz:5001/',
	nexus_repository='nexus.czk/repository/docker/' 
):
	client = docker.from_env()
	image_tags = read_file_image_docker()
	index = check_file_correct_entry(image_tags)
	print(f'downloading of docker images from the  {smog_resources}')

	def write_file_current_tag():
		with open(current_tag_file_name, 'w') as current_tag_file:
			current_tag_file.write(image + ',' + str(index_current))
	
	def write_file_error_log(message):	
		file_name_error='error.log'
		current_time= str(datetime.now())
		with open(file_name_error, 'a+') as file_error:
			file_error.write(message + current_time + '\n')
	
	def clean_content_current_tag_file():
		with open(current_tag_file_name, 'w') as current_tag_file:
			pass
		print(f"the content of file {current_tag_file_name} has been cleared as all images in the file have been processed")

	for index_current in range(index, len(image_tags)):
		image = image_tags[index_current]
		print(f"image download started {image}")
		write_file_current_tag()
		print(f"docker pull {image}")
		img = client.images.pull(image)
		delete_word='repo.krakow.xyz:5001/'
		new_tag = nexus_repository + image_tags[index_current].replace(delete_word, "")
		print(f"docker tag {image} {new_tag}")
		img.tag(new_tag)
		print("image push started")
		print(f"docker push {new_tag}")
		client.images.push(new_tag)
		try: 
			print("deletion of a previously downloaded image")
			print(f"docker rmi {image}")
			client.images.remove(image)
			print("deletion of previously tagged downloaded image")
			print(f"docker rmi {new_tag}")
			client.images.remove(new_tag)
		except docker.errors.DockerException as ex:
			write_file_error_log(str(ex))
		clean_content_current_tag_file()

if  __name__ == '__main__' :
	push_images_from_smog_to_nexus()
