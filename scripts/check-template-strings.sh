#!/usr/bin/env bash
# Fails the build if a template contains literal user-facing text that isn't
# wrapped in a gettext call (`{{ _('...') }}` / `{% trans %}`). See the
# `web-frontend-localization` spec (sweetrpg/platform,
# openspec/changes/full-localization-web-apps) for the convention.
#
# Allowed literals: brand/proper nouns and non-translatable strings.
set -euo pipefail
cd "$(dirname "$0")/.."

ALLOWED='SweetRPG|GitHub|Pilgrimage Software|^Sweet$|^RPG$|^v\s*(&middot;|·)?\s*built'
status=0

for template in $(find src -name '*.html'); do
    # Strip Jinja blocks/expressions, scripts, and inline styles, then report
    # remaining text between tags. (Styles are stripped because these templates
    # embed page-specific <style> blocks - assets-web's checker doesn't need to.)
    violations=$(
        perl -0777 -pe 's/<style.*?<\/style>//gs; s/<script.*?<\/script>//gs; s/\{%.*?%\}//gs; s/\{\{.*?\}\}//gs' "$template" |
            perl -0777 -ne 'while (/>[^<]+</g) { my $t = $&; $t =~ s/^>|<$//g; print "$t\n" if $t =~ /\S/; }' |
            grep -vE "(${ALLOWED})" || true
    )
    if [ -n "$violations" ]; then
        echo "ERROR: $template contains hardcoded user-facing strings:"
        echo "$violations"
        status=1
    fi
done

exit $status
