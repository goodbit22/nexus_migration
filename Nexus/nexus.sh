#!/bin/bash

NEXUS_BASE_URL=http://localhost:8081#### # to change!
NEXUS_API_REPOSITORIES=$NEXUS_BASE_URL/service/rest/v1/repositories
NEXUS_API_SEARCH=$NEXUS_BASE_URL/service/rest/v1/search?repository=
NEXUS_API_DELETE_COMPONENT=$NEXUS_BASE_URL/service/rest/v1/components
NEXUS_API_TASK_LIST=$NEXUS_BASE_URL/service/rest/v1/tasks
NEXUS_API_TASK_RUN=$NEXUS_BASE_URL/service/rest/v1/tasks

USER=#### # to change!
PASSWORD=#### # to change!

listRepoNames () {

	curl -s -X GET -u $USER:$PASSWORD $NEXUS_API_REPOSITORIES | jq '.[].name' | sed 's/"//g'

}

listDockerImages () {
   
	curl -s -u $USER:$PASSWORD -X GET "${NEXUS_API_SEARCH}$1" | jq '.items' | jq '.[]|.name + ":" + .version + " ->" + .id' | sed 's/"//g' >> components.json

	if [ -s components.json ]; then 
	  echo "Images for repository $repoName"
	  cat components.json | sed 's/->.*//'
	else
	  echo "No components for this repo!"
	  exit
	fi	  
}

deleteSingleComponent() { # $1 - component_id
   
	curl -s -u $USER:$PASSWORD -X DELETE "${NEXUS_API_DELETE_COMPONENT}/$1"

}

selectComponentsToDelete () { #$1 - patern 

	cat components.json | grep $1 >> componentsToDelete.json

	if [ -s componentsToDelete.json ]; then 
	  cat componentsToDelete.json
	  sed -i 's/^.*->//' componentsToDelete.json
	else	
	  echo "Pattern not found!"
	  exit
	fi    
}

deleteComponents () {
  
	while read p; do
	deleteSingleComponent $p  
	done < componentsToDelete.json
}

listTasks () {
  
	curl -s -u $USER:$PASSWORD -X GET $NEXUS_API_TASK_LIST | jq '.items' | jq '.[]|.name + " ->" + .id' | sed 's/"//g' >> tasks.json
	echo "Tasks list:"
	cat tasks.json | sed 's/->.*//'

}

runTask () {

	curl -s -u $USER:$PASSWORD -X POST $NEXUS_API_TASK_RUN/$1/run
}

runTasks () {
	
	while read p; do
	runTask $p  
	done < tasksToRun.json

}

selectTask () { #$1 - patern 

	cat tasks.json | grep $1 > tasksToRun.json
	
	if [ -s tasksToRun.json ]; then 
	  cat tasksToRun.json
	  sed -i 's/^.*->//' tasksToRun.json
	else	
	  echo "Task not found!"
	  exit
	fi    
}

deleteNexusComponent () {

	echo "Repository names:"
	listRepoNames

	echo "Pick repository(name):"
	read -e repoName
	listDockerImages $repoName

	echo "Insert patern:"
	read -e patern

	selectComponentsToDelete $patern
	deleteComponents
	echo "--------------------"

}

executeNexusTask () {

	listTasks
	anotherTask="Y"
	
	while [ $anotherTask = "Y" -o $anotherTask = "y" ]
	do
		echo "Pick task to run:"
		read -e taskPatern
		
		echo "$taskPatern"
		selectTask $taskPatern
		runTasks
		echo "Run other task?(Y/N)"
		read -e anotherTask
	done
}

cleanProcessWorkspace () {

	rm -rf components.json
	rm -rf componentsToDelete.json
	rm -rf tasks.json
	rm -rf tasksToRun.json
}

cleanProcessWorkspace

deleteNexusComponent
executeNexusTask

cleanProcessWorkspace
