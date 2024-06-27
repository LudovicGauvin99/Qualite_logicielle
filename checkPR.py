import os
import subprocess
import anthropic

# Step 1: Run the git diff command and capture its output
try:
    result = subprocess.run(['git', 'diff', 'origin/main...HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    git_diff_content = result.stdout
except subprocess.CalledProcessError as e:
    git_diff_content = f"An error occurred while running git diff: {e.stderr}"

# Step 2: Prepare the content for the Anthropics API call
content_for_api = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": git_diff_content
        }
    ]
}

# Step 3: Call the Anthropics API with the git diff content
try:
    ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
except KeyError:
    ANTHROPIC_API_KEY = "Token not available!"
    
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    temperature=0,
    system="You are a Lead developer. Analyse the code and return recommendatations.",
    messages=[
        content_for_api
    ]
)

response_content = message.content
print("Premiere response content : ");
print(response_content);

# Step 4: Extract the response content
if message.content:
    response_content = message.content[0].text
else:
    response_content = "No recommendations returned from the API."

print("Deuxime response content : ");
print(response_content);

# Save the response to a file
with open('response.txt', 'w') as file:
    file.write(response_content)