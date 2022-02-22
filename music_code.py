import youtubesearchpython as yt# https://github.com/alexmercerind/youtube-search-python/blob/main/README.md
import random


# def vid_search_top(artist, limit): # OLD BUG
#     """finds the top songs of an artist on youtube"""
#     videos, count, songs = yt.VideosSearch(artist), 0, []
#     while count != -1:# using -1 to break the loop
#         for song in videos.result()['result']:
#             if int(song['duration'].split(":")[0]) < 10 and len(song['duration'].split(":")) < 3:# removes albums
#                 current_details = {'id': song['id'],
#                                    'title': song['title'],
#                                    'duration': song['duration'],
#                                    'channel': song['channel']['link']}
#                 songs.append(current_details); count += 1
#                 if count == limit:# once the given amount of songs has been added
#                     count = -1; break# stop adding songs
#         if count % 16 == 0:# 16 results are returned for each ".next()", so after 16 songs, load the next 16
#             videos.next()
#     return songs# return a list of dicts


def check_for_duplicates(arr):
    """Check if given list contains any duplicates"""
    expected = len(arr)
    actual = len(set(arr))
    if expected == actual:
        return False
    else:
        return True


def vid_search_top(artist, limit):
    """finds the top songs of an artist on youtube"""
    videos, count, songs = yt.VideosSearch(artist), 0, []
    while count < limit:
        for sub_dict in videos.result()['result']:
            split = sub_dict['duration'].split(":")
            if int(split[0]) < 15 and len(split) < 3:# removes albums
                count += 1
                songs.append({'title': sub_dict['title'], 'id': sub_dict['id'], 'duration': sub_dict['duration'], 'channel': sub_dict['channel']['link']})
        videos.next()
    songs = songs[:limit]
    IDs = []
    for song in songs:
        IDs.append(song['id'])
    if not check_for_duplicates(IDs):# can't get a set of dictionaries so IDs are checked instead
        return songs
    else:
        IDs = set(IDs)
        filtered_songs, filtered_IDs = [], []
        for song in songs:
            ID = song['id']
            if ID in IDs and ID not in filtered_IDs:
                filtered_songs.append(song)
                filtered_IDs.append(ID)
        return filtered_songs
    

# def vid_search_random(artist, limit): OLD BUG
#     """chooses random songs from more than just the top few of an artist on youtube"""
#     videos = yt.VideosSearch(artist); video_options = []
#     for i in range((2 + ceil(limit/5))):# this sum is used to make sure theres enough to get a good random selection, but not so much its lags
#         for song in videos.result()['result']:
#             if int(song['duration'].split(":")[0]) < 10 and len(song['duration'].split(":")) < 3:
#                 current_details = {'id': song['id'],
#                                    'title': song['title'],
#                                    'duration': song['duration']}
#                 video_options.append(current_details)
#         videos.next()# load next
#     chosen_songs = []; i = 0
#     while i < limit:# until enough songs have been chosen
#         current = random.choice(video_options)# choose a song
#         if not current['id'] in chosen_songs:# if it hasn't already been chosen
#             chosen_songs.append(current); i += 1# add it to the list of chosen songs
#     return chosen_songs# return the songs


def vid_search_random(artist, limit):
    """chooses random songs from more than just the top few of an artist on youtube"""
    videos, count, songs, search_limit = yt.VideosSearch(artist), 0, [], limit * 3
    while count < search_limit:
        for sub_dict in videos.result()['result']:
            split = sub_dict['duration'].split(":")
            if int(split[0]) < 15 and len(split) < 3:# removes albums
                count += 1
                songs.append({'title': sub_dict['title'], 'id': sub_dict['id'], 'duration': sub_dict['duration'], 'channel': sub_dict['channel']['link']})
        videos.next()
    selected = []
    IDs = []
    for song in songs:
        IDs.append(song['id'])
    if not check_for_duplicates(IDs):# can't get a set of dictionaries so IDs are checked instead
        length = 0
        while length < limit:
            choice = random.choice(songs)
            selected.append(choice)
            songs.remove(choice)
            length += 1
        return selected
    else:
        IDs = set(IDs)
        filtered_songs, filtered_IDs = [], []
        for song in songs:
            ID = song['id']
            if ID in IDs and ID not in filtered_IDs:
                filtered_songs.append(song)
                filtered_IDs.append(ID)
        length = 0
        while length < limit:
            choice = random.choice(filtered_songs)
            selected.append(choice)
            filtered_songs.remove(choice)
            length += 1
        return selected


def find_channel(artist):
    """finds a channel"""
    search = yt.ChannelsSearch(artist, limit=10).result()['result']
    refined_search = []
    targets = ["title", "subscribers", "link"]
    for i in range(len(search)):
        refined_search.append({'title': None, 'subscribers': None, 'link': None})
        for target in targets:
            refined_search[i][target] = search[i][target]
    return refined_search


def search_by_link(link):
    """search by link"""
    try:# if its a video this works
        video = yt.Video.get(link)
        return [{'id': video['id'], 'title': video['title'], 'duration': "{:.2f}".format(float((int(video['streamingData']['adaptiveFormats'][0]['approxDurationMs']) / 1000 / 60)))}]
    except ValueError:# if its a playlist
        videos = yt.Playlist.get(link)
        songs = []
        for sub_dict in videos['videos']:
            songs.append({'title': sub_dict['title'], 'id': sub_dict['id'], 'duration': sub_dict['duration']})
        return songs
        

# ↓ debug ↓
if __name__ == '__main__':
    from pprint import pprint
    pprint(search_by_link("https://www.youtube.com/playlist?list=PLU1XqNAUBP5Vp2fOpaUV3aYa6XwfkL73f"))
    print()
    pprint(search_by_link("https://www.youtube.com/watch?v=aEHxqBHCkFc"))
