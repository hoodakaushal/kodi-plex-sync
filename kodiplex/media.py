from abc import ABC, abstractmethod

from kodiplex.kodi.kodi_rpc import KodiRPC
from logger import logger


class MediaType:
    movie = "movie"
    show = "show"
    episode = "episode"


class Media(ABC):
    def __init__(self, path, raw):
        self.raw = raw
        self.watched = self.getWatchedFromRaw()
        self.path = path

    @abstractmethod
    def updateWatched(self, watched: bool):
        pass

    @abstractmethod
    def getWatchedFromRaw(self):
        pass

    def __eq__(self, other):
        return self.path == other.path

    def __repr__(self):
        return "{} raw: {}".format(self.path, self.raw.__repr__())

    def __str__(self):
        return self.__repr__()


class KodiMedia(Media):
    def __init__(self, path, raw, kodi: KodiRPC):
        Media.__init__(self, path, raw)
        self.kodi = kodi

    def getWatchedFromRaw(self):
        return self.raw["playcount"] > 0

    def updateWatched(self, watched: bool):
        logger.debug("Setting {} watched to {}".format(self.raw, watched))
        if watched:
            if "movieid" in self.raw:
                return self.kodi.markMovieWatched(self.raw)
            else:
                return self.kodi.markEpisodeWatched(self.raw)
        else:
            if "movieid" in self.raw:
                return self.kodi.markMovieUnwatched(self.raw)
            else:
                return self.kodi.markEpisodeUnwatched(self.raw)


class PlexMedia(Media):
    def getWatchedFromRaw(self):
        return self.raw.isWatched

    def updateWatched(self, watched: bool):
        logger.debug("Setting {} watched to {}".format(self.raw, watched))
        if watched:
            self.raw.markWatched()
        else:
            self.raw.markUnwatched()
