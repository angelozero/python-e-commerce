import os
from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langsmith import traceable

# Load environment variables from .env file
load_dotenv()

# Configuration constants retrieved from environment
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MAX_ITERATIONS = os.getenv("MAX_ITERATIONS")


def get_chat_model():
    """
    Initializes and returns the Chat Model (LLM) instance.
    Uses LiteLLM proxy via OpenAI-compatible interface.
    """
    return init_chat_model(
        model=MODEL_NAME,
        model_provider="openai",
        api_key=API_KEY,
        base_url=BASE_URL,
    )


def get_embeddings():
    """
    Initializes and returns the Embeddings instance.
    Configured to handle float encoding format for Ollama compatibility.
    """
    return init_embeddings(
        model=MODEL_NAME,
        provider="openai",
        api_key=API_KEY,
        base_url=BASE_URL,
        # Force float encoding to avoid LiteLLM/Ollama base64 errors
        model_kwargs={"encoding_format": "float"},
    )


@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    print(f"\n>>Executing @tool get_product_price (product = '{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)


@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """
    Apply a discount tier to a price and return the final price
    Available tiers: bronze, siver, gold.
    """
    print(
        f"\n>>Executing @tool apply_discount (price = '{price}', discount_tier = '{discount_tier}')"
    )
    discount_percentage = {"bronze": 5, "silver": 12, "gold": 23}
    discount = discount_percentage.get(discount_tier, 0)
    return round(price * (1 - discount / 100), 2)


# ---------- #
# Agent Loop #
# ---------- #
@traceable(name="LangChain Agent Loop")
def run_agent(question: str):
    tools = [get_product_price, apply_discount]
    tools_dict = {t.name: t for t in tools}

    llm = get_chat_model()
    llm_with_tools = llm.bind_tools(tools)

    print(f"\nQuestion: {question}")
    print(f"=" * 65)
    print("")

    # ------------- #
    # Agent Thought #
    # ------------- #

    messages = [
        SystemMessage(
            content=(
                "You are a helpful shopping assistant."
                "You have access to a product catalog tool and a discount tool. \n\n"
                "STRICT RULES - you must follow these exactly: \n"
                "1. NEVER guess or assume any product price."
                "You MUST call get_product_price first to get the real price.\n"
                "2. Only call apply_discount AFTER you have received a price \n"
                "from get_product_priec. Pass the exact price returned by get_product_price "
                "- do NOT pass a made-up number.\n"
                "3. NEVER calculate discounts yourself using math.\n"
                "Always use the apply_discount tool.\n"
                "4. If the user does not specify a discount tier, "
                "ask them wich tier to use - do NOT assume one."
            )
        ),
        HumanMessage(question),
    ]
