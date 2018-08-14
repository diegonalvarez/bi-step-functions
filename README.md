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