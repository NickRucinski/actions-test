# Requirements
Make sure you have python3 installed
CD to the webserver folder
Then to install all the requirements
Windows
```
    py -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    deactivate

```
Mac(I think)
```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    deactivate
```

Also an AI model is needed
Currently it is set to use Ollama's llama3.2'
Download and follow the prompts here https://ollama.com/

# Running the program
windows
```
    .venv\Scripts\activate
    py app.py
    deactivate

```
Mac(I think)
```
    source .venv/bin/activate
    python3 app.py
    deactivate
```