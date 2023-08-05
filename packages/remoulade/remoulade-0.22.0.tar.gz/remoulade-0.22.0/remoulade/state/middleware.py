import sys
from datetime import datetime, timezone

from ..middleware import Middleware
from .backend import State, StateNamesEnum


class MessageState(Middleware):

    """Middleware use to storage and update the state
    of the messages.
    Parameters
    state_ttl(int):Time(seconds) that the state will be storage
                    in the database
    max_size(int): Maximum size of arguments allow to storage
                    in the database, default 2MB
    """

    def __init__(self, backend, state_ttl=3600, max_size=2e6):
        self.backend = backend
        self.state_ttl = state_ttl
        self.max_size = max_size

    def save(self, message, state_name, priority=None, **kwargs):
        args = message.args
        kwargs_state = message.kwargs
        message_id = message.message_id
        actor_name = message.actor_name
        if sys.getsizeof(args) > self.max_size:
            # Arguments exceed maximum size to display
            #  do not save them.
            args = []
        if sys.getsizeof(kwargs_state) > self.max_size:
            # Keyword arguments exceed maximum size to
            #  display do not save them
            kwargs_state = {}
        self.backend.set_state(
            State(
                message_id,
                state_name,
                actor_name=actor_name,
                args=args,
                priority=priority,
                kwargs=kwargs_state,
                **kwargs,
            ),
            self.state_ttl,
        )

    def _get_current_time(self):
        return datetime.now(timezone.utc)

    def after_enqueue(self, broker, message, delay):
        priority = broker.get_actor(message.actor_name).priority
        self.save(
            message, state_name=StateNamesEnum.Pending, enqueued_datetime=self._get_current_time(), priority=priority
        )

    def after_skip_message(self, broker, message):
        self.save(message, state_name=StateNamesEnum.Skipped)

    def after_message_canceled(self, broker, message):
        self.save(message, state_name=StateNamesEnum.Canceled)

    def after_process_message(self, broker, message, *, result=None, exception=None):
        self.save(
            message,
            state_name=StateNamesEnum.Success if exception is None else StateNamesEnum.Failure,
            end_datetime=self._get_current_time(),
        )

    def before_process_message(self, broker, message):
        self.save(message, state_name=StateNamesEnum.Started, started_datetime=self._get_current_time())
