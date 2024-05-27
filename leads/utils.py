import openai

def chat_beautify(chat):
    pass

def generate_lead(chat_history):
    prompt = f"""You are given this chat history: {chat_history}.
    From this you need to generate a lead. Here is the format for it:
    Client Name: User's Name \n
    
    Contact details: User's Phone Number/email id \n
    
    Client's Property Requirements: The type of property the client wanted to see. \n
    
    Clients's Preferences: the properties that the client showed interest in. \n
    \n
    
    Overall: A brief about the client's buying profile, engagement with the bot, and any other info that seems relevant. \n
    \n
    
    Chat History: return the chat history in a readable markdown format. 
    """

    prompt = [{"role": "system", "content": prompt}]

    # Generate completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.7,
    )

    lead = response.choices[0].message["content"].strip('"')

    return lead


def find_lead_by_id(leads, lead_id):
    for lead in leads:
        if lead.get("lead_id") == lead_id:
            return lead
    return None
