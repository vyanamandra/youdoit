import re
import urllib.parse
import urllib.request
from ordered_set import OrderedSet


class YouTube():
    """
    Search and return the list of Youtube videos matching the search query
    """

    def __init__(self, search_string):
        self.search_string = search_string
        self.yList = None

    @classmethod
    def __gatherList__(self):
        """
        Private method. It is definitely related to the class and youtube search in particular
        Query youtube for a list of videos and save this list locally. It is a private function.
        :return: List of videos matching the result is stored in object variable yList
        """
        recompiled = re.compile(r'href=\"\/watch\?v=(.{11})')
        try:
            query_string = urllib.parse.urlencode({"search_query": searchString})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            self.yList = recompiled.findall(html_content.read().decode())
        except:
            self.yList = None

    def search(self, numResults):
        """
        :param numResults: Number of results you are expecting. It will be less than that usually since the YouTube
                            search returns duplicates.
        :return: Returns result in the form of a json. Only to leave scope for future enhancement.
        """
        results = None
        if not self.yList:
            self.__gatherList__()

        videos = list(OrderedSet(self.yList[:numResults]))
        yp = {}
        for vid in range(len(videos)):
            yp.append({"id": str(vid + 1), "pid": "player{}".format(vid + 1), "vid": videos[vid]})
        yplayers = {}
        yplayers['res'] = yp
        return (yplayers)

    @staticmethod
    def download(videoId, uid = None, savepath = None):
        """
        This static method will save a youtube video based on a user id to the savepath
        :param videoId: Id of the video that needs to be saved
        :param uid: User id requesting the video
        :param savepath: Path to save this video to
        :return: a json -
        {
        'status': success/failure,
        'videoId': video id that was saved,
        'savepath': path the video is saved at
        'access': uid of the user requesting the download
        }
        """
        video_url = 'https://www.youtube.com/watch?v=' + videoId
        res = {}
        if savepath:
            res['savedpath'] = savepath
        else:
            res['savedpath'] = os.getcwd() + os.path.sep + "downloads/"

        ydl_opts = {}
        # TODO:  a. Need to verify the download success/failure and other parameters.
        #        b. Need to update the master database of the md5sum, file location of the download, date time, uid, retention period of the file
        #        c. Need to update the user schema of the download information.

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            os.chdir(res['savedpath'])
            ydl.download([video_url])
        res['status']  = 'success'
        return res

