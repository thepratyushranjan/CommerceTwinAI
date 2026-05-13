import sqlite3
import json
import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from datetime import datetime

# Configure Paths
DB_PATH = 'data/orders.db'
CHROMA_PATH = 'data/chromadb'
TICKETS_PATH = 'data/tickets.json'

# Initialize Embeddings (must match ingestion)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def search_knowledge_base(query: str) -> str:
    """
    Searches the company knowledge base for policies, FAQs, return/refund procedures, 
    shipping info, warranty terms, and how-to guides. 
    Use this for any general policy or how-to question. 
    Returns the most relevant policy text.
    """
    if not os.path.exists(CHROMA_PATH):
        return "Knowledge base is currently unavailable."
    
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    results = vectordb.similarity_search(query, k=3)
    
    if not results:
        return "No relevant information found in the knowledge base."
    
    formatted_results = []
    for doc in results:
        source = doc.metadata.get('source', 'Unknown')
        formatted_results.append(f"Source: {source}\nContent: {doc.page_content}")
    
    return "\n\n---\n\n".join(formatted_results)

def get_order_status(query: str) -> str:
    """
    Retrieves the current status and details of customer orders. 
    Can search by:
    1. Order ID (format ORD-XXXX)
    2. Customer Email (e.g., user@example.com)
    Returns status, items, tracking info, and dates.
    """
    if not os.path.exists(DB_PATH):
        return "Order database is currently unavailable."
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        if "@" in query:
            cursor.execute("SELECT * FROM orders WHERE customer_email = ?", (query.lower(),))
            rows = cursor.fetchall()
            if not rows:
                return f"No orders found for customer email: {query}"
            
            summary = [f"Found {len(rows)} orders for {query}:"]
            for row in rows:
                summary.append(f"- {row[0]}: Status: {row[2]}, Total: ${row[4]:.2f}")
            return "\n".join(summary)
        else:
            order_id = query.upper()
            if not order_id.startswith("ORD-"):
                if order_id.isdigit():
                    order_id = f"ORD-{order_id}"
            
            cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
            row = cursor.fetchone()
            
            if not row:
                return f"Order {order_id} not found."
            
            items = json.loads(row[3])
            items_list = "\n".join([f"  - {item['name']} (${item['price']})" for item in items])
            
            response = (
                f"Order Details for {row[0]}:\n"
                f"Customer: {row[1]}\n"
                f"Status: {row[2].upper()}\n"
                f"Order Date: {row[5]}\n"
                f"Ship Date: {row[6] if row[6] else 'Not yet shipped'}\n"
                f"Tracking: {row[7] if row[7] else 'N/A'}\n"
                f"Total: ${row[4]:.2f}\n"
                f"Items:\n{items_list}"
            )
            return response
            
    except Exception as e:
        return f"Error retrieving order: {str(e)}"
    finally:
        conn.close()

def escalate_to_human(customer_message: str, reason: str) -> str:
    """
    ONLY use this when:
    - The customer EXPLICITLY asks for a human, agent, or manager.
    - The issue involves LEGAL threats, chargebacks, or severe customer anger.
    - You have tried using other tools multiple times but cannot solve the E-COMMERCE related issue.
    DO NOT use this for unrelated topics like weather, general knowledge, or small talk.
    """
    ticket_id = f"TKT-{random_id()}"
    ticket = {
        "ticket_id": ticket_id,
        "timestamp": datetime.now().isoformat(),
        "customer_message": customer_message,
        "reason": reason,
        "status": "open"
    }
    
    tickets = []
    if os.path.exists(TICKETS_PATH):
        with open(TICKETS_PATH, 'r') as f:
            try:
                tickets = json.load(f)
            except:
                tickets = []
    
    tickets.append(ticket)
    
    with open(TICKETS_PATH, 'w') as f:
        json.dump(tickets, indent=2, fp=f)
        
    return (
        f"I've escalated your request to our human support team. "
        f"A representative will contact you within 24 hours. "
        f"Your ticket ID is {ticket_id}."
    )

def random_id():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
