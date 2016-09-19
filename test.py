# -*- coding: utf-8 -*-

import time
import requests
import re
from lxml import etree
from public.mysqlpooldao import MysqlDao
from public.headers import Headers

last_url = '共 6492 页 129834 条 </span>首页</a>1</a>2</a>3</a>4</a>5</a>6</a>7</a>8</a>末页</a>'
match_obj = re.search(r'共 (.*?) 页', last_url, re.M | re.I)
last_page = int(match_obj.group(1))
print(last_page)