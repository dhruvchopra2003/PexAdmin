from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import os
from dotenv import load_dotenv

from pymongo import MongoClient
import openai
import markdown2

from .utils import *

# === Loading the API keys ===
load_dotenv()
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    mongo_password = os.getenv("MONGO_PASSWORD")
except Exception as e:
    print("Error setting THE KEYS API key:", e)


MONGODB_URI = f"mongodb+srv://tejvir:{mongo_password}@cluster0.4sfe71x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "property_exchange"
COLLECTION_NAME = "chats"

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


# === Defining the views ===
def index(request):
    """
    This view is to fetch all the chats from MongoDB, put them in a session's table
    and display here.

    """
    
    sorted_leads = request.session.get('sorted_leads')
    
    if not sorted_leads:
        sorted_leads = collection.find().sort("lead_id", -1)

        sorted_leads = [
            {
                "lead_id": lead["lead_id"],
                "chat_history": lead["chat_history"][1:],
                "date": lead["lead_id"][:10],
            }
            for lead in sorted_leads
            if len(lead["chat_history"][1:]) > 2
        ]

        request.session["sorted_leads"] = sorted_leads

    return render(
        request,
        "leads/index.html",
        {
            "sorted_leads": sorted_leads,
        },
    )


def leadView(request, leadId):
    # lead = collection.find_one({"lead_id": leadId})
    lead = find_lead_by_id(request.session["sorted_leads"], leadId)
    # Convert chat history to HTML
    if lead:
        for chat in lead["chat_history"]:
            chat["content"] = markdown2.markdown(chat["content"])

    else:
        return HttpResponse("No lead found", status=404)

    return render(
        request,
        "leads/lead.html",
        {
            "lead": lead,
            "date": lead["lead_id"][:10],
        },
    )


def finalLead(request, leadId):
    # lead = collection.find_one({"lead_id": leadId})
    lead = find_lead_by_id(request.session["sorted_leads"], leadId)
    chat_history = lead["chat_history"]

    generated_lead = generate_lead(chat_history)
    generated_lead_md = markdown2.markdown(generated_lead)

    request.session[f"generated_lead_{leadId}"] = generated_lead

    print(generated_lead)
    return render(
        request,
        "leads/final_lead.html",
        {
            "leadId": leadId,
            "generatedLead": generated_lead_md,
        },
    )


def download_lead(request, leadId):
    generated_lead = request.session.get(f"generated_lead_{leadId}")
    if not generated_lead:
        return HttpResponse("No generated lead found.", status=404)

    response = HttpResponse(generated_lead, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="lead_{leadId}.txt"'
    return response
