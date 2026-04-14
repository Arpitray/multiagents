from agent import build_search_agent, build_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    state = {}
    # Step 1: Search for information
    print("\n" + "=" * 20 + " Step 1: Searching for information " + "=" * 20)
    print(f"Searching for information on: {topic}")
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Search for information on: {topic}")]}
    )
    state["search_result"] = search_result["messages"][-1].content
    print(f"\n Search Result: {state['search_result']}")

    # Step 2: Read and extract information
    print("\n" + "=" * 20 + " Step 2: Reading and extracting information " + "=" * 20)
    print("Extracting information from search results...")

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Based on the search result about {topic}:,"
                    f"pick the most relevant urls and extract key information from them."
                    f"Search Result: {state['search_result'][:800]}",
                )
            ]
        }
    )
    state["reader_result"] = reader_result["messages"][-1].content
    print(f"\n Extracted Information: {state['reader_result']}")

    # Step 3: Write a comprehensive report
    print("\n" + "=" * 20 + " Step 3: Writing a comprehensive report " + "=" * 20)
    print("Writing a comprehensive report based on the extracted information...")

    research_combined = (
        f"Search Result: {state['search_result']}\n\n"
        f"Extracted Information: {state['reader_result']}"
    )

    state["writer_result"] = writer_chain.invoke(
        {"topic": topic, "research": research_combined}
    )
    print(f"\n Written Report: {state['writer_result']}")
    #critic report
    print("\n" + "=" * 20 + " Step 4: Critiquing the report " + "=" * 20)
    print("Critiquing the report for accuracy and completeness...")
    state["critic_result"] = critic_chain.invoke({"report": state["writer_result"]})
    print(f"\n Critique: {state['critic_result']}")
    
    return state

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_research_pipeline(topic)