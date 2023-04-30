import time
import uuid
from pynostr.event import Event
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters

pub = 'npub1p3m6cqqug80h42rtksv7yts2hhdl7ptzvd59wy3wr3gzgcp5e69smqygr8'
pub_hex = '0c77ac001c41df7aa86bb419e22e0abddbff0562636857122e1c50246034ce8b'
priv = 'nsec1atjckahx3vc4s8ysdsk7ffg9dyuas0w73pr54x4f8w332wmv29mqdk6y2n' 
priv_hex = 'eae58b76e68b31581c906c2de4a5056939d83dde88474a9aa93ba3153b6c5176'# crea una instancia rele

relay_manager = RelayManager(timeout=6)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
#private_key = PrivateKey(priv_hex)

filters = FiltersList([Filters(authors=[pub_hex], limit=100)])
subscription_id = uuid.uuid1().hex
relay_manager.add_subscription_on_all_relays(subscription_id, filters)

event = Event("Hola chubut")
event.sign(priv_hex)

relay_manager.publish_event(event)
relay_manager.run_sync()
time.sleep(5) # allow the messages to send

