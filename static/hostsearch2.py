# -*- coding: utf-8 -*-
import json
import re
import os
import urllib
import csv
import subprocess
from subprocess import Popen, PIPE, check_call

mobtrackers = [
        'Inmobi', 'Mopub', 'Facebook', 'Chartboost',
        'Crashlytics', 'Heyzap', 'Applovin',
        'Unitytechnologies', 'Vungle', 'Fyber',
        'Millenialmedia', 'Ironsource', 'Tapjoy',
        'Flurry', 'Google', 'Bitstadium', 'Presage',
        'Comscore', 'Umeng', 'Tencent', 'Nexage',
        'Mixpanel', 'Appboy', 'Yandex', 'Kochava',
        'Urbanairship', 'Daum', 'Milkman', 'Playhaven',
        'Umeng', 'Mail.Ru', 'Newrelic', 'Admob',
        'Moat', 'Smaato', 'Admarvel', 'Appodeal',
        'Cauley', 'Revmob', 'Adbuddiz', 'Igaworks',
        'Nativex', 'Smartadserver', 'Mobfox',
        'Pubnative', 'Hyprmx', 'Pingstart', 'Tune',
        'Baidu', 'Swrve', 'Tnkfactory', 'Appnext',
        'Tencent',
]

webtrackers = [
        'Google', 'Doubleclick', 'Facebook',
        'Cloudfront', 'Scorecardresearch', 'Appnexus',
        'Twitter', 'Amazon', 'Criteo', 'Yahoo',
        'Oracle', 'Quantcast', 'Iponweb', 'Adobe',
        'Openx', 'Ghostery', 'Rubicon', 'Bluekai',
        'Cloudflare', 'Liveramp', 'The Nielsen Company',
        'Demdex', 'Truste', 'Newrelic',
        'Integral Ad Science', 'Adsrvr', 'Moatads',
        'Pubmatic', 'Turn', 'Indexchange',
        'Doubleverify', 'Mathtag', 'Chartbeat',
        'Optimizely', 'Youtube', 'Tapad', 'Exelate',
        'Targus', 'Lotame', 'Sizmek', 'Iasds',
        'Neustar', 'Jquery', 'Krxd', 'Adroll',
        'Brightroll', 'Audiencescience', 'Bootstrap',
        'Rocketfuel', 'Dataxu', 'Tubemogul',
        'Microsoft', 'Yandex', 'Conversant',
        'Videology', 'Flashtalking', 'Akamai',
        'Adap.Tv', 'Magnetic', 'Dstillery', 'Baidu',
        'Smartadserver', 'Taboola', 'H&R Block',
        'Tealium', 'Convertro', 'MSN', 'Linkedin',
        'Mookie1', 'Contextweb', 'Liverail', 'Yadro',
        'Bug', 'Chango', 'Conversant Llc', 'Trueffect',
        'Signal-Privacy', 'Crazy Egg', 'Drawbridge Inc',
        'Sovrn', 'Ovh', 'Exponential', 'Yieldoptimizer',
        'Spotxchange', 'Owneriq', 'Insightexpress',
        'Adform', 'Automattic', 'Disqus', 'Outbrain',
        'Flipps', 'Centromedia', 'Ignitionone',
        'Skimlinks', 'Simpli.Fi', 'Wordpress',
        'Openx Technologies', 'Ensighten',
        'Visual Website Optimizer', 'Rhythmone',
        'Mixpanel', 'Sonobi', 'Hotjar', 'Voicefive',
        'Gssprt', 'At Internet', 'Ml314', 'Radiumone',
        'Parsely', 'Improve Digital Bv', 'Gumgum',
        'Amgdgt', 'Effective Measure', 'Pinterest',
        'Vk', 'Adition', 'Exoclick', 'Ixi Corporation',
        'Nugg.Ad', 'Umeng', 'Alibaba', 'Marketo',
        'Gskinner', 'Gigya', 'Tns', 'Eq Works',
        'Cxense Asa', 'Steelhouse', 'Yieldlab',
        '33Across', 'Mail.Ru', 'Pingdom Ab',
        'Smart Adserver', 'Brightcove', 'Postrelease',
        'Adriver', 'Pagefair', 'Microad',
        'Marin Software', 'Collective', 'Trafficjunky',
        'Pixalate', 'Demandbase', 'Yieldbot',
        'Visualdna', 'Ioam', 'Signal', 'Shopzilla',
        'Sharethrough', 'Rambler', 'Clicktale',
        "Sociomantic", 'Datonics', 'Run', 'Myspace',
        'Taobao', 'Adgear Technologies', 'Sharethis',
        'Mybuys', 'Stroeer Media',
        'The Mcgraw-Hill Companies', 'Vizury', 'Abc',
        'Dyn', 'Longtail Ad Solutions', 'Netseer',
        'Smaato', 'The Adex Gmbh', 'Adblade',
        'Mxptint', 'Maxymiser', 'Admeta', 'Mcro',
        'Sourcepoint Technologies', 'Yieldmanager',
        'Rfihub', 'Bounce Exchange', 'Wtp',
        'Convertmedia', 'Rackspace Us', 'Eyeview',
        'Qualtrics', 'Intent Iq', 'Stickyads.Tv',
        'Soasta', 'Cedexis Inc', 'Weborama',
        'Invite Media', 'Histats', 'Statcounter',
        'Paypal', 'Bidr', 'Springserve', 'Yahoo',
        'Nexstar Broadcasting', 'Triplelift',
        'Polar', 'Adelphic Inc', 'Deep Forest Media',
        'Cedexis', 'Richrelevance', 'Resonate',
        'Impact-Ad', 'Jivox', 'Mediade',
        'Liveperson', 'Zedo', 'Yabidos', 'Adfox',
        'Fout', 'Switch', 'Navegg S.A.', 'Adsnative',
        'Eyeota Limited', 'Jsdelivr',
        'Consumerinfo.Com', 'Brandscreen Pty Ltd',
        'Mythings', 'Polar Mobile Group',
        'Answercloud', 'Komoona', 'Admeta',
        'Meltdsp', 'Appier Inc', 'Netdna',
        'Budgetedbauer', 'Gfk', 'Bidtheatre',
        'Research Now', 'Undertone Networks',
        'Viglink', 'Adbrain', 'Adstir', 'Sailthru',
        'Vimeo', 'Mediametrie', 'Livefyre',
        'Mediaforge', 'Webklipper', 'Tencent',
        'Ib-Ibi',
]

trackers = set(mobtrackers)|set(webtrackers)
obj  = json.load(open('../mitm_out/company_details.json'))
toptrackers = obj.copy()
for tracker in trackers:
	if toptrackers[tracker]["id"] not in trackers:
		toptrackers.pop(tracker)

for tracker in toptrackers:
	domains = toptrackers[tracker]["domains"]
	fulldomains = filter(None, domains)
	toptrackers[tracker]["domains"] = fulldomains

def getDomainCo(host):
	for tracker in toptrackers:
		for domain in toptrackers[tracker]["domains"]:
			if domain in host:
				return toptrackers[tracker]["id"]

# open the text file which is output of grep, record any recognised domains in the output.json file

def recordTrackers(apkname, urlsname):
	urls = open(urlsname).read()
	trackers = []
	for tracker in toptrackers:
		for domain in toptrackers[tracker]["domains"]:
			if str(domain) in urls:
				trackers.append(str(tracker))
	trackers = list(set(trackers))
	print trackers
	irrelevant = ["app", "identity", "n/a", "other", "", "library"]
	for tracker in trackers:
		for cat in irrelevant:
			if (obj[tracker]["typetag"] == cat):
				trackers.remove(tracker)
				print 'removed %s because %s' % (tracker, obj[tracker]["typetag"])
	print trackers
	line = '"%s": %s,' % (apkname, json.dumps(trackers))
	output.write(line)

# # toptrackers = getPopTrackers()

output = open('output_testing.json', 'a')

directory = '../../apks/top/'

selectedApps1 = ['Cam.SILENT', 'Com.sktelecom.minit', 'Game.NDK', 'Game.SpeedCar2', 'Game.SpeedMoto', 'HinKhoj.Dictionary', 'SSGlobal.pack', 'Uxpp.UC', 'acogame.duoihinhbatchu', 'afzkl.development.mVideoPlayer', 'air.BRFree', 'air.BattleofZombies', 'air.BeautyCenter', 'air.FSWeddingandroid', 'air.FashionStudioPromDressDesign', 'air.FlashStuntZ', 'air.Hangman20', 'air.KittyPrincessHairSalon', 'air.KuninNikolay.RailwayBridge.Free', 'air.MSPMobile', 'air.QCHMOBILE', 'air.air.com.jessoft.flvplayer.FLVPlayer', 'air.au.com.metro.DumbWaysToDie', 'air.balletdancer', 'air.beingfashiondesigner', 'air.br.com.bitlabs.FLVPlayer', 'air.br.com.bitlabs.VideoPlayer', 'air.byss.mobi.instaweatherfree', 'air.cbn.superbook.bible.app.android', 'air.charmycleanup', 'air.coloringGamespaceship', 'air.com.CleanUpHairSalon', 'air.com.CreativeTech.LogicPuzzles', 'air.com.FunPlusMore.RebuildACar', 'air.com.PopcornMaker', 'air.com.SuperCarWash', 'air.com.adobe.connectpro', 'air.com.arpamedia.preschoollearningprincessfun', 'air.com.arpamedia.princessmermaidsalon', 'air.com.arpamedia.princessspasalonfrozen', 'air.com.axisentertainment.babyhazelgingerbreadhouse', 'air.com.befunky.BeFunkyPhotoEditor', 'air.com.bitrhymes.bingo', 'air.com.blake.postcardAppAndroid', 'air.com.cocosapps.HandDoctorTreatment', 'air.com.cocosapps.LittleCuteBabyCare', 'air.com.cocosapps.NurseBathing', 'air.com.crescentmoongames.optical', 'air.com.devgameapp.PrincessMakeoverSalon', 'air.com.differencegames.threepyramidtripeaksfree', 'air.com.dressupone.parishairsalon', 'air.com.dressupone.thebadstudent', 'air.com.eastsidegamestudio.PFGrassRoots', 'air.com.enjoycookinggames.thumbelinagirldressup', 'air.com.fde.kungfupandaandroid', 'air.com.feerik.eredanbattle', 'air.com.fictionlabs.apobondoehni', 'air.com.flaregames.wordon', 'air.com.games2win.fabtattooartist', 'air.com.generamobile.colormaniaguess', 'air.com.gerwinsoftware.superbuzzer', 'air.com.goodgamestudios.shadowkings', 'air.com.igg.perfectbraidhairdresser', 'air.com.izmo.gercekgiydirme', 'air.com.kitchenscramble.goo', 'air.com.microcookinggames.icecreamconecupcake', 'air.com.mobestmedia.letsescape', 'air.com.mobigrow.canyouescape2', 'air.com.mobigrow.canyouescapeadventure', 'air.com.mobigrow.canyouescapetower', 'air.com.netfunmedia.fairytaleprincesshairsalon', 'air.com.netfunmedia.mermaidprincessspasalon', 'air.com.nextdifferencegames.AdventureHiddenobjects', 'air.com.nextdifferencegames.MysteryHiddenStory', 'air.com.oak.OddSocksMob', 'air.com.officemax.magicmirror.ElfYourSelf', 'air.com.oranginalplan.weaphonesfree', 'air.com.oranginalplan.weaphonesvol2free', 'air.com.oranginalplan.weaphonesww2free', 'air.com.peppapig.activitymaker', 'air.com.playtika.slotomania', 'air.com.sgn.cookiejam.gp', 'air.com.smileydressup.fairydressup', 'air.com.sticksports.sticktennis', 'air.com.tamalaki.homemakeovertwo.gp', 'air.com.tedven.youmustescape2', 'air.com.tensquaregames.letsfish', 'air.com.turbonuke.dirtbikeracing', 'air.com.tutotoons.app.babyhouse', 'air.com.tutotoons.app.misspastrychef', 'air.com.tutotoons.app.sweetbabygirl', 'air.com.ubisoft.csi.HiddenCrimes', 'air.com.zyncstudio.PoolBabyCare', 'air.cz.cfc.androidgp.AbbyBasicSkillsLite', 'air.endlessescape', 'air.fashionstudio', 'air.fisherprice.com.Puppy', 'air.fisherprice.com.animalsounds', 'air.fisherprice.com.shapesAndColors', 'air.isporch', 'air.kazi', 'air.meez.app.Towers', 'air.mwe.cookingcuteheartcupcakes', 'air.mwe.cookingsoftiesugarcookies', 'air.mwe.supermacaroonscookinggames', 'air.net.m7g7.MermaidBathing', 'air.net.ozonedevelopment.AbbysHomeLaundry', 'air.net.ozonedevelopment.BabyGirlsLaundry', 'air.net.ozonedevelopment.CutePuppyCaring', 'air.net.purplestudio.FarmingPrincess', 'air.nn.mobile.app.main', 'air.org.axisentertainment.BabyHazelBathroomHygiene', 'air.org.axisentertainment.BabyHazelFarmTour', 'air.org.axisentertainment.BabyHazelFlowerGirl', 'air.org.axisentertainment.BabyHazelGardeningTime', 'air.org.axisentertainment.BabyHazelGoesSick', 'air.org.axisentertainment.BabyHazelKitchenTime', 'air.org.axisentertainment.BabyHazelLegInjury', 'air.org.axisentertainment.BabyHazelMischiefTime', 'air.org.axisentertainment.BabyHazelMothersDay', 'air.org.axisentertainment.BabyHazelNewbornBaby', 'air.org.axisentertainment.BabyHazelPreschool', 'air.org.axisentertainment.BabyHazelRoyalBath', 'air.org.axisentertainment.BabyHazelSkinTrouble', 'air.org.axisentertainment.BabyHazelStomachCare', 'air.org.axisentertainment.BabyHazelSummerFun', 'air.org.axisentertainment.BabyHazelSwimmingTime', 'air.org.axisentertainment.SofysBabyShoppe', 'air.princessroomdecoration', 'air.prof']
selectedApps = ['cc.dict.dictcc', 'com.dictionary', 'com.dictionary.bn', 'com.duckduckgo.mobile.android', 'com.ebooks.ebookreader', 'com.goodreads', 'com.merriamwebster', 'com.microsoft.bing', 'com.oup.gab.odquicksearch', 'com.scribd.app.reader0', 'com.tfd.mobile.TfdSearch', 'com.urbandictionary.android', 'org.freedictionary', 'org.leo.android.dict', 'org.wikipedia', 'com.cisco.webex.meetings', 'com.citrix.saas.gotowebinar', 'com.citrixonline.android.gotomeeting', 'com.fiverr.fiverr', 'com.indeed.android.jobsearch', 'com.jobkorea.app', 'com.timesgroup.timesjobs', 'com.monster.android.Views', 'naukriApp.appModules.login', 'net.infojobs.mobile.android', 'net.slideshare.mobile', 'com.crunchyroll.crmanga', 'com.dccomics.comics', 'com.marvel.comics', 'jp.comico', 'com.cinemex', 'com.eventbrite.attendee', 'com.imbc.mini', 'com.imdb.mobile', 'com.mobile.ign', 'com.netflix.mediaclient', 'com.ninegag.android.app', 'com.sonyliv', 'com.tudou.xoom.android', 'com.vimeo.android.videoapp', 'com.wikia.singlewikia.gta', 'com.wwe.universe', 'de.tvspielfilm', 'fr.m6.m6replay', 'tv.pps.mobile', 'au.com.nab.mobile', 'br.com.bb.android', 'br.com.gabba.Caixa', 'com.aastocks.dzh', 'com.akbank.android.apps.akbank_direkt', 'com.bca', 'com.bccard.mobilecard', 'com.bradesco', 'com.garanti.cepsubesi', 'com.hanaskcard.app.touchstamp', 'com.htsu.hsbcpersonalbanking', 'com.kbcard.cxh.appcard', 'com.kbstar.kbbank', 'com.paypal.android.p2pmobile', 'com.santander.app', 'com.sbi.SBIFreedomPlus', 'com.snapwork.hdfc', 'com.vakifbank.mobile', 'com.wf.wellsfargomobile', 'com.wooribank.pib.smart', 'com.wooricard.smartapp', 'com.yahoo.mobile.client.android.finance', 'fr.creditagricole.androidapp', 'gov.irs', 'info.percentagecalculator', 'pl.mbank', 'ru.tcsbank.mcp', 'se.bankgirot.swish', 'ua.privatbank.ap24', 'au.com.realestate.app', 'com.application.zomato', 'com.appsphere.innisfreeapp', 'com.aufeminin.marmiton.activities', 'com.cookpad.android.activities', 'com.done.faasos', 'com.dubizzle.horizontal', 'com.frenys.verdadoreto', 'com.global.foodpanda.android', 'com.gumtree.android', 'com.hotornot.app', 'com.houzz.app', 'com.ikea.catalogue.android', 'com.inditex.pullandbear', 'com.inditex.zara', 'com.kt.ollehfamilybox', 'com.move.realtor', 'com.openrice.snap', 'com.redfin.android', 'com.restaurant.mobile', 'com.rightmove.android', 'com.scripps.android.foodnetwork', 'com.trulia.android', 'com.trulia.android.rentals', 'com.zoopla.activity', 'de.mcdonalds.mcdonaldsinfoapp', 'de.pixelhouse', 'ecowork.seven', 'fr.disneylandparis.android', 'jp.co.recruit.mtl.android.hotpepper', 'kr.co.station3.dabang', 'com.AnatomyLearning.Anatomy3DViewer3', 'com.anghami', 'com.bandsintown', 'com.gaana', 'com.gaana.oldhindisongs', 'com.jangomobile.android', 'com.kugou.android', 'com.mixcloud.player', 'com.musixmatch.android.lyrify', 'com.spotify.music', 'com.vevo', 'de.radio.android', 'uk.co.sevendigital.android', 'com.abc.abcnews', 'com.andrewshu.android.reddit', 'com.backelite.vingtminutes', 'com.cnn.mobile.android.phone', 'com.dailymail.online', 'com.elpais.elpais', 'com.et.reader.activities', 'com.foxnews.android', 'com.google.android.apps.genie.geniewidget', 'com.hespress.android', 'com.huffingtonpost.android', 'com.ideashower.readitlater.pro', 'com.idmedia.android.newsportal', 'com.indomedia.tabpulsa', 'com.issuu.android.app', 'com.july.ndtv', 'com.makonda.blic', 'com.mobilesrepublic.appy', 'com.newspaperdirect.pressreader.android', 'com.newspaperdirect.pressreader.android.hc', 'com.nextmedia', 'com.nextmediatw', 'com.nextradiotv.bfmtvandroid', 'com.now.newsapp', 'com.nytimes.android', 'com.sumarya', 'com.tilab', 'com.Time', 'com.toi.reader.activities', 'com.usatoday.android.news', 'com.zing.znews', 'com.zinio.mobile.android.reader', 'com.zumobi.msnbc', 'de.cellular.focus', 'de.cellular.tagesschau', 'de.heute.mobile', 'de.lineas.lit.ntv.android', 'fr.lepoint.android', 'fr.playsoft.android.tv5mondev2', 'fr.playsoft.lefigarov3', 'id.co.babe', 'in.AajTak.headlines', 'net.aljazeera.english', 'net.trikoder.android.kurir', 'org.detikcom.rss', 'ru.rian.reader', 'se.sr.android', 'uk.co.economist', 'blibli.mobile.commerce', 'br.com.dafiti', 'com.acerstore.android', 'com.alibaba.aliexpresshd', 'com.appnana.android.giftcardrewards', 'com.asda.android', 'com.asos.app', 'com.ebay.kleinanzeigen', 'com.ebay.mobile', 'com.elevenst', 'com.elevenst.deals', 'com.etsy.android', 'com.flipkart.android', 'com.geomobile.tiendeo', 'com.goldtouch.ct.yad2', 'com.groupon', 'com.hmallapp', 'com.hnsmall', 'com.homeshop18.activity', 'com.interpark.shop', 'com.jabong.android', 'com.lamoda.lite', 'com.mercadolibre', 'com.mobisoft.morhipo', 'com.myntra.android', 'com.opensooq.OpenSooq', 'com.sahibinden', 'com.shopclues', 'com.shopping.limeroad', 'com.shpock.android', 'com.snapdeal.main', 'com.souq.app']

# selected apps version

from glob import glob
from os import path

#for filename in selectedApps1:
#	fullpath = path.join(directory, filename)
for fullpath in glob(path.join(directory, '*.apk')):
	fullpath = '.'.join(fullpath.split('.')[:-1])
	filename = path.basename(fullpath)
	print path.basename(fullpath)
	print fullpath
	os.system("java -jar apktool.jar d %s.apk" % fullpath)
	unpackedname = filename.rsplit( ".", 1 )[ 0 ]
	urlsname = "%s_urls.txt" % filename
	os.system('grep -Er "https?://[^ >]+" %s > %s' % (filename, urlsname))
#	os.system('grep -Er "iponweb" %s > %s' % (filename, urlsname))
#	os.system("grep -Er %s %s > %s" % ("http://\K[^']+", filename, urlsname))
	recordTrackers(filename,urlsname)
	os.system("rm -r %s" % filename)
	os.system("rm %s" % urlsname)
