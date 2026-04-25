import asyncio
import time
import httpx
import json
import itertools
import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from typing import Tuple
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
# (অন্যান্য ইম্পোর্টের সাথে এটি যোগ করো)
from protobuf_decoder.protobuf_decoder import Parser

# ==========================================
# 1. NATIVE PROTOBUF INJECTION
# ==========================================
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf import json_format, message
from google.protobuf.message import Message

_sym_db = _symbol_database.Default()
_globals = globals()

# --- FreeFire_pb2 ---
DESCRIPTOR_FF = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eFreeFire.proto\"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d \x01(\t\x12\x1b\n\x13orign_platform_type\x18c \x01(\t\"]\n\x10BlacklistInfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e2\n.BanReason\x12\x17\n\x0fexpire_duration\x18\x02 \x01(\r\x12\x10\n\x08ban_time\x18\x03 \x01(\r\"f\n\x0eLoginQueueInfo\x12\r\n\x05allow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\"\xa0\x03\n\x08LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11agora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0eemulator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b2\x11.BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b2\x0f.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18\x0f \x01(\r\x12\x0f\n\x07ano_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n\tBanReason\x12\x16\n\x12BAN_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17BAN_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11BAN_REASON_REFUND\x10\x02\x12\x15\n\x11BAN_REASON_OTHERS\x10\x03\x12\x16\n\x12BAN_REASON_SKINMOD\x10\x04\x12 \n\x1bBAN_REASON_IN_GAME_AUTO_NEW\x10\xf6\x07b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_FF, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_FF, 'FreeFire_pb2', _globals)

# --- main_pb2 ---
DESCRIPTOR_MAIN = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csample.proto\"*\n\x12SearchWorkshopCode\x12\t\n\x01a\x18\x01 \x01(\t\x12\t\n\x01b\x18\x02 \x01(\x05\"-\n\x15GetPlayerPersonalShow\x12\t\n\x01a\x18\x01 \x01(\x03\x12\t\n\x01b\x18\x02 \x01(\x05\"\xf8\x08\n\x0cJwtGenerator\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cversion_code\x18\x05 \x01(\x05\x12\x13\n\x0bapp_version\x18\x07 \x01(\t\x12\x17\n\x0fandroid_version\x18\x08 \x01(\t\x12\x13\n\x0bdevice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03dpi\x18\x0e \x01(\t\x12\x10\n\x08cpu_info\x18\x0f \x01(\t\x12\x0b\n\x03fps\x18\x10 \x01(\x05\x12\x11\n\tgpu_model\x18\x11 \x01(\t\x12\x16\n\x0eopengl_version\x18\x12 \x01(\t\x12\x11\n\tdevice_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x13\n\x0bdevice_hash\x18\x16 \x01(\t\x12\x14\n\x0cos_api_level\x18\x17 \x01(\t\x12\x15\n\ros_build_type\x18\x18 \x01(\t\x12\x14\n\x0cdevice_model\x18\x19 \x01(\t\x12\x19\n\x11package_signature\x18\x1d \x01(\t\x12\x12\n\nuser_level\x18\x1e \x01(\x05\x12\x14\n\x0ccarrier_name\x18) \x01(\t\x12\x1a\n\x12network_generation\x18* \x01(\t\x12\x15\n\rapp_signature\x189 \x01(\t\x12\x11\n\tplayer_id\x18< \x01(\x03\x12\x12\n\nsession_id\x18= \x01(\x03\x12\x10\n\x08match_id\x18> \x01(\x05\x12\r\n\x05score\x18@ \x01(\x03\x12\x13\n\x0btotal_score\x18A \x01(\x03\x12\x12\n\nhigh_score\x18B \x01(\x03\x12\x11\n\tmax_score\x18C \x01(\x03\x12\x13\n\x0bplayer_rank\x18I \x01(\x05\x12\x17\n\x0fnative_lib_path\x18J \x01(\t\x12\x15\n\ris_debuggable\x18L \x01(\x05\x12\x12\n\napp_source\x18M \x01(\t\x12\x0f\n\x07is_beta\x18N \x01(\x05\x12\x11\n\tis_tester\x18O \x01(\x05\x12\x1b\n\x13target_architecture\x18Q \x01(\t\x12\x18\n\x10app_version_code\x18S \x01(\t\x12\x19\n\x11app_revision_code\x18U \x01(\x05\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x18\n\x10max_texture_size\x18W \x01(\x05\x12\x17\n\x0fprocessor_count\x18X \x01(\x05\x12\x16\n\x0eencryption_key\x18Y \x01(\t\x12\x19\n\x11frame_buffer_size\x18\\ \x01(\x05\x12\x15\n\rplatform_type\x18] \x01(\t\x12\x16\n\x0esecurity_token\x18^ \x01(\t\x12\x18\n\x10display_settings\x18` \x01(\t\x12\x14\n\x0cis_logged_in\x18a \x01(\x05b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_MAIN, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_MAIN, 'main_pb2', _globals)

# --- AccountPersonalShow_pb2 ---
DESCRIPTOR_ACC = _descriptor_pool.Default().AddSerializedFile(b'\n\x19AccountPersonalShow.proto\x12\x08freefire\"\xbc\x01\n\x0eAccountPrefers\x12\x15\n\rhide_my_lobby\x18\x01 \x01(\x08\x12\x1c\n\x14pregame_show_choices\x18\x02 \x03(\r\x12\x1f\n\x17br_pregame_show_choices\x18\x03 \x03(\r\x12\x1a\n\x12hide_personal_info\x18\x04 \x01(\x08\x12\x1f\n\x17disable_friend_spectate\x18\x05 \x01(\x08\x12\x17\n\x0fhide_occupation\x18\x06 \x01(\x08\"\x8a\x01\n\x10ExternalIconInfo\x12\x15\n\rexternal_icon\x18\x01 \x01(\t\x12,\n\x06status\x18\x02 \x01(\x0e2\x1c.freefire.ExternalIconStatus\x121\n\tshow_type\x18\x03 \x01(\x0e2\x1e.freefire.ExternalIconShowType\"\\\n\x0fSocialHighLight\x12\'\n\nhigh_light\x18\x01 \x01(\x0e2\x13.freefire.HighLight\x12\x11\n\texpire_at\x18\x02 \x01(\x03\x12\r\n\x05value\x18\x03 \x01(\r\"\xfc\x01\n\x14WeaponPowerTitleInfo\x12\x0e\n\x06region\x18\x01 \x01(\t\x12\x14\n\x0ctitle_cfg_id\x18\x02 \x01(\r\x12\x16\n\x0eleaderboard_id\x18\x03 \x01(\x04\x12\x11\n\tweapon_id\x18\x04 \x01(\r\x12\x0c\n\x04rank\x18\x05 \x01(\r\x12\x13\n\x0bexpire_time\x18\x06 \x01(\x03\x12\x13\n\x0breward_time\x18\x07 \x01(\x03\x12\x12\n\nRegionName\x18\x08 \x01(\t\x129\n\nRegionType\x18\t \x01(\x0e2%.freefire.ELeaderBoardTitleRegionType\x12\x0c\n\x04IsBr\x18\n \x01(\x08\"\xad\x01\n\x11GuildWarTitleInfo\x12\x0e\n\x06region\x18\x01 \x01(\t\x12\x0f\n\x07clan_id\x18\x02 \x01(\x04\x12\x14\n\x0ctitle_cfg_id\x18\x03 \x01(\r\x12\x16\n\x0eleaderboard_id\x18\x04 \x01(\x04\x12\x0c\n\x04rank\x18\x05 \x01(\r\x12\x13\n\x0bexpire_time\x18\x06 \x01(\x03\x12\x13\n\x0breward_time\x18\x07 \x01(\x03\x12\x11\n\tclan_name\x18\x08 \x01(\t\"\x92\x01\n\x14LeaderboardTitleInfo\x12?\n\x17weapon_power_title_info\x18\x01 \x03(\x0b2\x1e.freefire.WeaponPowerTitleInfo\x129\n\x14guild_war_title_info\x18\x02 \x03(\x0b2\x1b.freefire.GuildWarTitleInfo\"\xfb\x03\n\x0fSocialBasicInfo\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12 \n\x06gender\x18\x02 \x01(\x0e2\x10.freefire.Gender\x12$\n\x08language\x18\x03 \x01(\x0e2\x12.freefire.Language\x12)\n\x0btime_online\x18\x04 \x01(\x0e2\x14.freefire.TimeOnline\x12)\n\x0btime_active\x18\x05 \x01(\x0e2\x14.freefire.TimeActive\x12/\n\nbattle_tag\x18\x06 \x03(\x0e2\x1b.freefire.PlayerBattleTagID\x12\'\n\nsocial_tag\x18\x07 \x03(\x0e2\x13.freefire.SocialTag\x12)\n\x0bmode_prefer\x18\x08 \x01(\x0e2\x14.freefire.ModePrefer\x12\x11\n\tsignature\x18\t \x01(\t\x12%\n\trank_show\x18\n \x01(\x0e2\x12.freefire.RankShow\x12\x18\n\x10battle_tag_count\x18\x0b \x03(\r\x12!\n\x19signature_ban_expire_time\x18\x0c \x01(\x03\x12:\n\x12leaderboard_titles\x18\r \x01(\x0b2\x1e.freefire.LeaderboardTitleInfo\"\x92\x01\n#SocialHighLightsWithSocialBasicInfo\x125\n\x12social_high_lights\x18\x01 \x03(\x0b2\x19.freefire.SocialHighLight\x124\n\x11social_basic_info\x18\x02 \x01(\x0b2\x19.freefire.SocialBasicInfo\"c\n\x0eOccupationInfo\x12\x15\n\roccupation_id\x18\x01 \x01(\r\x12\x0e\n\x06scores\x18\x02 \x01(\x04\x12\x13\n\x0bproficients\x18\x03 \x01(\x04\x12\x15\n\rproficient_lv\x18\x04 \x01(\r\"d\n\x14OccupationSeasonInfo\x12\x11\n\tseason_id\x18\x01 \x01(\r\x12\x11\n\tgame_mode\x18\x02 \x01(\r\x12&\n\x04info\x18\x03 \x01(\x0b2\x18.freefire.OccupationInfo\"\xcb\x0c\n\x10AccountInfoBasic\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x14\n\x0caccount_type\x18\x02 \x01(\r\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x13\n\x0bexternal_id\x18\x04 \x01(\t\x12\x0e\n\x06region\x18\x05 \x01(\t\x12\r\n\x05level\x18\x06 \x01(\r\x12\x0b\n\x03exp\x18\x07 \x01(\r\x12\x15\n\rexternal_type\x18\x08 \x01(\r\x12\x15\n\rexternal_name\x18\t \x01(\t\x12\x15\n\rexternal_icon\x18\n \x01(\t\x12\x11\n\tbanner_id\x18\x0b \x01(\r\x12\x10\n\x08head_pic\x18\x0c \x01(\r\x12\x11\n\tclan_name\x18\r \x01(\t\x12\x0c\n\x04rank\x18\x0e \x01(\r\x12\x16\n\x0eranking_points\x18\x0f \x01(\r\x12\x0c\n\x04role\x18\x10 \x01(\r\x12\x16\n\x0ehas_elite_pass\x18\x11 \x01(\x08\x12\x11\n\tbadge_cnt\x18\x12 \x01(\r\x12\x10\n\x08badge_id\x18\x13 \x01(\r\x12\x11\n\tseason_id\x18\x14 \x01(\r\x12\r\n\x05liked\x18\x15 \x01(\r\x12\x12\n\nis_deleted\x18\x16 \x01(\x08\x12\x11\n\tshow_rank\x18\x17 \x01(\x08\x12\x15\n\rlast_login_at\x18\x18 \x01(\x03\x12\x14\n\x0cexternal_uid\x18\x19 \x01(\x04\x12\x11\n\treturn_at\x18\x1a \x01(\x03\x12\x1e\n\x16championship_team_name\x18\x1b \x01(\t\x12$\n\x1cchampionship_team_member_num\x18\x1c \x01(\r\x12\x1c\n\x14championship_team_id\x18\x1d \x01(\x04\x12\x0f\n\x07cs_rank\x18\x1e \x01(\r\x12\x19\n\x11cs_ranking_points\x18\x1f \x01(\r\x12\x19\n\x11weapon_skin_shows\x18  \x03(\r\x12\x0e\n\x06pin_id\x18! \x01(\r\x12\x19\n\x11is_cs_ranking_ban\x18\" \x01(\x08\x12\x10\n\x08max_rank\x18# \x01(\r\x12\x13\n\x0bcs_max_rank\x18$ \x01(\r\x12\x1a\n\x12max_ranking_points\x18% \x01(\r\x12\x15\n\rgame_bag_show\x18& \x01(\r\x12\x15\n\rpeak_rank_pos\x18\' \x01(\r\x12\x18\n\x10cs_peak_rank_pos\x18( \x01(\r\x121\n\x0faccount_prefers\x18) \x01(\x0b2\x18.freefire.AccountPrefers\x12\x1f\n\x17periodic_ranking_points\x18* \x01(\r\x12\x15\n\rperiodic_rank\x18+ \x01(\r\x12\x11\n\tcreate_at\x18, \x01(\x03\x12:\n\x16veteran_leave_days_tag\x18- \x01(\x0e2\x1a.freefire.VeteranLeaveDays\x12\x1b\n\x13selected_item_slots\x18. \x03(\r\x128\n\x10pre_veteran_type\x18/ \x01(\x0e2\x1e.freefire.PreVeteranActionType\x12\r\n\x05title\x180 \x01(\r\x126\n\x12external_icon_info\x181 \x01(\x0b2\x1a.freefire.ExternalIconInfo\x12\x17\n\x0frelease_version\x182 \x01(\t\x12\x1b\n\x13veteran_expire_time\x183 \x01(\x04\x12\x14\n\x0cshow_br_rank\x184 \x01(\x08\x12\x14\n\x0cshow_cs_rank\x185 \x01(\x08\x12\x0f\n\x07clan_id\x186 \x01(\x04\x12\x15\n\rclan_badge_id\x187 \x01(\r\x12\x19\n\x11custom_clan_badge\x188 \x01(\t\x12\x1d\n\x15use_custom_clan_badge\x189 \x01(\x08\x12\x15\n\rclan_frame_id\x18: \x01(\r\x12\x18\n\x10membership_state\x18; \x01(\x08\x12:\n\x12select_occupations\x18< \x03(\x0b2\x1e.freefire.OccupationSeasonInfo\x12Y\n\"social_high_lights_with_basic_info\x18= \x01(\x0b2-.freefire.SocialHighLightsWithSocialBasicInfo\"\x9a\x01\n\x0fAvatarSkillSlot\x12\x14\n\x07slot_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x15\n\x08skill_id\x18\x02 \x01(\x04H\x01\x88\x01\x01\x120\n\x0cequip_source\x18\x03 \x01(\x0e2\x15.freefire.EquipSourceH\x02\x88\x01\x01B\n\n\x08_slot_idB\x0b\n\t_skill_idB\x0f\n\r_equip_source\"\xfe\x03\n\rAvatarProfile\x12\x16\n\tavatar_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nskin_color\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x0f\n\x07clothes\x18\x04 \x03(\r\x12\x16\n\x0eequiped_skills\x18\x05 \x03(\r\x12\x18\n\x0bis_selected\x18\x06 \x01(\x08H\x02\x88\x01\x01\x12\x1f\n\x12pve_primary_weapon\x18\x07 \x01(\rH\x03\x88\x01\x01\x12\x1f\n\x12is_selected_awaken\x18\x08 \x01(\x08H\x04\x88\x01\x01\x12\x15\n\x08end_time\x18\t \x01(\rH\x05\x88\x01\x01\x12.\n\x0bunlock_type\x18\n \x01(\x0e2\x14.freefire.UnlockTypeH\x06\x88\x01\x01\x12\x18\n\x0bunlock_time\x18\x0b \x01(\rH\x07\x88\x01\x01\x12\x1b\n\x0eis_marked_star\x18\x0c \x01(\x08H\x08\x88\x01\x01\x12\x1e\n\x16clothes_tailor_effects\x18\r \x03(\rB\x0c\n\n_avatar_idB\r\n\x0b_skin_colorB\x0e\n\x0c_is_selectedB\x15\n\x13_pve_primary_weaponB\x15\n\x13_is_selected_awakenB\x0b\n\t_end_timeB\x0e\n\x0c_unlock_typeB\x0e\n\x0c_unlock_timeB\x11\n\x0f_is_marked_star\"\xd8\x02\n\x12AccountNewsContent\x12\x10\n\x08item_ids\x18\x01 \x03(\r\x12\x11\n\x04rank\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nmatch_mode\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x13\n\x06map_id\x18\x04 \x01(\rH\x02\x88\x01\x01\x12\x16\n\tgame_mode\x18\x05 \x01(\rH\x03\x88\x01\x01\x12\x17\n\ngroup_mode\x18\x06 \x01(\rH\x04\x88\x01\x01\x12\x1b\n\x0etreasurebox_id\x18\x07 \x01(\rH\x05\x88\x01\x01\x12\x19\n\x0ccommodity_id\x18\x08 \x01(\rH\x06\x88\x01\x01\x12\x15\n\x08store_id\x18\t \x01(\rH\x07\x88\x01\x01B\x07\n\x05_rankB\r\n\x0b_match_modeB\t\n\x07_map_idB\x0c\n\n_game_modeB\r\n\x0b_group_modeB\x11\n\x0f_treasurebox_idB\x0f\n\r_commodity_idB\x0b\n\t_store_id\"\xa7\x01\n\x0bAccountNews\x12%\n\x04type\x18\x01 \x01(\x0e2\x12.freefire.NewsTypeH\x00\x88\x01\x01\x122\n\x07content\x18\x02 \x01(\x0b2\x1c.freefire.AccountNewsContentH\x01\x88\x01\x01\x12\x18\n\x0bupdate_time\x18\x03 \x01(\x03H\x02\x88\x01\x01B\x07\n\x05_typeB\n\n\x08_contentB\x0e\n\x0c_update_time\"\x99\x02\n\x0bBasicEPInfo\x12\x18\n\x0bep_event_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nowned_pass\x18\x02 \x01(\x08H\x01\x88\x01\x01\x12\x15\n\x08ep_badge\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x16\n\tbadge_cnt\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x14\n\x07bp_icon\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x16\n\tmax_level\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x17\n\nevent_name\x18\x07 \x01(\tH\x06\x88\x01\x01B\x0e\n\x0c_ep_event_idB\r\n\x0b_owned_passB\x0b\n\t_ep_badgeB\x0c\n\n_badge_cntB\n\n\x08_bp_iconB\x0c\n\n_max_levelB\r\n\x0b_event_name\"\x9d\x02\n\rClanInfoBasic\x12\x14\n\x07clan_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x16\n\tclan_name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x17\n\ncaptain_id\x18\x03 \x01(\x04H\x02\x88\x01\x01\x12\x17\n\nclan_level\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x15\n\x08capacity\x18\x05 \x01(\rH\x04\x88\x01\x01\x12\x17\n\nmember_num\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x18\n\x0bhonor_point\x18\x07 \x01(\rH\x06\x88\x01\x01B\n\n\x08_clan_idB\x0c\n\n_clan_nameB\r\n\x0b_captain_idB\r\n\x0b_clan_levelB\x0b\n\t_capacityB\r\n\x0b_member_numB\x0e\n\x0c_honor_point\"|\n\x0cPetSkillInfo\x12\x13\n\x06pet_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x15\n\x08skill_id\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x18\n\x0bskill_level\x18\x03 \x01(\rH\x02\x88\x01\x01B\t\n\x07_pet_idB\x0b\n\t_skill_idB\x0e\n\x0c_skill_level\"\x84\x03\n\x07PetInfo\x12\x0f\n\x02id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x11\n\x04name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05level\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x10\n\x03exp\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x18\n\x0bis_selected\x18\x05 \x01(\x08H\x04\x88\x01\x01\x12\x14\n\x07skin_id\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x0f\n\x07actions\x18\x07 \x03(\r\x12&\n\x06skills\x18\x08 \x03(\x0b2\x16.freefire.PetSkillInfo\x12\x1e\n\x11selected_skill_id\x18\t \x01(\rH\x06\x88\x01\x01\x12\x1b\n\x0eis_marked_star\x18\n \x01(\x08H\x07\x88\x01\x01\x12\x15\n\x08end_time\x18\x0b \x01(\rH\x08\x88\x01\x01B\x05\n\x03_idB\x07\n\x05_nameB\x08\n\x06_levelB\x06\n\x04_expB\x0e\n\x0c_is_selectedB\n\n\x08_skin_idB\x14\n\x12_selected_skill_idB\x11\n\x0f_is_marked_starB\x0b\n\t_end_time\"<\n\x0eDiamondCostRes\x12\x19\n\x0cdiamond_cost\x18\x01 \x01(\rH\x00\x88\x01\x01B\x0f\n\r_diamond_cost\"\xfd\x03\n\x14CreditScoreInfoBasic\x12\x19\n\x0ccredit_score\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x14\n\x07is_init\x18\x02 \x01(\x08H\x01\x88\x01\x01\x120\n\x0creward_state\x18\x03 \x01(\x0e2\x15.freefire.RewardStateH\x02\x88\x01\x01\x12&\n\x19periodic_summary_like_cnt\x18\x04 \x01(\rH\x03\x88\x01\x01\x12)\n\x1cperiodic_summary_illegal_cnt\x18\x05 \x01(\rH\x04\x88\x01\x01\x12\x1d\n\x10weekly_match_cnt\x18\x06 \x01(\rH\x05\x88\x01\x01\x12(\n\x1bperiodic_summary_start_time\x18\x07 \x01(\x03H\x06\x88\x01\x01\x12&\n\x19periodic_summary_end_time\x18\x08 \x01(\x03H\x07\x88\x01\x01B\x0f\n\r_credit_scoreB\n\n\x08_is_initB\x0f\n\r_reward_stateB\x1c\n\x1a_periodic_summary_like_cntB\x1f\n\x1d_periodic_summary_illegal_cntB\x13\n\x11_weekly_match_cntB\x1e\n\x1c_periodic_summary_start_timeB\x1c\n\x1a_periodic_summary_end_time\"-\n\x0cEquipAchInfo\x12\x0e\n\x06ach_id\x18\x01 \x01(\r\x12\r\n\x05level\x18\x02 \x01(\r\"\xfa\x06\n\x17AccountPersonalShowInfo\x123\n\nbasic_info\x18\x01 \x01(\x0b2\x1a.freefire.AccountInfoBasicH\x00\x88\x01\x01\x122\n\x0cprofile_info\x18\x02 \x01(\x0b2\x17.freefire.AvatarProfileH\x01\x88\x01\x01\x12$\n\x17ranking_leaderboard_pos\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12#\n\x04news\x18\x04 \x03(\x0b2\x15.freefire.AccountNews\x12.\n\x0fhistory_ep_info\x18\x05 \x03(\x0b2\x15.freefire.BasicEPInfo\x125\n\x0fclan_basic_info\x18\x06 \x01(\x0b2\x17.freefire.ClanInfoBasicH\x03\x88\x01\x01\x12;\n\x12captain_basic_info\x18\x07 \x01(\x0b2\x1a.freefire.AccountInfoBasicH\x04\x88\x01\x01\x12(\n\x08pet_info\x18\x08 \x01(\x0b2\x11.freefire.PetInfoH\x05\x88\x01\x01\x123\n\x0bsocial_info\x18\t \x01(\x0b2\x19.freefire.SocialBasicInfoH\x06\x88\x01\x01\x127\n\x10diamond_cost_res\x18\n \x01(\x0b2\x18.freefire.DiamondCostResH\x07\x88\x01\x01\x12>\n\x11credit_score_info\x18\x0b \x01(\x0b2\x1e.freefire.CreditScoreInfoBasicH\x08\x88\x01\x01\x12=\n\x10pre_veteran_type\x18\x0c \x01(\x0e2\x1e.freefire.PreVeteranActionTypeH\t\x88\x01\x01\x12,\n\x0cequipped_ach\x18\r \x03(\x0b2\x16.freefire.EquipAchInfoB\r\n\x0b_basic_infoB\x0f\n\r_profile_infoB\x1a\n\x18_ranking_leaderboard_posB\x12\n\x10_clan_basic_infoB\x15\n\x13_captain_basic_infoB\x0b\n\t_pet_infoB\x0e\n\x0c_social_infoB\x13\n\x11_diamond_cost_resB\x14\n\x12_credit_score_infoB\x13\n\x11_pre_veteran_type*\xa0\x01\n\x10VeteranLeaveDays\x12\x19\n\x15VeteranLeaveDays_NONE\x10\x00\x12\x1a\n\x16VeteranLeaveDays_SHORT\x10\x01\x12\x1b\n\x17VeteranLeaveDays_NORMAL\x10\x02\x12\x19\n\x15VeteranLeaveDays_LONG\x10\x03\x12\x1d\n\x19VeteranLeaveDays_VERYLONG\x10\x04*w\n\x14PreVeteranActionType\x12\x1d\n\x19PreVeteranActionType_NONE\x10\x00\x12!\n\x1dPreVeteranActionType_ACTIVITY\x10\x01\x12\x1d\n\x19PreVeteranActionType_BUFF\x10\x02*s\n\x12ExternalIconStatus\x12\x1b\n\x17ExternalIconStatus_NONE\x10\x00\x12!\n\x1dExternalIconStatus_NOT_IN_USE\x10\x01\x12\x1d\n\x19ExternalIconStatus_IN_USE\x10\x02*t\n\x14ExternalIconShowType\x12\x1d\n\x19ExternalIconShowType_NONE\x10\x00\x12\x1f\n\x1bExternalIconShowType_FRIEND\x10\x01\x12\x1c\n\x18ExternalIconShowType_ALL\x10\x02*\xf0\x02\n\tHighLight\x12\x12\n\x0eHighLight_NONE\x10\x00\x12\x14\n\x10HighLight_BR_WIN\x10\x01\x12\x14\n\x10HighLight_CS_MVP\x10\x02\x12\x1b\n\x17HighLight_BR_STREAK_WIN\x10\x03\x12\x1b\n\x17HighLight_CS_STREAK_WIN\x10\x04\x12#\n\x1fHighLight_CS_RANK_GROUP_UPGRADE\x10\x05\x12\x16\n\x12HighLight_TEAM_ACE\x10\x06\x12 \n\x1cHighLight_WEAPON_POWER_TITLE\x10\x07\x12#\n\x1fHighLight_BR_RANK_GROUP_UPGRADE\x10\t\x12&\n\"HighLight_BR_STREAK_WIN_EXECELLENT\x10\n\x12&\n\"HighLight_CS_STREAK_WIN_EXECELLENT\x10\x0b\x12\x15\n\x11HighLight_VETERAN\x10\x0c*T\n\x06Gender\x12\x0f\n\x0bGender_NONE\x10\x00\x12\x0f\n\x0bGender_MALE\x10\x01\x12\x11\n\rGender_FEMALE\x10\x02\x12\x15\n\x10Gender_UNLIMITED\x10\xe7\x07*\xf5\x03\n\x08Language\x12\x11\n\rLanguage_NONE\x10\x00\x12\x0f\n\x0bLanguage_EN\x10\x01\x12\x1a\n\x16Language_CN_SIMPLIFIED\x10\x02\x12\x1b\n\x17Language_CN_TRADITIONAL\x10\x03\x12\x11\n\rLanguage_Thai\x10\x04\x12\x17\n\x13Language_VIETNAMESE\x10\x05\x12\x17\n\x13Language_INDONESIAN\x10\x06\x12\x17\n\x13Language_PORTUGUESE\x10\x07\x12\x14\n\x10Language_SPANISH\x10\x08\x12\x14\n\x10Language_RUSSIAN\x10\t\x12\x13\n\x0fLanguage_KOREAN\x10\n\x12\x13\n\x0fLanguage_FRENCH\x10\x0b\x12\x13\n\x0fLanguage_GERMAN\x10\x0c\x12\x14\n\x10Language_TURKISH\x10\r\x12\x12\n\x0eLanguage_HINDI\x10\x0e\x12\x15\n\x11Language_JAPANESE\x10\x0f\x12\x15\n\x11Language_ROMANIAN\x10\x10\x12\x13\n\x0fLanguage_ARABIC\x10\x11\x12\x14\n\x10Language_BURMESE\x10\x12\x12\x11\n\rLanguage_URDU\x10\x13\x12\x14\n\x10Language_BENGALI\x10\x14\x12\x17\n\x12Language_UNLIMITED\x10\xe7\x07*l\n\nTimeOnline\x12\x13\n\x0fTimeOnline_NONE\x10\x00\x12\x16\n\x12TimeOnline_WORKDAY\x10\x01\x12\x16\n\x12TimeOnline_WEEKEND\x10\x02\x12\x19\n\x14TimeOnline_UNLIMITED\x10\xe7\x07*\x84\x01\n\nTimeActive\x12\x13\n\x0fTimeActive_NONE\x10\x00\x12\x16\n\x12TimeActive_MORNING\x10\x01\x12\x18\n\x14TimeActive_AFTERNOON\x10\x02\x12\x14\n\x10TimeActive_NIGHT\x10\x03\x12\x19\n\x14TimeActive_UNLIMITED\x10\xe7\x07*\xf6\x02\n\x11PlayerBattleTagID\x12\x1a\n\x16PlayerBattleTagID_NONE\x10\x00\x12!\n\x1cPlayerBattleTagID_DOMINATION\x10\xcd\x08\x12\x1e\n\x19PlayerBattleTagID_UNCROWN\x10\xce\x08\x12\"\n\x1dPlayerBattleTagID_BESTPARTNER\x10\xcf\x08\x12\x1d\n\x18PlayerBattleTagID_SNIPER\x10\xd0\x08\x12\x1c\n\x17PlayerBattleTagID_MELEE\x10\xd1\x08\x12!\n\x1cPlayerBattleTagID_PEACEMAKER\x10\xd2\x08\x12\x1d\n\x18PlayerBattleTagID_AMBUSH\x10\xd3\x08\x12 \n\x1bPlayerBattleTagID_SHORTSTOP\x10\xd4\x08\x12\x1e\n\x19PlayerBattleTagID_RAMPAGE\x10\xd5\x08\x12\x1d\n\x18PlayerBattleTagID_LEADER\x10\xd6\x08*\xe4\x01\n\tSocialTag\x12\x12\n\x0eSocialTag_NONE\x10\x00\x12\x16\n\x11SocialTag_FASHION\x10\xb5\x10\x12\x15\n\x10SocialTag_SOCIAL\x10\xb6\x10\x12\x16\n\x11SocialTag_VETERAN\x10\xb7\x10\x12\x15\n\x10SocialTag_NEWBIE\x10\xb8\x10\x12\x19\n\x14SocialTag_PLAYFORWIN\x10\xb9\x10\x12\x19\n\x14SocialTag_PLAYFORFUN\x10\xba\x10\x12\x16\n\x11SocialTag_VOICEON\x10\xbb\x10\x12\x17\n\x12SocialTag_VOICEOFF\x10\xbc\x10*\x80\x01\n\nModePrefer\x12\x13\n\x0fModePrefer_NONE\x10\x00\x12\x11\n\rModePrefer_BR\x10\x01\x12\x11\n\rModePrefer_CS\x10\x02\x12\x1c\n\x18ModePrefer_ENTERTAINMENT\x10\x03\x12\x19\n\x14ModePrefer_UNLIMITED\x10\xe7\x07*X\n\x08RankShow\x12\x11\n\rRankShow_NONE\x10\x00\x12\x0f\n\x0bRankShow_BR\x10\x01\x12\x0f\n\x0bRankShow_CS\x10\x02\x12\x17\n\x12RankShow_UNLIMITED\x10\xe7\x07*L\n\x1bELeaderBoardTitleRegionType\x12\x08\n\x04None\x10\x00\x12\x0b\n\x07Country\x10\x01\x12\x0c\n\x08Province\x10\x02\x12\x08\n\x04City\x10\x03*6\n\nUnlockType\x12\x13\n\x0fUnlockType_NONE\x10\x00\x12\x13\n\x0fUnlockType_LINK\x10\x01*E\n\x0bEquipSource\x12\x14\n\x10EquipSource_SELF\x10\x00\x12 \n\x1cEquipSource_CONFIDANT_FRIEND\x10\x01*\xfa\x01\n\x08NewsType\x12\x11\n\rNewsType_NONE\x10\x00\x12\x11\n\rNewsType_RANK\x10\x01\x12\x14\n\x10NewsType_LOTTERY\x10\x02\x12\x15\n\x11NewsType_PURCHASE\x10\x03\x12\x18\n\x14NewsType_TREASUREBOX\x10\x04\x12\x16\n\x12NewsType_ELITEPASS\x10\x05\x12\x1a\n\x16NewsType_EXCHANGESTORE\x10\x06\x12\x13\n\x0fNewsType_BUNDLE\x10\x07\x12#\n\x1fNewsType_LOTTERYSPECIALEXCHANGE\x10\x08\x12\x13\n\x0fNewsType_OTHERS\x10\t*]\n\x0bRewardState\x12\x18\n\x14REWARD_STATE_INVALID\x10\x00\x12\x1a\n\x16REWARD_STATE_UNCLAIMED\x10\x01\x12\x18\n\x14REWARD_STATE_CLAIMED\x10\x02b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_ACC, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_ACC, 'AccountPersonalShow_pb2', _globals)

LoginReq = _globals['LoginReq']
LoginRes = _globals['LoginRes']
GetPlayerPersonalShow = _globals['GetPlayerPersonalShow']
AccountPersonalShowInfo = _globals['AccountPersonalShowInfo']

# ==========================================
# 2. CONFIGURATION & MULTI-BOT CREDENTIALS
# ==========================================
BOT_ACCOUNTS = [
    {"uid": "4744822452", "pass": "OUT_OF_LAW_47145DFBD348F5F2D68B5D75AFA957AF10BE04EF89332B5B8E5EA"},
    {"uid": "4744822456", "pass": "OUT_OF_LAW_6C6E2DB1FE8C6087D999992B683D28E2ABF6B782E9B1CBDD2B9B0"},
    {"uid": "4744822457", "pass": "OUT_OF_LAW_6C6E2DB1FE8C6087D999992B683D28E2ABF6B782E9B1CBDD2B9B0"},
    {"uid": "4744822455", "pass": "OUT_OF_LAW_49498E67BDAED34F1EB9D2845C96AB5BBDA28F4EC6D6AE88891CC"},
    {"uid": "4744822458", "pass": "OUT_OF_LAW_01BC9E8D0CC57F2B1AA63E1849781A2CBE2E3BC9A505379C6D5F3"},
    {"uid": "4744822464", "pass": "OUT_OF_LAW_47771F6395572BDA9F059686233E41CC38072D340F0BEFFBE3B0A"},
    {"uid": "4744822466", "pass": "OUT_OF_LAW_40FC70E1F85187425F311DFE0845CCC1B9F171F64C21D607FDC13"},
    {"uid": "4744822463", "pass": "OUT_OF_LAW_54060612F8C41A0FDE07CBA2B699345EC7CAA0D818A2C5DF6D086"},
    {"uid": "4744822467", "pass": "OUT_OF_LAW_8A76FC82404B248D2747AF5C37159F73445CDEE34B3FE8BF1E37B"},
    {"uid": "4744822470", "pass": "OUT_OF_LAW_7FB007F5A8F15FC8F4C2622D65A7112379F81AD285DA44395CDFE"}
]

MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')
RELEASEVERSION = "OB53"
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 10; SM-A515F Build/QP1A.190711.020)"

app = Flask(__name__)
CORS(app)

BD_TOKENS_CACHE = [{"token": "0", "server_url": "0", "expires_at": 0} for _ in BOT_ACCOUNTS]
bot_cycle = itertools.cycle(range(len(BOT_ACCOUNTS)))

# ==========================================
# 3. ENCRYPTION & DECRYPTION 
# ==========================================
def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(pad(plaintext, AES.block_size))

def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    if len(ciphertext) % 16 != 0: return ciphertext
    try:
        aes = AES.new(key, AES.MODE_CBC, iv)
        decrypted = aes.decrypt(ciphertext)
        return unpad(decrypted, AES.block_size)
    except: return ciphertext

def decode_protobuf(encoded_data: bytes, message_type: message.Message) -> message.Message:
    instance = message_type()
    instance.ParseFromString(encoded_data)
    return instance

async def json_to_proto(json_data: str, proto_message: Message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)
    return proto_message.SerializeToString()

# ==========================================
# 4. GARENA AUTHENTICATION FLOW (UPDATED FROM OB53)
# ==========================================
# lord2.py থেকে নতুন User-Agent নেওয়া হলো
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)"

async def get_access_token(bot_index: int):
    bot = BOT_ACCOUNTS[bot_index]
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    payload = {"uid": bot["uid"], "password": bot["pass"], "response_type": "token", "client_type": "2", "client_id": "100067", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"}
    
    headers = {'User-Agent': USERAGENT, 'Connection': "close", 'Accept-Encoding': "gzip", 'Content-Type': "application/x-www-form-urlencoded"}
    
    async with httpx.AsyncClient(verify=False, timeout=15.0) as client:
        try:
            resp = await client.post(url, data=payload, headers=headers)
            data = resp.json()
            if "access_token" not in data: return "0", "0"
            return data.get("access_token"), data.get("open_id")
        except: return "0", "0"

async def create_bd_jwt(bot_index: int):
    token_val, open_id = await get_access_token(bot_index)
    if token_val == "0": return

    body = json.dumps({"open_id": open_id, "open_id_type": "4", "login_token": token_val, "orign_platform_type": "4"})
    proto_bytes = await json_to_proto(body, LoginReq())
    payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)
    
    # FIX: ggblueshark.com এর বদলে lord2.py এর ggpolarbear.com দেওয়া হলো
    url = "https://loginbp.ggpolarbear.com/MajorLogin"
    
    headers = {
        'User-Agent': USERAGENT, 
        'Accept-Encoding': "gzip", 
        'Content-Type': "application/octet-stream", 
        'X-Unity-Version': "2018.4.11f1", 
        'X-GA': "v1 1", 
        'ReleaseVersion': RELEASEVERSION
    }
    
    async with httpx.AsyncClient(verify=False, timeout=20.0) as client:
        try:
            resp = await client.post(url, data=payload, headers=headers)
            if resp.status_code != 200: return
                
            parsed_proto = decode_protobuf(resp.content, LoginRes)
            msg = json.loads(json_format.MessageToJson(parsed_proto, preserving_proto_field_name=True))
            real_token = msg.get('token', '')
            if not real_token: return
                
            BD_TOKENS_CACHE[bot_index]['token'] = f"Bearer {real_token}"
            BD_TOKENS_CACHE[bot_index]['server_url'] = msg.get('server_url') or msg.get('serverUrl') or '0'
            BD_TOKENS_CACHE[bot_index]['expires_at'] = time.time() + 3600 
        except Exception as e: 
            pass

async def get_valid_token(bot_index: int) -> Tuple[str, str]:
    cache = BD_TOKENS_CACHE[bot_index]
    if time.time() >= cache['expires_at'] or cache['token'] == '0': 
        await create_bd_jwt(bot_index)
    return BD_TOKENS_CACHE[bot_index]['token'], BD_TOKENS_CACHE[bot_index]['server_url']


# ==========================================
# RAW PROTOBUF DECODER (SCHEMA BYPASS)
# ==========================================
def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint": field_data['data'] = result.data
        elif result.wire_type == "string": field_data['data'] = result.data
        elif result.wire_type == "bytes": field_data['data'] = result.data
        elif result.wire_type == 'length_delimited': field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_Raw_Protobuf(hex_string):
    try:
        parsed_results = Parser().parse(hex_string)
        return Fix_PackEt(parsed_results)
    except Exception as e:
        return {"error": f"Raw Decode Failed: {str(e)}"}

# ==========================================
# 5. FETCH PLAYER INFO 
# ==========================================
async def GetAccountInformation(uid: str, endpoint: str, bot_index: int):
    payload = await json_to_proto(json.dumps({'a': uid, 'b': 7}), GetPlayerPersonalShow())
    data_enc = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, payload)
    
    token, server = await get_valid_token(bot_index)
    
    if token == "0" or server == "0": 
        raise Exception("Token generation failed.")
        
    headers = {
        'User-Agent': USERAGENT, 
        'Accept-Encoding': "gzip", 
        'Content-Type': "application/octet-stream", 
        'Authorization': token, 
        'X-Unity-Version': "2018.4.11f1", 
        'X-GA': "v1 1", 
        'ReleaseVersion': RELEASEVERSION
    }
    
    full_url = f"{server.rstrip('/')}{endpoint}"

    async with httpx.AsyncClient(verify=False, timeout=15.0) as client:
        resp = await client.post(full_url, data=data_enc, headers=headers)
        
        if resp.status_code != 200: 
            raise Exception(f"HTTP Error {resp.status_code}")
            
        decrypted_content = aes_cbc_decrypt(MAIN_KEY, MAIN_IV, resp.content)
        
        try:
            # প্রথমে নরমাল স্কিমা দিয়ে ট্রাই করবে
            parsed_data = decode_protobuf(decrypted_content, AccountPersonalShowInfo)
            return json.loads(json_format.MessageToJson(parsed_data, preserving_proto_field_name=True))
        
        except Exception as e:
            # 🚨 স্কিমা ফেইল করলে Raw Schema-less Decoder ব্যবহার করবে 🚨
            raw_hex = decrypted_content.hex()
            raw_json_data = DeCode_Raw_Protobuf(raw_hex)
            
            return {
                "status": "OB53 Schema Bypassed",
                "message": "Player Data extracted using Raw Decoder.",
                "raw_data": raw_json_data
            }

# ==========================================
# 6. ASYNC FLASK ROUTE FOR VERCEL & LOCALHOST
# ==========================================
@app.route('/')
def home():
    return jsonify({"status": "API is Online", "usage": "/player-info?uid=YOUR_UID"})

@app.route('/player-info')
async def get_account_info():
    uid = request.args.get('uid')
    if not uid: return jsonify({"error": "Please provide UID."}), 400

    last_error_data = {}
    
    for _ in range(3):
        current_bot_index = next(bot_cycle)
        try:
            return_data = await GetAccountInformation(uid, "/GetPlayerPersonalShow", current_bot_index)
            if return_data: 
                formatted_json = json.dumps(return_data, ensure_ascii=False)
                return Response(formatted_json, status=200, mimetype='application/json; charset=utf-8')
                
        except Exception as e:
            # Error টিকে JSON হিসেবে পার্স করে স্টোর করবে
            try:
                last_error_data = json.loads(str(e))
            except:
                last_error_data = {"raw_error": str(e)}
            continue # পরের বট দিয়ে ট্রাই করবে

    # ৩ বারের চেষ্টাতেও ফেইল করলে ডিবাগ ইনফরমেশন শো করবে
    return jsonify({
        "error": "Failed after multiple attempts.",
        "debug_info": last_error_data
    }), 500

# ==========================================
# LOCALHOST SUPPORT
# ==========================================
if __name__ == '__main__':
    print("Running in Localhost mode...")
    app.run(host='0.0.0.0', port=5000, debug=True)
