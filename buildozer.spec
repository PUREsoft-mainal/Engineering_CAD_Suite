[app]
title = Engineering CAD Suite
package.name = engineeringcad
package.domain = org.mostafa.cad
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,dxf
version = 1.0.0
requirements = python3,kivy,ezdxf
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.release_artifact = aab

[buildozer]
log_level = 2
warn_on_root = 1
