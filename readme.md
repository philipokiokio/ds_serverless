### Notes on Task
While the deployment was posible using SAM CLI, there is a complication at the last layer of the task. The job that picks up the id_param from the EventBus from the Async Job function was not created via SAM or something alonf tbat line. 

But I trust the code at the last level. 

My Deployment URL= https://h7pdiewrb7.execute-api.us-east-1.amazonaws.com/Prod/dataspan/delay

### Stesps for Deployment.

The easiest way to deploy the code in this repo is to clone the repo

``` git clone git@github.com:philipokiokio/ds_serverless.git ```

The next step is to export the ```AWS_SECRET``` and ```AWS_SECRET_KEY``` which is the alternative to the AWS SECRET embeded sucesssfully in the *environmnental_variables* of the computer.
The next step is depended on the SAM cli installed:
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

The command to deploy to AWS via sam is
``` sam deploy --guided     ```
