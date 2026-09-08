import unittest

from scripts.audit_site import Fetch, findings_for, normalize, parse_page


class AuditSiteTests(unittest.TestCase):
    def test_normalize_query_policy(self):
        self.assertEqual(normalize("HTTPS://Example.COM/path?x=1#frag"), "https://example.com/path")
        self.assertEqual(normalize("https://example.com/path?x=1", True), "https://example.com/path?x=1")

    def test_parser_collects_static_signals(self):
        html = b'''<!doctype html><html lang="en"><head>
        <title> Example Page </title>
        <meta name="description" content="A description">
        <meta name="viewport" content="width=device-width">
        <link rel="canonical" href="/canonical">
        <link rel="alternate" hreflang="fa" href="/fa/page">
        <script type="application/ld+json">{"@context":"https://schema.org","@type":["WebPage","Article"]}</script>
        </head><body><h1>Hello <span>world</span></h1><h2>Section</h2>
        <a href="/next">Next</a><img src="a.jpg"><img src="b.jpg" alt="">
        </body></html>'''
        r = Fetch(
            requested="https://example.com/page",
            final="https://example.com/page",
            status=200,
            content_type="text/html",
            headers={"content-type": "text/html; charset=utf-8"},
            body=html,
        )
        page, links = parse_page("https://example.com/page", r, "https://example.com/", False)
        self.assertEqual(page.title, "Example Page")
        self.assertEqual(page.meta_description, "A description")
        self.assertEqual(page.canonical, "https://example.com/canonical")
        self.assertEqual(page.html_lang, "en")
        self.assertEqual(page.h1, ["Hello world"])
        self.assertEqual(page.static_jsonld_types, ["Article", "WebPage"])
        self.assertEqual(page.images_missing_alt_attribute, 1)
        self.assertEqual(links, ["https://example.com/next"])

    def test_followed_redirect_is_preserved_as_evidence(self):
        r = Fetch(
            requested="https://example.com/old",
            final="https://example.com/new",
            status=200,
            content_type="text/html",
            headers={"content-type": "text/html"},
            body=b"<html><head><title>New</title></head><body><h1>New</h1></body></html>",
        )
        page, _ = parse_page("https://example.com/old", r, "https://example.com/", False)
        self.assertTrue(page.redirected)
        findings, _ = findings_for([page], set())
        self.assertTrue(any(x["code"] == "redirected-url" for x in findings))

    def test_no_static_jsonld_is_not_reported_as_missing_schema(self):
        r = Fetch(
            requested="https://example.com/",
            final="https://example.com/",
            status=200,
            content_type="text/html",
            headers={"content-type": "text/html"},
            body=b'<html lang="en"><head><title>Home</title><meta name="description" content="x"><meta name="viewport" content="width=device-width"><link rel="canonical" href="/"></head><body><h1>Home</h1></body></html>',
        )
        page, _ = parse_page("https://example.com/", r, "https://example.com/", False)
        findings, _ = findings_for([page], set())
        self.assertEqual(page.static_jsonld_count, 0)
        self.assertFalse(any("schema" in str(x["code"]) and "missing" in str(x["code"]) for x in findings))


if __name__ == "__main__":
    unittest.main()
