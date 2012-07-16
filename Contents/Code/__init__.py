ART 			= "art-default.jpg"
ICON 			= "icon-default.png"
ICON_MORE		= "icon-more.png"
NAME 			= L("Title")

BASEURL = "http://www.pu.nl"
PUTVURL = BASEURL + "/pu-tv"
####################################################################################################
def Start():

	Plugin.AddPrefixHandler("/video/pu-tv", MainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")

	ObjectContainer.title1 = NAME
	ObjectContainer.view_group = "List"
	ObjectContainer.art = R(ART)
	
	VideoClipObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) Gecko/20100101 Firefox/13.0.1"


####################################################################################################
def MainMenu(page=0):
	oc = ObjectContainer()
	
	pagestr=str(page)
	url = PUTVURL + "?page=" + pagestr

	for clip in HTML.ElementFromURL(url).xpath("//div[contains(@class ,'PU-TV')]"):
		clip_link 	= BASEURL + clip.xpath(".//div[@class='field_image']/a")[0].get("href")
		clip_thumb 	= clip.xpath(".//div[@class='field_image']/a/img")[0].get("src")
		clip_title	= clip.xpath(".//div[@class='views-field views-field-title']/span/a")[0].text
		try:
			clip_desc	= clip.xpath("./text()[normalize-space()]")[0]
		except:
			clip_desc	= ""
	
		oc.add(VideoClipObject(
			url = clip_link,
			title = clip_title,
			summary = clip_desc,
			thumb=Resource.ContentsOfURLWithFallback(url=clip_thumb, fallback=ICON)
		))

	if len(oc) == 0:
		return MessageContainer(L('NoVideo'))
		
	else:
		if len(clip.xpath('//li[@class="pager-next"]')) > 0:
			oc.add(DirectoryObject(key=Callback(MainMenu, page=page+1), title=L('More'), thumb=R(ICON_MORE)))
	
	return oc