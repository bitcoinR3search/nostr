import time
import uuid
from pynostr.event import EventKind
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters

pub_hex = '0c77ac001c41df7aa86bb419e22e0abddbff0562636857122e1c50246034ce8b'

relay_manager = RelayManager(timeout=3)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://eden.nostr.land")

filters_notes = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], authors=[pub_hex], limit=10)])
subscription_id = uuid.uuid1().hex
relay_manager.add_subscription_on_all_relays(subscription_id, filters_notes)
relay_manager.run_sync()

events = {}
while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    events[event_msg.event.id] = event_msg.event.content

for event_id, content in events.items():
    print(f"Event ID: {event_id}, Content: {content}")

filters_responses = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], event_refs=list(events.keys()), limit=10)])
relay_manager.add_subscription_on_all_relays(subscription_id, filters_responses)
relay_manager.run_sync()
time.sleep(5)

responses = {}
while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    responses[event_msg.event.id] = event_msg.event.content

for response_id, content in responses.items():
    print(f"Response ID: {response_id}, Content: {content}")

relay_manager.close_all_relay_connections()
