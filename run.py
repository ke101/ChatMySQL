import produce_input as i
import produce_output as o
import sqlalchemy as engine

# import sys
import click


@click.command()
def run():
    db = engine.create_engine(
        click.prompt("Please enter your database connection string")
    )
    input_str = i.produce_input(db)
    request = click.prompt("Please enter your request")
    history_chat = [
        {"role": "system", "content": input_str},
        {
            "role": "user",
            "content": request,
        },
    ]
    respond = o.openai_output(input_str, request)
    if len(respond) == 3:
        # query, p_query, respond = o.openai_output(input_str, request)
        history_chat.append({"role": "assistant", "content": respond[2]})
        click.echo(respond[1])
        click.echo(i.execute(respond[0], db))
    else:
        click.echo(
            "Did not find query in the response, please check your request and try again."
        )
        click.echo(respond[0])

    while True:
        following = click.prompt(
            "new query (n) / cuurent query (c) / exit :",
            type=click.Choice(["n", "c", "exit"], case_sensitive=False),
        )

        if following == "n":
            request = click.prompt("Please enter your request")
            history_chat = [
                {"role": "system", "content": input_str},
                {
                    "role": "user",
                    "content": request,
                },
            ]
            respond = o.openai_output(input_str, request)
            if len(respond) == 3:   
                # query, p_query, respond = o.openai_output(input_str, request)
                history_chat.append(
                    {"role": "assistant", "content": respond[2]}
                )
                click.echo(respond[1])
                click.echo(i.execute(respond[0], db))
            else:   
                click.echo(
                    "Did not find query in the response, please check your request and try again."
                )
                click.echo(respond[0])
        elif following == "c":
            while True:
                repost = click.prompt(
                    "more details (d) / mannual query (m):",
                    type=click.Choice(["d", "m"], case_sensitive=False),
                )
                if repost == "d":
                    request = click.prompt("Please enter your request")
                    request = "here's more details on last query:" + request
                    respond= o.openai_output (input_str, request, history=history_chat)
                    if len(respond) == 3:
                        # query, p_query, respond = o.openai_output(input_str, request)
                        history_chat.append(
                            {"role": "assistant", "content": respond[2]}
                        )
                        click.echo(respond[1])
                        click.echo(i.execute(respond[0], db))
                    else:
                        click.echo(
                            "Did not find query in the response, please check your request and try again."
                        )
                        click.echo(respond[0])
                    break
                elif repost == "m":
                    query = click.prompt("Please enter your SQL query")
                    click.echo(i.execute(query, db))
                    break
                else:
                    click.echo("Invalid option. Please try again.")
                    continue

        elif following == "exit":
            break
        else:
            click.echo("Invalid option. Please try again.")


if __name__ == "__main__":
    run()
