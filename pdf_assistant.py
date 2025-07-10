from agno.agent import Agent
import typer
from typing import Optional, List
from agno.models.groq import Groq
from agno.storage.postgres import PostgresStorage
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector, SearchType

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
  urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
  vector_db = PgVector(table_name="recipes", db_url=db_url, search_type=SearchType.hybrid)
)

knowledge_base.load()

storage= PostgresStorage(table_name="pdf_assistant", db_url=db_url)

def pdf_assistant(new: bool = False, user: str = "user"):
  assistant = Agent(
    model = Groq(id = "Meta-Llama/Llama-4-Maverick-17b-128e-instruct"),
    user_id = user,
    knowledge = knowledge_base,
    storage = storage,
    show_tool_calls = True,
    search_knowledge = True,
    read_chat_history = True,
  )

  assistant.cli_app(markdown = True)


if __name__ == "__main__":
  typer.run(pdf_assistant)







