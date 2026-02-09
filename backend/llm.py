from langchain_community.llms import LlamaCpp

def load_llm():
    return LlamaCpp(
        model_path="models/llama3.2-3b-custom-v3.gguf",
        n_ctx=512,
        n_threads=1,          
        n_batch=16,          
        max_tokens=128,      
        temperature=0.2,
        top_p=0.95,
        use_mmap=False,       
        use_mlock=False,      
        verbose=True
    )

llm = load_llm()