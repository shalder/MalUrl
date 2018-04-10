from urlparse import urlparse
import re
import urllib2
import urllib
from xml.dom import minidom
import csv
import pygeoip

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

nf=-1

def url_tokenize(url):

        tokenized_word=re.split('\W+',url)
        num_element = 0
        sum_of_element=0
        largest=0
        for element in tokenized_word:
                l=len(element)
                sum_of_element+=l
                if l>0:                                        ## for empty element exclusion in average length
                        num_element+=1
                if largest<l:
                        largest=l
        try:
            return [float(sum_of_element)/num_element,num_element,largest]
        except:
            return [0,num_element,largest]


def find_ele_with_attribute(dom,ele,attribute):
    for subelement in dom.getElementsByTagName(ele):
        if subelement.hasAttribute(attribute):
            return subelement.attributes[attribute].value
    return nf
        

def sitepopularity(host):

        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
        #print xmlpath
        try:
            xml= urllib2.urlopen(xmlpath)
            dom =minidom.parse(xml)
            rank_host=find_ele_with_attribute(dom,'REACH','RANK')
            #country=find_ele_with_attribute(dom,'REACH','RANK')
            rank_country=find_ele_with_attribute(dom,'COUNTRY','RANK')
            return [rank_host,rank_country]

        except:
            return [nf,nf]


def get_sec_sensitive_words(tokenized_words):

    sec_sen_words=['confirm', 'account', 'banking', 'secure', 'viagra', 'rolex', 'login', 'signin']
    count=0
    for element in sec_sen_words:
        if(element in tokenized_words):
            count= count + 1;

    return count

def url_has_exe(url):
    if url.find('.exe')!=-1:
        return 1
    return 0

def Check_IPaddress(tokens_words):

    cnt=0;
    for ele in tokens_words:
        if unicode(ele).isnumeric():
            cnt+=1
        else:
            if cnt>=4 :
                return 1
            else:
                cnt=0;
    if cnt>=4:
        return 1
    return 0
    
def getASN(host):
    try:
        g = pygeoip.GeoIP('GeoIPASNum.dat')
        asn=int(g.org_by_name(host).split()[0][2:])
        return asn
    except:
        return  nf


def web_content_features(url):
    webfeatures={}
    total_count=0
    try:        
        source_code = str(opener.open(url))
        #print source_code[:500]

        webfeatures['src_html_cnt']=source_code.count('<html')
        webfeatures['src_hlink_cnt']=source_code.count('<a href=')
        webfeatures['src_iframe_cnt']=source_code.count('<iframe')
        #suspicioussrc_ javascript functions count

        webfeatures['src_eval_cnt']=source_code.count('eval(')
        webfeatures['src_escape_cnt']=source_code.count('escape(')
        webfeatures['src_link_cnt']=source_code.count('link(')
        webfeatures['src_underescape_cnt']=source_code.count('underescape(')
        webfeatures['src_exec_cnt']=source_code.count('exec(')
        webfeatures['src_search_cnt']=source_code.count('search(')
        
        for key in webfeatures:
            if(key!='src_html_cnt' and key!='src_hlink_cnt' and key!='src_iframe_cnt'):
                total_count=total_count + webfeatures[key]
        webfeatures['src_total_jfun_cnt']=total_count
    
    except Exception, e:
        print "Error"+str(e)+" in downloading page "+url 
        default_value=nf
        
        webfeatures['src_html_cnt']=default_value
        webfeatures['src_hlink_cnt']=default_value
        webfeatures['src_iframe_cnt']=default_value
        webfeatures['src_eval_cnt']=default_value
        webfeatures['src_escape_cnt']=default_value
        wfeatures['src_link_cnt']=default_value
        webfeatures['src_underescape_cnt']=default_value
        webfeatures['src_exec_cnt']=default_value
        webfeatures['src_search_cnt']=default_value
        webfeatures['src_total_jfun_cnt']=default_value    
    
    return webfeatures

def safebrowsing(url):
    api_key = "ABQIAAAA8C6Tfr7tocAe04vXo5uYqRTEYoRzLFR0-nQ3fRl5qJUqcubbrw"
    name = "URL_check"
    ver = "1.0"

    req = {}
    req["client"] = name
    req["apikey"] = api_key
    req["appver"] = ver
    req["pver"] = "3.0"
    req["url"] = url #change to check type of url

    try:
        params = urllib.urlencode(req)
        req_url = "https://sb-ssl.google.com/safebrowsing/api/lookup?"+params
        res = urllib2.urlopen(req_url)
        # print res.code
        # print res.read()
        if res.code==204:
            # print "safe"
            return 0
        elif res.code==200:
            # print "The queried URL is either phishing, malware or both, see the response body for the specific type."
            return 1
        elif res.code==204:
            print "The requested URL is legitimate, no response body returned."
        elif res.code==400:
            print "Bad Request The HTTP request was not correctly formed."
        elif res.code==401:
            print "Not Authorized The apikey is not authorized"
        else:
            print "Service Unavailable The server cannot handle the request. Besides the normal server failures, it could also indicate that the client has been throttled by sending too many requests"
    except:
        return -1

def feature_extract(url_input):

        Feature={}
        tokens_words=re.split('\W+',url_input)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
        #print tokens_words,len(tokens_words)

        #token_delimit1=re.split('[./?=-_]',url_input)
        #print token_delimit1,len(token_delimit1)

        obj=urlparse(url_input)
        host=obj.netloc
        path=obj.path

        Feature['URL']=url_input

        Feature['rank_host'],Feature['rank_country'] =sitepopularity(host)

        Feature['host']=obj.netloc
        Feature['path']=obj.path

        Feature['Length_of_url']=len(url_input)
        Feature['Length_of_host']=len(host)
        Feature['No_of_dots']=url_input.count('.')

        Feature['avg_token_length'],Feature['token_count'],Feature['largest_token'] = Tokenise(url_input)
        Feature['avg_domain_token_length'],Feature['domain_token_count'],Feature['largest_domain'] = Tokenise(host)
        Feature['avg_path_token'],Feature['path_token_count'],Feature['largest_path'] = Tokenise(path)

        Feature['sec_sen_word_cnt'] = Security_sensitive(tokens_words)
        Feature['IPaddress_presence'] = Check_IPaddress(tokens_words)
        
        # print host
        # print getASN(host)
        # Feature['exe_in_url']=exe_in_url(url_input)
        Feature['ASNno']=getASN(host)
        Feature['safebrowsing']=safebrowsing(url_input)
        """wfeatures=web_content_features(url_input)
        
        for key in wfeatures:
            Feature[key]=wfeatures[key]
        """
        #debug
        # for key in Feature:
        #     print key +':'+str(Feature[key])
        return Feature
