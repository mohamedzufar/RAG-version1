from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class GenerationPipeline:
    def __init__(self):
        # ✅ Phi model for generation
        self.llm = OllamaLLM(
            model="phi",  # ✅ Use phi
            temperature=0,
            base_url="http://localhost:11434"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant.
            ONLY answer using the provided context.
            If the context doesn't contain the answer, say "I don't know".
            
            CONTEXT:
            {context}"""),
            ("human", "Question: {question}\n\nAnswer:")
        ])
    
    def generate(self, context: str, question: str) -> str:
        try:
            chain = self.prompt | self.llm | StrOutputParser()
            return chain.invoke({
                "context": context,
                "question": question
            })
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "I encountered an error. Please try again."