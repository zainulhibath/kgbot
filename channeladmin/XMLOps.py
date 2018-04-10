from lxml import etree as et


class XMLOps:

    def __init__(self):
        self.xml_path = "file_xml/chan.xml"

    def addCategory(self, cat_name):
        """
        Add new category to the xml file
        :param cat_name: Category Name
        """
        xml = et.parse(self.xml_path)
        data = xml.getroot()
        new_cat = et.Element("category", name=cat_name, id=str(len(data)))
        data.append(new_cat)
        file = et.ElementTree(data)
        file.write(self.xml_path, pretty_print=True)

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

    def deleteChannel(self, cat_id, chan_id):
        """
        Delete channel
        :param cat_id: Category ID
        :param chan_id: Channel ID
        """
        xml = et.parse(self.xml_path)
        data = xml.getroot()
        del(data[cat_id][chan_id])
        file = et.ElementTree(data)
        file.write(self.xml_path, pretty_print=True)
