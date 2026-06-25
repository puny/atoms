import json
import boto3

session = boto3.Session()

bedrock = session.client(service_name='bedrock-runtime', region_name='us-east-1') #creates a Bedrock client
bedrock_model_id = "global.anthropic.claude-sonnet-4-5-20250929-v1:0" #set the foundation model
prompt = "What is the largest city in New Hampshire?" #the prompt to send to the model

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",                
                "text": prompt
            }
        ]
    }
]

body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "messages": messages,
    "max_tokens": 1024,
    "top_p": 0.5
    
}) #build the request payload
# body = json.dumps({
#     "schemaVersion": "messages-v1",
#     "messages": messages,
#     "inferenceConfig": {
#         "max_tokens": 1024,
#         "top_p": 0.5,
#         "top_k": 20,
#         "temperature": 0.0
#     }
# }) #build the request payload


response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json') #send the payload to Amazon Bedrock

response_body = json.loads(response.get('body').read().decode('utf-8')) # read the response

# response_text = response_body["output"]["message"]["content"][0]["text"] #extract the text from the JSON response
response_text = response_body['content'][0]['text']

print(response_text)
