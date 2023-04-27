'''
Este script se conecta a reles y se suscribe a eventos en la red
'''


from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
import time
import uuid

pub = 'npub1p3m6cqqug80h42rtksv7yts2hhdl7ptzvd59wy3wr3gzgcp5e69smqygr8'
pub_hex = '0c77ac001c41df7aa86bb419e22e0abddbff0562636857122e1c50246034ce8b'
priv = 'nsec1atjckahx3vc4s8ysdsk7ffg9dyuas0w73pr54x4f8w332wmv29mqdk6y2n' 
priv_hex = 'eae58b76e68b31581c906c2de4a5056939d83dde88474a9aa93ba3153b6c5176'# crea una instancia rele



relay_manager = RelayManager(timeout=2)

#agregamos los reles que queramos
relay_manager.add_relay("wss://nostr.relayer.se")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://nostr.lacrypta.com.ar")
#filtra el evento que queramos
filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])

#genera un id 
subscription_id = uuid.uuid1().hex

#se suscribe a todos los eventos de los reles con el id y filters
relay_manager.add_subscription_on_all_relays(subscription_id, filters)
relay_manager.run_sync()


while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    if event_msg.event.pubkey == my_pubkey:
    print(event_msg.event.content)
relay_manager.close_all_relay_connections()