import produce_input as i
import produce_output as o
import sqlalchemy as engine
import helper

# import sys
import click


@click.command()
@click.option("--path", "-f", help="data description file path (optional).")
def run(path):
    # connect to the database
    try:
        db = engine.create_engine(
            click.prompt("Please enter your database connection string")
        )
    except Exception as e:
        click.echo(f"Failed to connect to the database: {e}")
        return run(path)
    input_str = i.produce_input(db, description=path)

    # API key input
    def key():
        try:
            key = click.prompt("Please enter your openai key", hide_input=True)
            return key
        except Exception as e:
            click.echo(f"Failed to get the key: {e}")
            return key()

    key = key()

    # firsr request
    request = click.prompt("Please enter your request")
    history_chat = [
        {"role": "system", "content": input_str},
        {
            "role": "user",
            "content": request,
        },
    ]
    respond = o.openai_output(input_str, request, key=key)

    # scuessful extract SQL from response
    if len(respond) == 3:
        history_chat.append({"role": "assistant", "content": respond[2]})
        click.echo(respond[1])
        query = respond[0]

        # check if the query is a modification query
        if helper.identify_process(query) == 1:
            check = click.prompt(
                "are you sure to run this query?(y/n)",
                click.Choice(["y", "n"], case_sensitive=False),
            )
            if check == "y":
                click.echo(i.modify(query, db))
            else:
                pass

        else:
            df = i.execute(query, db)
            if len(df) >= 20:
                idea = click.prompt("if output to csv (y/n):")
                if idea == "y":
                    file_name = click.prompt(
                        "Please enter the file name (without extension): "
                    )
                    df.to_csv(f"{file_name}.csv", index=False)
                else:
                    click.echo(df.head(20))
            else:
                click.echo(df)
    # unsuccessful extract SQL from response
    else:
        click.echo(
            "Did not find query in the response, please check your request and try again."
        )
        click.echo(respond)

    # continue the conversation
    while True:
        following = click.prompt(
            "new query (n) / current query (c) / exit :",
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
            respond = o.openai_output(input_str, request, key=key)
            if len(respond) == 3:
                history_chat.append({"role": "assistant", "content": respond[2]})
                click.echo(respond[1])
                query = respond[0]
                if helper.identify_process(query) == 1:
                    check = click.prompt(
                        "are you sure to run this query?(y/n)",
                        click.Choice(["y", "n"], case_sensitive=False),
                    )
                    if check == "y":
                        click.echo(i.modify(query, db))
                    else:
                        continue
                else:
                    df = i.execute(query, db)
                    if len(df) >= 20:
                        idea = click.prompt("if output to csv (y/n):")
                        if idea == "y":
                            file_name = click.prompt(
                                "Please enter the file name (without extension): "
                            )
                            df.to_csv(f"{file_name}.csv", index=False)
                        else:
                            click.echo(df.head(20))
                    else:
                        click.echo(df)

            else:
                click.echo(
                    "Did not find query in the response, please check your request and try again."
                )
                click.echo(respond)
        elif following == "c":
            while True:
                repost = click.prompt(
                    "more details (d) / mannual query (m):",
                    type=click.Choice(["d", "m"], case_sensitive=False),
                )
                if repost == "d":
                    request = click.prompt("Please enter your request")
                    request = "here's more details on last query:" + request
                    respond = o.openai_output(
                        input_str, request, history=history_chat, key=key
                    )
                    if len(respond) == 3:
                        history_chat.append(
                            {"role": "assistant", "content": respond[2]}
                        )
                        click.echo(respond[1])
                        query = respond[0]
                        if helper.identify_process(query) == 1:
                            check = click.prompt(
                                "are you sure to run this query?(y/n)",
                                click.Choice(["y", "n"], case_sensitive=False),
                            )
                            if check == "y":
                                click.echo(i.modify(query, db))
                            else:
                                continue

                        else:
                            df = i.execute(query, db)
                            if len(df) >= 20:
                                idea = click.prompt("if output to csv (y/n):")
                                if idea == "y":
                                    file_name = click.prompt(
                                        "Please enter the file name (without extension): "
                                    )
                                    df.to_csv(f"{file_name}.csv", index=False)
                                else:
                                    click.echo(df.head(20))
                            else:
                                click.echo(df)

                    else:
                        click.echo(
                            "Did not find query in the response, please check your request and try again."
                        )
                        click.echo(respond)
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
