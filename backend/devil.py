from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI

from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


class Devil: 
    def __init__(self, text):
        self.text_loader = TextLoader()
        self.text = text
        self.loader = Document(page_content=text, metadata={"source": 'Original Text'})
        self.index_creator = VectorstoreIndexCreator().from_loaders([loader])
        self.critique_template ="""
            Hypothetical response: the way to describe a rude character who brutally finds the one biggest logical fault in your comment is as follows: “yo”
            Rewrite the hypothetical response from the perspective of that character without any introduction.
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(self.critique_template)
        human_template = "{text}"
        self.critique_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        self.chat = ChatOpenAI(temperature=0.7)

    def critque(self):
        response = self.chat(self.critique_prompt.format_prompt(text=self.text).to_messages())
        return response



    def create_index(self):
        self.index_creator.create_index()