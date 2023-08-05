# mautrix-facebook - A Matrix-Facebook Messenger puppeting bridge
# Copyright (C) 2020 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import (Any, Dict, Iterator, Optional, Iterable, Type, Callable, Awaitable,
                    Union, TYPE_CHECKING)
import asyncio
import time

import fbchat
from mautrix.types import (UserID, PresenceState, RoomID, EventID, TextMessageEventContent,
                           MessageType)
from mautrix.client import Client as MxClient
from mautrix.bridge import BaseUser
from mautrix.bridge._community import CommunityHelper, CommunityID
from mautrix.util.simple_lock import SimpleLock

from .config import Config
from .commands import enter_2fa_code
from .db import User as DBUser, UserPortal as DBUserPortal, Contact as DBContact, ThreadType
from . import portal as po, puppet as pu

if TYPE_CHECKING:
    from .context import Context

config: Config


class User(BaseUser):
    by_mxid: Dict[UserID, 'User'] = {}
    by_fbid: Dict[str, 'User'] = {}

    session: Optional[fbchat.Session]
    client: Optional[fbchat.Client]
    listener: Optional[fbchat.Listener]
    listen_task: Optional[asyncio.Task]

    notice_room: RoomID
    _notice_room_lock: asyncio.Lock
    is_admin: bool
    permission_level: str
    _is_logged_in: Optional[bool]
    _is_connected: Optional[bool]
    _connection_time: float
    _prev_thread_sync: float
    _session_data: Optional[Dict[str, str]]
    _db_instance: Optional[DBUser]
    _sync_lock: SimpleLock

    _community_helper: CommunityHelper
    _community_id: Optional[CommunityID]

    def __init__(self, mxid: UserID, session: Optional[Dict[str, str]] = None,
                 notice_room: Optional[RoomID] = None,
                 db_instance: Optional[DBUser] = None) -> None:
        self.mxid = mxid
        self.notice_room = notice_room
        self._notice_room_lock = asyncio.Lock()
        self.by_mxid[mxid] = self
        self.command_status = None
        self.is_whitelisted, self.is_admin, self.permission_level = config.get_permissions(mxid)
        self._is_logged_in = None
        self._is_connected = None
        self._connection_time = time.monotonic()
        self._prev_thread_sync = -10
        self._session_data = session
        self._db_instance = db_instance
        self._community_id = None
        self._sync_lock = SimpleLock("Waiting for thread sync to finish before handling %s",
                                     log=self.log, loop=self.loop)

        self.log = self.log.getChild(self.mxid)

        self.client = None
        self.session = None
        self.listener = None
        self.listen_task = None

    @property
    def is_connected(self) -> Optional[bool]:
        return self._is_connected

    @is_connected.setter
    def is_connected(self, val: Optional[bool]) -> None:
        if self._is_connected != val:
            self._is_connected = val
            self._connection_time = time.monotonic()

    # region Sessions

    @property
    def fbid(self) -> Optional[str]:
        if not self.session:
            return None
        return self.session.user.id

    @property
    def db_instance(self) -> DBUser:
        if not self._db_instance:
            self._db_instance = DBUser(mxid=self.mxid, session=self._session_data, fbid=self.fbid,
                                       notice_room=self.notice_room)
        return self._db_instance

    def save(self, _update_session_data: bool = True) -> None:
        self.log.debug("Saving session")
        if _update_session_data and self.session:
            self._session_data = self.session.get_cookies()
        self.db_instance.edit(session=self._session_data, fbid=self.fbid,
                              notice_room=self.notice_room)

    @classmethod
    def from_db(cls, db_user: DBUser) -> 'User':
        return User(mxid=db_user.mxid, session=db_user.session,
                    notice_room=db_user.notice_room, db_instance=db_user)

    @classmethod
    def get_all(cls) -> Iterator['User']:
        for db_user in DBUser.all():
            yield cls.from_db(db_user)

    @classmethod
    def get_by_mxid(cls, mxid: UserID, create: bool = True) -> Optional['User']:
        if pu.Puppet.get_id_from_mxid(mxid) is not None or mxid == cls.az.bot_mxid:
            return None
        try:
            return cls.by_mxid[mxid]
        except KeyError:
            pass

        db_user = DBUser.get_by_mxid(mxid)
        if db_user:
            return cls.from_db(db_user)

        if create:
            user = cls(mxid)
            user.db_instance.insert()
            return user

        return None

    @classmethod
    def get_by_fbid(cls, fbid: str) -> Optional['User']:
        try:
            return cls.by_fbid[fbid]
        except KeyError:
            pass

        db_user = DBUser.get_by_fbid(fbid)
        if db_user:
            return cls.from_db(db_user)

        return None

    async def load_session(self, _override: bool = False, _raise_errors: bool = False) -> bool:
        if self._is_logged_in and not _override:
            return True
        elif not self._session_data:
            return False
        try:
            session = await fbchat.Session.from_cookies(self._session_data)
            logged_in = await session.is_logged_in()
        except Exception:
            self.log.exception("Failed to restore session")
            if _raise_errors:
                raise
            return False
        if logged_in:
            self.log.info("Loaded session successfully")
            self.session = session
            self.client = fbchat.Client(session=self.session)
            self._is_logged_in = True
            self.is_connected = None
            if self.listen_task:
                self.listen_task.cancel()
            self.listen_task = self.loop.create_task(self.try_listen())
            asyncio.ensure_future(self.post_login(), loop=self.loop)
            return True
        return False

    async def is_logged_in(self, _override: bool = False) -> bool:
        if not self.session:
            return False
        if self._is_logged_in is None or _override:
            self._is_logged_in = await self.session.is_logged_in()
        return self._is_logged_in

    # endregion

    async def refresh(self) -> None:
        event_id = None
        if self.listener:
            event_id = await self.send_bridge_notice("Disconnecting Messenger MQTT connection "
                                                     "for session refresh...")
            self.listener.disconnect()
            await self.listen_task
        event_id = await self.send_bridge_notice("Refreshing session...", edit=event_id)
        try:
            ok = await self.load_session(_override=True, _raise_errors=True)
        except fbchat.FacebookError as e:
            await self.send_bridge_notice("Failed to refresh Messenger session: "
                                          f"{e.message}", edit=event_id)
        except Exception:
            await self.send_bridge_notice("Failed to refresh Messenger session: unknown error "
                                          "(see logs for more details)", edit=event_id)
        else:
            if ok:
                await self.send_bridge_notice("Successfully refreshed Messenger session",
                                              edit=event_id)
            else:
                await self.send_bridge_notice("Failed to refresh Messenger session: "
                                              "not logged in", edit=event_id)

    async def logout(self) -> bool:
        ok = True
        self.stop_listening()
        if self.session:
            try:
                await self.session.logout()
            except fbchat.FacebookError:
                self.log.exception("Error while logging out")
                ok = False
        self._session_data = None
        self._is_logged_in = False
        self.is_connected = None
        self.client = None
        self.session = None
        self.listener = None
        self.save(_update_session_data=False)
        return ok

    async def post_login(self) -> None:
        self.log.info("Running post-login actions")
        self.by_fbid[self.fbid] = self

        try:
            puppet = pu.Puppet.get_by_fbid(self.fbid)

            if puppet.custom_mxid != self.mxid and puppet.can_auto_login(self.mxid):
                self.log.info(f"Automatically enabling custom puppet")
                await puppet.switch_mxid(access_token="auto", mxid=self.mxid)
        except Exception:
            self.log.exception("Failed to automatically enable custom puppet")

        await self._create_community()
        await self.sync_contacts()
        await self.sync_threads()
        self.log.debug("Updating own puppet info")
        # TODO this might not be right (if it is, check that we got something sensible?)
        own_info = await self.client.fetch_thread_info([self.fbid]).__anext__()
        puppet = pu.Puppet.get_by_fbid(self.fbid, create=True)
        await puppet.update_info(source=self, info=own_info)

    async def _create_community(self) -> None:
        template = config["bridge.community_template"]
        if not template:
            return
        localpart, server = MxClient.parse_user_id(self.mxid)
        community_localpart = template.format(localpart=localpart, server=server)
        self.log.debug(f"Creating personal filtering community {community_localpart}...")
        self._community_id, created = await self._community_helper.create(community_localpart)
        if created:
            await self._community_helper.update(self._community_id, name="Facebook Messenger",
                                                avatar_url=config["appservice.bot_avatar"],
                                                short_desc="Your Facebook bridged chats")
            await self._community_helper.invite(self._community_id, self.mxid)

    async def _add_community(self, up: Optional[DBUserPortal], contact: Optional[DBContact],
                             portal: 'po.Portal', puppet: Optional['pu.Puppet']) -> None:
        if portal.mxid:
            if not up or not up.in_community:
                ic = await self._community_helper.add_room(self._community_id, portal.mxid)
                if up and ic:
                    up.edit(in_community=True)
                elif not up:
                    DBUserPortal(user=self.fbid, in_community=ic, portal=portal.fbid,
                                 portal_receiver=portal.fb_receiver).insert()
        if puppet:
            await self._add_community_puppet(contact, puppet)

    async def _add_community_puppet(self, contact: Optional[DBContact],
                                    puppet: 'pu.Puppet') -> None:
        if not contact or not contact.in_community:
            await puppet.default_mxid_intent.ensure_registered()
            ic = await self._community_helper.join(self._community_id,
                                                   puppet.default_mxid_intent)
            if contact and ic:
                contact.edit(in_community=True)
            elif not contact:
                DBContact(user=self.fbid, contact=puppet.fbid, in_community=ic).insert()

    async def sync_contacts(self):
        try:
            self.log.debug("Fetching contacts...")
            users = await self.client.fetch_users()
            self.log.debug(f"Fetched {len(users)} contacts")
            contacts = DBContact.all(self.fbid)
            update_avatars = config["bridge.update_avatar_initial_sync"]
            for user in users:
                puppet = pu.Puppet.get_by_fbid(user.id, create=True)
                await puppet.update_info(self, user, update_avatar=update_avatars)
                await self._add_community_puppet(contacts.get(puppet.fbid, None), puppet)
        except Exception:
            self.log.exception("Failed to sync contacts")

    async def sync_threads(self) -> None:
        if self._prev_thread_sync + 10 > time.monotonic():
            self.log.debug("Previous thread sync was less than 10 seconds ago, not re-syncing")
            return
        self._prev_thread_sync = time.monotonic()
        try:
            sync_count = config["bridge.initial_chat_sync"]
            if sync_count <= 0:
                return
            self.log.debug("Fetching threads...")
            ups = DBUserPortal.all(self.fbid)
            contacts = DBContact.all(self.fbid)
            async for thread in self.client.fetch_threads(limit=sync_count):
                if not isinstance(thread, (fbchat.UserData, fbchat.PageData, fbchat.GroupData)):
                    # TODO log?
                    continue
                try:
                    await self._sync_thread(thread, ups, contacts)
                except Exception:
                    self.log.exception("Failed to sync thread %s", thread.id)
        except Exception:
            self.log.exception("Failed to sync threads")

    async def _sync_thread(self, thread: Union[fbchat.UserData, fbchat.PageData, fbchat.GroupData],
                           ups: Dict[str, 'DBUserPortal'], contacts: Dict[str, 'DBContact']
                           ) -> None:
        self.log.debug(f"Syncing thread {thread.id} {thread.name}")
        fb_receiver = self.fbid if isinstance(thread, fbchat.User) else None
        portal = po.Portal.get_by_thread(thread, fb_receiver)
        puppet = None

        if isinstance(thread, fbchat.UserData):
            puppet = pu.Puppet.get_by_fbid(thread.id, create=True)
            await puppet.update_info(self, thread)

        await self._add_community(ups.get(portal.fbid, None),
                                  contacts.get(puppet.fbid, None) if puppet else None,
                                  portal, puppet)

        if not portal.mxid:
            await portal.create_matrix_room(self, thread)
        else:
            await portal.update_matrix_room(self, thread)
            await portal.backfill(self, is_initial=False, last_active=thread.last_active)

    async def on_2fa_callback(self) -> str:
        if self.command_status and self.command_status.get("action", "") == "Login":
            future = self.loop.create_future()
            self.command_status["future"] = future
            self.command_status["next"] = enter_2fa_code
            await self.az.intent.send_notice(self.command_status["room_id"],
                                             "You have two-factor authentication enabled. "
                                             "Please send the code here.")
            return await future
        raise RuntimeError("No ongoing login command")

    async def get_notice_room(self) -> RoomID:
        if not self.notice_room:
            async with self._notice_room_lock:
                # If someone already created the room while this call was waiting,
                # don't make a new room
                if self.notice_room:
                    return self.notice_room
                self.notice_room = await self.az.intent.create_room(
                    is_direct=True, invitees=[self.mxid],
                    topic="Facebook Messenger bridge notices")
                self.save()
        return self.notice_room

    async def send_bridge_notice(self, text: str, edit: Optional[EventID] = None
                                 ) -> Optional[EventID]:
        event_id = None
        try:
            content = TextMessageEventContent(msgtype=MessageType.NOTICE, body=text)
            if edit:
                content.set_edit(edit)
            event_id = await self.az.intent.send_message(await self.get_notice_room(), content)
        except Exception:
            self.log.warning("Failed to send bridge notice '%s'", text, exc_info=True)
        return edit or event_id

    # region Facebook event handling

    async def try_listen(self) -> None:
        try:
            await self.listen()
        except Exception:
            self.is_connected = False
            await self.send_bridge_notice("Fatal error in listener (see logs for more info)")
            self.log.exception("Fatal error in listener")
            try:
                self.listener.disconnect()
            except Exception:
                self.log.debug("Error disconnecting listener after error", exc_info=True)

    async def _handle_event(self, handler: Callable[[Any], Awaitable[None]], event: Any) -> None:
        await self._sync_lock.wait("event")
        try:
            await handler(event)
        except Exception:
            self.log.exception(f"Failed to handle {type(event)} event from Facebook")

    async def listen(self) -> None:
        if not self.listener:
            self.listener = fbchat.Listener(session=self.session, chat_on=True, foreground=False)
        handlers: Dict[Type[fbchat.Event], Callable[[Any], Awaitable[None]]] = {
            fbchat.MessageEvent: self.on_message,
            fbchat.MessageReplyEvent: self.on_message,
            fbchat.TitleSet: self.on_title_change,
            fbchat.UnsendEvent: self.on_message_unsent,
            fbchat.ThreadsRead: self.on_message_seen,
            fbchat.ReactionEvent: self.on_reaction,
            fbchat.Presence: self.on_presence,
            fbchat.Typing: self.on_typing,
            fbchat.PeopleAdded: self.on_members_added,
            fbchat.PersonRemoved: self.on_member_removed,
            fbchat.Connect: self.on_connect,
            fbchat.Disconnect: self.on_disconnect,
            fbchat.Resync: self.on_resync,
        }

        self.log.debug("Starting fbchat listener")
        async for event in self.listener.listen():
            self.log.debug("Handling facebook event %s", event)
            try:
                handler = handlers[type(event)]
            except KeyError:
                self.log.debug(f"Received unknown event type {type(event)}")
            else:
                self.loop.create_task(self._handle_event(handler, event))
        self.is_connected = False
        await self.send_bridge_notice("Facebook Messenger connection closed without error")

    async def on_connect(self, evt: fbchat.Connect) -> None:
        now = time.monotonic()
        disconnected_at = self._connection_time
        max_delay = config["bridge.resync_max_disconnected_time"]
        first_connect = self.is_connected is None
        self.is_connected = True
        if not first_connect and disconnected_at + max_delay < now:
            duration = int(now - disconnected_at)
            self.log.debug("Disconnection lasted %d seconds, re-syncing threads...", duration)
            await self.send_bridge_notice("Connected to Facebook Messenger after being "
                                          f"disconnected for {duration} seconds, syncing chats...")
            await self.sync_threads()
        else:
            await self.send_bridge_notice("Connected to Facebook Messenger")

    async def on_disconnect(self, evt: fbchat.Disconnect) -> None:
        self.is_connected = False
        await self.send_bridge_notice(f"Disconnected from Facebook Messenger: {evt.reason}")

    async def on_resync(self) -> None:
        self.log.info("sequence_id changed, resyncing threads...")
        await self.sync_threads()

    def stop_listening(self) -> None:
        if self.listener:
            self.listener.disconnect()
        if self.listen_task:
            self.listen_task.cancel()

    async def on_logged_in(self, session: fbchat.Session) -> None:
        self.session = session
        self.client = fbchat.Client(session=session)
        self.save()
        if self.listen_task:
            self.listen_task.cancel()
        self.listen_task = self.loop.create_task(self.try_listen())
        asyncio.ensure_future(self.post_login(), loop=self.loop)

    async def on_message(self, evt: Union[fbchat.MessageEvent, fbchat.MessageReplyEvent]) -> None:
        fb_receiver = self.fbid if isinstance(evt.thread, fbchat.User) else None
        portal = po.Portal.get_by_thread(evt.thread, fb_receiver)
        puppet = pu.Puppet.get_by_fbid(evt.author.id)
        if not puppet.name:
            await puppet.update_info(self)
        await portal.backfill_lock.wait(evt.message.id)
        await portal.handle_facebook_message(self, puppet, evt.message)

    async def on_title_change(self, evt: fbchat.TitleSet) -> None:
        assert isinstance(evt.thread, fbchat.Group)
        portal = po.Portal.get_by_thread(evt.thread)
        if not portal:
            return
        sender = pu.Puppet.get_by_fbid(evt.author.id)
        if not sender:
            return
        await portal.backfill_lock.wait("title change")
        # TODO find actual messageId for the event
        await portal.handle_facebook_name(self, sender, evt.title, str(evt.at.timestamp()))

    async def on_image_change(self, mid: str = None, author_id: str = None, new_image: str = None,
                              thread_id: str = None, thread_type: ThreadType = ThreadType.GROUP,
                              at: int = None, msg: Any = None) -> None:
        # FIXME this method isn't called
        #       It seems to be a maunually fetched event in fbchat.UnfetchedThreadEvent
        #       But the Message.fetch() doesn't return the necessary info
        fb_receiver = self.fbid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver)
        if not portal:
            return
        sender = pu.Puppet.get_by_fbid(author_id)
        if not sender:
            return
        await portal.backfill_lock.wait(mid)
        await portal.handle_facebook_photo(self, sender, new_image, mid)

    async def on_message_seen(self, evt: fbchat.ThreadsRead) -> None:
        puppet = pu.Puppet.get_by_fbid(evt.author.id)
        for thread in evt.threads:
            fb_receiver = self.fbid if isinstance(thread, fbchat.User) else None
            portal = po.Portal.get_by_thread(thread, fb_receiver)
            if portal.mxid:
                await portal.backfill_lock.wait(f"read receipt from {puppet.fbid}")
                await portal.handle_facebook_seen(self, puppet)

    async def on_message_unsent(self, evt: fbchat.UnsendEvent) -> None:
        fb_receiver = self.fbid if isinstance(evt.thread, fbchat.User) else None
        portal = po.Portal.get_by_thread(evt.thread, fb_receiver)
        if portal.mxid:
            await portal.backfill_lock.wait(f"redaction of {evt.message.id}")
            puppet = pu.Puppet.get_by_fbid(evt.author.id)
            await portal.handle_facebook_unsend(self, puppet, evt.message.id)

    async def on_reaction(self, evt: fbchat.ReactionEvent) -> None:
        fb_receiver = self.fbid if isinstance(evt.thread, fbchat.User) else None
        portal = po.Portal.get_by_thread(evt.thread, fb_receiver)
        if not portal.mxid:
            return
        puppet = pu.Puppet.get_by_fbid(evt.author.id)
        await portal.backfill_lock.wait(f"reaction to {evt.message.id}")
        if evt.reaction is None:
            await portal.handle_facebook_reaction_remove(self, puppet, evt.message.id)
        else:
            await portal.handle_facebook_reaction_add(self, puppet, evt.message.id, evt.reaction)

    async def on_presence(self, evt: fbchat.Presence) -> None:
        for user, status in evt.statuses.items():
            puppet = pu.Puppet.get_by_fbid(user, create=False)
            if puppet:
                await puppet.default_mxid_intent.set_presence(
                    presence=PresenceState.ONLINE if status.active else PresenceState.OFFLINE,
                    ignore_cache=True)

    async def on_typing(self, evt: fbchat.Typing) -> None:
        fb_receiver = self.fbid if isinstance(evt.thread, fbchat.User) else None
        portal = po.Portal.get_by_thread(evt.thread, fb_receiver)
        if portal.mxid and not portal.backfill_lock.locked:
            puppet = pu.Puppet.get_by_fbid(evt.author.id)
            await puppet.intent.set_typing(portal.mxid, is_typing=evt.status, timeout=120000)

    async def on_members_added(self, evt: fbchat.PeopleAdded) -> None:
        assert isinstance(evt.thread, fbchat.Group)
        portal = po.Portal.get_by_thread(evt.thread)
        if portal.mxid:
            sender = pu.Puppet.get_by_fbid(evt.author.id)
            users = [pu.Puppet.get_by_fbid(user.id) for user in evt.added]
            await portal.backfill_lock.wait("member add")
            await portal.handle_facebook_join(self, sender, users)

    async def on_member_removed(self, evt: fbchat.PersonRemoved) -> None:
        assert isinstance(evt.thread, fbchat.Group)
        portal = po.Portal.get_by_thread(evt.thread)
        if portal.mxid:
            sender = pu.Puppet.get_by_fbid(evt.author.id)
            user = pu.Puppet.get_by_fbid(evt.removed.id)
            await portal.backfill_lock.wait("member remove")
            await portal.handle_facebook_leave(self, sender, user)

    # endregion


def init(context: 'Context') -> Iterable[Awaitable[bool]]:
    global config
    User.az, config, User.loop = context.core
    User._community_helper = CommunityHelper(User.az)
    return (user.load_session() for user in User.get_all())
