import discord

from settings import GuildSettings, GuildSetting
from wards import guild_admin

import settings

from .data import studyban_durations


@GuildSettings.attach_setting
class mod_log(settings.Channel, GuildSetting):
    category = "Moderation"

    attr_name = 'mod_log'
    _data_column = 'mod_log_channel'

    display_name = "mod_log"
    desc = "Moderation event logging channel."

    long_desc = (
        "Channel to post moderation tickets.\n"
        "These are produced when a manual or automatic moderation action is performed on a member. "
        "This channel acts as a more context rich moderation history source than the audit log."
    )

    _chan_type = discord.ChannelType.text

    @property
    def success_response(self):
        if self.value:
            return "Moderation tickets will be posted to {}.".format(self.formatted)
        else:
            return "The moderation log has been unset."


@GuildSettings.attach_setting
class studyban_role(settings.Role, GuildSetting):
    category = "Moderation"

    attr_name = 'studyban_role'
    _data_column = 'studyban_role'

    display_name = "studyban_role"
    desc = "The role given to members to prevent them from using server study features."

    long_desc = (
        "This role is to be given to members to prevent them from using the server's study features.\n"
        "Typically, this role should act as a 'partial mute', and prevent the user from joining study voice channels, "
        "or participating in study text channels.\n"
        "It will be given automatically after study related offences, "
        "such as not enabling video in the video-only channels."
    )

    @property
    def success_response(self):
        if self.value:
            return "The study ban role is now {}.".format(self.formatted)


@GuildSettings.attach_setting
class studyban_durations(settings.SettingList, settings.ListData, settings.Setting):
    category = "Moderation"

    attr_name = 'studyban_durations'

    _table_interface = studyban_durations
    _id_column = 'guildid'
    _data_column = 'duration'
    _order_column = "rowid"

    _default = [
        5 * 60,
        60 * 60,
        6 * 60 * 60,
        24 * 60 * 60,
        168 * 60 * 60,
        720 * 60 * 60
    ]

    _setting = settings.Duration

    write_ward = guild_admin
    display_name = "studyban_durations"
    desc = "Sequence of durations for automatic study bans."

    long_desc = (
        "This sequence describes how long a member will be automatically study-banned for "
        "after committing a study-related offence (such as not enabling their video in video only channels).\n"
        "If the sequence is `1d, 7d, 30d`, for example, the member will be study-banned "
        "for `1d` on their first offence, `7d` on their second offence, and `30d` on their third. "
        "On their fourth offence, they will not be unbanned.\n"
        "This does not count pardoned offences."
    )
    accepts = (
        "Comma separated list of durations in days/hours/minutes/seconds, for example `12h, 1d, 7d, 30d`."
    )

    # Flat cache, no need to expire objects
    _cache = {}

    @property
    def success_response(self):
        if self.value:
            return "The automatic study ban durations are now {}.".format(self.formatted)
        else:
            return "Automatic study bans will never be reverted."


