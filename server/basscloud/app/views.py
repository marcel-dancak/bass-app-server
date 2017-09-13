
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from basscloud.catalog.models import Project
from basscloud.libs.lzstring import LZString



def app(request):
    return render(request, "app/index.html")


def app_data(request, id, *args):
    project = get_object_or_404(Project, pk=id)
    return HttpResponse(project.data, content_type='text/plain')


class YtLogger(object):
    output = ''
    url = ''
    json = ''
    def debug(self, msg):
        self.output += msg+'\n'
        if msg.startswith('https://'):
            self.url = msg
        if msg.startswith('{"'):
            self.json = msg

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def extract_streams(request):
    # link = 'https://www.youtube.com/watch?v='+request.GET['id']
    link = request.GET['url']
    import youtube_dl
    # youtube_dl._real_main(['-f', '250', '-g', link])

    logger = YtLogger()
    ydl_opts = {
        'quiet': True,
        'simulate': True,
        'forcejson': True,
        # 'forceurl': True,
        # 'format': '250',
        'logger': logger,
        'verbose': False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        # print(logger.output)

    return HttpResponse(logger.json, content_type='application/json')
    return HttpResponse(logger.url, content_type='text/plain')