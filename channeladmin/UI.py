import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram import InlineKeyboardButton


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
         self.URL, self.WRITE) = range(6)
        self.Title = ""
        self.Url = ""
        self.Cat = ""
        self.xml = xml

    def addEntry(self, bot, update):
        """
        Conversation: Add
        State: Entry
        Handler: Entry
        Entry point for channel updation
        Prompts channel name
        """
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
        # cat_name = update.message.text
        # self.xml.addCategory(cat_name)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='New category Added')
        self.showCategory(bot, update)
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
        categories = self.xml.getCategories()
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
        # self.Cat = update.callback_query.message.text
        bot.sendMessage(chat_id=update.callback_query.message.chat_id,
                        text="Enter The Title of The Channel")
        # self.Title = update.message.text
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
        self.Url = update.message.text
        return self.WRITE

    def addWrite(self, bot, update):
        """
        Conversation: Add
        Display updation status (success of failure)
        write new item to the xml
        """
        # dont have a clear idea how to store channel title and url.
        #chan = self.Title + self.Url
        query = update.callback_query
        cat_id = query.data
        self.xml.addChannel(cat_id, self.Title, self.Url)
        bot.sendMessage(chat_id=update.callback_query.message.chat_id,
                        text="channel added Successfully")
    def deleteEntry(self, bot, update):
        """
        Conversation: delete
        Entry point for entry delete conversation
        gets category list from XMLOps.getCategories()
        Prompts category choice
        """
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="you can delete The Channels here",)
        categories = self.xml.getCategories()
        keyboard = []
        size = 3
        for i in range(0, len(categories), size):
            list = []
            for j in categories[i:i+size]:
                list.append(j)
            keyboard.append(list)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "select category to delete channel",
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
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="enter the id of channel to delete")
        query = update.callback_query
        cat_id = query.data
        chan_list = getChannels(cat_id)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=chan_list)
        return self.CHOICE_CHAN

    def deleteChannel(self, bot, update):
        """
        Conversation:  delete
        Prompts chosen channel, whether to delete or not
        """
        choice = update.message.text
        selected_chan = XMLops.getChannel(cat_id, choice)
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
        deleteChannel(cat_id, choice)
        bot.SendMessage(chat_id=update.message.chat_id,
                        text="The Channel Deleted Successfully")
