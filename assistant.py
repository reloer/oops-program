
from core.search import search_memories

def answer_question(question):

    results = search_memories(question, top_k=5)

    if not results:
        return "I couldn't find relevant information in your memories.", []

    answer = "I found the following relevant memories:\n\n"

    for memory in results[:3]:

        answer += "**" + memory["title"] + "**\n\n"

        answer += memory["content"][:500]

        answer += "\n\n"

    answer += "These results are retrieved from your saved information."

    return answer, results
