from EasyLogin import EasyLogin
from pprint import pprint
from config import cookiestring

a=EasyLogin()

def getone(id):
    page = a.get("https://www.zhihu.com/api/v4/questions/{}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20".format(id),o=True,cookiestring=cookiestring).json()
    data=[]
    data.extend(page["data"])
    while not page["paging"]["is_end"]:
        page = a.get(page["paging"]["next"],o=True,cookiestring=cookiestring).json()
        data.extend(page["data"])
    pprint(data)
getone("54595683")