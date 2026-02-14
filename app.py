from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

class SocialMediaState(TypedDict):
    topic: str
    twitter_post: str
    facebook_post: str
    twitter_approved: bool
    facebook_approved: bool
    twitter_feedback: str
    facebook_feedback: str
    attempt: int
    platform_to_optimize: str


llm = ChatGroq(
    api_key="YOUR_API_KEY_HERE",
    model="llama-3.3-70b-versatile"
)

def generate_posts(state: SocialMediaState):
    twitter_prompt = [
        SystemMessage(content="You are a Twitter expert. Write short, engaging tweets with hashtags. Max 280 chars."),
        HumanMessage(content=f"Write a tweet about: {state['topic']}")
    ]

    facebook_prompt = [
        SystemMessage(content="You are a Facebook content creator. Write detailed, conversational posts that encourage comments."),
        HumanMessage(content=f"Write a Facebook post about: {state['topic']}")
    ]

    twitter_response = llm.invoke(twitter_prompt)
    facebook_response = llm.invoke(facebook_prompt)

    print(f"\nTwitter Draft: {twitter_response.content[:60]}...")
    print(f"Facebook Draft: {facebook_response.content[:60]}...\n")

    return {
        "twitter_post": twitter_response.content,
        "facebook_post": facebook_response.content,
        "attempt": state.get("attempt", 0) + 1
    }

def evaluate_twitter(state: SocialMediaState):
    prompt = [
        SystemMessage(content="Reply ONLY with 'approve' or 'reject' and one short feedback line."),
        HumanMessage(content=f"Evaluate this tweet:\n{state['twitter_post']}")
    ]

    response = llm.invoke(prompt)
    approved = "approve" in response.content.lower()

    print(f"Twitter Review: {'Approved' if approved else 'Rejected'}")

    return {
        "twitter_approved": approved,
        "twitter_feedback": response.content
    }


def evaluate_facebook(state: SocialMediaState):
    prompt = [
        SystemMessage(content="Reply ONLY with 'approve' or 'reject' and one short feedback line."),
        HumanMessage(content=f"Evaluate this Facebook post:\n{state['facebook_post']}")
    ]

    response = llm.invoke(prompt)
    approved = "approve" in response.content.lower()

    print(f"Facebook Review: {'Approved' if approved else 'Rejected'}")

    return {
        "facebook_approved": approved,
        "facebook_feedback": response.content
    }

def optimize_twitter(state: SocialMediaState):
    prompt = [
        SystemMessage(content="Improve this tweet with better engagement and hashtags."),
        HumanMessage(content=f"Original:\n{state['twitter_post']}\nFeedback:\n{state['twitter_feedback']}")
    ]

    response = llm.invoke(prompt)

    print("Twitter Optimized\n")

    return {"twitter_post": response.content}


def optimize_facebook(state: SocialMediaState):
    prompt = [
        SystemMessage(content="Improve this Facebook post to be more conversational and engaging."),
        HumanMessage(content=f"Original:\n{state['facebook_post']}\nFeedback:\n{state['facebook_feedback']}")
    ]

    response = llm.invoke(prompt)

    print("Facebook Optimized\n")

    return {"facebook_post": response.content}


def approve_posts(state: SocialMediaState):
    print("\n" + "=" * 60)
    print("FINAL APPROVED POSTS")
    print("=" * 60)
    print(f"\nTwitter:\n{state['twitter_post']}\n")
    print(f"Facebook:\n{state['facebook_post']}\n")
    print(f"Total Attempts: {state['attempt']}")
    print("=" * 60)

    return {}

def router_function(state: SocialMediaState):

    if state["twitter_approved"] and state["facebook_approved"]:
        return "approve"

    elif not state["twitter_approved"] and state["facebook_approved"]:
        return "optimize_twitter"

    elif state["twitter_approved"] and not state["facebook_approved"]:
        return "optimize_facebook"

    else:
        if state["attempt"] >= 5:
            return "approve"
        return "optimize_both"


graph = StateGraph(SocialMediaState)

graph.add_node("generate", generate_posts)
graph.add_node("evaluate_twitter", evaluate_twitter)
graph.add_node("evaluate_facebook", evaluate_facebook)
graph.add_node("optimize_twitter", optimize_twitter)
graph.add_node("optimize_facebook", optimize_facebook)
graph.add_node("approve", approve_posts)

graph.set_entry_point("generate")

graph.add_edge("generate", "evaluate_twitter")
graph.add_edge("evaluate_twitter", "evaluate_facebook")

graph.add_conditional_edges(
    "evaluate_facebook",
    router_function,
    {
        "approve": "approve",
        "optimize_twitter": "optimize_twitter",
        "optimize_facebook": "optimize_facebook",
        "optimize_both": "optimize_twitter"
    }
)

graph.add_edge("optimize_twitter", "evaluate_twitter")
graph.add_edge("optimize_facebook", "evaluate_facebook")
graph.add_edge("approve", END)

app = graph.compile()

topic = input("Which topic should we create posts about? ")

initial_state = {
    "topic": topic,
    "twitter_post": "",
    "facebook_post": "",
    "twitter_approved": False,
    "facebook_approved": False,
    "twitter_feedback": "",
    "facebook_feedback": "",
    "attempt": 0,
    "platform_to_optimize": ""
}

print("\n Social Media Post Automation Started...\n")

result = app.invoke(initial_state)