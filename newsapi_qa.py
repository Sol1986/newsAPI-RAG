from langchain_community.document_loaders import JSONLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(), override=True)


loader = JSONLoader(
    file_path = '/content/cleaned_articles.json',
    text_content = False,
    jq_schema = '.[].content'
)

data = loader.load()



text_splitter =RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=0)
chunks = text_splitter.split_documents(data)


embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(chunks, embeddings)

def ask_and_get_answer(vectorstore, question, chat_history = []):
  llm = ChatOpenAI(model ='gpt-3.5-turbo', temperature =1)
  retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k':3})

  conversational_chain = ConversationalRetrievalChain.from_llm(
      llm=llm,
      chain_type ="stuff",
      retriever =retriever,
      return_source_documents= True
  )
  answer = conversational_chain({'question': question, 'chat_history': chat_history})
  chat_history.append((question, answer['answer']))
  return answer, chat_history



#Setting it up as a chat conversation

import time
i = 1
chat_history=[]
print('write Quit to quit')
while True:
  question= input(f'Question #{i}: ')
  i = i+1
  if question.lower() in ['quit', 'exit']:
    print('Quitting... bye')
    time.sleep(2)
    break
  answer, chat_history = ask_and_get_answer(vectorstore, question, chat_history)
  print(f'Answer: {answer["answer"]}')
  print(f'\n{"-"*50}\n')