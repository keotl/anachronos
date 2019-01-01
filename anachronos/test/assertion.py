from anachronos.communication.anachronos import AnachronosException


class Assertion(object):

    def run(self, anachronos: "Anachronos"):
        raise NotImplementedError

    def _do_assertion(self, boolean: bool, message: str):
        if not boolean:
            raise AnachronosException(message)
