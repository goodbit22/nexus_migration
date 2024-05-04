#!/usr/bin/env python3
from sys import argv
from os import path, system

artifact_file = "current_artifact.txt"


def get_last_processed_artifact(current_artifact_file_name=artifact_file) -> str:
    current_artifact = ''
    if path.isfile(current_artifact_file_name):
        print("File {0} exists".format(current_artifact_file_name))
        with open(current_artifact_file_name, 'r+') as current_artifact_file:
            current_artifact = current_artifact_file.readline().replace('\n', '')
    else:
        create_empty_file(current_artifact_file_name)
    return current_artifact


def create_empty_file(current_artifact_file_name):
    print("File {0} does not exist".format(current_artifact_file_name))
    with open(current_artifact_file_name, 'w'):
        pass
    print("File {0} was created".format(current_artifact_file_name))


def read_artifacts_file(artifacts_file_name='test_data.txt'):
    with open(artifacts_file_name, 'r') as artifacts_file:
        artifacts = [artifact.replace('\n', '') for artifact in artifacts_file.readlines()]
    return artifacts


def read_start_index(artifacts):
    current_artifact = get_last_processed_artifact()
    if current_artifact == "":
        return 0
    elif current_artifact.find(',') == -1:
        raise Exception("Clean up {0} or write a line that you would like to start processing from. It should be in format name,index".format(artifact_file))
    current_name_artifact, current_index = current_artifact.split(',')
    if artifacts[int(current_index)] == current_name_artifact:
        return int(current_index)
    else:
        raise Exception("We couldn't find given line in artifacts to be processed, check {0}. It should be in format name,index ".format(artifact_file))


def move_artifacts(process_next_x_lines, current_artifact_file_name=artifact_file):
    artifacts = read_artifacts_file()
    start_index = read_start_index(artifacts)
    end_index = start_index + process_next_x_lines

    if end_index > len(artifacts):
        print("You picked range that is higher that possible artifacts to migrate, ")
        end_index = len(artifacts)

    def save_currently_processed_artifact(index):
        with open(current_artifact_file_name, 'w') as current_artifact_file:
            current_artifact_file.write(artifact + ',' + str(index))

    print("Starting artifact upload from source nexus to target nexus...")
    for index_current in range(start_index, end_index):
        artifact = artifacts[index_current]
        save_currently_processed_artifact(index_current)
        print('Executing command {0}'.format(artifact))
        system(artifact)
        print('Executed {0}'.format(artifact))


def main():
    number_arguments = len(argv)
    if number_arguments == 1:
        print("You need to pick how many upload commands will be processed")
    elif number_arguments == 2:
        try:
            start_from_line = int(argv[1])
            print("We will process {0} lines".format(start_from_line))
            move_artifacts(start_from_line)
        except ValueError:
            print("Amount of lines to process should be an numeric value")
    else:
        print("Too many arguments")


if __name__ == "__main__":
    main()
