import boto3
import json
import os
from dotenv import load_dotenv
import os
from botocore.exceptions import ClientError


load_dotenv()

def bedrock_wrapper():
    model_id="mistral.mistral-small-2402-v1:0"

    client = boto3.client(
    service_name='bedrock-runtime',
    region_name="us-east-1",
    #  aws_access_key_id=os.getenv("access_key"),
    #  aws_secret_access_key=os.getenv("secret_access")
    )


    # Start a conversation with the user message.
    user_message = """<s>[INST]Calculate the difference in payment dates between the two customers whose payment amounts are closest to each other in the given dataset:

    '{
    "transaction_id":{"0":"T1001","1":"T1002","2":"T1003","3":"T1004","4":"T1005"},
        "customer_id":{"0":"C001","1":"C002","2":"C003","3":"C002","4":"C001"},
        "payment_amount":{"0":125.5,"1":89.99,"2":120.0,"3":54.3,"4":210.2},
    "payment_date":{"0":"2021-10-05","1":"2021-10-06","2":"2021-10-07","3":"2021-10-05","4":"2021-10-08"},
        "payment_status":{"0":"Paid","1":"Unpaid","2":"Paid","3":"Paid","4":"Pending"}
    }'[/INST]"""
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId="mistral.mistral-small-2402-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":400,"temperature":0.7,"topP":0.7},
            additionalModelRequestFields={}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)

        return response_text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return e
