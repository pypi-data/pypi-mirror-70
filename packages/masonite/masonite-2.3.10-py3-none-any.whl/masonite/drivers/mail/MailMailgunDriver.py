"""Mailgun Driver Module."""
import requests

from ...contracts.MailContract import MailContract
from ...drivers import BaseMailDriver


class MailMailgunDriver(BaseMailDriver, MailContract):
    """Mailgun driver."""

    def send(self, message=None):
        """Send the message through the Mailgun service.

        Keyword Arguments:
            message {string} -- The message to be sent to Mailgun. (default: {None})

        Returns:
            requests.post -- Returns the response as a requests object.
        """

        if self._queue:
            from wsgi import container
            from ... import Queue
            return container.make(Queue).push(self._send_mail, args=(message,))

        return self._send_mail(message)

    def _send_mail(self, message):
        """Wrapper around sending mail so it can also be used with queues.

        Arguments:
            message {string|None} -- The message to be sent passed in from the send method.

        Returns:
            requests.post
        """
        if not message:
            message = self.message_body

        domain = self.config.DRIVERS['mailgun']['domain']
        secret = self.config.DRIVERS['mailgun']['secret']

        return requests.post(
            "https://api.mailgun.net/v3/{0}/messages".format(domain),
            auth=("api", secret),
            data={
                "from": self.mail_from_header,
                "to": self.to_addresses,
                "subject": self.message_subject,
                "h:Reply-To": self.message_reply_to,
                "html": message})
