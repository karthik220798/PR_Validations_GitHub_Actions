# .github/scripts/validate_pr_template.py
import os
import re
import sys

# Get PR body and required sections from environment variables
pr_body = os.environ.get('PR_BODY', '')
required_sections_str = os.environ.get('REQUIRED_SECTIONS', '')
required_sections = required_sections_str.splitlines()

errors = []
found_sections = {}

# Normalize PR body: ensure consistent newlines and trim leading/trailing whitespace
# Add a newline at the end to help regex capture content for the last section
pr_body = pr_body.replace('\r\n', '\n').strip() + '\n'

# Regex pattern to find all headings and their content
# This pattern looks for a heading, then captures everything until the next heading or end of string
pattern = r'(###\s*(.*?))\n(.*?)(?=\n###\s*|\Z)'
matches = re.finditer(pattern, pr_body, re.DOTALL | re.IGNORECASE)

for match in matches:
    full_heading = match.group(1).strip() # e.g., '### Description'
    content = match.group(3).strip()     # Content after the heading

    found_sections[full_heading] = content

# Check for missing headings and empty content
for section in required_sections:
    if section not in found_sections:
        errors.append(f'❌ Missing required section heading: "{section}"')
    else:
        content = found_sections[section]
        if not content: # Check if content is empty after stripping whitespace
            errors.append(f'❌ Section "{section}" is present but has no content.')
        else:
            print(f'✅ Section "{section}" found with content.')

if errors:
    for error in errors:
        print(f'::error::{error}')
    print('::error::PR template validation failed.')
    sys.exit(1) # Exit with a non-zero code to fail the GitHub Actions step
else:
    print('All required PR template sections are present and have content.')
