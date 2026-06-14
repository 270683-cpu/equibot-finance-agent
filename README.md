# EquiBot: Your Personal Investing Mentor 🌱

## General Information
* **The Problem:** Many beginner investors find the stock market overwhelming, filled with complex jargon, and intimidating. They often don't know where to start or how to assess a company without getting buried in raw data.
* **Intended User:** Teenagers, young adults, or any beginner investor looking to learn about the stock market in a safe, jargon-free sandbox environment.
* **Key Features:** * Conversational interview pathway to narrow down user interests (Everyday Brands, Tech, etc.).
  * Real-time stock data fetching using `yfinance`.
  * Plain-English explanations of complex valuation metrics (e.g., P/E ratios).
  * Safe learning environment disclaimer to prevent real-world financial risk.

## How the Starter App Was Adapted
The initial starter application was a basic conversational interface. To improve it, I adapted the codebase to include:
1. **LangGraph & Tool Integration:** I transitioned the agent to use LangGraph's `create_react_agent`, allowing the LLM to route queries to specific tools (`get_stock_price`, `financial_calculator`, and DuckDuckGo web search).
2. **Custom Streamlit UI:** I completely overhauled the frontend using custom CSS in Streamlit to create a modern, dark-themed "intro-card" layout that feels welcoming rather than strictly analytical.
3. **Regex Sanitization:** I implemented robust string-cleaning pipelines (using Python's `re` module) to intercept the LLM's output and strip out unwanted Markdown link artifacts and backticks before rendering it in Streamlit.

## Iteration on Prompts & RAG Context
Getting the AI to behave like a patient mentor rather than an eager stockbroker required significant prompt engineering.

* **Before (Initial Prompt):** *"You are a financial advisor. Tell the user about a stock they might like based on their preferences."*
  * **Result:** The AI would immediately dump a massive, confusing financial report the second the user said "Hello", overwhelming the beginner. It also formatted numbers inside weird Markdown code blocks.
  
* **After (Iterated System Prompt):**
  *"CONVERSATIONAL INTERVIEW PATHWAY (CRITICAL RULES): 1. NO IMMEDIATE REPORTS. 2. ONE QUESTION AT A TIME: Acknowledge their choice, then ask ONE simple follow-up question. 3. ESTABLISH RISK... CRITICAL EXPLANATION: You MUST explain what the valuation metric means in plain English..."*
  * **Result:** The AI now forces a back-and-forth dialogue. It waits to learn the user's risk tolerance before suggesting a ticker. Furthermore, strict formatting headers were enforced in the prompt so the final report is readable and structured.

## Evaluation
EquiBot successfully addresses its core purpose: making financial analysis accessible. 

**Example Input:**
> "Option A: I want to check out familiar everyday brands."

**Example Intermediate Output (Interview Phase):**
> "Great choice! Everyday brands are a fantastic way to start... What kind of products do you actually buy day-to-day? Are you more into food/beverage brands, or retail/clothing?"

**Example Final Output (Report Phase):**
> **1. Company Profile & Price Snapshot**
> Company: The Coca-Cola Company (KO)
> Current Price: $59.80
> Valuation Metric: A P/E of 24 means you pay 24 dollars for every 1 dollar the company earns in profit. 
> ...
> *(Followed by Next Steps for Beginners and safety disclaimers).*

## Instructions to Recreate
If you would like to run this approach locally, follow these steps:

1. **Clone the repository:**
   `git clone https://github.com/YOUR_USERNAME/equibot.git`
   `cd equibot`
2. **Set up a virtual environment:**
   `python3 -m venv venv`
   `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
3. **Install the dependencies:**
   `pip install -r requirements.txt` *(Ensure yfinance, streamlit, langchain, langchain-cohere, and langgraph are included).*
4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Cohere API key:
   `COHERE_API_KEY=your_api_key_here`
5. **Run the application:**
   `streamlit run main.py`
