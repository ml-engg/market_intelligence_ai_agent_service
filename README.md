This project implements a market analysis agent powered by multiple tools, wrapped in a Flask API. The AIAgent compares brands, analyzes sentiment, retrieves insights from RAG, and performs external search queries.

Architecture
<img width="1126" height="560" alt="image" src="https://github.com/user-attachments/assets/c22fde48-754f-4c09-b36f-2c4f4ca73654" />


Components

1. Flask API
   Exposes /analyze endpoint.
   Accepts user queries (e.g., "Compare _____ with ____ based on reviews").
   Orchestrates the AI Agent workflow.

2. AI Agent (ReAct style)
   Central reasoning engine.
   Breaks queries into steps.
   Decides which tools to call.
   Uses historical context + RAG

3. Tools
   Sentiment Tool → Analyzes product reviews and customer opinions for a particular brand 
   Compare Tool → If this is selected, then, it invokes RAG to retrieve in-house brand details, and do a comparion with the band in question
   Tavily Search Tool → Fetches competitor brand information for which we dont have data in RAG database 

4. Storage & Memory
   Short-term Memory: Keeps track of current session context, at user level 
   Long-term Memory (RAG): Stores brand details retrieved documents.

5. Logging
   log all user question and final response at each user X session level 

Workflow
1. User sends a query to the Flask endpoint.
2. The AI Agent interprets the request.
3. Based on reasoning, the Agent calls one or more tools:
        Compare → If this is selected, then, it invokes RAG to retrieve in-house brand details, and do a comparion with the band in question
        Sentiment Tool → analyze text sentiment.
        Tavily Search → Fetches competitor brand information for which we dont have data in RAG database.
4. Agent integrates results into a final response.
5. Response returned via API.
6. Log question and reponse

Example
curl -X POST http://127.0.0.1:5000/analyze -H "Content-Type: application/json" -d "{\"prompt\": \"Compare ____ with ____ shampoo based on reviews\"}"

Note 
Names are replaced by _____ in the above request
In all the codes base, brands are named as brand_a, brand_b like, in a real world case, this will be the correct brand names from which the analysis will be done


