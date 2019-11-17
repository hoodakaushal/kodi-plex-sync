Script to sync watched status between media centers, supports Kodi and Plex for now.
Both Episodes and Movies are supported. Sync at Tv Show/season level is not supported.
Basic knowledge of python is expected to configure/run this.

Matching files across media centers is done by file path. A video in plex and kodi is considered same if they both have the same underlying file.
This has the advantage of not requiring any external API (eg TVDB) and can be run offline.
Paths are treated as case sensitive by default, on *nix systems this is fine, on Windows it can cause videos to not be matched.
This also means that scenarios where one file contains multiple episodes are not supported - either they'll all end up
being marked watched or unwatched, depending on the order in which they are processed.
If your media tagging in plex and kodi is not the same this can lead to incorrect behavior.
I tested this on my setup (which only used local files), so no guarantees for remote shares (eg samba, nfs, etc) - it
depends on both media centers representing the path of the video in same fashion.

Dependencies:
python3
plexapi and requests module for python (pip install -r requirements.txt)

Usage/Config:
Change the endpoints for plex and kodi according to your setup in sync.py

Set the sync mode and strictness as you want (default is bidirectional sync without strict checking)

    Sync mode:
    0 -> UNIDIRECTIONAL FROM a to b, a always overrides b. In strict mode media in b but not a is ignored.
    1 -> BIDIRECTIONAL, if a and b conflict, mark both as watched
    2 -> BIDIRECTIONAL, if a and b conflict, mark both as unwatched

    strict sync:
    True -> If media in a and not b, raise error. If media in b and not a, raise error only for BIDIRECTIONAL sync mode.
    False -> Ignore discrepancies in media in a and b.
    Note that if strict, checking is done before doing any updates.

And just let it run!

Once you have it configured to work with your setup, you can have it run periodically via Scheduled Task/cron.

Note on Auth:
By default the script expects to be able to connect to Kodi without auth, and for Plex an auth token is supported.
For plex if you want to use username/password instead, you'll need to change the connect code. Internally plexapi
is used to connect to plex, refer their docs for more connection methods - https://pypi.org/project/PlexAPI/

I don't intend to actively maintain it, but feel free to hit me up if you have a request/suggestion.
