import logging
import os
import json
from openai import AzureOpenAI
from config.config import (
    AZURE_OPENAI_ENDPOINT,  
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION
    )

# Configure Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

def summarize_and_tag(post_data: dict) -> (str, list):
    """
    Summarize a Teams post (including replies) and generate tags using Azure OpenAI.
    """
    logging.info(f"Summarizing and tagging post data: {post_data}") 
    text = post_data.get("post", {})
    replies = post_data.get("replies", [])
    # Convert post and replies to a single string
    post_str = str(text)
    replies_str = " ".join([str(reply) for reply in replies])
    full_text = f"Post :: {post_str} Replies :: {replies_str}".strip()

    prompt = f"""
    You are given a Microsoft Teams conversation (post and replies).

    Conversation:
    Title : {text.get("title", "No Title")}
    Text: {full_text}

    Your tasks:
    1. Write exactly one complete sentence summarizing the conversation clearly and meaningfully so that anyone (even outside the team) can understand it. 
    - Do not use bullet points or fragments.
    - Keep it concise and human-readable.

    2. Assign 1–3 tags that describe the conversation.
    - Use both main category and sub-category if applicable.
    - If no sub-category exists, use only the main category.
    - If no suitable tag is found, return ["Others"].

    3. Set the "groupTag" to the main category of the first tag in the "tags" array.
    - If the tags array is ["Others"], then groupTag should also be "Others".

    Tag List: 
    Categories:
        Group Tag   - [Sub Tag]
        Reliability - [ Outer Loop , Inner-Loop , Codespaces Reliability, Codespaces Stability, Deployment Pipeline Reliability, Flaky Test Detection & Triage, Non-Intentional Visual Diffs in PR, Live Site]
        Performance - [ yarn start , yarn fast , yarn test , yarn install , CI Perf ]
        PR Pipeline - [ 1PipeLine PR , 1Pipeline CI , E2E Test Pipeline , Other Pipeline Issues ]  
        Codespaces
        Test Automation - [ E2E Tests , Unit Tests , Component Tests , Flaky Tests , Test Coverage ]
        Build and Release
        Security - [ Application Security , Dependency Updates , Security Incident Response ]
        Publish Npm /NuGet Packages 
        1JS - Documentation - [ Test Automation Docs , 1JS Onboarding Docs , Codespaces Docs , 1JS Contribution Guide , 1JS Architecture Docs , 1JS Best Practices ]
        Git Operations
        Others
        Not Related to 1JS

    Output format:
    Respond only in JSON structure as below without any additional text or formatting:
    {{
        "summary": "...",
        "tags": ["tag1", "tag2"],
        "groupTag": "groupTag"
    }}
    """

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,   # this must match your deployed model name
        messages=[
            {"role": "system", "content": """
              You are an expert assistant that summarizes and classifies Microsoft Teams conversations. 
              Your goals: 
              1. Always produce a clear, single-sentence summary that captures the full meaning of the conversation (More weight to the post and less to the reply). 
              2. Act as a strict classifier: assign 1-2 tags only from the approved taxonomy of categories and tags provided.
              3. Be deterministic and consistent in tagging — never invent new tags, never miss obvious matches, and prefer the most specific tag(s). 
              4. Also assign a group tag based on the main category of the first tag. 
              5. If none of the tags match, return \"Others\". 
              6. Output only valid JSON as instructed — no explanations, no extra text. 
              7. If the conversation is not related to 1JS, return \"Not Related to 1JS\" as the only tag and group tag."
             """},
            
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
        summary = result.get("summary", "")
        tags = result.get("tags", [])
        group_tag = result.get("groupTag", "")  
        
    except Exception:
        summary = content[:200]
        tags = ["uncategorized"]
        group_tag = "uncategorized"

    return summary, tags , group_tag
