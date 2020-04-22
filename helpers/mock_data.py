from json import dumps

body = {
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "us-east-1",
            "eventTime": "2020-04-22T14:43:18.042Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "A36QOG33I2IUIN"
            },
            "requestParameters": {
                "sourceIPAddress": "192.80.110.129"
            },
            "responseElements": {
                "x-amz-request-id": "9D4830BD1AC60B88",
                "x-amz-id-2": "4Xhv6ul2GB7lQDZ9UH7knXLlmKSr9R4Qqfc7b/DqnipNEzLtTZ/tvgcSmudUctjh6KmNSOh0tu+UZuSHv+0cI5KP9elfZftUrJU2PnWt23s=",
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "ProcessImages",
                "bucket": {
                    "name": "knoppers.icu",
                    "ownerIdentity": {
                        "principalId": "A36QOG33I2IUIN"
                    },
                    "arn": "arn:aws:s3:::knoppers.icu",
                },
                "object": {
                    "key": "images/unprocessed/spring/DSC_3942.jpg",
                    "size": 1227,
                    "eTag": "cdd580c254b3999e0a3af7d0cbe3d08a",
                    "sequencer": "005EA0580AE200DB88",
                },
            },
        }
    ]
}

message = {
    "messageId": "3c341ef2-4878-4d6a-936b-acd6a1a51332",
    "receiptHandle": "AQEBVeihIg82bitJFSLcyfhaoh7FkN5cRBczwtjcxXykgH+gGPpVuojBWnh5hGLYMX/EJsYvKQHoylqsJUwYHann0cs83+YMHxT1s/g73S7sa6ktl3vQexN+tbZqdist+VCVLEiljyXFllwXob6RQ0CyrhxKJ8dTTJ4qmEejRJWsXkRGGOIEH+jEZF3USl8OChujx5kh9Mk0u6QrHgiSSJ5GnmDYFtT4NZbv6QZpYggsuy7BncrIsCgvOmRAw+KQPxZB4Gl0EQ3Jjv/9+EV/Ug5nkmzkh8lkxw9V3yG5FoWZrr8yYi1datcZG4twbq4n4bslMjOtUavj7jvAWxWQxdxmQvBFefaMYHptJ/rEmKUcH1Pox0khtvQISAPUNMaZxnnOvakiY4Zi7yP7Xb9SUqgDkQ==",
    "body": dumps(body),
    "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1587566604108",
        "SenderId": "AIDAJHIPRHEMV73VRJEBU",
        "ApproximateFirstReceiveTimestamp": "1587566604109",
    },
    "messageAttributes": {},
    "md5OfBody": "6e6b43be4bc5be47255d5ee579647c6f",
    "eventSource": "aws:sqs",
    "eventSourceARN": "arn:aws:sqs:us-east-1:961171806715:img-pipe-knopper-icu",
    "awsRegion": "us-east-1",
}

event = {"Records": [message]}
