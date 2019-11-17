import plexapi
from plexapi.server import PlexServer


class Types:
    movie = 'movie'
    show = 'show'
    episode = 'episode'


def multi():
    baseurl = 'http://192.168.0.100:32400'
    plex = PlexServer(baseurl)
    multiFile = []
    for thing in plex.library.all():
        if thing.TYPE == Types.movie:
            files = getFiles(thing)
            if len(files) > 1:
                multiFile.append((thing, files))
        if thing.type == Types.show:
            for ep in thing.episodes():
                files = getFiles(ep)
                if len(files) > 1:
                    multiFile.append((ep, files))
    return multiFile


def getFiles(thing):
    files = []
    for m in thing.media:
        for p in m.parts:
            files.append(p.file)
    return files


if __name__ == "__main__":
    m = multi()
    for x in m:
        print(x)
