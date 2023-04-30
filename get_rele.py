'''
Este script se conecta a reles y rescata los eventos de un 
npub especifico o los últimos recibidos de los nodos. Esto 
se puede especificar en filters

mas en:
https://www.e2encrypted.com/nostr/nips/#message-types
'''


from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
import time
import uuid

pub_hex = '0c77ac001c41df7aa86bb419e22e0abddbff0562636857122e1c50246034ce8b'

relay_manager = RelayManager(timeout=3)

relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://eden.nostr.land")

filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], authors=[pub_hex], limit=10)])

subscription_id = uuid.uuid1().hex

relay_manager.add_subscription_on_all_relays(subscription_id, filters)
relay_manager.run_sync()

events = {}

while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    event_id = event_msg.event.id
    if event_id not in events:
        events[event_id] = event_msg.event
        print(f"Event ID: {event_id}, Content: {event_msg.event.content}")

relay_manager.close_all_relay_connections()