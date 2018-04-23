from lxml import etree as et


class XMLOps:

    # ~ def __init__(self):
        # ~ self.xml_path = self.path
        
    def addCategory(self, cat_name, path):
        """
		Add new category to the xml file
		:param cat_name: Category Name
        """
        print (path)
        xml = et.parse(path)
        data = xml.getroot()
        new_cat = et.Element("category", name=cat_name, id=str(len(data)))
        data.append(new_cat)
        file = et.ElementTree(data)
        file.write(path, pretty_print=True)

    def addChannel(self, cat_id, chan_title, chan_url, path):
        """
        Add new channel under the given category
        :param cat_id: Category ID
        :param chan_title: Channel title/name
        :param chan_url: Channel URL/username
        """
        xml = et.parse(path)
        data = xml.getroot()
        new_chan = et.Element("link", title=chan_title)
        new_chan.text = chan_url
        data[cat_id].append(new_chan)
        file = et.ElementTree(data)
        file.write(path, pretty_print=True)

    def getCategories(self, path):
        """
        Get category list from the xml
        :return categories: a list of list containing  id and name of categories
        """
        print (path)
        xml = et.parse(path)
        data = xml.getroot()
        categories = []
        for item in data:
            categories.append([item.attrib.get("id"), item.attrib.get("name")])
        return(categories)

    def getChannels(self, cat_id, path):
        """
        Get Channel list from the xml
        :param cat_id: Category ID
        :return channels: a list of list containing title and link of channels
        """
        xml = et.parse(path)
        data = xml.getroot()
        channels = []
        i=0
        for item in data[cat_id]:
          text = item.attrib.get("title")
          text2 = item.text
          channels.append(str(i)+" "+"👉🏿"+text2+"  "+text)
          i+=1
       
        for k in channels:
          text +="\n"+k
        return(text)

       

# ~ for index, s in enumerate(stocks_list):
    # ~ print index, s


        

    def getChannel(self, cat_id, chan_id, path):
        """
        Get channel info
        :param cat_id: Category ID
        :param chan_id: Channel ID
        :return channel_info: a list containing channel info, title and url
        """
        xml = et.parse(path)
        data = xml.getroot()
        channel = data[cat_id][chan_id]
        channel_info = [channel.attrib.get("title"), channel.text]
        return(channel_info)

    def deleteChannel(self, cat_id, chan_id, path):
        """
        Delete channel
        :param cat_id: Category ID
        :param chan_id: Channel ID
        """
        xml = et.parse(path)
        data = xml.getroot()
        del(data[cat_id][chan_id])
        file = et.ElementTree(data)
        file.write(path, pretty_print=True)
        
    def deleteCategory(self, cat_id, path):
        """
        Delete channel
        :param cat_id: Category ID
        """
        xml = et.parse(path)
        data = xml.getroot()
        del(data[cat_id])
        file = et.ElementTree(data)
        file.write(path, pretty_print=True)
        
    def getCategory(self, cat_id, path):
        """
        Get category list from the xml
        :return categories: a list of list containing  id and name of categories
        """
        print (path)
        xml = et.parse(path)
        data = xml.getroot()
        categ = data[cat_id]
        categ_info = [categ.attrib.get("name")]
        return(categ_info)
                   
