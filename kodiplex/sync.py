from collections.abc import Iterable

from plexapi.server import PlexServer

from kodiplex.kodi.kodi_rpc import KodiRPC
from kodiplex.media import Media, KodiMedia, PlexMedia
from kodiplex.plex.plex import Types
from logger import logger


class MediaSyncer:
    """
    Sync mode:
    0 -> UNIDIRECTIONAL FROM a to b, a always overrides b. In strict mode media in b but not a is ignored.
    1 -> BIDIRECTIONAL, if a and b conflict, mark both as watched
    2 -> BIDIRECTIONAL, if a and b conflict, mark both as unwatched

    strict sync:
    True -> If media in a and not b, raise error. If media in b and not a, raise error only for BIDIRECTIONAL sync mode.
    False -> Ignore discrepancies in media in a and b.
    Note that if strict, checking is done before doing any updates.
    """

    def __init__(self, a, b, mode: int, strict=False):
        self.a = a
        self.b = b
        if not 0 <= mode <= 2:
            raise ValueError("mode must be 0,1 or 2")
        self.mode = mode
        self.strict = strict

    def verify(self):
        if not self.strict:
            return
        inAnotB = []
        inBnotA = []
        for mediaA in self.a:
            for mediaB in self.b:
                if mediaA == mediaB:
                    break
            else:  # Loop fell through without finding mediaA in b.
                inAnotB.append(mediaA)
        if self.mode > 0:
            for mediaB in self.b:
                for mediaA in self.a:
                    if mediaB == mediaA:
                        break
                else:
                    inBnotA.append(mediaB)
        if len(inBnotA) + len(inAnotB) > 0:
            logger.error("Media mismatch!")
            logger.error("Media in a but not b:")
            [logger.error(str(x)) for x in inAnotB]
            logger.error("Media in b but not a:")
            [logger.error(str(x)) for x in inBnotA]
            raise Exception("Media mismatch!")

    def unidirectionalSync(self):
        self.verify()
        for mediaA in self.a:
            for mediaB in self.b:
                if mediaA == mediaB and mediaA.watched != mediaB.watched:
                    mediaB.updateWatched(mediaA.watched)

    def bidirectionalSync(self):
        self.verify()
        for mediaA in self.a:
            for mediaB in self.b:
                if mediaA == mediaB and mediaA.watched != mediaB.watched:
                    if self.mode == 1:
                        if not mediaA.watched:
                            mediaA.updateWatched(True)
                        if not mediaB.watched:
                            mediaB.updateWatched(True)
                    elif self.mode == 2:
                        if mediaA.watched:
                            mediaA.updateWatched(False)
                        if mediaB.watched:
                            mediaB.updateWatched(False)

    def sync(self):
        if self.mode == 0:
            self.unidirectionalSync()
        else:
            self.bidirectionalSync()


def getKodiMedia(kodiUrl: str):
    kodi = KodiRPC(kodiUrl)
    kodiMedia = kodi.getEpisodes() + kodi.getMovies()
    kodiMedia = [KodiMedia(x["file"], x, kodi) for x in kodiMedia]
    return kodiMedia


def getPlexMedia(plexUrl: str, plexToken=None):
    plex = PlexServer(plexUrl, token=plexToken)
    plexMedia = []
    for thing in plex.library.all():
        if thing.TYPE == Types.movie:
            files = getFiles(thing)
            for f in files:
                plexMedia.append(PlexMedia(f, thing))
        if thing.type == Types.show:
            for ep in thing.episodes():
                files = getFiles(ep)
                for f in files:
                    plexMedia.append(PlexMedia(f, ep))
    return plexMedia


def getFiles(thing):
    files = []
    for m in thing.media:
        for p in m.parts:
            files.append(p.file)
    return files


if __name__ == "__main__":
    kodiMedia = getKodiMedia("http://localhost:8080")
    plexMedia = getPlexMedia("http://192.168.0.100:32400")
    sync = MediaSyncer(kodiMedia, plexMedia, 1, strict=False)
    sync.bidirectionalSync()
