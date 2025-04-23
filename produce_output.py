import produce_input
import openai


def openai_output(input, request, history=None):
    #openai.api_key = ""
    if history is None:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": input},
                {
                    "role": "user",
                    "content": request,
                },
            ],
            temperature=1,
            max_tokens=600,
            top_p=1,
        )
        respond = response.choices[0].message.content
        #print(respond)
        try:
            p_query = respond.split("```sql")[1].split("```")[0]
            query = p_query.strip().replace("\n", " ")
            return (query, p_query, respond)
        except IndexError:
            print("Please check your request and try again.")
            return (respond)
    else:
        history.append(
                {
                    "role": "user",
                    "content": request
                }
            )
    
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
        )
        respond = response.choices[0].message.content
        try:
            p_query = respond.split("```sql")[1].split("```")[0]
            query = p_query.strip().replace("\n", " ")
            return (query, p_query, respond)
        except IndexError:
            print("Please check your request and try again.")
            return (respond)
