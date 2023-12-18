from info import scp_184


text = ''
for i in scp_184['notes']['notes_dict']:
    text += i + '\n'


audios_dict = ''
for i in scp_184['code_name']['audiofiles']:
    audios_dict += i + '\n'


def yes_no(message):
    return message.text.lower() == 'да'



list = {
            1: 'mp3_1',
            2: 'mp3_2',
            3: 'mp3_3',
            4: 'mp3_4',
            5: 'mp3_5',
            6: 'mp3_6',
            7: 'mp3_7',
            8: 'mp3_8',
            9: 'mp3_9',
            10: 'mp3_10',
            11: 'mp3_11',
            12: 'mp3_12',
            13: 'mp3_13',
            14: 'mp3_14',
            15: 'mp3_15',
        }
