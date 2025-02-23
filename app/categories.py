# Categories and their respective keywords
categories = {
    "food": ["bread", "pizza", "sandwich", "meal", "groceries", "lunch", "dinner", "snack"],
    "transport": ["taxi", "uber", "bus", "car", "train", "transport"],
    "entertainment": ["movie", "concert", "game", "music", "theater", "show"],
    "shopping": ["clothes", "shoes", "shopping", "store", "purchase", "item", "product"],
    "others": ["misc", "others", "various"]
}

async def categorize_expense(transcribed_text: str) -> str:
    """
    Categorize the expense based on the keywords in the transcribed text.
    """
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in transcribed_text.lower():
                return category
    return "others"  # Default to 'others' if no keyword matches
