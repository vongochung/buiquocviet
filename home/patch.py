# -*- coding: utf-8 -*-
from django.contrib.auth.models import User


def get_image(self):
    if self.username == "vohien":
        return "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xfa1/v/t1.0-1/c0.8.50.50/p50x50/28772_114592531904646_6681744_n.jpg?oh=3b3e926bff754f54b0063be4f32ba60d&oe=54D64EE3&__gda__=1427771457_e61b233fa6fa5446d3c4932ffbb0e65b"
    elif self.username == "met" or self.username == "oMet":
        return "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xap1/v/t1.0-1/c0.0.160.160/p160x160/11608_373424162819254_2043029436955836004_n.jpg?oh=b064caae5f1cc2c61026de977343e3f1&oe=55184D6D&__gda__=1426544220_48597063de14f4b91395acce335ceaf2"
    elif self.username == "aKhoa":
        return "https://scontent-b-hkg.xx.fbcdn.net/hphotos-xpa1/v/t1.0-9/1394186_1434088103479827_1579304151_n.jpg?oh=101d41b3deaa38aee9b15d2d8b78bda3&oe=54FCAACA"
    else:
        return "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/c2.0.50.50/p50x50/10177407_839821572703570_3363226913857924213_n.jpg?oh=82b709d4e4130d4b4fa2c2d5013a9242&oe=551F5CF9&__gda__=1423660972_967de75eaa114a961cfc2145cea0cc8a"


User.add_to_class("get_image", get_image)
