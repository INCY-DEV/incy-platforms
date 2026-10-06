# Publishing releases

## Android

In this repository, run **Actions → Publish Android APK** with the APK's
`versionName` (e.g. `3.7.0`) and an HTTPS URL of the signed release APK.
The version field can be left empty to read it directly from the APK.
No new cross-repository token is required. The workflow checks the signature,
package `llc.itdev.incy`, version and non-debuggable flag, then creates
`android-v3.7.0` / `Android v3.7.0` with `Incy.apk` and `SHA256SUMS` only.
It updates the Android section of `RELEASE.json` and the README APK link.
An already existing release is not overwritten. Do not increment a tag without
building an APK with the matching versionName and a higher versionCode; always
use the existing production signing key for upgrade compatibility.

For manual publication use the same tag/title/asset names. The **Update platform
download links** workflow runs on published/edited releases. If an asset was
uploaded late or a manifest commit failed, rerun that workflow with the tag.
Do not re-publish the binary to fix metadata.

## Desktop

Use **Publish to incy-platforms** in `incy-linux`, with a completed source release
such as `v3.8.8`. This copies only desktop installers to `desktop-v3.8.8`.
The source repository uses its existing `PLATFORMS_TOKEN` secret. A token-created
release triggers this repository's manifest workflow. Re-running a mirror
updates the desktop assets; APKs are never sourced from incy-linux.

## Independent update feeds and legacy links

`RELEASE.json` remains the client update feed. Every download URL is pinned to
its platform's versioned release. Manifest updates preserve the other platforms,
refuse incomplete releases and never roll a platform back to an older version.
The workflow serializes Android/desktop metadata updates.

GitHub provides only one global `/releases/latest`. Android publication sets
`latest=false`; desktop keeps that label for existing desktop download URLs.
New consumers must use the manifest or versioned links. The old Android
`/releases/latest/download/Incy.apk` may return a legacy APK or become unavailable
when a new desktop release is published; migrate those links to `android.download`
in RELEASE.json. Existing mixed releases are retained, not deleted or retagged.

Obtainium must use the Android title filter in the README and disable Verify
Latest Tag. Import `obtainium.json` for those settings. It should not track the
repository's overall latest tag or infer an Android version from a desktop tag.

Validation: `python3 -m unittest discover -s tests -v`.
