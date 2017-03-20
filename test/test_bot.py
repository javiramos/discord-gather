import re
import unittest
from unittest import mock
from .helper import async_test
from gather.bot import ListenerBot


class TestListenerBot(unittest.TestCase):
    def test_register(self):
        bot = ListenerBot()
        self.assertEqual({}, bot.actions)
        regex = r'^test'
        action = mock.Mock()
        bot.register_action(regex, action)
        self.assertEqual(
            {regex: (re.compile(regex, re.IGNORECASE), action)},
            bot.actions
        )

    def test_overwrite(self):
        bot = ListenerBot()
        self.assertEqual({}, bot.actions)
        regex = r'^test'
        action = mock.Mock()
        bot.register_action(regex, action)

        new_action = mock.Mock()
        bot.register_action(regex, new_action)
        self.assertEqual(
            {regex: (re.compile(regex, re.IGNORECASE), new_action)},
            bot.actions
        )

    @async_test
    async def test_on_message_from_bot(self):
        bot = ListenerBot()
        bot.username = 'testuser'
        regex = r'^test'
        action = mock.Mock()
        bot.actions = {regex: (re.compile(regex, re.IGNORECASE), action)}
        await bot.on_message(mock.Mock(), 'testuser', 'test')
        action.assert_not_called()

    @async_test
    async def test_on_message_from_other(self):
        bot = ListenerBot()
        bot.username = 'testuser'
        regex = r'^test'
        action = mock.Mock()
        bot.actions = {regex: (re.compile(regex, re.IGNORECASE), action)}
        await bot.on_message(mock.Mock(), 'anotheruser', 'test')
        self.assertTrue(action.called)


if __name__ == '__main__':
    unittest.main()
