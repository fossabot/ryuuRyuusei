"""
# Internationalization Bot Module

All language files are stored in the i18n folder. Strings to change and view languages must be in English.
"""


import csv
from json import load
from json import loads as jlo
from typing import Any

import pandas as pd
from fuzzywuzzy import fuzz
from interactions import (AutoShardedClient, BaseContext, Embed, EmbedField,
                          InteractionContext)
from interactions.ext.paginators import Paginator

from modules.const import LANGUAGE_CODE


def fetch_language_data(code: str, use_raw: bool = True) -> dict[str, Any]:
    """
    Get the language strings for a given language code

    Args:
        code (str): The language code to get the strings for
        use_raw (bool): Whether to return the raw JSON data or not

    Returns:
        dict[str, Any]: The language strings
    """
    try:
        with open(f"i18n/{code}.json", "r", encoding="utf-8") as f:  # skipcq: PTC-W6004
            data: dict[str, Any] = jlo(f.read())
            if use_raw:
                return data
            return data["strings"]  # type: ignore
    except FileNotFoundError:
        return fetch_language_data(LANGUAGE_CODE)


def read_user_language(ctx: BaseContext | InteractionContext) -> str:
    """
    Read the user's language preference from the database

    Args:
        ctx (BaseContext | InteractionContext): The context to read the user's language preference from

    Returns:
        str: The user's language preference
    """
    user_df: pd.DataFrame = pd.read_csv("database/member.csv", sep="\t")

    # find the row in the user DataFrame that matches the user's ID
    user_row = user_df.loc[user_df["discordId"] == ctx.author.id]

    # check if a match was found and return the language if it was
    if len(user_row) > 0:
        return user_row["language"].iloc[0]  # type: ignore

    try:
        if ctx.guild is None:
            return LANGUAGE_CODE
        server_df = pd.read_csv("database/server.csv", sep="\t")
        # type: ignore
        server_row = server_df.loc[server_df["discordId"] == ctx.guild.id]
        if len(server_row) > 0:
            return server_row["language"].iloc[0]  # type: ignore
    # pylint: disable-next=broad-except
    except BaseException:
        pass

    return LANGUAGE_CODE


async def paginate_language(bot: AutoShardedClient, ctx: InteractionContext) -> None:
    """
    Paginate the language list

    Args:
        bot (AutoShardedClient): The bot client
        ctx (InteractionContext): The context to send the language list to
    """
    with open("i18n/_index.json", "r", encoding="utf-8") as file_:
        langs = jlo(file_.read())
    pages: list[Embed] = []
    for i in range(0, len(langs), 15):
        paged: list[EmbedField] = []
        for lang in langs[i: i + 15]:
            flag = lang["code"].split("_")[1].lower()
            match flag:
                case "sp":
                    flag_ = "rs"
                case _:
                    flag_ = flag
            paged += [
                EmbedField(
                    name=f":flag_{flag_}: `{lang['code']}` - {lang['name']}",
                    value=f"{lang['native']}",
                    inline=True,
                )
            ]
        pages += [
            Embed(
                title="Languages",
                description="List of all available languages.\nUse `/usersettings language set code:<code>` by replacing `<code>` with the language code (for example `en_US`) to change your language.\n\nIf you want to contribute, visit [Crowdin page](https://crowdin.com/project/ryuuRyuusei).",
                color=0x996422,
                fields=paged,  # type: ignore
            )
        ]
    pagin = Paginator.create_from_embeds(bot, *pages, timeout=60)
    await pagin.send(ctx)


def search_language(query: str) -> list[dict[str, Any]]:
    """
    Search for a language for auto-complete

    Args:
        query (str): The query to search for

    Returns:
        list[dict]: The list of languages that match the query
    """
    with open("i18n/_index.json", "r", encoding="utf-8") as file_:
        data = load(file_)
    results: list[dict[str, Any]] = []
    for item in data:
        name_ratio = fuzz.token_set_ratio(query, item["name"])
        native_ratio = fuzz.token_set_ratio(query, item["native"])
        dialect_ratio = fuzz.token_set_ratio(query, item["dialect"])
        max_ratio = max(name_ratio, native_ratio, dialect_ratio)
        if max_ratio >= 70:  # minimum similarity threshold of 70%
            results.append(item)
    return results


def check_lang_exist(code: str) -> bool:
    """
    Check if a language exists

    Args:
        code (str): The language code to check

    Returns:
        bool: Whether the language exists or not
    """
    with open("i18n/_index.json", "r", encoding="utf-8") as f:
        langs = jlo(f.read())
    for lang in langs:
        if lang["code"] == code:
            return True
    return False


async def set_default_language(
    code: str, ctx: InteractionContext, is_guild: bool = False
) -> None:
    """
    Set the user's/guild's language preference

    Args:
        code (str): The language code to set the user's/guild's language preference to
        ctx (InteractionContext): The context to send the language list to
        is_guild (bool, optional): Whether to set the guild's language preference or not. Defaults to False.
    """
    if is_guild is True:
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server")
            return
        if check_lang_exist(code) is False:
            # pylint: disable-next=broad-exception-raised
            raise Exception(
                "Language not found, recheck the spelling and try again")
        # check if guild is already in database
        try:
            dataframe = pd.read_csv("database/server.csv", sep="\t")
            if dataframe.query(f"serverId == {ctx.guild.id}").empty:  # type: ignore
                dfa = pd.DataFrame(
                    [[ctx.guild.id, code]],
                    columns=["serverId", "language"],  # type: ignore
                )
                dfen = dfa.append(dataframe, ignore_index=True)  # type: ignore
                dfen.to_csv("database/server.csv", sep="\t", index=False)
            else:
                # if it is, update it
                dataframe.loc[dataframe["serverId"] == ctx.guild.id, "language"] = code
                dataframe.to_csv("database/server.csv", sep="\t", index=False)
        # pylint: disable-next=broad-exception-caught
        except BaseException:
            # if the database doesn't exist, create it
            with open("database/server.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter="\t")
                writer.writerow(["serverId", "language"])
                writer.writerow([ctx.guild.id, code])
    else:
        if check_lang_exist(code) is False:
            # pylint: disable-next=broad-exception-raised
            raise Exception(
                "Language not found, recheck the spelling and try again")

        try:
            dataframe = pd.read_csv(
                "database/member.csv",
                sep="\t",
                encoding="utf-8",
                dtype={"discordId": str},
            )

            if dataframe.query(f"discordId == '{str(ctx.author.id)}'").empty:
                dfa = pd.DataFrame([[str(ctx.author.id), code]], columns=[
                    "discordId", "language"])
                dfen = dfa.append(dataframe, ignore_index=True)  # type: ignore
                dfen.to_csv("database/member.csv", sep="\t", index=False)
            else:
                # if it is, update it
                dataframe.loc[dataframe["discordId"] == str(
                    ctx.author.id), "language"] = f"{code}"
                dataframe.to_csv("database/member.csv", sep="\t", index=False)
        # pylint: disable-next=broad-except
        except BaseException:
            # if the database doesn't exist, create it
            with open("database/member.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter="\t")
                writer.writerow(["discordId", "language"])
                writer.writerow([str(ctx.author.id), code])
