from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.evaluation.qa import QAEvalChain
import os
from evaluate import load

os.environ['OPENAI_API_KEY'] = ""

prompt = PromptTemplate(template="You are an expert lawyer answering a question from a Bar Exam. Here is the: {question}", 
                        input_variables=["question"])
llm = OpenAI(model_name="text-davinci-003", temperature=0.)
chain = LLMChain(llm=llm, prompt=prompt)

# TODO: Import our jsonl files and format it into a list with each element being a Dict with a "question" key and an "answer" key (see below example).
# Here is an example from the Barabri data:
examples = [
    {
        "question": """
                    St. Minny, a town with a population of 30,000 , was located on the west bank of a small river. Immediately across the river, on the east bank, was Paulopolis, a city of 60,000 . Over the years, many civic improvement groups urged that the two municipalities be merged into "Minnypaulos," a single city of 90,000 souls. The arguments in favor of merger stressed savings to taxpayers accruing from the elimination of duplicate services. Proposals to merge the two places had appeared as referenda on the ballot on two separate occasions. Although the voters of Paulopolis approved each proposal by heavy margins, the voters of St. Minny, fearing that control of the government would be in the hands of more populous Paulopolis, rejected the referendum proposals by more than two to one.

                    To avoid the failure of yet another such referendum, a new proposal was made for the governance of the proposed combined city. For a period of 20 years, beginning at the date of the merger, the city council of the merged city would consist of six persons. The former Paulopolis would be divided into three council districts, as would the former city of St. Minny. Thus, each St. Minny council representative would be elected from a district with a population of 10,000, while the Paulopolis districts would contain 20,000 persons each. A mayor would be elected at large. The proposal was placed on the ballot and was carried by large majorities in both St. Minny and Paulopolis. Representatives from Paulopolis and St. Minny carved each former city into three council electoral districts. Three Paulopolis taxpayers filed suit to enjoin the holding of an election with council districts of such disparate proportions.

                    Which of the following represents the plaintiffs' best constitutional argument?
                    A. The government of the merged cities is not a republican form of government.

                    B. The plaintiffs and other Paulopolitans have been denied equal protection of the law.

                    C. The plaintiffs and other Paulopolitans have been denied the privileges and immunities of citizenship as guaranteed by Article IV. of the federal Constitution.

                    D. The plaintiffs and other Paulopolitans have been denied due process of law.

                    Final Answer ('A.', 'B.', 'C.' or 'D.'):
                    """,
        "answer": "B."
    }
]

# This will predict an "answer" for every "question", iterating through each Dict in the list
predictions = chain.apply(examples)

########################
# LLM-based Eval
########################
_PROMPT_TEMPLATE = """You are an expert professor specialized in grading answers to questions.
You are grading the following question:
{query}
Here is the real answer:
{answer}
You are grading the following predicted answer:
{result}
What grade do you give from 0 to 10, where 0 is the lowest (very low similarity) and 10 is the highest (very high similarity)?
"""

PROMPT = PromptTemplate(input_variables=["query", "answer", "result"], template=_PROMPT_TEMPLATE)
eval_chain = QAEvalChain.from_llm(llm)
graded_outputs = eval_chain.evaluate(examples, predictions, 
                                     question_key="question", prediction_key="text")

########################
# Determinisic Classic Eval
########################
for i, eg in enumerate(examples):
    eg['id'] = str(i)
    eg['answers'] = {"text": [eg['answer']], "answer_start": [0]}
    predictions[i]['id'] = str(i)
    predictions[i]['prediction_text'] = predictions[i]['text']

for p in predictions:
    del p['text']

new_examples = examples.copy()
for eg in new_examples:
    del eg ['question']
    del eg['answer']

squad_metric = load("squad")
results = squad_metric.compute(
    references=new_examples,
    predictions=predictions,
)
