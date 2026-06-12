import html
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass

from app.providers.base import ChatRequest


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class ResearchTools:
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
        html_text = self._fetch_text(url)
        results = self._parse_duckduckgo_html(html_text)
        return results[:limit]

    def fetch_page_text(self, url: str, max_chars: int = 2200) -> str:
        try:
            html_text = self._fetch_text(url)
        except Exception:
            return ""

        text = re.sub(r"<script.*?</script>", " ", html_text, flags=re.S | re.I)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars]

    def research(self, query: str, provider_manager=None) -> str:
        results = self.search(query, limit=5)

        source_blocks = []
        evidence_lines = []
        for index, result in enumerate(results, start=1):
            source_text = self.fetch_page_text(result.url, max_chars=700)
            snippet = result.snippet or source_text[:220]
            source_blocks.append(
                {
                    "rank": index,
                    "title": result.title,
                    "url": result.url,
                    "snippet": snippet,
                }
            )
            if snippet:
                evidence_lines.append(f"- {result.title}: {snippet[:220]}")

        synthesized = None
        if provider_manager and source_blocks:
            prompt = self._build_synthesis_prompt(query, source_blocks)
            try:
                _, synthesized = provider_manager.chat(
                    request=ChatRequest(
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2,
                    ),
                    task_text=query,
                    purpose="research",
                )
            except Exception:
                synthesized = None

        if synthesized:
            return synthesized

        return self._format_report(query, source_blocks, evidence_lines)

    def _build_synthesis_prompt(self, query: str, source_blocks: list[dict]) -> str:
        sources_json = json.dumps(source_blocks, indent=2, ensure_ascii=False)
        language_hint = self._language_hint(query)
        return (
            "You are a research analyst. Write a concise, factual research report.\n"
            f"Topic: {query}\n\n"
            f"Language style: {language_hint}\n"
            "Use only the provided source notes below. Do not invent facts.\n"
            "Return a clean report with these sections:\n"
            "- Summary\n- Key Findings\n- Sources\n- Caveats\n\n"
            f"Source Notes:\n{sources_json}\n"
        )

    def _format_report(self, query: str, source_blocks: list[dict], evidence_lines: list[str]) -> str:
        lines = [
            f"Research Report: {query}",
            "",
            "Summary",
            "- Research sources were found and summarized below.",
            "",
            "Key Findings",
        ]

        if evidence_lines:
            lines.extend(evidence_lines[:5])
        else:
            lines.append("- No strong source snippets were extracted.")

        lines.extend(
            [
                "",
                "Sources",
            ]
        )

        for block in source_blocks:
            lines.append(f"- {block['title']} -> {block['url']}")

        lines.extend(
            [
                "",
                "Caveats",
                "- This report is generated from live search results and page extraction.",
                "- For a stricter deep-dive, add more source verification or structured citations.",
            ]
        )

        return "\n".join(lines)

    def _fetch_text(self, url: str) -> str:
        req = urllib.request.Request(url, headers={"User-Agent": self.USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode("utf-8", errors="ignore")

    def _parse_duckduckgo_html(self, html_text: str) -> list[SearchResult]:
        results: list[SearchResult] = []

        link_pattern = re.compile(
            r'<a[^>]*class="[^"]*result__a[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            re.S | re.I,
        )

        snippet_pattern = re.compile(
            r'<(?:a|div)[^>]*class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</(?:a|div)>',
            re.S | re.I,
        )

        links = link_pattern.findall(html_text)
        snippets = snippet_pattern.findall(html_text)

        for index, (url, title_html) in enumerate(links):
            if len(results) >= 10:
                break

            title = self._clean_html(title_html)
            cleaned_url = self._normalize_result_url(url)
            snippet = self._clean_html(snippets[index]) if index < len(snippets) else ""
            results.append(
                SearchResult(
                    title=title or cleaned_url,
                    url=cleaned_url,
                    snippet=snippet,
                )
            )

        return results

    def _normalize_result_url(self, url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        if "uddg" in query:
            return urllib.parse.unquote(query["uddg"][0])
        return url

    def _clean_html(self, text: str) -> str:
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _language_hint(self, query: str) -> str:
        devanagari = any("\u0900" <= ch <= "\u097f" for ch in query)
        lowered = query.lower()
        hinglish_markers = ("kya", "koi", "sunao", "bhai", "bata", "hathi", "ek aur")

        if devanagari:
            return "Respond in Hindi using Devanagari script."
        if any(marker in lowered for marker in hinglish_markers):
            return "Respond in Hinglish with a natural Hindi-English mix."
        return "Respond in the same language as the user."
