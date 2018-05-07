#!/usr/bin/env python3

import itchat
import time
import numpy as np
import matplotlib.pyplot as plt
import re
import io
import jieba
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

def parse_contacts():
	print('please wait a minute...')
	sexDic = dict()
	signatureList = []
	male = 'male'
	famale = 'famale'
	other = 'other'

	itchat.auto_login(True)
	friendList = itchat.get_friends(update=True)[0:]
	for friend in friendList:
		sex = friend['Sex']
		if sex == 1:
			sexDic[male] = sexDic.get(male, 0) + 1
		elif sex == 2:
			sexDic[famale] = sexDic.get(famale, 0) + 1
		else:
			sexDic[other] = sexDic.get(other, 0) + 1

		signature = friend['Signature'].strip().replace("span", "").replace("class", "").replace("emoji","")
		rep = re.compile("1f\d+\w*|[<>/=]")
		signature = rep.sub("", signature)
		signatureList.append(signature)
		
	total = len(friendList[1:])
	print('共有好友%d人' % total + '\n' + '男性好友：%.2f%%' % (float(sexDic[male]) / total * 100) + '\n' + '女性好友：%.2f%%' % (float(sexDic[famale]) / total * 100) + '\n' + '不明性别好友：%.2f%%' % (float(sexDic[other]) / total * 100))	
	draw(sexDic)

	signature_text = "".join(signatureList)
	with io.open('signature.txt', 'a', encoding='utf-8') as f:
		wordlist = jieba.cut(signature_text, cut_all=True)
		word_space_split = " ".join(wordlist)
		f.write(word_space_split)
		f.close()
		draw_signature()

def draw(datas):
	for key in datas.keys():
		plt.bar(key, datas[key])

	plt.legend()
	plt.xlabel('sex')
	plt.ylabel('rate')
	plt.title("Gender of your friends")
	plt.show()

def draw_signature():
	text = open(u'signature.txt', encoding='utf-8').read()
	alice_mask = np.array(Image.open('girl.png'))
	wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask, font_path="SimSun.ttf").generate(text)
	image_colors = ImageColorGenerator(alice_mask)
	plt.imshow(wc.recolor(color_func=image_colors))
	plt.imshow(wc)
	plt.axis('off')
	plt.show()

	# 这一句可直接保存图片
	# wc.to_file('wc_new.png')

parse_contacts()	
