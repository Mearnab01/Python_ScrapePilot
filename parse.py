from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3.2")

def parse_with_ollama(dom_content: list[str], parse_description: str) -> str:
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    parsed_result = []

    for i, chunk in enumerate(dom_content, start=1):
        print(f"\n[INFO] Parsing chunk {i}/{len(dom_content)}...")

        try:
            response = chain.invoke(
                {
                    "dom_content": chunk,
                    "parse_description": parse_description
                }
            )
            if response and response.strip():
                parsed_result.append(response.strip())
            else:
                print("⚠️ [WARN] Empty response for this chunk")

        except Exception as e:
            print(f"[ERROR] Failed on chunk {i}: {e}")
            parsed_result.append("")

    final_output = "\n".join([r for r in parsed_result if r]).strip()

    if final_output:
        return final_output
    return "⚠️ No matching data found."
