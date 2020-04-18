# JobSubmitter

## Submit job to jenkins and fetch status

This is simple web application for triggering already created jobs to build in jenkins and fetching build status.

Current implementation can works only with token that was generated in Jenkins.

To run application type:
1. ```docker build -t app .```
1. ```docker-compose up -d```

For testing this [repo](https://github.com/AlexandrKhabarov/simple-java-maven-app) can be used.

