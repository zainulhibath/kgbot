import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram import InlineKeyboardButton
import xml.etree.ElementTree as ET
import settings
from listitems import Listing




class UI:
    """
    Object that abstracts admin operation on channel data in xml format
    """

    def __init__(self,xml):
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')
        self.xml_path = "path to xml"
        (self.NEW_CATEG, self.SAVE_CATEG, self.SHOW_CATEG, self.TITLE,
         self.URL, self.WRITE, self.SHWCTG, self.NEW_ENTRY, self.LIST_CHAN, self.CHOICE_CHAN, self.CONFIRM_CHAN, self.ADMIN_REJECT, self.LIST_CTG, self.CONFIRM_CATEG) = range(14)
        self.Title = ""
        self.Url = ""
        self.Cat = ""
        self.xml = xml
        self.path = ""

    def adminCheck(self, bot, update):
        chat_id = update.message.chat_id
        is_admin = chat_id in settings.ADMINS
        if is_admin:
          self.adminButton(bot, update)
          return self.NEW_ENTRY
        else:
          custom_keyboard = [
          ['Cancel']]
          reply_markup = ReplyKeyboardMarkup(
                  custom_keyboard, one_time_keyboard=True)	
          bot.sendMessage(
                  chat_id=update.message.chat_id,
                  text="Only Admin Can Do this Operation press Cancel and /start again",
                   parse_mode='Markdown',
                   reply_markup=reply_markup)
          return self.ADMIN_REJECT
          
    def adminButton(self, bot, update):
        custom_keyboard = [
          ['Add Channel'],
          ['Delete Channel'],
          ['Add Group'],
          ['Delete Group'],
          ['Add Bot'],
          ['Delete Bot'],
          ['Delete Chan Category'],
          ['Delete Grp Category'],
          ['Delete Bot Category'],
          ['Cancel']]
        reply_markup = ReplyKeyboardMarkup(
                  custom_keyboard, one_time_keyboard=True)
        bot.sendMessage(
                  chat_id=update.message.chat_id,
                  text="ആവശ്യമുള്ളത് തിരഞ്ഞെടുക്കുക",
                   parse_mode='Markdown',
                  reply_markup=reply_markup)
        return self.NEW_ENTRY
      
    def addEntry(self, bot, update):
        """
        Conversation: Add
        State: Entry
        Handler: Entry
        Entry point for channel updation
        Prompts channel name
        """
        entryid = update.message.text
        print(entryid)
        if entryid == 'Add Channel':
          self.path = 'file_xml/chan.xml'
        if entryid == 'Add Group':
          self.path = 'file_xml/groups.xml'  
        if entryid == 'Add Bot':
          self.path = 'file_xml/bot.xml'  
          print(self.path)
        custom_keyboard = [['Yes', 'No, add to existing category']]
        reply_markup = ReplyKeyboardMarkup(
            custom_keyboard, one_time_keyboard=True)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Do you want to add to new category",
            reply_markup=reply_markup)

        # TODO: ask if the user wants to add a new cateogry
        # TODO: show category list, and ask the user to choose one
        # TODO: ask user to send channel name
        # TODO: call XMLOps.addCategory(cat_name) to add new category
        # TODO: call XMLOps.addChannel(cat_id, chan) to add new channel
        return self.NEW_CATEG

    def addNewCategory(self, bot, update):
        """
        Conversation: Add
        State: NEW_CATEG
        Handler: RegEx('yes')
        Prompts new category name
        """
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Enter New Category Name")
        return self.SAVE_CATEG

    def addSaveCategory(self, bot, update):
        """
        Conversation: Add
        State: SAVE_CATEG
        Handler: Message("Category Name")
        Accepts category name
        """
        self.cat_name = update.message.text
        self.xml.addCategory(self.cat_name, self.path)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Succesfully Added New Category type OK to continue")
        return self.SHWCTG    
        
       
# Cleaned UP-->

    def showCategory(self, bot, update):
        """
        Conversation: Add
        State: SHOW_CATEG, NEW_CATEG
        Handler: no handler, RegEx('No')
        """
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Selecet required category")
        print(self.path)    
        categories = self.xml.getCategories(self.path)
        keyboard = []
        size = 3
        for i in range(0, len(categories), size):
            list = []
            for j in categories[i:i+size]:
                list.append(InlineKeyboardButton(j[1], callback_data=j[0]))
            keyboard.append(list)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "select category to add channel",
            parse_mode='Markdown',
            reply_markup=reply_markup)
        return self.TITLE

    def addTitle(self, bot, update):
        """
        Conversation: Add
        Accepts channel title to Title variable
        Prompts channel url
        """
        self.query = update.callback_query
        self.cat_id = self.query.data
        
        # self.Cat = update.callback_query.message.text
        bot.sendMessage(chat_id=update.callback_query.message.chat_id,
                        text="Enter The Title of The Channel")
        # ~ self.Title = update.callback_query.message.text
        return self.URL

    def addUrl(self, bot, update):
        """
        Conversation: Add
        Accepts channel url to Url variable
        Prompts submission of new updation
        """
        self.Title = update.message.text
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Enter The channel Url")
        return self.WRITE

    def addWrite(self, bot, update):
        """
        Conversation: Add
        Display updation status (success of failure)
        write new item to the xml
        """
        # dont have a clear idea how to store channel title and url.
        #chan = self.Title + self.Url
        # ~ query = update.callback_query
        # ~ cat_id = query.data
        self.Url = update.message.text
        self.xml.addChannel(int(self.cat_id), self.Title, self.Url, self.path)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Entry added Successfully")
        self.adminButton(bot, update)
        return self.NEW_ENTRY                
                      
    def deleteEntry(self, bot, update):
        """
        Conversation: delete
        Entry point for entry delete conversation
        gets category list from XMLOps.getCategories()
        Prompts category choice
        """
        deleteid = update.message.text
        print(deleteid)
        if deleteid == 'Delete Channel':
          self.path = 'file_xml/chan.xml'
        if deleteid == 'Delete Group':
          self.path = 'file_xml/groups.xml'  
        if deleteid == 'Delete Bot':
          self.path = 'file_xml/bot.xml'  
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="you can delete The Channels here",)
        categories = self.xml.getCategories(self.path)
        keyboard = []
        size = 3
        for i in range(0, len(categories), size):
            list = []
            for j in categories[i:i+size]:
                list.append(InlineKeyboardButton(j[1], callback_data=j[0]))
            keyboard.append(list)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "select category to Delete",
            parse_mode='Markdown',
            reply_markup=reply_markup)
        
        return self.LIST_CHAN

 # TODO: Accept Category ID
 # TODO: Accept Channel ID
 # TODO: Call XMLOps.deleteChannel(cat_id, chan_id)
 # TODO: XMLOps.getCategories() returns categories (ID and Name)
 # TODO: XMLOps.getChannel(cat_id) returns list of channels in the given cat
 # TODO: XMLOps.getChannel(cat_id, chan_id) returns channel info

    def deleteListChannel(self, bot, update):
        """
        Conversation: delete
        gets channel list from XMLOps.getChannels(category_id)
        Prompts channel choice

        """
        bot.sendMessage(chat_id=update.callback_query.message.chat_id,
                        text="enter the id of channel to delete")
        self.query = update.callback_query
        self.cat_id = self.query.data
        chan_list = self.xml.getChannels(int(self.cat_id), self.path)
        bot.sendMessage(
            chat_id=update.callback_query.message.chat_id,
            text=chan_list)
        return self.CHOICE_CHAN

    def deleteChannel(self, bot, update):
        """
        Conversation:  delete
        Prompts chosen channel, whether to delete or not
        """
        self.choice = update.message.text
        selected_chan = self.xml.getChannel(int(self.cat_id), int(self.choice), self.path)
        custom_keyboard = [['Yes', 'Cancel']]
        reply_markup = ReplyKeyboardMarkup(
            custom_keyboard, one_time_keyboard=True)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="are you sure to delete %s channel" % selected_chan,
            reply_markup=reply_markup)
        return self.CONFIRM_CHAN

    def deleteConfirm(self, bot, update):
        """
        Conversation: delete
        Accepts the confirmation to delete
        deletes the channel with XMLOps.deleteChannel(channel_id)
        """
        self.xml.deleteChannel(int(self.cat_id), int(self.choice), self.path)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="The Channel Deleted Successfully")
        self.adminButton(bot, update)
        return self.NEW_ENTRY
        
    def deleteCategoryentry(self, bot, update):
        """
        Conversation: delete
        Entry point for entry delete conversation
        gets category list from XMLOps.getCategories()
        Prompts category choice
        """
        deleteid = update.message.text
        print(deleteid)
        if deleteid == 'Delete Chan Category':
          self.path = 'file_xml/chan.xml'
        if deleteid == 'Delete Grp Category':
          self.path = 'file_xml/groups.xml'  
        if deleteid == 'Delete Bot Category':
          self.path = 'file_xml/bot.xml'  
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="you can delete The Channels here",)
        categories = self.xml.getCategories(self.path)
        keyboard = []
        size = 3
        k=0
        for i in range(0, len(categories), size):
            list = []
            for j in categories[i:i+size]:
                print(j)
                list.append(InlineKeyboardButton(j[1], callback_data=k))
                k+=1
            keyboard.append(list)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "select category to Delete",
            parse_mode='Markdown',
            reply_markup=reply_markup)
        
        return self.LIST_CTG
        
    def deleteCategory(self, bot, update):
        """
        Conversation:  delete
        Prompts chosen channel, whether to delete or not
        """
        self.query = update.callback_query
        self.cat_id = self.query.data
        print (self.cat_id)
        selected_categ = self.xml.getCategory(int(self.cat_id), self.path)
        custom_keyboard = [['Yes', 'Cancel']]
        reply_markup = ReplyKeyboardMarkup(
            custom_keyboard, one_time_keyboard=True)
        bot.sendMessage(
            chat_id=update.callback_query.message.chat_id,
            text="are you sure to delete %s Category" % selected_categ,
            reply_markup=reply_markup)
        return self.CONFIRM_CATEG
        
    def deleteConfirmcateg(self, bot, update):
        """
        Conversation: delete
        Accepts the confirmation to delete
        deletes the channel with XMLOps.deleteChannel(channel_id)
        """
        self.xml.deleteCategory(int(self.cat_id), self.path)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="The Category Deleted Successfully")
        self.adminButton(bot, update)
        return self.NEW_ENTRY        
        
                              
