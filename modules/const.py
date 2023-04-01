from modules.commons import *

gittyHash = get_git_revision_hash()
gtHsh = get_git_revision_short_hash()

# =============================================================================
# About Bot

ownerUserUrl = f'https://discord.com/users/{AUTHOR_USERID}'

ABOUT_BOT = f'''<@!{BOT_CLIENT_ID}> is a bot personally created and used by [nattadasu](<https://nattadasu.my.id>) with the initial purpose as for member verification and MAL profile integration bot, which is distributed under [AGPL 3.0](<https://www.gnu.org/licenses/agpl-3.0.en.html>) license. ([Source Code](<https://github.com/nattadasu/ryuuRyuusei>), source code in repository may be older than main production maintained by nattadasu for)

However, due to how advanced the bot in querying information regarding user, anime on MAL, and manga on AniList, invite link is available for anyone who's interested to invite the bot (see `/invite`).

This bot may requires your consent to collect and store your data when you invoke `/register` command. You can see the privacy policy by using `/privacy` command.

However, you still able to use the bot without collecting your data, albeit limited usage.

If you want to contact the author, send a DM to [{AUTHOR_USERNAME}](<{ownerUserUrl}>) or via [support server](<{BOT_SUPPORT_SERVER}>).

Bot version, in Git hash: [`{gtHsh}`](<https://github.com/nattadasu/ryuuRyuusei/commit/{gittyHash}>)
'''

# =============================================================================
# Privacy Policy

PRIVACY_POLICY = '''Hello and thank you for your interest to read this tl;dr version of Privacy Policy.

In this message we shortly briefing which content we collect, store, and use, including what third party services we used for bot to function as expected. You can read the full version of [Privacy Policy here at anytime you wish](<https://github.com/nattadasu/ryuuRyuusei/blob/main/PRIVACY.md>).

__We collect, store, and use following data__:
- Discord: username, discriminator, user snowflake ID, joined date, guild/server ID of registration, server name, date of registration, user referral (if any)
- MyAnimeList: username, user ID, joined date

__We shared limited personal information about you to 3rd Party__:
This is required for the bot to function as expected, with the following services:
Discord, Last.FM, MAL Heatmap, MyAnimeList

__We cached data for limited features of the bot__:
Used to reduce the amount of API calls to 3rd party services, and to reduce the amount of time to process the data and no information tied to you.

__We do not collect, however, following data__:
Any logs of messages sent by system about you under any circumstances. Logging of messages only occurs when you invoked general commands (such as `/help`, `/anime`, `/manga`, etc.) and during the bot's development process. Maintenance will announced in the Bot status channel in Support Server and Bot Activity.

Data stored locally to Data Maintainer's (read: owner) server/machine of this bot as CSV. To read your profile that we've collected, type `/export_data` following your username.

As user, you have right to access, know, data portability, modify/rectify, delete, restrict, limit, opt-out, and/or withdraw your consent to use your data.

For any contact information, type `/about`.'''

# =============================================================================
# Support Development

SUPPORT_DEVELOPMENT = f'''{EMOJI_ATTENTIVE} Thanks for your interest in supporting me!

You can support me on [Ko-Fi](<https://ko-fi.com/nattadasu>), [PayPal](<https://paypal.me/nattadasu>), or [GitHub Sponsors](<https://github.com/sponsors/nattadasu>).

For Indonesian users, you can use [Trakteer](<https://trakteer.id/nattadasu>) or [Saweria](<https://saweria.co/nattadasu>).

Or, are you a developer? You can contribute to the bot's code on [GitHub](<https://github.com/nattadasu/ryuuRyuusei>)

If you have any questions (or more payment channels), please join my [support server]({BOT_SUPPORT_SERVER})!'''

# =============================================================================
# Declined GDPR notice

DECLINED_GDPR =  '''**You have not accepted the GDPR/CCPA/CPRA Privacy Consent!**
Unfortunately, we cannot register you without your consent. However, you can still use the bot albeit limited.

Allowed commands:
- `/profile mal_username:<str>`
- `/ping`

If you want to register, please use the command `/register` again and accept the consent by set the `accept_gdpr` option to `true`!

We only store your MAL username, MAL UID, Discord username, Discord UID, and joined date for both platforms, also server ID during registration.
We do not store any other data such as your email, password, or any other personal information.
We also do not share your data with any third party than necessary, and it only limited to the required platforms such Username.

***We respect your privacy.***

For more info what do we collect and use, use `/privacy`.
'''

# =============================================================================

# Common errors and messages

MESSAGE_MEMBER_REG_PROFILE = f"{EMOJI_DOUBTING} **You are looking at your own profile!**\nYou can also use </profile:1072608801334755529> without any arguments to get your own profile!"

MESSAGE_INVITE = "To invite me, simply press \"**Invite me!**\" button below!\nFor any questions, please join my support server!"

MESSAGE_SELECT_TIMEOUT = "*Selection menu has reached timeout, please try again if you didn't pick the option!*"

ERR_KAIZE_SLUG_MODDED = '''We've tried to search for the anime using the slug (and even fix the slug itself), but it seems that the anime is not found on Kaize via AnimeApi.
Please send a message to AnimeApi maintainer, nattadasu (he is also a developer of this bot)'''
