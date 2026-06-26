import sys
import boto3
#

def get_text_response(model, input_content):

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    message = {
        "role": "user",
        "content": [ { "text": input_content } ]
    }
    
    response = bedrock.converse(
        modelId=model,
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "stopSequences": []
        },
    )
    
    return response['output']['message']['content'][0]['text']
    

response = get_text_response(sys.argv[1], sys.argv[2])

print(response)

# execute the script with the following command:
# python3 params.py <model_name> <input_content>
# python3 params.py "mistral.mixtral-8x7b-instruct-v0:1" "Write a haiku:" 


'''
launch.json file is used to configure the debugging settings for Visual Studio Code (VS Code). It allows you to specify how to launch and debug your Python scripts. In this case, it is set up to run the params.py script with specific arguments.

{
    // IntelliSense를 사용하여 가능한 특성에 대해 알아보세요.
    // 기존 특성에 대한 설명을 보려면 가리킵니다.
    // 자세한 내용을 보려면 https://go.microsoft.com/fwlink/?linkid=830387을(를) 방문하세요.
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python 디버거: 현재 파일",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": [
                "global.anthropic.claude-sonnet-4-5-20250929-v1:0",
                "Write a haiku:"
            ]
        }
    ]
}

"Write a haiku"는 영어 표현으로, 직역하면 "하이쿠를 쓰다"라는 뜻.
여기서 haiku(하이쿠)는 일본 전통 시 형식으로, 보통 5-7-5 음절 구조의 세 줄로 이루어진 아주 짧은 시를 말함. 
자연, 계절, 감정 같은 주제를 간결하게 표현하는 것이 특징.


'''
