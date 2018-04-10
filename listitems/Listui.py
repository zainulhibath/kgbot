import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram import InlineKeyboardButton


class Listui:
    """
    Object that abstracts admin operation on channel data in xml format
    """

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')
        (self.FINPUT, self.GDIV, self.STICKER_NAME, self.STICKER_URL, self.STICKER_IMG, self.KNWTG, self.CHNL, self.BOT) = range(8)
        self.ST_NAME = ""
        self.ST_URL = ""
        self.CUR_PAGE = ""
        
        
    def start(self, bot, update):
      intro_file_handle = open('info/intro.txt')
      intro_text = intro_file_handle.read()
      bot.sendMessage(
          chat_id=update.message.chat_id,
          text=intro_text)
      custom_keyboard = [
          ['Know telegram'],
          ['Groups'],
          ['Channels'],
          ['Bots'],
          ['Stickers'],
          ['Rules'],
          ['Cancel']]
      reply_markup = ReplyKeyboardMarkup(
                  custom_keyboard, one_time_keyboard=True)
      bot.sendMessage(
                  chat_id=update.message.chat_id,
                  text="ആവശ്യമുള്ളത് തിരഞ്ഞെടുക്കുക",
                   parse_mode='Markdown',
                  reply_markup=reply_markup)
      return self.FINPUT
      
    def know_tg(self, bot, update):
      keyboard = [[InlineKeyboardButton("What Is a Bot", callback_data='1'),
        InlineKeyboardButton("What is channels", callback_data='2')],
        [InlineKeyboardButton("What is Supergroup", callback_data='3'),
        InlineKeyboardButton("contact Admin", callback_data='4')],
        [InlineKeyboardButton("Back to Main menu", callback_data='5')]]

      reply_markup = InlineKeyboardMarkup(keyboard)
      tg_file_handle = open('info/tg.txt')
      tg_text = tg_file_handle.read()
      update.message.reply_text(
        tg_text,
        parse_mode='HTML',
        reply_markup=reply_markup)
      return self.KNWTG


    def button(self, bot, update):
      keyboard = [[InlineKeyboardButton("What Is a Bot", callback_data='1'),
        InlineKeyboardButton("What is channels", callback_data='2')],
        [InlineKeyboardButton("What is Supergroup", callback_data='3'),
        InlineKeyboardButton("contact Admin", callback_data='4')],
        [InlineKeyboardButton("Back to Main menu", callback_data='5')]]

      reply_markup = InlineKeyboardMarkup(keyboard)
      query = update.callback_query
      choice = query.data
      if choice == '1':
        path = 'info/wtisbot.txt'
      elif choice == '2':
        path = 'info/wtischannel.txt'
      elif choice == '3':
        path = 'info/wtisgrp.txt'
      elif choice == '4':
        path = 'info/admin.txt'
      elif choice == '5':
        start(bot, query)
      return self.FINPUT
      file = open(path)
      text = file.read()
      bot.editMessageText(text=text,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        parse_mode='HTML',
                        reply_markup=reply_markup)


    def rules(self, bot, update):
      rule_file_handle = open('info/rules.txt')
      rule_text = rule_file_handle.read()
      bot.sendMessage(
          chat_id=update.message.chat_id,
          text=rule_text)


    def stickerStart(self, bot, update):
        """
        Entry point for sticker updation
         Prompts sticker name
        """
        bot.sendMessage(
        chat_id=update.message.chat_id,
        text='sent the sticker packs Name')
        return self.STICKER_NAME


    def stickerName(self, bot, update):
        """
        Prompts sticker url
        Accepts sticker name
        """
        
        global ST_NAME
        ST_NAME = update.message.text
        bot.sendMessage(
        chat_id=update.message.chat_id,
        text='sent the sticker packs Url')
        return self.STICKER_URL


    def stickerURL(self, bot, update):
      """
      Prompts sticker preview image
      Accepts sticker url
      """
      global ST_URL
      if(1):
        ST_URL = update.message.text
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='sent a preview Image of the sticker pack')
        return self.STICKER_IMG
      else:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='[ERROR] Malformed URL')
        return self.STICKER_URL


    def stickerImage(self, bot, update):
      """
      Exit point for sticker updation
      Accepts sticker image
      """
      ST_LOC = "sticker_img/%s.jpeg" % ST_NAME
      file_id = update.message.photo[-1].file_id
      ST_FILE = bot.getFile(file_id)
      ST_FILE.download(ST_LOC)
      stdb = StickersDB()
      stdb.save_sticker(ST_NAME, ST_URL, ST_LOC)
      bot.sendMessage(
        chat_id=update.message.chat_id,
        text='Succefully added The Sticker')
      return self.FINPUT


    def groupsEntry(self, bot, update):
      tree = ET.parse('file_xml/groups.xml')
      root = tree.getroot()
      keyboard = []
      size = 3
      for i in range(0, len(root), size):
        list = []
        for j in root[i:i+size]:
            list.append(InlineKeyboardButton(j.attrib.get("name"),
                                             callback_data=j.attrib.get("id")))
        keyboard.append(list)
      keyboard.append([InlineKeyboardButton("Back to Main",
                                          callback_data='main')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      chan_file_handle = open('info/groupintro.txt')
      chan_text = chan_file_handle.read()
      update.message.reply_text(
        chan_text,
        parse_mode='HTML',
        reply_markup=reply_markup)
      return self.GDIV


    def groupsInfo(self, bot, update):
      tree = ET.parse('file_xml/groups.xml')
      root = tree.getroot()
      keyboard = []
      size = 3
      for i in range(0, len(root), size):
        list = []
        for j in root[i:i+size]:
            list.append(InlineKeyboardButton(j.attrib.get("name"),
                                             callback_data=j.attrib.get("id")))
        keyboard.append(list)
      keyboard.append([InlineKeyboardButton("Back to Main",
                                          callback_data='main')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      query = update.callback_query
      choice = query.data
      if choice == 'main':
        start(bot, query)
        return self.FINPUT
      else:
        lists = []
        tree = ET.parse('file_xml/groups.xml')
        root = tree.getroot()
        for child in root[int(choice)]:
            text = child.text
            text2 = child.attrib.get("title")
            lists.append("👉🏿"+text2+"  "+text)
        tex = ""
        for k in lists:
            tex +="\n"+k

        bot.editMessageText(text=tex,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            parse_mode='HTML',
                            reply_markup=reply_markup,
                            disable_web_page_preview=True)
      return self.GDIV

    def channels(self, bot, update):
      tree = ET.parse('file_xml/chan.xml')
      root = tree.getroot()
      keyboard = []
      size = 3
      for i in range(0, len(root), size):
        list = []
        for j in root[i:i+size]:
            list.append(InlineKeyboardButton(j.attrib.get("name"),
                                             callback_data=j.attrib.get("id")))
        keyboard.append(list)
      keyboard.append([InlineKeyboardButton("Back to Main",
                                          callback_data='main')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      chan_file_handle = open('info/chanintro.txt')
      chan_text = chan_file_handle.read()
      update.message.reply_text(
        chan_text,
        parse_mode='HTML',
        reply_markup=reply_markup)
      return self.CHNL


    def button_channel(self, bot, update):
      tree = ET.parse('file_xml/chan.xml')
      root = tree.getroot()
      keyboard = []
      size = 3
      for i in range(0, len(root), size):
        list = []
        for j in root[i:i+size]:
            list.append(InlineKeyboardButton(j.attrib.get("name"),
                                             callback_data=j.attrib.get("id")))
        keyboard.append(list)
      keyboard.append([InlineKeyboardButton("Back to Main",
                                          callback_data='main')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      query = update.callback_query
      choice = query.data
      if choice == 'main':
        start(bot, query)
        return self.FINPUT
      else:
        lists = []
        tree = ET.parse('file_xml/chan.xml')
        root = tree.getroot()
        for child in root[int(choice)]:
            text = child.text
            text2 = child.attrib.get("title")
            lists.append("👉🏿"+text2+"  "+text)
        tex = ""
        for k in lists:
            tex +="\n"+k

        bot.editMessageText(text=tex,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            parse_mode='HTML',
                            reply_markup=reply_markup,
                            disable_web_page_preview=True)
        return self.CHNL


    def bo_t(self, bot, update):
      tree = ET.parse('file_xml/bot.xml')
      root = tree.getroot()
      keyboard = []
      size = 3
      for i in range(0, len(root), size):
        list = []
        for j in root[i:i+size]:
            list.append(InlineKeyboardButton(j.attrib.get("name"),
                                             callback_data=j.attrib.get("id")))
        keyboard.append(list)
      keyboard.append([InlineKeyboardButton("Back to Main",
                                          callback_data='main')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      chan_file_handle = open('info/botintro.txt')
      chan_text = chan_file_handle.read()
      update.message.reply_text(
        chan_text,
        parse_mode='HTML',
        reply_markup=reply_markup)
      return self.BOT
      


    def button_bot(self, bot, update):
      tree = ET.parse('file_xml/bot.xml')
      root = tree.getroot()
      keyboard = []
      size = 3
      for i in range(0, len(root), size):
        list = []
        for j in root[i:i+size]:
            list.append(InlineKeyboardButton(j.attrib.get("name"),
                                             callback_data=j.attrib.get("id")))
        keyboard.append(list)
      keyboard.append([InlineKeyboardButton("Back to Main",
                                          callback_data='main')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      query = update.callback_query
      choice = query.data
      if choice == 'main':
        start(bot, query)
        return self.FINPUT
      else:
        lists = []
        tree = ET.parse('file_xml/bot.xml')
        root = tree.getroot()
        for child in root[int(choice)]:
            text = child.text
            text2 = child.attrib.get("title")
            lists.append("👉🏿"+text2+"  "+text)
        tex = ""
        for k in lists:
            tex +="\n"+k

        bot.editMessageText(text=tex,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            parse_mode='HTML',
                            reply_markup=reply_markup,
                            disable_web_page_preview=True)
        return self.BOT


    def stick_er(self, bot, update):
      global CUR_PAGE
      stdb = StickersDB()
      pages = stdb.fetch_list()
      choice = update.message.text
      if pages:
        if choice == 'Stickers':
            page_entry = pages[CUR_PAGE]
            # page_entry [0]-ID, [1]-Name, [2]-URL, [3]-Path to preview
            display(page_entry, bot, update)
        if choice == 'Previous':
            if CUR_PAGE > 0:
                CUR_PAGE = CUR_PAGE - 1
                page_entry = pages[CUR_PAGE]
            else:
                page_entry = pages[CUR_PAGE]
            display(page_entry, bot, update)
        elif choice == 'Next':
            if (CUR_PAGE < (len(pages) - 1)):
                CUR_PAGE = CUR_PAGE + 1
                page_entry = pages[CUR_PAGE]
            else:
                page_entry = pages[CUR_PAGE]
            display(page_entry, bot, update)
        elif choice == 'GoBack':
            return self.FINPUT

      else:
        # TODO: ERROR MESSAGE
        print("Database Returned Null Entry")


    def display(self, page_entry, bot, update):
      bot.sendMessage(chat_id=update.message.chat_id, text=page_entry[1])
      bot.sendPhoto(
        chat_id=update.message.chat_id,
        photo=open(page_entry[3], 'rb'),
        caption=page_entry[2])
      custom_keyboard = [['Previous'], ['Next'], ['GoBack']]
      reply_markup = ReplyKeyboardMarkup(
                custom_keyboard)
      bot.sendMessage(
                chat_id=update.message.chat_id,
                text="select next to get stickers",
                parse_mode='Markdown',
                reply_markup=reply_markup)
      return self.FINPUT


    def addChannel(self, cat_id, chan_title, chan_url):
        """
        Add new channel under the given category
        :param cat_id: Category ID
        :param chan_title: Channel title/name
        :param chan_url: Channel URL/username
        """
        xml = et.parse(self.xml_path)
        data = xml.getroot()
        new_chan = et.Element("link", title=chan_title)
        new_chan.text = chan_url
        data[cat_id].append(new_chan)
        file = et.ElementTree(data)
        file.write(self.xml_path, pretty_print=True)

    def getCategories(self):
        """
        Get category list from the xml
        :return categories: a list of list containing  id and name of categories
        """
        xml = et.parse(self.xml_path)
        data = xml.getroot()
        categories = []
        for item in data:
          categories.append([item.attrib.get("id"), item.attrib.get("name")])
        return(categories)

    def getChannels(self, cat_id):
        """
        Get Channel list from the xml
        :param cat_id: Category ID
        :return channels: a list of list containing title and link of channels
        """
        xml = et.parse(self.xml_path)
        data = xml.getroot()
        channels = []
        for item in data[cat_id]:
            channels.append([item.attrib.get("title"), item.text])
        return(channels)

    def getChannel(self, cat_id, chan_id):
       """
        Get channel info
        :param cat_id: Category ID
        :param chan_id: Channel ID
        :return channel_info: a list containing channel info, title and url
        """
       xml = et.parse(self.xml_path)
       data = xml.getroot()
       channel = data[cat_id][chan_id]
       channel_info = [channel.attrib.get("title"), channel.text]
       return(channel_info)    

    
