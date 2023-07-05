# Set up local environment

```
cd FastChat
git checkout fschat-with-top-k-kb-prompts
cd ../Vicuna-LangChain
```

# Select Model
- lmsys/fastchat-t5-3b-v1.0
- lmsys/vicuna-7b-v1.3

```
export MODEL_NAME=lmsys/vicuna-7b-v1.3
```

## Chat without KB

```
python3 vicuna_cli.py --vicuna-dir $MODEL_NAME --load-8bit
```

## Chat with KB

```
python3 vicuna_cli.py --vicuna-dir $MODEL_NAME --load-8bit --knowledge-base
```






