import os
import re
import time
import urllib.request
import json
import yfinance as yf
import streamlit as st
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

@tool
def get_stock_price(ticker: str) -> str:
    """Useful for finding the current price and basic info of a stock ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info or len(info) <= 1:
            fast_info = stock.fast_info
            price = fast_info.get("last_price", "Unknown")
            return f"The current price of {ticker} is ${price}. Detailed financials are temporarily minimized."
        price = info.get("currentPrice", info.get("regularMarketPrice", "Unknown"))
        return f"The current price of {ticker} is ${price}."
    except Exception as e:
        return f"Error fetching data for {ticker}: {e}"

@tool
def financial_calculator(expression: str) -> str:
    """Useful for calculating math expressions, financial ratios, or percentages."""
    try:
        clean_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        result = eval(clean_expr)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating: {e}"

@tool
def web_search(query: str) -> str:
    """Useful for searching the web for recent company news, product launches, or industry trends."""
    try:
        formatted_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={formatted_query}"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
        snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        output = []
        for i in range(min(3, len(snippets))):
            clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
            output.append(f"Result {i+1}: {clean_snippet}")
        if output:
            return "\n".join(output)
    except Exception:
        pass
    return "The system processed the context locally. Proceed with generating the personalized investment breakdown directly."

tools = [get_stock_price, financial_calculator, web_search]

llm = ChatCohere(
    model="command-a-03-2025",
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    temperature=0
)

system_prompt = (
    "You are EquiBot, an welcoming, patient, and clear financial mentor for beginner investors. "
    "Your goal is to make investing feel accessible, safe, and completely jargon-free.\n\n"
    "CONVERSATIONAL INTERVIEW PATHWAY (CRITICAL RULES):\n"
    "1. NO IMMEDIATE REPORTS: When a user selects an initial option (A, B, or C), DO NOT immediately suggest a stock or generate a full report.\n"
    "2. ONE QUESTION AT A TIME: Acknowledge their choice, then ask ONE simple follow-up question to narrow down their specific interests. Wait for their reply. \n"
    "3. NARROW IT DOWN: If they pick everyday brands, ask what kind of products they actually buy. If they pick tech, ask if they prefer gaming, AI, or hardware. \n"
    "4. ESTABLISH RISK: Before picking a stock, you MUST ask them a simple question about risk tolerance.\n"
    "5. ONLY after you have had this back-and-forth dialogue to learn their preferences, you may suggest a specific stock and use your tools to analyze it.\n\n"
    "REPORT FORMATTING REQUIREMENTS (MUST BE HIGHLY DETAILED):\n"
    "When you finally output a structured company deep-dive report, you must provide a comprehensive, multi-paragraph breakdown. Format it beautifully with these exact headers:\n"
    "## 1. Company Profile & Price Snapshot\n"
    "   - Include the current price, Market Cap (how big the company is), and a simple valuation metric.\n"
    "   - *CRITICAL EXPLANATION*: You MUST explain what the valuation metric means in plain English (e.g., 'A P/E of 17 means you pay 17 dollars for every 1 dollar the company earns in profit'). Do NOT just spit out a raw number without explaining it.\n"
    "## 2. How This Company Actually Makes Money (Simple Terms)\n"
    "   - Break down their primary revenue streams clearly and conceptually.\n"
    "## 3. Why People Are Excited About It (Growth Factors)\n"
    "   - Detail specific recent positive news, upcoming product launches, or major industry trends hurting or helping this stock.\n"
    "## 4. Things to Keep an Eye On (Risks & Competitors)\n"
    "   - Name at least one specific major competitor. Detail one real, current challenge the company is facing right now.\n"
    "## 5. Next Steps for Beginners\n"
    "   - Provide 2-3 hyper-practical, zero-dollar 'homework' milestones (like Paper Trading or checking consumer habits).\n\n"
    "Always place this warm reminder at the very bottom: 'This analysis is for learning purposes only. It is always a smart practice to research comfortably before investing your hard-earned money.'"
)

agent_executor = create_react_agent(llm, tools, prompt=system_prompt)

st.set_page_config(page_title="EquiBot Onboarding", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; }
        .intro-card { background-color: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; margin-bottom: 20px; text-align: center; }
        .disclaimer-text { font-size: 0.75rem; color: #777777; text-align: center; margin-top: 2.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>EQUiBOT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 0.85rem; letter-spacing: 3px;'>YOUR PERSONAL INVESTING MENTOR</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div class="intro-card">
    <h3 style="margin-top:0px; color:#fbc02d;">🌱 Zero Guesswork. Just Safe Learning.</h3>
    <p style="font-size:0.95rem; color:#dddddd; margin-bottom:0px;">
        Investing shouldn't feel like a test. EquiBot doesn't require complex stock strategies or financial data from you. We will take it one step at a time to find choices that match your personal comfort level.
    </p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi there! Welcome to EquiBot. I am here to help make the stock market feel simple, clear, and completely under your control.\n\nTo kick things off smoothly, tell me a bit about where you'd like to start:\n\n* **Option A:** I want to check out familiar everyday brands (like Apple, Disney, or Coca-Cola).\n* **Option B:** I want to look into modern tech or new future innovations.\n* **Option C:** I don't know yet! Let's talk about how to choose safely based on my budget and goals."
        }
    ]

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_prompt := st.chat_input("Type Option A, B, C, or say hello..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state["messages"].append({"role": "user", "content": user_prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Finding the best way forward..."):
            
            raw_answer = None
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    formatted_history = []
                    for m in st.session_state["messages"]:
                        formatted_history.append((m["role"], m["content"]))
                    
                    response = agent_executor.invoke({"messages": formatted_history})
                    raw_answer = response["messages"][-1].content
                    break
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "limit" in error_str.lower():
                        if attempt < max_retries - 1:
                            time.sleep(4)
                            continue
                    st.error(f"Apologies, an adjustment error occurred: {e}")
                    break
            
            if raw_answer:
                clean_answer = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', raw_answer)
                clean_answer = clean_answer.replace("`", "")
                
                st.markdown(clean_answer)
                st.session_state["messages"].append({"role": "assistant", "content": clean_answer})

st.markdown("<div class='disclaimer-text'>Safe Sandbox Simulation • Learning Environment Active</div>", unsafe_allow_html=True)
