import time
import uuid
from pynostr.event import Event, EventKind
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters

pub_hex = '0c77ac001c41df7aa86bb419e22e0abddbff0562636857122e1c50246034ce8b'
priv_hex = 'eae58b76e68b31581c906c2de4a5056939d83dde88474a9aa93ba3153b6c5176'

relay_manager = RelayManager(timeout=6)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://eden.nostr.land")

filters_notes = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], authors=[pub_hex], limit=100)])
subscription_id = uuid.uuid1().hex
relay_manager.add_subscription_on_all_relays(subscription_id, filters_notes)
relay_manager.run_sync()

original_notes = {}
while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    original_notes[event_msg.event.id] = event_msg.event

filters_responses = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], event_refs=list(original_notes.keys()), limit=100)])
relay_manager.add_subscription_on_all_relays(subscription_id, filters_responses)
relay_manager.run_sync()
time.sleep(5)

responses = {}
while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    responses[event_msg.event.id] = event_msg.event

for response_id, response in responses.items():
    print(f"Responding to: {response_id}, Content: {response.content}")
    reply = Event(content="Saludos desde python!!", kind=EventKind.TEXT_NOTE)
    reply.add_event_ref(response.id)
    reply.add_pubkey_ref(pub_hex)
    reply.sign(priv_hex)
    relay_manager.publish_event(reply)

relay_manager.run_sync()
time.sleep(5)

relay_manager.close_all_relay_connections()
