TEAMS = [
    'MACCABI_TEL_AVIV',
    'IRONI_KIRYAT_SHMONA',
    'MACCABI_PETAH_TIKVA',
    'MACCABI_NETANYA',
    'MACCABI_HAIFA',
    'F_C_ASHDOD',
    'HAPOEL_TEL_AVIV',
    'HAPOEL_KFAR_SABA',
    'HAPOEL_HAIFA',
    'HAPOEL_HADERA',
    'HAPOEL_BEER_SHEVA',
    'BNEI_SAKHNIN',
    'BNEI_YEHUDA',
    'BEITAR_JERUSALEM',
]

# Teams Page in One:
ONE_TEAMS_PAGES = {
    'MACCABI_TEL_AVIV':     'https://www.one.co.il/Soccer/team/3',
    'IRONI_KIRYAT_SHMONA':  'https://www.one.co.il/Soccer/team/3112',
    'MACCABI_PETAH_TIKVA':  'https://www.one.co.il/Soccer/team/10',
    'MACCABI_NETANYA':      'https://www.one.co.il/Soccer/team/8',
    'MACCABI_HAIFA':        'https://www.one.co.il/Soccer/team/4',
    'F_C_ASHDOD':           'https://www.one.co.il/Soccer/team/9',
    'HAPOEL_TEL_AVIV':      'https://www.one.co.il/Soccer/team/5',
    'HAPOEL_KFAR_SABA':     'https://www.one.co.il/Soccer/team/12',
    'HAPOEL_HAIFA':         'https://www.one.co.il/Soccer/team/1',
    'HAPOEL_HADERA':        'https://www.one.co.il/Soccer/team/6940',
    'HAPOEL_BEER_SHEVA':    'https://www.one.co.il/Soccer/team/22',
    'BNEI_SAKHNIN':         'https://www.one.co.il/Soccer/team/17',
    'BNEI_YEHUDA':          'https://www.one.co.il/Soccer/team/11',
    'BEITAR_JERUSALEM':     'https://www.one.co.il/Soccer/team/2'
}
TEAMS_ONE_REVERSE = {v: k for k, v in ONE_TEAMS_PAGES.items()}

# Teams Page in Walla Sport:
WALLA_TEAMS_PAGES = {
    'MACCABI_TEL_AVIV':     'https://sports.walla.co.il/team/739?league=157',
    'IRONI_KIRYAT_SHMONA':  'https://sports.walla.co.il/team/9707?league=157',
    'MACCABI_PETAH_TIKVA':  'https://sports.walla.co.il/team/744?league=157',
    'MACCABI_NETANYA':      'https://sports.walla.co.il/team/750?league=157',
    'MACCABI_HAIFA':        'https://sports.walla.co.il/team/740?league=157',
    'F_C_ASHDOD':           'https://sports.walla.co.il/team/749?league=157',
    'HAPOEL_TEL_AVIV':      'https://sports.walla.co.il/team/738?league=157',
    'HAPOEL_KFAR_SABA':     'https://sports.walla.co.il/team/3983?league=157',
    'HAPOEL_HAIFA':         'https://sports.walla.co.il/team/741?league=157',
    'HAPOEL_HADERA':        'https://sports.walla.co.il/team/11775?league=157',
    'HAPOEL_BEER_SHEVA':    'https://sports.walla.co.il/team/3987?league=157',
    'BNEI_SAKHNIN':         'https://sports.walla.co.il/team/4008?league=157',
    'BNEI_YEHUDA':          'https://sports.walla.co.il/team/745?league=157',
    'BEITAR_JERUSALEM':     'https://sports.walla.co.il/team/742?league=157'
}
TEAMS_WALLA_REVERSE = {v: k for k, v in WALLA_TEAMS_PAGES.items()}
# Teams Page in Sport5:
SPORT5_TEAMS_PAGES = {
    'MACCABI_TEL_AVIV':     'https://www.sport5.co.il/team.aspx?FolderID=192',
    'IRONI_KIRYAT_SHMONA':  'https://www.sport5.co.il/team.aspx?FolderID=845',
    'MACCABI_PETAH_TIKVA':  'https://www.sport5.co.il/team.aspx?FolderID=199',
    'MACCABI_NETANYA':      'https://www.sport5.co.il/team.aspx?FolderID=193',
    'MACCABI_HAIFA':        'https://www.sport5.co.il/team.aspx?FolderID=163',
    'F_C_ASHDOD':           'https://www.sport5.co.il/team.aspx?FolderID=198',
    'HAPOEL_TEL_AVIV':      'https://www.sport5.co.il/team.aspx?FolderID=164',
    'HAPOEL_KFAR_SABA':     'https://www.sport5.co.il/team.aspx?FolderID=196',
    'HAPOEL_HAIFA':         'https://www.sport5.co.il/team.aspx?FolderID=1632',
    'HAPOEL_HADERA':        'https://www.sport5.co.il/team.aspx?FolderID=8518',
    'HAPOEL_BEER_SHEVA':    'https://www.sport5.co.il/team.aspx?FolderID=1639',
    'BNEI_SAKHNIN':         'https://www.sport5.co.il/team.aspx?FolderID=195',
    'BNEI_YEHUDA':          'https://www.sport5.co.il/team.aspx?FolderID=190',
    'BEITAR_JERUSALEM':     'https://www.sport5.co.il/team.aspx?FolderID=191'
}
TEAMS_SPORT5_REVERSE = {v: k for k, v in SPORT5_TEAMS_PAGES.items()}

MAX_ARTICLES_FROM_SITE = 15