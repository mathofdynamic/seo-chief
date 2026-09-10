from __future__ import annotations

import unittest

from scripts.validate_response_matrix import validate_payload


class ResponseMatrixTests(unittest.TestCase):
    def test_html_markdown_404_variants_and_cache_headers(self) -> None:
        payload = {
            "schema_version": "1.0.0",
            "responses": [
                {
                    "id": "html-404",
                    "status": 404,
                    "url": "https://example.test/missing",
                    "headers": {
                        "Content-Type": "text/html; charset=utf-8",
                        "X-Robots-Tag": "noindex, nofollow",
                        "Vary": "Accept, Accept-Encoding",
                    },
                    "body": '<html><head><title>Not found</title></head><body><a href="/">Home</a></body></html>',
                    "expect": {
                        "status": [404, 410],
                        "content_type": "text/html",
                        "format": "html",
                        "x_robots_contains": ["noindex"],
                        "body_contains": ["href"],
                    },
                },
                {
                    "id": "markdown-404",
                    "status": 404,
                    "url": "https://example.test/missing",
                    "headers": {
                        "Content-Type": "text/markdown; charset=utf-8",
                        "X-Robots-Tag": "noindex, nofollow",
                        "Vary": "Accept, Accept-Encoding",
                    },
                    "body": "# Not found\n\n[Sitemap](/sitemap.xml)\n[Docs](/docs)",
                    "expect": {
                        "status": [404, 410],
                        "content_type": "text/markdown",
                        "format": "markdown",
                        "vary_contains": ["Accept", "Accept-Encoding"],
                        "x_robots_contains": ["noindex"],
                        "markdown_links_any": ["/sitemap.xml", "/docs"],
                    },
                },
                {
                    "id": "markdown-q-value",
                    "status": 404,
                    "url": "https://example.test/missing",
                    "headers": {
                        "Content-Type": "text/markdown; charset=utf-8",
                        "Vary": "Accept, Accept-Encoding",
                    },
                    "body": "# Not found\n\n[Sitemap](/sitemap.xml)",
                    "expect": {
                        "status": [404, 410],
                        "content_type": "text/markdown",
                        "format": "markdown",
                        "vary_contains": ["Accept"],
                    },
                },
            ],
            "variant_groups": [
                {
                    "id": "missing-representations",
                    "response_ids": ["html-404", "markdown-404", "markdown-q-value"],
                    "same_status": True,
                    "different_content_type": True,
                    "vary_contains": ["Accept"],
                }
            ],
        }
        self.assertEqual(validate_payload(payload), [])

    def test_html_json_ld_and_machine_readable_endpoints(self) -> None:
        payload = {
            "schema_version": "1.0.0",
            "responses": [
                {
                    "id": "home",
                    "status": 200,
                    "url": "https://example.test/",
                    "headers": {"Content-Type": "text/html; charset=utf-8"},
                    "body": (
                        '<html lang="en"><head><title>Example</title>'
                        '<meta name="description" content="Example site">'
                        '<link rel="canonical" href="https://example.test/">'
                        '<script type="application/ld+json">'
                        '{"@context":"https://schema.org","@type":"Organization"}'
                        '</script></head><body><h1>Example</h1></body></html>'
                    ),
                    "expect": {
                        "status": 200,
                        "content_type": "text/html",
                        "format": "html",
                        "html": {
                            "title_required": True,
                            "description_required": True,
                            "canonical_required": True,
                            "h1_required": True,
                            "json_ld_types": ["Organization"],
                        },
                    },
                },
                {
                    "id": "robots",
                    "status": 200,
                    "url": "https://example.test/robots.txt",
                    "headers": {"Content-Type": "text/plain"},
                    "body": "User-agent: *\nAllow: /\nSitemap: https://example.test/sitemap.xml\n",
                    "expect": {
                        "status": 200,
                        "content_type": "text/plain",
                        "format": "robots",
                        "robots_must_contain": ["Sitemap:"],
                    },
                },
                {
                    "id": "sitemap",
                    "status": 200,
                    "url": "https://example.test/sitemap.xml",
                    "headers": {"Content-Type": "application/xml"},
                    "body": '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.test/</loc></url></urlset>',
                    "expect": {
                        "status": 200,
                        "content_type": "application/xml",
                        "format": "sitemap",
                        "sitemap_min_urls": 1,
                    },
                },
                {
                    "id": "private",
                    "status": 401,
                    "url": "https://example.test/account",
                    "headers": {"X-Robots-Tag": "noindex, nofollow"},
                    "body": "Authentication required",
                    "expect": {"status": [401, 403], "x_robots_contains": ["noindex"]},
                },
                {
                    "id": "redirect",
                    "status": 308,
                    "url": "http://example.test/",
                    "headers": {"Location": "https://example.test/"},
                    "body": "",
                    "expect": {"status": [301, 308], "location_contains": ["https://example.test/"]},
                },
                {
                    "id": "asset",
                    "status": 200,
                    "url": "https://example.test/favicon.ico",
                    "headers": {"Content-Type": "image/x-icon"},
                    "body_bytes": 4,
                    "body": "\x00\x00\x01\x00",
                    "expect": {"status": [200, 304], "format": "asset"},
                },
                {
                    "id": "api",
                    "status": 200,
                    "url": "https://example.test/api/health",
                    "headers": {"Content-Type": "application/json; charset=utf-8"},
                    "body": '{"status":"ok"}',
                    "expect": {
                        "status": 200,
                        "content_type_prefix": "application/json",
                        "format": "api",
                        "api_required_keys": ["status"],
                    },
                },
            ],
        }
        self.assertEqual(validate_payload(payload), [])


if __name__ == "__main__":
    unittest.main()
