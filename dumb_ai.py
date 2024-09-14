from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#instructions for the LLM
template = (
    "Your task is to extract **only** the specific information from the following text content: {dom_content}. "
    "Please adhere to the following instructions strictly:\n\n"
    "1. **Extract Relevant Data:** Extract only the information that precisely matches the description provided: {parse_description}. "
    "2. **Exclude Irrelevant Data:** Do not include any extra content, commentary, or explanations beyond the requested information. "
    "3. **Return an Empty String:** If no information matches the description, return an empty string (''). No partial matches are allowed."
    "4. **No Additional Formatting:** Output only the exact data requested, with no additional formatting, headers, or unnecessary characters."
)



model = OllamaLLM(model="llama3.1") #get the model

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template) #give prompt
    chain = prompt | model #create a chain that prompt the LLM to response

    parsed_result = [] 

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke(
                {"dom_content": chunk, "parse_description": parse_description}
            )
            print(f"Parsed batch {i} of {len(dom_chunks)}")
            parsed_result.append(response)
        except Exception as e:
            print(f"Error parsing batch {i}: {e}")
            parsed_result.append("")  # Append empty string if an error occurs

    return "\n".join(parsed_result)

