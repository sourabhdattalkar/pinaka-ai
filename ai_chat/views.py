from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from huggingface_hub import InferenceClient
from .forms import APIKeyForm, ChatForm

# Path to save API key
API_KEY_FILE_PATH = 'ai_chat/api_key.txt'

def load_api_key():
    """Load the saved API key."""
    try:
        with open(API_KEY_FILE_PATH, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_api_key(key):
    """Save the API key to a file."""
    with open(API_KEY_FILE_PATH, 'w') as f:
        f.write(key)

def set_api_key(request):
    """Handle the API key input from the user."""
    if request.method == "POST":
        api_key = request.POST.get('api_key')
        if api_key:
            save_api_key(api_key)
            return render(request, 'ai_chat/set_api_key.html', {'success': True})
    return render(request, 'ai_chat/set_api_key.html')

@csrf_exempt  # Temporarily disable CSRF check for this view (for simplicity)
def get_response(request):
    """Get response from the AI model."""
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            print("Received Data:", data)  # Log the received data for debugging
            question = data.get('question', '').strip()
            print(f"Question provided: '{question}'")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        api_key = load_api_key()
        if not api_key:
            return JsonResponse({'error': 'API key not set'}, status=400)

        client = InferenceClient(api_key=api_key)
        if not question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        messages = [
            {"role": "user", "content": question},
            {"role": "assistant", "content": "Sure, I'd be happy to help."}
        ]

        # Get the AI response (streamed output)
        stream = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct", 
            messages=messages, 
            temperature=0.5,
            max_tokens=15360,
            top_p=0.7,
            stream=True
        )

        # Collect the response text
        response_text = ""
        for chunk in stream:
            response_text += chunk.choices[0].delta.content

        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def home(request):
    """Render the main chat interface."""
    form = ChatForm()  
    return render(request, 'ai_chat/home.html', {'form': form})
