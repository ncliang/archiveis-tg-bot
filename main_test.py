import unittest
from unittest.mock import MagicMock, patch

from main import extract_urls, is_valid_url, handle_message


class TestExtractUrls(unittest.TestCase):
    def test_single_url(self):
        text = "Check out this website: https://example.com"
        expected = ["https://example.com"]
        self.assertEqual(extract_urls(text), expected)

    def test_multiple_urls(self):
        text = "Here are some links: https://example.com and https://another.com"
        expected = ["https://example.com", "https://another.com"]
        self.assertEqual(extract_urls(text), expected)

    def test_www_urls(self):
        text = "Visit www.example.com or www.another.com"
        expected = ["www.example.com", "www.another.com"]
        self.assertEqual(extract_urls(text), expected)

    def test_mixed_urls(self):
        text = "Links: https://example.com, www.example.com, and https://another.com"
        expected = ["https://example.com", "www.example.com", "https://another.com"]
        self.assertEqual(extract_urls(text), expected)

    def test_urls_with_paths(self):
        text = "Check these: https://example.com/path and https://another.com/page?param=value"
        expected = ["https://example.com/path", "https://another.com/page?param=value"]
        self.assertEqual(extract_urls(text), expected)

    def test_no_urls(self):
        text = "This is just regular text without any URLs"
        expected = []
        self.assertEqual(extract_urls(text), expected)

    def test_urls_with_special_characters(self):
        text = "Visit https://example.com/path?param=value&another=param"
        expected = ["https://example.com/path?param=value&another=param"]
        self.assertEqual(extract_urls(text), expected)

    def test_urls_with_quotes(self):
        text = 'Check "https://example.com" and "www.example.com"'
        expected = ["https://example.com", "www.example.com"]
        self.assertEqual(extract_urls(text), expected)

    def test_urls_with_angle_brackets(self):
        text = "Visit <https://example.com> or <www.example.com>"
        expected = []
        self.assertEqual(extract_urls(text), expected)

    def test_urls_with_newlines(self):
        text = """Here are some links:
        https://example.com
        www.example.com"""
        expected = ["https://example.com", "www.example.com"]
        self.assertEqual(extract_urls(text), expected)


class TestIsValidUrl(unittest.TestCase):
    def test_valid_http_url(self):
        self.assertTrue(is_valid_url("http://example.com"))

    def test_valid_https_url(self):
        self.assertTrue(is_valid_url("https://example.com"))

    def test_valid_url_with_path(self):
        self.assertTrue(is_valid_url("https://example.com/path"))

    def test_valid_url_with_query(self):
        self.assertTrue(is_valid_url("https://example.com?param=value"))

    def test_valid_url_with_fragment(self):
        self.assertTrue(is_valid_url("https://example.com#section"))

    def test_valid_url_with_port(self):
        self.assertTrue(is_valid_url("https://example.com:8080"))

    def test_valid_url_with_subdomain(self):
        self.assertTrue(is_valid_url("https://sub.example.com"))

    def test_invalid_missing_scheme(self):
        self.assertFalse(is_valid_url("example.com"))

    def test_invalid_missing_netloc(self):
        self.assertFalse(is_valid_url("https://"))

    def test_invalid_unsupported_scheme(self):
        self.assertFalse(is_valid_url("ftp://example.com"))

    def test_invalid_empty_url(self):
        self.assertFalse(is_valid_url(""))

    def test_invalid_url_with_angle_brackets(self):
        self.assertFalse(is_valid_url("<https://example.com>"))

    def test_invalid_url_with_quotes(self):
        self.assertFalse(is_valid_url('"https://example.com"'))


class TestHandleMessage(unittest.TestCase):
    def setUp(self):
        self.bot = MagicMock()
        self.chat_id = 123456789

    def test_single_valid_url(self):
        message_text = "Check out https://example.com"
        handle_message(self.bot, self.chat_id, message_text)
        self.bot.sendMessage.assert_called_once_with(
            chat_id=self.chat_id,
            text="https://archive.is/https://example.com"
        )

    def test_multiple_valid_urls(self):
        message_text = "Links: https://example.com and https://another.com"
        handle_message(self.bot, self.chat_id, message_text)
        self.assertEqual(self.bot.sendMessage.call_count, 2)
        calls = self.bot.sendMessage.call_args_list
        self.assertEqual(calls[0][1]['text'], "https://archive.is/https://example.com")
        self.assertEqual(calls[1][1]['text'], "https://archive.is/https://another.com")

    def test_invalid_url(self):
        message_text = "Check out example.com"  # Missing scheme
        handle_message(self.bot, self.chat_id, message_text)
        self.bot.sendMessage.assert_not_called()

    def test_mixed_valid_and_invalid_urls(self):
        message_text = "Links: https://valid.com and invalid.com"
        handle_message(self.bot, self.chat_id, message_text)
        self.bot.sendMessage.assert_called_once_with(
            chat_id=self.chat_id,
            text="https://archive.is/https://valid.com"
        )

    def test_url_with_query_parameters(self):
        message_text = "Check https://example.com?param=value&another=param"
        handle_message(self.bot, self.chat_id, message_text)
        self.bot.sendMessage.assert_called_once_with(
            chat_id=self.chat_id,
            text="https://archive.is/https://example.com?param=value&another=param"
        )

    def test_empty_message(self):
        message_text = ""
        handle_message(self.bot, self.chat_id, message_text)
        self.bot.sendMessage.assert_not_called()

    def test_message_without_urls(self):
        message_text = "This is just regular text without any URLs"
        handle_message(self.bot, self.chat_id, message_text)
        self.bot.sendMessage.assert_not_called()

    def test_url_with_special_characters(self):
        message_text = "Visit https://example.com/path?param=value&another=param"
        handle_message(self.bot, self.chat_id, message_text)
        self.bot.sendMessage.assert_called_once_with(
            chat_id=self.chat_id,
            text="https://archive.is/https://example.com/path?param=value&another=param"
        )


if __name__ == '__main__':
    unittest.main()
