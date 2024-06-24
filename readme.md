### Notes on Task
While the deployment was posible using SAM CLI, there is a complication at the last layer of the task. The job that picks up the id_param from the EventBus from the Async Job function was not created via SAM or something alonf tbat line. 

But I trust the code at the last level. 

My Deployment URL= https://h7pdiewrb7.execute-api.us-east-1.amazonaws.com/Prod/dataspan/delay

### Stesps for Deployment.

* The easiest way to deploy the code in this repo is to clone the repo

``` git clone git@github.com:philipokiokio/ds_serverless.git ```

* The next step is to export the ```AWS_SECRET``` and ```AWS_SECRET_KEY``` which is the alternative to the AWS SECRET embeded sucesssfully in the *environmnental_variables* of the computer.

* The next step is depended on the SAM cli installed [not need if SAM has been installed]:
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

* The command to deploy to AWS via sam is
``` sam deploy --guided```


## Feedback Question

##### suppose we want to apply this limit per user (say we have 12,000 users) - meaning that each user can have up to 5 concurrent jobs

 answer: 

 ```    
    If the job is limited to 5 people the approach would include 
    1. The user_uid: this can be extracted via the auth token.
    2. The user_uid is store with every job record in dynamo db with the user_uid. 
    3. This user_uid is then used to query the record of active job as such the filter case is user_uid== user_uid AND status=="ACTIVE"
    4. This case above combine assures that it is impossible to have more than 5 when combine with the rest of the architecture.
    
```

##### after handling millions of requests - how long will dynamodb.scan() take?
answer: 
```
    I cant categorically state the answer to this question but from my experience with SQL DB's I will infer that it takes a few secs and here is why. The scan() function/method without a filter_case all the documents will be loaded in the memory, however with a filter_case say we are interest in all completed cases for a user we cut down the documents feteched.

    I think a subset of data would be faster than loading all data into memory.

```
