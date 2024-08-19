from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="LLM-APPLICATION-USING-LCEL"

model = ChatGroq(model="Gemma2-9b-It",api_key=GROQ_API_KEY)

## 1. Create Prompt Template

system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [
    ("system",system_template),
    ("user","{text}")
    ]
)

parser = StrOutputParser()

## Chain
chain =  prompt_template|model|parser


## App Defination
app=FastAPI(title="Langchain Serve",
            version="1.0",
            description="A Simple API server using Langchain runnable interfaces")

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)