# -*- coding: utf-8 -*-
from CheXun_Spider.settings import *

def Save_Source(data, name):
    file_object = open('%s\%s.txt' %(FILE, name), 'w')
    file_object.write(data)
    file_object.close()