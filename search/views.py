from django.shortcuts import render,redirect
import requests
from django.conf import settings
from isodate import parse_duration

def home_view(request):
    video_results=[]
    comment_results=[]
    # playlist_url='https://www.googleapis.com/youtube/v3/playlistItems'
    # playlist_id='PLLoUziOB0bCSjRh8F8CJBBb51s2BnNwbt'
    # nextPageToken=None
    # while True:
    #     playlist_params={
    #                     'part':'snippet',
    #                     'key':settings.YOUTUBE_DATA_API_KEY,
    #                     'maxResults': 50,
    #                     'playlistId': playlist_id
    #             }
    #     videos=requests.get(playlist_url,params=playlist_params).json()['items']
    #     for video in videos:
    #         print(video)
    #         print('     ')
    #     nextPageToken=videos['nextPageToken']
       
    #     if not nextPageToken:
    #         break

    if request.method=='POST':
        search_url='https://www.googleapis.com/youtube/v3/search'
        video_url='https://www.googleapis.com/youtube/v3/videos'
        comments_url='https://www.googleapis.com/youtube/v3/commentThreads'
        search_results=[]
        params={
                    'part':'snippet',
                    'q':request.POST.get("search"),
                    'key':settings.YOUTUBE_DATA_API_KEY,
                    'maxResults': 9,
                    'type': 'video',
            }


        results=requests.get(search_url,params).json()['items']

        for result in results:
            search_results.append(result['id']['videoId'])
        
        if request.POST.get('submit')=='lucky':
            return redirect(f'https://www.youtube.com/watch?v={search_results[0]}')


        video_params={
                    'part':'snippet,contentDetails',
                    'key':settings.YOUTUBE_DATA_API_KEY,
                    'maxResults': 9,
                    'id': ','.join(search_results)
            }
        results=requests.get(video_url,video_params).json()['items']

        for result in results:
            video_data={
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url':f'https://www.youtube.com/watch?v={result["id"]}',
                'duration' : parse_duration(result['contentDetails']['duration']),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'] 
            }    
            video_results.append(video_data)

        # for result in search_results:
        #     comments_params={
        #         'key':settings.YOUTUBE_DATA_API_KEY,
        #         'part':'snippet',
        #         'videoId':f'{result}',
        #         'maxResults':5
        #     }
        #     results=requests.get(comments_url,comments_params).json()['items']
        #     for resultz in results:
        #         comments_data={
        #             'text': resultz['snippet']['topLevelComment']['snippet']['textOriginal'],
        #             'author':resultz['snippet']['topLevelComment']['snippet']['authorDisplayName']
        #         }
        #         print(comments_data)
        #         comment_results.append(comments_data)






    context={'video_data':video_results}
    return render(request,'home.html',context)




