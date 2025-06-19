import openai


openai.api_key = "" #openai api-key


def get_openai_response(type, prompt):
    try:
        if type == "chat":
            system_content = "Jesteś psychologiem z doświadczeniem, które wykorzystywane jest w aplikacji do śledzenia i poprawy zdrowia psychicznego. Podaj praktyczne porady i bądź najlepszym przyjacielem.:"
            prompt = prompt + "Odpowiadaj zawsze TYLKO po polsku, do 100 słów lub krótkimi poradami."
        else:
            system_content = "Jesteś psychologiem z doświadczeniem, które wykorzystywane jest w aplikacji do śledzenia i poprawy zdrowia psychicznego. Prowadzę zapiski w dzienniku, pomóż lub ogrzej dobrym słowem/rekomendacjami/oceną zdrowia psychicznego."
            prompt = prompt + "Odpowiadaj zawsze TYLKO po polsku, w którym napisano zapytanie, do 150 słów."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7,
        )

        result = response['choices'][0]['message']['content'].strip()
        return result

    except Exception as e:
        return "Provide API key or try again later."
        #return f"API Error: {str(e)}"

