from src.generation.prompt_templates import RAG_PROMPT


def test_rag_prompt_format():
    prompt = RAG_PROMPT.format(context="some context", question="what is this?")
    assert "some context" in prompt
    assert "what is this?" in prompt
