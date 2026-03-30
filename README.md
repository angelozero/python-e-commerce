# python-e-commerce

```shell
# 1 
# via terminal
# curl http://localhost:4000/v1/models
# {
#     "data": [
#         {
#             "id": "ai-angelo-zero",
#             "object": "model",
#             "created": 1677610602,
#             "owned_by": "openai"
#         }
#     ],
#     "object": "list"
# }

# 2
# launchctl setenv OLLAMA_HOST "0.0.0.0"

# 3
# Open Ollama and execute on terminal 'netstat -an | grep 11434'
# The result must be like this
# tcp46      0      0  *.11434                *.*                    LISTEN 
```