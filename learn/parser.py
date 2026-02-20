"""Parse lesson pages from README.md files using marker comments."""

import os
import re

PAGE_MARKER = re.compile(r"<!--\s*lesson:page\s+(.*?)\s*-->")
END_MARKER = re.compile(r"<!--\s*lesson:end\s*-->")
IMAGE_LINE = re.compile(r"!\[(.*?)\]\((.*?)\)")

# Sentinel used to mark image positions in content strings.
# UI layer splits on this to interleave Markdown and image renderables.
IMG_DELIM = "\x00"


def _image_marker(alt, abs_path):
    """Build an inline image marker the UI layer can detect."""
    return f"{IMG_DELIM}IMG[{alt}]({abs_path}){IMG_DELIM}"


def parse_readme(readme_path):
    """Parse lesson pages from a README with markers.

    Markers:
        <!-- lesson:page Page Title --> — starts a new page
        <!-- lesson:end -->             — stops parsing (rest is ignored)

    Image lines (![alt](path)) are converted to inline markers with
    resolved absolute paths.  The UI layer handles rendering or fallback.

    Returns:
        List of {"title": str, "content": str} dicts, one per page.
        Returns empty list if file not found or has no markers.
    """
    if not os.path.isfile(readme_path):
        return []

    readme_dir = os.path.dirname(os.path.abspath(readme_path))

    with open(readme_path, encoding="utf-8") as f:
        text = f.read()

    # Truncate at <!-- lesson:end --> if present
    end_match = END_MARKER.search(text)
    if end_match:
        text = text[: end_match.start()]

    # Split into pages on <!-- lesson:page Title -->
    parts = PAGE_MARKER.split(text)
    # parts alternates: [before_first_marker, title1, content1, title2, content2, ...]

    if len(parts) < 3:
        # No markers found
        return []

    pages = []
    # Skip parts[0] (content before first marker)
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""

        # Replace image lines with markers containing absolute paths
        def _replace_image(match):
            alt = match.group(1)
            rel_path = match.group(2)
            abs_path = os.path.normpath(os.path.join(readme_dir, rel_path))
            return _image_marker(alt, abs_path)

        content = IMAGE_LINE.sub(_replace_image, content)

        # Clean up excessive blank lines
        content = re.sub(r"\n{3,}", "\n\n", content)

        content = content.strip()
        if content:
            pages.append({"title": title, "content": content})

    return pages
