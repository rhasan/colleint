from pydelicious import get_popular,get_userposts,get_urlposts
import time

def initializeUserDict(tag,count=5):
  user_dict={}
  # get the top count' popular posts
  for p1 in get_popular(tag=tag)[0:count]:
    # find all users who posted this
    for p2 in get_urlposts(p1['url']):
      user=p2['user']
      user_dict[user]={}
  return user_dict


def fillItems(user_dict):
  all_items={}
  # Find links posted by all users
  for user in user_dict:
    for i in range(3):
      try:
        posts=get_userposts(user)
        break
      except:
        print "Failed user "+user+", retrying"
        time.sleep(4)
    for post in posts:
      url=post['url']
      user_dict[user][url]=1.0
      all_items[url]=1
  
  # Fill in missing items with 0
  for ratings in user_dict.values():
    for item in all_items:
      if item not in ratings:
        ratings[item]=0.0

# ch2 exercise 2
# build a dataset of tags and items
# this method returns a dictionary with tags and accociated urls for thos tags given a list of users

def getItemsTags(user_dict,n=5):
  urltag_dict = {}
  all_tags = {}
  count = 0
  url_limit_per_user = 5
  break_flag = 0
  for user in user_dict:
    if(count==n):
      break_flag = 1
      break
    count += 1
    url_count = 0
    for url in user_dict[user]:
      #print "Url["+url+"]"
      if(url_count>url_limit_per_user):
        break;
      url_count += 1
      retry_count = 0
      for i in range(3):
        try:
          posts=get_urlposts(url)
          break
        except:
          print "Failed url "+url+", retrying"
          time.sleep(4)
          retry_count +=1
      if(retry_count>=3):
        continue
      for post in posts[0:10]:
        #print post['tags']
        tag_count = 0
        for tag in post['tags'].split():
          #print "working with tag %s" % tag
          all_tags[tag]=1
          urltag_dict.setdefault(url,{})
          urltag_dict[url][tag]=1.0
          tag_count+=1
        #print "\\ttags %d" %tag_count
      #break  
  print "Collecting tags finished"
  # Fill in missing tags with 0
  for tags_ratings in urltag_dict.values():
    for tag in all_tags:
      if tag not in tags_ratings:
        tags_ratings[tag]=0.0
          

  return urltag_dict

  
