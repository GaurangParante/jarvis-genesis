import unittest

from app.tools.research_tools import ResearchTools


class ResearchToolsTests(unittest.TestCase):
    def test_parse_duckduckgo_html(self):
        html = """
        <html>
          <body>
            <a rel="nofollow" class="result__a" href="https://example.com/?utm=1">Example Title</a>
            <div class="result__snippet">Example snippet text.</div>
          </body>
        </html>
        """

        tools = ResearchTools()
        results = tools._parse_duckduckgo_html(html)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Example Title")
        self.assertEqual(results[0].url, "https://example.com/?utm=1")
        self.assertEqual(results[0].snippet, "Example snippet text.")

    def test_normalize_result_url(self):
        tools = ResearchTools()
        url = "https://duckduckgo.com/l/?uddg=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FShah_Rukh_Khan"

        normalized = tools._normalize_result_url(url)

        self.assertEqual(normalized, "https://en.wikipedia.org/wiki/Shah_Rukh_Khan")


if __name__ == "__main__":
    unittest.main()
