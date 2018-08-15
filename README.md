## How it works

A explanation on how it works can founded here:

- https://dev.to/diegonalvarez/aws-lambda---step-functions---rds---s3---aurora---part-1-1fe


### Json For Unique Machine

```
{
  "Comment": "State machine to populate databases for reports.",
  "StartAt": "MySql To S3 Files",
  "States": {
    "MySql To S3 Files": {
      "Type": "Task",
      "Resource": "ARN",
      "ResultPath": "$.guid",
      "Next": "S3 Data To Mysql",
      "Retry": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ]
    },
    "S3 Data To Mysql": {
      "Type": "Task",
      "Resource": "ARN",
      "InputPath": "$.guid",
      "End": true,
      "Retry": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ]
    }
  }
}
```

### Json For Parallel Machines

```
{
  "Comment": "State machine to populate databases for reports.",
  "StartAt": "MySql To S3 Files",
  "States": {
    "MySql To S3 Files": {
      "Type": "Task",
      "Resource": "lambda-arn",
      "ResultPath": "$.guid",
      "Next": "InsertDataToMysql",
      "Retry": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ]
    },
    "InsertDataToMysql": {
      "Type": "Parallel",
      "End": true,
      "Branches": [
        {
         "StartAt": "InsertLeadsMysql",
         "States": {
           "InsertInfoOrderMysql": {
             "Type": "Task",
             "Resource":
               "lambda-arn",
             "End": true
           }
         }
       },
       {
         "StartAt": "InsertRestMysql",
         "States": {
           "InsertRestMysql": {
             "Type": "Task",
             "Resource":
               "lambda-arn",
             "End": true
           }
         }
       }
      ]
    }
  }
}
```